#!/usr/bin/env ruby
# frozen_string_literal: true

require 'net/http'
require 'json'
require 'uri'
require 'fileutils'
require 'date'

COUNTRY = "jp"
PORTFOLIO_HTML = File.expand_path('../portfolio/index.html', __dir__)

def extract_app_ids_from_html(html_path)
  return [] unless File.exist?(html_path)

  content = File.read(html_path)

  # App Store URLからアプリIDを抽出
  # パターン: /id(\d+)
  app_ids = content.scan(/apps\.apple\.com[^"]*\/id(\d+)/).flatten.uniq

  puts "Extracted #{app_ids.count} app IDs from HTML"
  app_ids
end

def fetch_app_by_id(app_id, country)
  uri = URI("https://itunes.apple.com/lookup?id=#{app_id}&country=#{country}")

  response = Net::HTTP.get_response(uri)

  if response.code.to_i != 200
    puts "  Error fetching #{app_id}: HTTP #{response.code}"
    return nil
  end

  data = JSON.parse(response.body)

  if data['resultCount'] > 0
    data['results'].first
  else
    puts "  Not found: #{app_id}"
    nil
  end
rescue => e
  puts "  Error: #{e.message}"
  nil
end

def transform_app_data(app)
  return nil unless app

  {
    id: app['trackId'],
    name: app['trackName'],
    bundle_id: app['bundleId'],
    app_store_url: app['trackViewUrl'],
    icon_url: app['artworkUrl512'] || app['artworkUrl100'],
    icon_url_60: app['artworkUrl60'],

    # カテゴリ情報
    primary_genre: app['primaryGenreName'],
    genres: app['genres'],
    genre_ids: app['genreIds'],

    # 価格情報
    price: app['price'],
    formatted_price: app['formattedPrice'],
    currency: app['currency'],

    # 評価情報
    rating: app['averageUserRating'],
    rating_count: app['userRatingCount'],
    rating_count_current_version: app['userRatingCountForCurrentVersion'],

    # バージョン情報
    version: app['version'],
    release_notes: app['releaseNotes'],

    # 日付情報
    release_date: app['releaseDate'],
    current_version_release_date: app['currentVersionReleaseDate'],

    # 説明
    description: app['description'],

    # スクリーンショット
    screenshots: app['screenshotUrls'] || [],
    ipad_screenshots: app['ipadScreenshotUrls'] || [],

    # その他の情報
    content_advisory_rating: app['contentAdvisoryRating'],
    minimum_os_version: app['minimumOsVersion'],
    supported_devices: app['supportedDevices'],
    file_size_bytes: app['fileSizeBytes'],
    developer_name: app['artistName'],
    seller_name: app['sellerName'],
    developer_url: app['artistViewUrl']
  }
end

def generate_category_list(apps)
  categories = {}

  apps.each do |app|
    genre = app[:primary_genre] || 'Other'
    categories[genre] ||= 0
    categories[genre] += 1
  end

  categories.sort_by { |_, count| -count }
end

def main
  puts "=" * 60
  puts "App Store Data Fetcher for Portfolio"
  puts "=" * 60
  puts

  # HTMLからアプリIDを抽出
  app_ids = extract_app_ids_from_html(PORTFOLIO_HTML)

  if app_ids.empty?
    puts "No app IDs found!"
    return
  end

  # 各アプリの情報を取得
  apps = []
  app_ids.each_with_index do |app_id, index|
    puts "Fetching #{index + 1}/#{app_ids.count}: #{app_id}"

    raw_app = fetch_app_by_id(app_id, COUNTRY)
    if raw_app
      app = transform_app_data(raw_app)
      apps << app if app
      puts "  OK: #{app[:name]}"
    end

    # API制限を避けるため少し待機
    sleep(0.3)
  end

  puts "\n" + "=" * 60
  puts "Successfully fetched #{apps.count} apps"
  puts "=" * 60

  # リリース日でソート（新しいものが先）
  apps.sort_by! do |app|
    begin
      DateTime.parse(app[:release_date] || '1970-01-01')
    rescue
      DateTime.new(1970, 1, 1)
    end
  end.reverse!

  # 出力ディレクトリを作成
  output_dir = File.expand_path('../assets/data', __dir__)
  FileUtils.mkdir_p(output_dir)

  # JSONファイルに保存
  output = {
    generated_at: Time.now.strftime('%Y-%m-%d %H:%M:%S'),
    total_apps: apps.count,
    categories: generate_category_list(apps).to_h,
    apps: apps
  }

  output_path = File.join(output_dir, 'apps.json')
  File.write(output_path, JSON.pretty_generate(output))
  puts "\nSaved to: #{output_path}"

  # サマリーを出力
  puts "\n" + "=" * 60
  puts "Summary"
  puts "=" * 60
  puts "Total Apps: #{apps.count}"
  puts "\nCategories:"
  generate_category_list(apps).each do |cat, count|
    puts "  #{cat}: #{count}"
  end

  # 評価サマリー
  rated_apps = apps.select { |a| a[:rating] }
  if rated_apps.any?
    avg_rating = rated_apps.sum { |a| a[:rating] } / rated_apps.count
    total_reviews = apps.sum { |a| a[:rating_count] || 0 }
    puts "\nRatings:"
    puts "  Average Rating: #{avg_rating.round(2)}"
    puts "  Total Reviews: #{total_reviews}"
  end

  puts "\nDone!"
end

main
