/**
 * Portfolio Filter（ガチャのラインナップの絞り込み）
 * 名前で探す・レア度・カテゴリ・並び順。カードは portfolio-renderer.js が作り、'portfolio-rendered' で始まる。
 * 並び順が「レア度ごと」のときだけ、段の見出し（.ga-tier）を出す。0件のときは #filterEmpty を出す。
 * スクショを押すと拡大（#lightbox）。
 */
(function () {
  'use strict';

  var IS_EN = window.tsuzukitLang === 'en';

  var searchInput = document.getElementById('searchInput');
  var sortFilter = document.getElementById('sortFilter');
  var filterResults = document.getElementById('filterResults');
  var filterClear = document.getElementById('filterClear');
  var filterEmpty = document.getElementById('filterEmpty');
  var emptyClear = document.getElementById('emptyClear');
  var appGrid = document.getElementById('appGrid');
  var rareChips = Array.prototype.slice.call(document.querySelectorAll('[data-filter-rarity]'));
  var catChips = Array.prototype.slice.call(document.querySelectorAll('[data-filter-category]'));

  var state = { q: '', rarity: '', category: '', sort: 'default' };
  var cards = [];
  var tiers = [];

  // <option> は中に span を置けないので、英語表示のときは data-en の文言に差し替える
  if (IS_EN && sortFilter) {
    Array.prototype.forEach.call(sortFilter.querySelectorAll('option[data-en]'), function (o) {
      o.textContent = o.dataset.en;
    });
  }

  function init() {
    if (!appGrid) return;
    cards = Array.prototype.slice.call(appGrid.querySelectorAll('.ga-card'));
    tiers = Array.prototype.slice.call(appGrid.querySelectorAll('.ga-tier'));

    // カテゴリの札に数を入れる。1本も無いカテゴリの札は出さない
    var catCount = {};
    cards.forEach(function (c) { catCount[c.dataset.category] = (catCount[c.dataset.category] || 0) + 1; });
    catChips.forEach(function (chip) {
      var key = chip.dataset.filterCategory;
      var n = key ? (catCount[key] || 0) : cards.length;
      var i = chip.querySelector('i');
      if (i) i.textContent = n;
      if (key && !n) chip.hidden = true;
    });
    rareChips.forEach(function (chip) {
      if (!chip.dataset.filterRarity) {
        var i = chip.querySelector('i');
        if (i) i.textContent = cards.length;
      }
    });

    if (searchInput) searchInput.addEventListener('input', debounce(function () { state.q = searchInput.value; apply(); }, 200));
    if (sortFilter) sortFilter.addEventListener('change', function () { state.sort = sortFilter.value; apply(); });
    rareChips.forEach(function (chip) {
      chip.addEventListener('click', function () { state.rarity = chip.dataset.filterRarity; apply(); });
    });
    catChips.forEach(function (chip) {
      chip.addEventListener('click', function () { state.category = chip.dataset.filterCategory; apply(); });
    });
    if (filterClear) filterClear.addEventListener('click', clear);
    if (emptyClear) emptyClear.addEventListener('click', function () { clear(); if (searchInput) searchInput.focus(); });

    apply();
  }

  function setPressed(list, attr, value) {
    list.forEach(function (chip) {
      var on = chip.dataset[attr] === value;
      chip.setAttribute('aria-pressed', on ? 'true' : 'false');
      chip.classList.toggle('is-on', on);
    });
  }

  function apply() {
    var q = state.q.toLowerCase().trim();
    var visible = [];
    cards.forEach(function (card) {
      var name = (card.dataset.searchName || card.dataset.name || '').toLowerCase();
      var ok = (!q || name.indexOf(q) !== -1) &&
        (!state.rarity || card.dataset.rarity === state.rarity) &&
        (!state.category || card.dataset.category === state.category);
      card.classList.toggle('hidden', !ok);
      if (ok) visible.push(card);
    });

    setPressed(rareChips, 'filterRarity', state.rarity);
    setPressed(catChips, 'filterCategory', state.category);
    order(visible);
    count(visible.length);
  }

  function date(el, key) {
    return new Date(el.dataset[key] || el.dataset.releaseDate || '1970-01-01').getTime();
  }

  function order(visible) {
    var sorted;
    var byName = function (a, b) {
      return (a.dataset.name || '').toLowerCase().localeCompare((b.dataset.name || '').toLowerCase(), 'ja');
    };
    switch (state.sort) {
      case 'release-desc': sorted = visible.sort(function (a, b) { return date(b, 'releaseDate') - date(a, 'releaseDate'); }); break;
      case 'release-asc': sorted = visible.sort(function (a, b) { return date(a, 'releaseDate') - date(b, 'releaseDate'); }); break;
      case 'update-desc': sorted = visible.sort(function (a, b) { return date(b, 'updateDate') - date(a, 'updateDate'); }); break;
      case 'update-asc': sorted = visible.sort(function (a, b) { return date(a, 'updateDate') - date(b, 'updateDate'); }); break;
      case 'popular': sorted = visible.sort(function (a, b) { return (+b.dataset.ratingCount || 0) - (+a.dataset.ratingCount || 0); }); break;
      case 'name-asc': sorted = visible.sort(byName); break;
      case 'name-desc': sorted = visible.sort(function (a, b) { return byName(b, a); }); break;
      default: sorted = null;
    }

    if (!sorted) {
      // レア度ごと: 段の見出しとカードを、作ったときの順に戻す。カードが1枚も残らない段は見出しも隠す
      var seen = {};
      visible.forEach(function (c) { seen[c.dataset.rarity] = (seen[c.dataset.rarity] || 0) + 1; });
      var all = Array.prototype.slice.call(appGrid.children);
      all.sort(function (a, b) { return pos(a) - pos(b); });
      all.forEach(function (el) { appGrid.appendChild(el); });
      tiers.forEach(function (t) {
        var n = seen[t.dataset.tier] || 0;
        t.classList.toggle('hidden', !n);
        var num = t.querySelector('.ga-tier-n');
        if (num) num.textContent = n;
        var u = t.querySelector('.ga-tier-u');
        if (u) u.textContent = IS_EN ? (n === 1 ? ' app' : ' apps') : '種';
      });
      return;
    }
    tiers.forEach(function (t) { t.classList.add('hidden'); });
    sorted.forEach(function (c) { appGrid.appendChild(c); });
  }

  // 作ったときの順番（段の見出しは、その段の最初のカードのすぐ前）
  function pos(el) {
    if (el.classList.contains('ga-tier')) {
      var first = cards.filter(function (c) { return c.dataset.rarity === el.dataset.tier; })[0];
      return first ? +first.dataset.originalIndex - 0.5 : -1;
    }
    return +el.dataset.originalIndex;
  }

  function count(visible) {
    var total = cards.length;
    var filtered = !!(state.q.trim() || state.rarity || state.category || state.sort !== 'default');
    if (filterResults) {
      if (IS_EN) {
        filterResults.textContent = visible === total ? 'Showing ' + total + ' apps' : 'Showing ' + visible + ' of ' + total + ' apps';
      } else {
        filterResults.textContent = visible === total ? total + '件表示中' : visible + '/' + total + '件表示中';
      }
    }
    if (filterClear) filterClear.hidden = !filtered || visible === 0;
    if (filterEmpty) filterEmpty.hidden = visible !== 0;
    var q = document.getElementById('emptyQuery');
    if (q) q.textContent = state.q.trim();
    var qWrap = document.querySelectorAll('[data-empty-q]');
    Array.prototype.forEach.call(qWrap, function (el) { el.hidden = !state.q.trim(); });
  }

  function clear() {
    state = { q: '', rarity: '', category: '', sort: 'default' };
    if (searchInput) searchInput.value = '';
    if (sortFilter) sortFilter.value = 'default';
    apply();
  }

  function debounce(fn, wait) {
    var t;
    return function () { clearTimeout(t); t = setTimeout(fn, wait); };
  }

  // スクショの拡大（アーカイブのカードも同じ）
  var lightbox = document.getElementById('lightbox');
  var lightboxImg = document.getElementById('lightbox-img');
  var lastFocus = null;
  function openLightbox(src) {
    if (!lightbox || !lightboxImg) return;
    lastFocus = document.activeElement;
    lightboxImg.src = src;
    requestAnimationFrame(function () { lightbox.classList.add('active'); });
    document.body.style.overflow = 'hidden';
    var btn = lightbox.querySelector('.lightbox-close');
    if (btn) btn.focus();
  }
  function closeLightbox() {
    if (!lightbox || !lightbox.classList.contains('active')) return;
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }
  document.addEventListener('click', function (e) {
    var shot = e.target.closest && e.target.closest('.ga-shot');
    if (shot) { openLightbox(shot.dataset.full || shot.querySelector('img').src); return; }
    if (lightbox && lightbox.contains(e.target)) closeLightbox();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeLightbox(); });

  document.addEventListener('portfolio-rendered', init);
})();
