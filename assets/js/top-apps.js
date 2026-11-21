/*
 * トップ（ガチャ）の動き: ラインナップの検索、カプセルを押したときのシート、機械を回す
 *
 * データは index.html の <script id="appsData">（scripts/build_top_apps.py が書く）
 * - ラインナップはレア度の段に分かれている。スマホで検索していないときは段ごとに8本まで（CSS）
 * - 「まわす！」「もう1回まわす」で、81本からランダムに1本を「出た！」の札に出す
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
    var tiers = Array.prototype.slice.call(grid.querySelectorAll('.t-tier'));

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
            tiers.forEach(function (t) { t.hidden = false; });
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
        tiers.forEach(function (t) { t.hidden = !t.querySelector('.app-tile:not([hidden])'); });
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
        el('sheetCap').className = 'g-cap app-sheet-cap g-cap--' + a.c;
        var rare = el('sheetRare');
        rare.className = 'g-rare g-rare--' + a.k;
        rare.textContent = a.k;
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

    // ---------- 回す ----------
    var won = el('gachaWon');
    var mach = el('gachaMachine');
    var current = (el('wonMore') || {}).getAttribute ? el('wonMore').getAttribute('data-app') : null;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var busy = false;

    function dlText(d) {
        if (isEn) return d >= 1000 ? (Math.round(d / 100) / 10) + 'K' : d.toLocaleString('en');
        return d >= 10000 ? (Math.round(d / 1000) / 10) + '万' : d.toLocaleString('ja');
    }
    function line(a) {
        var parts = [];
        var g = isEn ? a.ge : a.g;
        if (g) parts.push(g);
        if (a.rc > 0) parts.push(isEn ? '★' + a.r.toFixed(1) + ' (' + a.rc.toLocaleString('en') + ' ratings)' : '★' + a.r.toFixed(1) + '（' + a.rc.toLocaleString('ja') + '件）');
        if (a.d > 0) parts.push(isEn ? dlText(a.d) + ' downloads' : dlText(a.d) + 'ダウンロード');
        return parts.join(isEn ? ' · ' : '・');
    }
    function show(a) {
        el('wonIcon').src = a.i;
        el('wonOpen').style.setProperty('--c', 'var(--g-c' + a.c + ')');
        var rare = el('wonRare');
        rare.className = 'g-rare g-rare--' + a.k;
        rare.textContent = a.k;
        el('wonName').textContent = isEn ? a.sne : a.sn;
        el('wonLine').textContent = line(a);
        el('wonStore').href = storeUrl(a);
        el('wonMore').setAttribute('data-app', a.id);
        current = a.id;
        fillPop(a);
    }

    // ---------- 結果のポップアップ ----------
    var pop = el('gachaPop');
    var burst = el('popBurst');
    function fillPop(a) {
        if (!pop) return;
        el('popIcon').src = a.i;
        burst.style.setProperty('--c', 'var(--g-c' + a.c + ')');
        burst.setAttribute('data-rare', a.k);
        var rare = el('popRare');
        rare.className = 'g-rare g-rare--' + a.k;
        rare.textContent = a.k;
        el('popName').textContent = isEn ? a.ne : a.n;
        el('popLine').textContent = line(a);
        el('popStore').href = storeUrl(a);
        el('popMore').setAttribute('data-app', a.id);
    }
    function openPop() {
        if (!pop) return;
        document.documentElement.classList.add('sheet-open');
        if (!pop.open) {
            if (typeof pop.showModal === 'function') pop.showModal();
            else pop.setAttribute('open', '');
        }
        pop.classList.remove('is-pop');
        void pop.offsetWidth;
        pop.classList.add('is-pop');
    }
    function closePop() {
        if (typeof pop.close === 'function') pop.close();
        else pop.removeAttribute('open');
    }
    if (pop) {
        pop.addEventListener('close', function () {
            if (!sheet.open) document.documentElement.classList.remove('sheet-open');
        });
        el('popClose').addEventListener('click', closePop);
        pop.addEventListener('click', function (e) { if (e.target === pop) closePop(); });
    }
    // シートを閉じたとき、結果のポップアップがまだ開いていればスクロールを止めたままにする
    sheet.addEventListener('close', function () {
        if (pop && pop.open) document.documentElement.classList.add('sheet-open');
    });

    function spin() {
        if (busy || !won) return;
        busy = true;
        var next;
        do { next = apps[Math.floor(Math.random() * apps.length)]; } while (apps.length > 1 && next.id === current);
        if (reduce) { show(next); openPop(); busy = false; return; }
        var again = pop && pop.open;
        won.classList.remove('is-pop');
        won.classList.add('is-rolling');
        if (mach) mach.classList.add('is-rolling');
        // ポップアップの中で回し直したときは、ポップアップの中のカプセルを揺らす
        if (again) { pop.classList.remove('is-pop'); pop.classList.add('is-rolling'); }
        setTimeout(function () {
            if (mach) mach.classList.remove('is-rolling');
            won.classList.remove('is-rolling');
            if (pop) pop.classList.remove('is-rolling');
            show(next);
            void won.offsetWidth;
            won.classList.add('is-pop');
            openPop();
            busy = false;
        }, 650);
    }
    ['gachaKnob', 'gachaAgain', 'popAgain'].forEach(function (id) {
        var b = el(id);
        if (b) b.addEventListener('click', spin);
    });
})();
