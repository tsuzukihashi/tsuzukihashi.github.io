/**
 * Portfolio Renderer
 * apps.json からアプリカードを動的に生成する
 */
(function () {
  'use strict';

  const APPLE_SVG = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/></svg>';
  const ANDROID_SVG = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M3,20.5V3.5C3,2.91 3.34,2.39 3.84,2.15L13.69,12L3.84,21.85C3.34,21.6 3,21.09 3,20.5M16.81,15.12L6.05,21.34L14.54,12.85L16.81,15.12M20.16,10.81C20.5,11.08 20.75,11.5 20.75,12C20.75,12.5 20.53,12.9 20.18,13.18L17.89,14.5L15.39,12L17.89,9.5L20.16,10.81M6.05,2.66L16.81,8.88L14.54,11.15L6.05,2.66Z"/></svg>';

  /**
   * アイコンURLを256x256に変換
   */
  function toIcon256(url) {
    return url.replace(/\/\d+x\d+bb\.jpg$/, '/256x256bb.jpg');
  }

  /**
   * スクリーンショットHTML（最大3枚）を生成
   */
  function renderScreenshots(screenshots) {
    if (!screenshots || screenshots.length === 0) return '';
    const items = screenshots.slice(0, 3).map(function (url) {
      return '<div class="app-screenshot"><img src="' + url + '" alt="" loading="lazy"></div>';
    });
    return '<div class="app-screenshots">' + items.join('') + '</div>';
  }

  /**
   * マルチプラットフォームカード（iOS + Android）を生成
   */
  function renderMultiplatformCard(app) {
    return '<div class="app-card-store app-card-multiplatform">' +
      '<div class="app-header">' +
        '<div class="app-icon-store">' +
          '<img src="' + toIcon256(app.icon_url) + '" alt="' + app.name + '">' +
        '</div>' +
        '<div class="app-info">' +
          '<h3 class="app-name">' + app.name + '</h3>' +
          '<p class="app-subtitle">' + app.primary_genre + '</p>' +
          '<p class="app-meta">Free</p>' +
        '</div>' +
        '<div class="app-store-buttons-header">' +
          '<a href="' + app.app_store_url + '" target="_blank" class="store-btn-small store-btn-ios">' +
            APPLE_SVG + ' iOS' +
          '</a>' +
          '<a href="' + app.google_play_url + '" target="_blank" class="store-btn-small store-btn-android">' +
            ANDROID_SVG + ' Android' +
          '</a>' +
        '</div>' +
      '</div>' +
      renderScreenshots(app.screenshots) +
    '</div>';
  }

  /**
   * 標準カード（iOS のみ）を生成
   */
  function renderStandardCard(app) {
    var price = (app.price === 0 || app.formatted_price === '無料') ? 'Free' : app.formatted_price;
    return '<a href="' + app.app_store_url + '" target="_blank" class="app-card-store">' +
      '<div class="app-header">' +
        '<div class="app-icon-store">' +
          '<img src="' + toIcon256(app.icon_url) + '" alt="' + app.name + '">' +
        '</div>' +
        '<div class="app-info">' +
          '<h3 class="app-name">' + app.name + '</h3>' +
          '<p class="app-subtitle">' + app.primary_genre + '</p>' +
          '<p class="app-meta">' + price + '</p>' +
        '</div>' +
        '<div class="app-open-btn">開く</div>' +
      '</div>' +
      renderScreenshots(app.screenshots) +
    '</a>';
  }

  /**
   * 1つのアプリカードを生成
   */
  function renderAppCard(app) {
    if (app.google_play_url) {
      return renderMultiplatformCard(app);
    }
    return renderStandardCard(app);
  }

  // 上位固定アプリ（この順番で先頭に表示）
  var PINNED_IDS = [
    6478291625, // 旅行思い出マップ
    6758856276, // うんちくん
    6751716346, // 推しアイランド
    1598380826  // 流れるメモ帳
  ];

  /**
   * デフォルト並び順: 固定アプリを先頭、残りはリリース日の新しい順
   */
  function sortDefault(apps) {
    var pinned = [];
    var rest = [];

    apps.forEach(function (app) {
      var pinIndex = PINNED_IDS.indexOf(app.id);
      if (pinIndex !== -1) {
        pinned[pinIndex] = app;
      } else {
        rest.push(app);
      }
    });

    // 固定アプリの空スロットを除去
    pinned = pinned.filter(Boolean);

    // 残りはリリース日の新しい順
    rest.sort(function (a, b) {
      return new Date(b.release_date || '1970-01-01') - new Date(a.release_date || '1970-01-01');
    });

    return pinned.concat(rest);
  }

  /**
   * 全アプリカードをレンダリング
   */
  async function renderAllCards() {
    var grid = document.getElementById('appGrid');
    if (!grid) return;

    try {
      var response = await fetch('/assets/data/apps.json');
      var data = await response.json();
      var apps = sortDefault(data.apps || []);

      var html = apps.map(renderAppCard).join('');
      grid.innerHTML = html;

      // レンダリング完了イベントを発火
      document.dispatchEvent(new CustomEvent('portfolio-rendered', { detail: { apps: apps } }));
    } catch (error) {
      console.error('Failed to render portfolio:', error);
    }
  }

  // DOM Ready で実行
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderAllCards);
  } else {
    renderAllCards();
  }
})();
