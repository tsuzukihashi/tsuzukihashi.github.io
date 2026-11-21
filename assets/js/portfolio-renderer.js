/**
 * Portfolio Renderer（ガチャのラインナップ）
 * assets/data/apps.json から、アプリ1本ずつのカード（カプセル）を作って #appGrid に並べる。
 * レア度はダウンロード数（download_count）で決める。SSR 10万以上 / SR 1万以上 / R 1000以上 / N それ以外。
 * 並べ終わったら 'portfolio-rendered' を出す（絞り込みは portfolio-filter.js）。
 * 見た目は assets/css/gacha.css（g-）と assets/css/g-apps.css（ga-）。
 */
(function () {
  'use strict';

  var APPLE_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/></svg>';
  var PLAY_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3,20.5V3.5C3,2.91 3.34,2.39 3.84,2.15L13.69,12L3.84,21.85C3.34,21.6 3,21.09 3,20.5M16.81,15.12L6.05,21.34L14.54,12.85L16.81,15.12M20.16,10.81C20.5,11.08 20.75,11.5 20.75,12C20.75,12.5 20.53,12.9 20.18,13.18L17.89,14.5L15.39,12L17.89,9.5L20.16,10.81M6.05,2.66L16.81,8.88L14.54,11.15L6.05,2.66Z"/></svg>';

  // 言語（lang.js が決める。読み込まれていなければ日本語）
  var IS_EN = window.tsuzukitLang === 'en';

  // レア度の段。並びもこの順
  var TIERS = [
    { key: 'SSR', min: 100000, ja: '10万DL以上', en: '100K+ downloads' },
    { key: 'SR', min: 10000, ja: '1万DL以上', en: '10K+ downloads' },
    { key: 'R', min: 1000, ja: '1000DL以上', en: '1,000+ downloads' },
    { key: 'N', min: 0, ja: 'これから育つ', en: 'Still growing' }
  ];

  // カテゴリ（apps.json の primary_genre）の日本語
  var GENRE_JA = {
    'Utilities': 'ユーティリティ', 'Productivity': '仕事効率化', 'Reference': '辞書/辞典/その他',
    'Photo & Video': '写真/ビデオ', 'Lifestyle': 'ライフスタイル', 'Graphics & Design': 'グラフィック/デザイン',
    'Food & Drink': 'フード/ドリンク', 'Social Networking': 'ソーシャルネットワーキング', 'Games': 'ゲーム',
    'Music': 'ミュージック', 'Book': 'ブック', 'News': 'ニュース', 'Travel': '旅行', 'Education': '教育',
    'Medical': 'メディカル', 'Health & Fitness': 'ヘルスケア/フィットネス', 'Entertainment': 'エンターテインメント'
  };
  var GENRE_EN = { 'Book': 'Books' };

  function rarity(app) {
    var n = Number(app.download_count) || 0;
    for (var i = 0; i < TIERS.length; i++) {
      if (n >= TIERS[i].min) return TIERS[i].key;
    }
    return 'N';
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function displayName(app) {
    return (IS_EN && app.name_en) ? app.name_en : app.name;
  }

  function genreLabel(g) {
    if (!g) return '';
    return IS_EN ? (GENRE_EN[g] || g) : (GENRE_JA[g] || g);
  }

  function toIcon256(url) {
    return String(url || '').replace(/\/\d+x\d+bb\.(jpg|png)$/, '/256x256bb.$1');
  }

  function isFree(app) {
    return !app.price || app.price === 0 || app.price === '0' || app.price === '無料' || app.formatted_price === '無料';
  }

  function priceLabel(app) {
    if (isFree(app)) return IS_EN ? 'Free' : '無料';
    return app.formatted_price || app.price;
  }

  function dateLabel(iso) {
    if (!iso) return '';
    var d = new Date(iso);
    if (isNaN(d.getTime())) return '';
    return d.getFullYear() + '.' + (d.getMonth() + 1) + '.' + d.getDate();
  }

  // 名前の文字から、カプセルの色と傾きを決める（毎回同じになるように）
  function seed(app) {
    var s = String(app.id || app.name || ''), h = 0;
    for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) % 9973;
    return h;
  }

  function renderShots(app, name) {
    var shots = (app.screenshots || []).slice(0, 3);
    if (!shots.length) return '';
    return '<div class="ga-shots">' + shots.map(function (url, i) {
      var label = (IS_EN ? 'Enlarge screenshot ' : 'スクリーンショットを拡大 ') + (i + 1);
      return '<button type="button" class="ga-shot" data-full="' + esc(url) + '" aria-label="' + esc(name + ' ' + label) + '">' +
        '<img src="' + esc(url) + '" alt="" width="626" height="1357" loading="lazy"></button>';
    }).join('') + '</div>';
  }

  function renderButtons(app) {
    var out = '<a class="g-btn g-btn--k" href="' + esc(app.app_store_url) + '" target="_blank" rel="noopener">' +
      APPLE_SVG + 'App Store</a>';
    if (app.google_play_url) {
      out += '<a class="g-btn" href="' + esc(app.google_play_url) + '" target="_blank" rel="noopener">' +
        PLAY_SVG + 'Google Play</a>';
    }
    if (app.lp_url) {
      var external = /^https?:\/\//.test(app.lp_url);
      out += '<a class="g-btn g-btn--y" href="' + esc(app.lp_url) + '"' + (external ? ' target="_blank" rel="noopener"' : '') + '>' +
        (IS_EN ? 'App website' : '紹介ページ') + ' →</a>';
    }
    return '<div class="ga-card-btns">' + out + '</div>';
  }

  function renderCard(app, index) {
    var name = displayName(app);
    var rk = rarity(app);
    var s = seed(app);
    var meta = [genreLabel(app.primary_genre), priceLabel(app), dateLabel(app.release_date)].filter(Boolean).join(' · ');
    return '<article class="g-panel ga-card" data-rarity="' + rk + '" data-original-index="' + index + '"' +
      ' data-app-id="' + esc(app.id) + '"' +
      ' data-name="' + esc(app.name) + '"' +
      ' data-search-name="' + esc([app.name, app.name_en].filter(Boolean).join(' ')) + '"' +
      ' data-category="' + esc(app.primary_genre || '') + '"' +
      ' data-release-date="' + esc(app.release_date || '') + '"' +
      ' data-update-date="' + esc(app.current_version_release_date || '') + '"' +
      ' data-rating-count="' + (Number(app.rating_count) || 0) + '"' +
      ' data-download-count="' + (Number(app.download_count) || 0) + '">' +
      '<a class="ga-card-head" href="' + esc(app.app_store_url) + '" target="_blank" rel="noopener">' +
        '<span class="g-cap g-cap--' + (s % 6 + 1) + '" style="--rot:' + (s % 41 - 20) + 'deg">' +
          '<img src="' + esc(toIcon256(app.icon_url)) + '" alt="" width="256" height="256" loading="lazy">' +
        '</span>' +
        '<span class="ga-card-txt">' +
          '<span class="g-rare g-rare--' + rk + '">' + rk + '</span>' +
          '<h3 class="ga-card-name">' + esc(name) + '</h3>' +
          '<span class="ga-card-meta">' + esc(meta) + '</span>' +
        '</span>' +
      '</a>' +
      renderShots(app, name) +
      renderButtons(app) +
    '</article>';
  }

  function unit(n) {
    return IS_EN ? (n === 1 ? ' app' : ' apps') : '種';
  }

  function renderTier(tier, count) {
    return '<div class="ga-tier" data-tier="' + tier.key + '">' +
      '<span class="g-rare g-rare--' + tier.key + '">' + tier.key + '</span>' +
      '<small>' + (IS_EN ? tier.en : tier.ja) + ' · <span class="ga-tier-n">' + count + '</span><span class="ga-tier-u">' + unit(count) + '</span></small>' +
    '</div>';
  }

  /**
   * 並び: レア度の段ごと。段の中はダウンロード数の多い順、同じならリリースが新しい順
   */
  function sortByRarity(apps) {
    var order = { SSR: 0, SR: 1, R: 2, N: 3 };
    return apps.slice().sort(function (a, b) {
      var t = order[rarity(a)] - order[rarity(b)];
      if (t) return t;
      var d = (Number(b.download_count) || 0) - (Number(a.download_count) || 0);
      if (d) return d;
      return new Date(b.release_date || '1970-01-01') - new Date(a.release_date || '1970-01-01');
    });
  }

  // 頭の「排出のめやす」と、レア度の札の数を入れる
  function fillCounts(counts) {
    TIERS.forEach(function (t) {
      document.querySelectorAll('[data-tier-count="' + t.key + '"]').forEach(function (el) {
        el.textContent = counts[t.key] || 0;
      });
    });
  }

  async function renderAllCards() {
    var grid = document.getElementById('appGrid');
    if (!grid) return;

    try {
      var response = await fetch('/assets/data/apps.json');
      var data = await response.json();
      var apps = sortByRarity(data.apps || []);

      // 英語表示のときは US ストアの英語名とスクショ（assets/data/apps_en.json）に差し替える
      if (IS_EN) {
        try {
          var enResponse = await fetch('/assets/data/apps_en.json');
          var en = (await enResponse.json()).apps || {};
          apps.forEach(function (app) {
            var e = en[app.id];
            if (e && e.name) app.name_en = e.name;
            if (e && e.screenshots && e.screenshots.length) app.screenshots = e.screenshots;
          });
        } catch (e) {}
      }

      var counts = {};
      apps.forEach(function (app) {
        var k = rarity(app);
        counts[k] = (counts[k] || 0) + 1;
      });

      var html = '';
      var current = null;
      apps.forEach(function (app, i) {
        var k = rarity(app);
        if (k !== current) {
          current = k;
          html += renderTier(TIERS.filter(function (t) { return t.key === k; })[0], counts[k]);
        }
        html += renderCard(app, i);
      });
      grid.innerHTML = html;
      fillCounts(counts);

      document.dispatchEvent(new CustomEvent('portfolio-rendered', { detail: { apps: apps } }));
    } catch (error) {
      console.error('Failed to render portfolio:', error);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderAllCards);
  } else {
    renderAllCards();
  }
})();
