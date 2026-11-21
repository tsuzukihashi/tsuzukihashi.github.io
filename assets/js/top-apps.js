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

    // ---------- 回す（結果はポップアップだけで見せる） ----------
    var mach = el('gachaMachine');
    var pop = el('gachaPop');
    var burst = el('popBurst');
    var current = null;
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
    function fillPop(a) {
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
        current = a.id;
    }
    // 閉じたカプセルが出てきて、揺れて、開く（CSS の .is-pop）
    function rnd(a, b) { return a + Math.random() * (b - a); }
    function any(list) { return list[Math.floor(Math.random() * list.length)]; }
    // 揺れ方と開け方を、回すたびに選ぶ（CSS の --shake-* / --lid-* / --open-at に渡す）
    function shuffleMotion() {
        var s = pop.style;  // 文字の出る時間にも使うので、カプセルではなくポップアップ全体に置く
        var shake = any(['t-cap-shake', 't-cap-hop', 't-cap-twist']);
        var t = shake === 't-cap-hop' ? rnd(.26, .36) : rnd(.12, .22);
        var n = shake === 't-cap-hop' ? any([1, 2, 2, 3]) : any([2, 3, 4, 5]);
        s.setProperty('--shake-name', shake);
        s.setProperty('--shake-a', rnd(5, 14).toFixed(1) + 'deg');
        s.setProperty('--shake-h', rnd(8, 18).toFixed(1) + '%');
        s.setProperty('--shake-t', t.toFixed(2) + 's');
        s.setProperty('--shake-n', n);
        var openAt = .45 + t * n + rnd(.02, .18);
        s.setProperty('--open-at', openAt.toFixed(2) + 's');

        var side = Math.random() < .5 ? -1 : 1;
        var open = any(['hinge', 'hinge', 'wide', 'pop', 'slide']);
        var deg = rnd(32, 50);
        var origin = side < 0 ? '0 100%' : '100% 100%';
        var lid;
        if (open === 'hinge') lid = 'translate(' + (side * 4) + '%, -6%) rotate(' + (side * deg) + 'deg)';
        else if (open === 'wide') lid = 'translate(' + (side * 2) + '%, -2%) rotate(' + (side * rnd(68, 82)) + 'deg)';
        else if (open === 'pop') { origin = '50% 100%'; lid = 'translate(' + rnd(-22, 22).toFixed(0) + '%, ' + rnd(-80, -62).toFixed(0) + '%) rotate(' + rnd(-30, 30).toFixed(0) + 'deg)'; }
        else { origin = '50% 100%'; lid = 'translate(' + (side * rnd(48, 62)).toFixed(0) + '%, -22%) rotate(' + (side * rnd(18, 32)).toFixed(0) + 'deg)'; }
        s.setProperty('--lid-origin', origin);
        s.setProperty('--lid-open', lid);
        s.setProperty('--lid-t', (open === 'pop' ? rnd(.36, .46) : rnd(.24, .36)).toFixed(2) + 's');
        s.setProperty('--icon-rot', rnd(-12, 12).toFixed(0) + 'deg');
        return { shake: shake, t: t, n: n, openAt: openAt };
    }

    // ---------- 振動（Android は navigator.vibrate、iPhone は押した瞬間の「コッ」だけ） ----------
    // iPhone の Safari は navigator.vibrate が無い。iOS 17.4 からのスイッチ型のチェックボックスは、
    // 本物の指のタップで切り替わったときだけ「コッ」と鳴る（iOS 26.5 から、プログラムで押しても鳴らない）。
    // そこでボタンの中に透明なラベルを敷き、指がラベルを直接押すようにする。鳴るのは押した瞬間の1回だけ。
    var canVibrate = typeof navigator.vibrate === 'function';
    function buzz(pattern) {
        if (!canVibrate) return;
        try { navigator.vibrate(pattern); } catch (e) { /* 鳴らせない端末は黙って何もしない */ }
    }
    function tapTick(btn) {
        if (canVibrate || !btn) return;
        var label = document.createElement('label');
        label.className = 't-haptic';
        label.setAttribute('aria-hidden', 'true');
        var input = document.createElement('input');
        input.type = 'checkbox';
        input.setAttribute('switch', '');
        input.tabIndex = -1;
        label.appendChild(input);
        btn.appendChild(label);
    }
    // カプセルの動きに合わせた振動のパターン（[鳴らす, 休む, 鳴らす, …] のミリ秒）
    var OPEN_BUZZ = { N: [35], R: [45], SR: [40, 60, 50], SSR: [60, 50, 60, 50, 140] };
    function revealBuzz(m, rare) {
        var hits = [[280, 18]];  // 落ちてきて着地
        for (var i = 0; i < m.n; i++) {
            var at = 450 + (i + (m.shake === 't-cap-hop' ? .85 : .25)) * m.t * 1000;
            hits.push([at, 12]);
        }
        var openMs = m.openAt * 1000;
        var open = OPEN_BUZZ[rare] || OPEN_BUZZ.N;
        var pattern = [0];
        var cursor = 0;
        hits.forEach(function (h) {
            pattern.push(Math.max(0, Math.round(h[0] - cursor)), h[1]);
            cursor = h[0] + h[1];
        });
        pattern.push(Math.max(0, Math.round(openMs - cursor)));
        pattern = pattern.concat(open);
        buzz(pattern);
    }

    function reveal(a) {
        var m = shuffleMotion();
        revealBuzz(m, a.k);
        pop.classList.remove('is-leaving', 'is-pop');
        void pop.offsetWidth;
        pop.classList.add('is-pop');
    }
    function openPop() {
        document.documentElement.classList.add('sheet-open');
        pop.classList.add('is-first');
        if (typeof pop.showModal === 'function') pop.showModal();
        else pop.setAttribute('open', '');
    }
    function closePop() {
        if (typeof pop.close === 'function') pop.close();
        else pop.removeAttribute('open');
    }
    pop.addEventListener('close', function () {
        pop.classList.remove('is-first', 'is-pop', 'is-leaving');
        if (!sheet.open) document.documentElement.classList.remove('sheet-open');
    });
    el('popClose').addEventListener('click', closePop);
    pop.addEventListener('click', function (e) { if (e.target === pop) closePop(); });
    // シートを閉じたとき、結果のポップアップがまだ開いていればスクロールを止めたままにする
    sheet.addEventListener('close', function () {
        if (pop.open) document.documentElement.classList.add('sheet-open');
    });

    function pick() {
        var next;
        do { next = apps[Math.floor(Math.random() * apps.length)]; } while (apps.length > 1 && next.id === current);
        return next;
    }
    // 機械の「まわす！」: 機械を揺らしてから、ポップアップを開く
    function spin() {
        if (busy) return;
        busy = true;
        var next = pick();
        if (reduce) { fillPop(next); openPop(); busy = false; return; }
        if (mach) mach.classList.add('is-rolling');
        buzz([14, 90, 14, 90, 14, 90, 14]);  // 機械のガラガラ
        setTimeout(function () {
            if (mach) mach.classList.remove('is-rolling');
            fillPop(next);
            openPop();
            reveal(next);
            busy = false;
        }, 650);
    }
    // ポップアップの「もう1回まわす」: 今のカプセルを閉じて下へ落とし、次のカプセルを上から出す
    function spinAgain() {
        if (busy) return;
        busy = true;
        var next = pick();
        if (reduce) { fillPop(next); busy = false; return; }
        pop.classList.remove('is-pop', 'is-first');
        pop.classList.add('is-leaving');
        buzz([10, 300, 16]);  // 閉まる・落ちる
        setTimeout(function () {
            fillPop(next);
            reveal(next);
            busy = false;
        }, 540);
    }
    // ラベルを押すと、スイッチへの click も泡立ってくるので、スイッチ由来の click は数えない
    function onTap(fn) {
        return function (e) { if (e.target && e.target.tagName === 'INPUT') return; fn(); };
    }
    tapTick(el('gachaKnob'));
    tapTick(el('popAgain'));
    el('gachaKnob').addEventListener('click', onTap(spin));
    el('popAgain').addEventListener('click', onTap(spinAgain));
})();
