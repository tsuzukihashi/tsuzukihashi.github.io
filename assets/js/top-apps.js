/*
 * トップの「アプリを探す」と、アイコンを押したときのシート
 *
 * データは index.html の <script id="appsData">（scripts/build_top_apps.py が書く）
 * - 検索していないときは、ダウンロードの多い12本だけ見せる
 * - 検索は日本語・英語の名前の部分一致。ひらがなとカタカナ、全角と半角、大文字と小文字は区別しない
 * - シートは、LP を撮った画像があれば上の方を見切れさせて出し、無ければストアのスクショを横に並べる
 */
(function () {
    var dataEl = document.getElementById('appsData');
    var grid = document.getElementById('appGrid');
    if (!dataEl || !grid) return;

    var apps = JSON.parse(dataEl.textContent);
    var byId = {};
    apps.forEach(function (a) { byId[a.id] = a; });
    var lang = window.tsuzukitLang || document.documentElement.getAttribute('data-lang') || 'ja';
    var isEn = lang === 'en';

    document.querySelectorAll('.js-total').forEach(function (el) { el.textContent = apps.length; });

    // ---------- 検索 ----------
    var input = document.getElementById('appSearch');
    var count = document.getElementById('appCount');
    var empty = document.getElementById('appEmpty');
    var all = document.getElementById('appAll');
    var tiles = Array.prototype.slice.call(grid.querySelectorAll('.app-tile'));

    function norm(s) {
        return String(s || '')
            .normalize('NFKC')
            .toLowerCase()
            .replace(/[ァ-ヶ]/g, function (c) { return String.fromCharCode(c.charCodeAt(0) - 0x60); })
            .replace(/\s+/g, '');
    }
    var keys = {};
    apps.forEach(function (a) { keys[a.id] = norm(a.n) + '\n' + norm(a.ne); });

    function search() {
        var q = norm(input.value);
        if (!q) {
            grid.classList.remove('is-searching');
            tiles.forEach(function (li) { li.hidden = false; });
            empty.hidden = true;
            all.hidden = false;
            count.textContent = '';
            return;
        }
        var hits = 0;
        grid.classList.add('is-searching');
        tiles.forEach(function (li) {
            var id = li.firstElementChild.getAttribute('data-app');
            var ok = keys[id].indexOf(q) !== -1;
            li.hidden = !ok;
            if (ok) hits++;
        });
        empty.hidden = hits !== 0;
        all.hidden = hits === 0;
        empty.querySelectorAll('.js-q').forEach(function (el) { el.textContent = input.value.trim(); });
        count.textContent = hits === 0 ? '' : (isEn ? hits + (hits === 1 ? ' app' : ' apps') : hits + '本');
    }
    input.addEventListener('input', search);
    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') input.blur(); // iPhone のキーボードを下げる
        if (e.key === 'Escape') { input.value = ''; search(); }
    });
    document.getElementById('appClear').addEventListener('click', function () {
        input.value = '';
        search();
        input.focus();
    });

    // ---------- シート ----------
    var sheet = document.getElementById('appSheet');
    var el = function (id) { return document.getElementById(id); };

    function storeUrl(a) {
        // 英語で見ている人は国を決めずに開く（App Store がその人の国のページを出す）
        return isEn ? 'https://apps.apple.com/app/id' + a.id : a.s;
    }
    function helpUrl(a) {
        var u = (isEn ? a.su.en : a.su.ja) || a.su.ja;
        if (!u || /^https?:\/\/(www\.)?tsuzukit\.com\/contact\/?$/.test(u)) return '/contact/';
        return u;
    }

    function open(id) {
        var a = byId[id];
        if (!a) return;
        el('sheetIcon').src = a.i;
        el('sheetName').textContent = isEn ? a.ne : a.n;
        var meta = [];
        if (a.rc > 0) meta.push(isEn ? '★' + a.r.toFixed(1) + ' (' + a.rc.toLocaleString('en') + ' ratings)' : '★' + a.r.toFixed(1) + '（' + a.rc.toLocaleString('ja') + '件）');
        var g = isEn ? a.ge : a.g;
        if (g) meta.push(g);
        el('sheetMeta').textContent = meta.join(isEn ? ' · ' : '・');

        var lp = el('sheetLp');
        var shots = el('sheetShots');
        shots.innerHTML = '';
        if (a.lp) {
            lp.hidden = false;
            shots.hidden = true;
            lp.href = (isEn ? a.lp.url.en : a.lp.url.ja) || a.lp.url.ja;
            el('sheetLpImg').src = (isEn ? a.lp.img.en : a.lp.img.ja) || a.lp.img.ja;
        } else {
            lp.hidden = true;
            var list = (isEn && a.sse && a.sse.length) ? a.sse : a.ss;
            list.forEach(function (src) {
                var img = document.createElement('img');
                img.src = src;
                img.alt = '';
                img.loading = 'lazy';
                shots.appendChild(img);
            });
            shots.hidden = list.length === 0;
        }

        el('sheetStore').href = storeUrl(a);
        var play = el('sheetPlay');
        play.hidden = !a.p;
        if (a.p) play.href = a.p;
        el('sheetHelp').href = helpUrl(a);

        document.documentElement.classList.add('sheet-open');
        if (typeof sheet.showModal === 'function') sheet.showModal();
        else sheet.setAttribute('open', '');
        sheet.querySelector('.app-sheet-inner').scrollTop = 0;
    }

    function close() {
        if (typeof sheet.close === 'function') sheet.close();
        else sheet.removeAttribute('open');
    }
    sheet.addEventListener('close', function () { document.documentElement.classList.remove('sheet-open'); });
    el('sheetClose').addEventListener('click', close);
    // 外側（暗いところ）を押したら閉じる
    sheet.addEventListener('click', function (e) { if (e.target === sheet) close(); });

    document.addEventListener('click', function (e) {
        var t = e.target.closest('[data-app]');
        if (!t || !byId[t.getAttribute('data-app')]) return;
        e.preventDefault();
        if (document.activeElement === input) input.blur();
        open(t.getAttribute('data-app'));
    });
})();
