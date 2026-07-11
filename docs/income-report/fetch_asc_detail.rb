# App Store Connect 月次売上レポート詳細取得（SKU/Parent Identifier付き）
# 使い方: cd fastlane && bundle exec ruby /path/to/fetch_asc_detail.rb
require 'spaceship'
require 'json'
require 'net/http'
require 'zlib'
require 'stringio'
require 'date'

OUT_PATH = File.join(ENV.fetch('SCRATCH'), 'asc_detail.json')

File.readlines('.env').each do |line|
  next if line.strip.start_with?('#') || !line.include?('=')
  key, value = line.strip.split('=', 2)
  ENV[key] = value
end

token = Spaceship::ConnectAPI::Token.create(
  key_id: ENV['ASC_KEY_ID'],
  issuer_id: ENV['ASC_ISSUER_ID'],
  filepath: File.expand_path(ENV['ASC_KEY_FILEPATH'])
)

months = %w[2025-11 2025-12 2026-01 2026-02 2026-03 2026-04 2026-05 2026-06]
result = {}

months.each do |report_month|
  uri = URI('https://api.appstoreconnect.apple.com/v1/salesReports')
  uri.query = URI.encode_www_form(
    'filter[frequency]' => 'MONTHLY',
    'filter[reportDate]' => report_month,
    'filter[reportSubType]' => 'SUMMARY',
    'filter[reportType]' => 'SALES',
    'filter[vendorNumber]' => ENV['VENDOR_NUMBER']
  )

  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true
  request = Net::HTTP::Get.new(uri)
  request['Authorization'] = "Bearer #{token.text}"
  request['Accept'] = 'application/a-gzip'

  response = http.request(request)
  if response.code.to_i != 200
    puts "#{report_month}: ERROR #{response.code}"
    next
  end

  begin
    tsv = Zlib::GzipReader.new(StringIO.new(response.body)).read
  rescue Zlib::GzipFile::Error
    tsv = response.body
  end

  header = nil
  rows = []
  tsv.each_line do |line|
    cols = line.chomp.split("\t")
    if line.start_with?('Provider')
      header = cols
      next
    end
    next if cols.length < 15
    row = {}
    header.each_with_index { |h, i| row[h] = cols[i] }
    rows << {
      'sku' => row['SKU'],
      'title' => row['Title'],
      'product_type' => row['Product Type Identifier'],
      'units' => row['Units'].to_i,
      'proceeds_per_unit' => row['Developer Proceeds'].to_f,
      'currency' => row['Currency of Proceeds'],
      'apple_id' => row['Apple Identifier'],
      'parent_id' => row['Parent Identifier'],
      'country' => row['Country Code']
    }
  end
  result[report_month] = rows
  puts "#{report_month}: #{rows.size} rows"
end

File.write(OUT_PATH, JSON.pretty_generate(result))
puts "Saved to #{OUT_PATH}"
