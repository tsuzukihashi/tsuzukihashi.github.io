#!/usr/bin/env ruby
# 公開中の全アプリについて、ASC に登録した「マーケティングURL（LP）」と「サポートURL」を
# assets/data/app_urls.json に書き出す。トップのアプリのシートが使う。
#   cd fastlane && bundle exec ruby ../scripts/fetch_app_urls.rb
require 'json'
env = File.expand_path('../fastlane/.env', __dir__)
File.readlines(env, encoding: 'UTF-8').each do |l|
  k, v = l.strip.split('=', 2)
  ENV[k] = v.to_s.delete('"') if k && v && k =~ /\A[A-Z_]+\z/
end
require 'spaceship'
Spaceship::ConnectAPI.token = Spaceship::ConnectAPI::Token.create(
  key_id: ENV['ASC_KEY_ID'], issuer_id: ENV['ASC_ISSUER_ID'], filepath: ENV['ASC_KEY_FILEPATH'])

out = {}
apps = Spaceship::ConnectAPI::App.all
apps.each_with_index do |app, i|
  v = (app.get_live_app_store_version rescue nil)
  next unless v
  locs = (v.get_app_store_version_localizations rescue [])
  pick = ->(code) { locs.find { |x| x.locale == code } }
  ja = pick.('ja') || locs.first
  en = pick.('en-US') || pick.('en-GB') || ja
  out[app.id] = {
    'bundle_id' => app.bundle_id,
    'marketing_url' => { 'ja' => ja&.marketing_url, 'en' => en&.marketing_url },
    'support_url' => { 'ja' => ja&.support_url, 'en' => en&.support_url }
  }
  $stderr.puts "#{i + 1}/#{apps.size} #{app.name}"
end
path = File.expand_path('../assets/data/app_urls.json', __dir__)
File.write(path, JSON.pretty_generate(out) + "\n")
puts "wrote #{out.size} apps -> #{path}"
