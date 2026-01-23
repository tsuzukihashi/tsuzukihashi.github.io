#!/usr/bin/env ruby
# frozen_string_literal: true

require 'net/http'
require 'json'
require 'uri'
require 'fileutils'
require 'date'
require 'openssl'
require 'base64'
require 'zlib'
require 'stringio'
require 'dotenv'

# Load environment variables from .env
Dotenv.load(File.expand_path('../fastlane/.env', __dir__))

# App Store Connect API credentials from environment
ASC_KEY_ID = ENV['ASC_KEY_ID']
ASC_ISSUER_ID = ENV['ASC_ISSUER_ID']
ASC_KEY_FILEPATH = ENV['ASC_KEY_FILEPATH']
VENDOR_NUMBER = ENV['VENDOR_NUMBER']

# Validate required environment variables
%w[ASC_KEY_ID ASC_ISSUER_ID ASC_KEY_FILEPATH VENDOR_NUMBER].each do |var|
  if ENV[var].nil? || ENV[var].empty?
    puts "Error: #{var} is not set in .env file"
    exit 1
  end
end

def generate_jwt_token
  # Read private key
  private_key = OpenSSL::PKey::EC.new(File.read(ASC_KEY_FILEPATH))

  # JWT Header
  header = {
    alg: 'ES256',
    kid: ASC_KEY_ID,
    typ: 'JWT'
  }

  # JWT Payload
  now = Time.now.to_i
  payload = {
    iss: ASC_ISSUER_ID,
    iat: now,
    exp: now + 1200, # 20 minutes
    aud: 'appstoreconnect-v1'
  }

  # Encode header and payload
  header_encoded = Base64.urlsafe_encode64(header.to_json, padding: false)
  payload_encoded = Base64.urlsafe_encode64(payload.to_json, padding: false)

  # Sign
  signing_input = "#{header_encoded}.#{payload_encoded}"
  signature = private_key.sign(OpenSSL::Digest::SHA256.new, signing_input)

  # Convert DER signature to raw (r, s) format for ES256
  asn1 = OpenSSL::ASN1.decode(signature)
  r = asn1.value[0].value.to_s(2).rjust(32, "\x00")[-32..-1]
  s = asn1.value[1].value.to_s(2).rjust(32, "\x00")[-32..-1]
  raw_signature = r + s

  signature_encoded = Base64.urlsafe_encode64(raw_signature, padding: false)

  "#{signing_input}.#{signature_encoded}"
end

def fetch_sales_report(token, report_date, frequency = 'DAILY')
  uri = URI("https://api.appstoreconnect.apple.com/v1/salesReports")
  uri.query = URI.encode_www_form({
    'filter[reportType]' => 'SALES',
    'filter[reportSubType]' => 'SUMMARY',
    'filter[frequency]' => frequency,
    'filter[vendorNumber]' => VENDOR_NUMBER,
    'filter[reportDate]' => report_date
  })

  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true

  request = Net::HTTP::Get.new(uri)
  request['Authorization'] = "Bearer #{token}"
  request['Accept'] = 'application/a-gzip'

  response = http.request(request)

  case response.code.to_i
  when 200
    # Decompress gzip
    begin
      gz = Zlib::GzipReader.new(StringIO.new(response.body))
      content = gz.read
      gz.close
      content
    rescue Zlib::GzipFile::Error
      response.body
    end
  when 404
    nil
  else
    puts "Error: #{response.code} - #{response.body}"
    nil
  end
end

def parse_sales_report(content)
  return {} unless content

  lines = content.split("\n")
  headers = lines.first&.split("\t") || []

  # Find column indices
  sku_idx = headers.index('SKU') || 2
  title_idx = headers.index('Title') || headers.index('App Name') || 0
  units_idx = headers.index('Units') || 6
  product_type_idx = headers.index('Product Type Identifier') || 4

  downloads = {}

  lines[1..-1]&.each do |line|
    next if line.strip.empty?
    values = line.split("\t")

    sku = values[sku_idx]
    title = values[title_idx]
    units = values[units_idx]&.to_i || 0
    product_type = values[product_type_idx]

    # Only count app downloads (not IAP)
    # 1F = Free iPhone, 1T = Paid iPhone, 7F = Free Universal, 7T = Paid Universal
    next unless product_type =~ /^(1|7)[FT]$/

    downloads[sku] ||= { title: title, units: 0 }
    downloads[sku][:units] += units
  end

  downloads
end

def fetch_all_downloads(days = 365)
  puts "=" * 60
  puts "Fetching Download Statistics"
  puts "=" * 60
  puts

  token = generate_jwt_token
  all_downloads = {}

  # Fetch daily reports for the past N days
  puts "Fetching daily reports for the past #{days} days..."
  days.times do |i|
    date = (Date.today - i - 1).strftime('%Y-%m-%d')

    print "\rProcessing: #{date}"
    $stdout.flush

    content = fetch_sales_report(token, date, 'DAILY')
    if content
      daily_downloads = parse_sales_report(content)
      daily_downloads.each do |sku, data|
        all_downloads[sku] ||= { title: data[:title], units: 0 }
        all_downloads[sku][:units] += data[:units]
      end
    end

    # Rate limiting
    sleep(0.3)
  end

  puts "\n\n"
  all_downloads
end

def update_apps_json(downloads)
  apps_json_path = File.expand_path('../assets/data/apps.json', __dir__)

  unless File.exist?(apps_json_path)
    puts "apps.json not found!"
    return
  end

  data = JSON.parse(File.read(apps_json_path))

  # Update each app with download count
  data['apps'].each do |app|
    bundle_id = app['bundle_id']
    # Try to find matching download data by bundle_id or app name
    download_data = downloads.values.find { |d| d[:title] == app['name'] }

    if download_data
      app['download_count'] = download_data[:units]
      puts "#{app['name']}: #{download_data[:units]} downloads"
    else
      app['download_count'] = 0
    end
  end

  # Add total downloads
  total_downloads = data['apps'].sum { |app| app['download_count'] || 0 }
  data['total_downloads'] = total_downloads

  # Save updated JSON
  File.write(apps_json_path, JSON.pretty_generate(data))
  puts "\nUpdated apps.json with download counts"
  puts "Total downloads: #{total_downloads}"
end

def main
  begin
    downloads = fetch_all_downloads(30)

    puts "=" * 60
    puts "Download Summary (Last 365 days)"
    puts "=" * 60

    sorted = downloads.sort_by { |_, v| -v[:units] }
    sorted.each do |sku, data|
      puts "#{data[:title]}: #{data[:units]} downloads"
    end

    total = downloads.values.sum { |d| d[:units] }
    puts "\nTotal: #{total} downloads"

    # Update apps.json
    update_apps_json(downloads)

  rescue => e
    puts "Error: #{e.message}"
    puts e.backtrace.first(5).join("\n")
  end
end

main
