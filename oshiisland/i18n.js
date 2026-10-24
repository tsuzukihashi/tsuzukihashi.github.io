/*
 * 推しアイランドのページの言語切り替え（37言語）
 *
 * サイト共通の /assets/js/lang.js（日本語 / 英語の2つ）では足りないので、このフォルダだけこれを使う。
 * - URL は1つ。ブラウザの言語の並び（navigator.languages）を上から見て、最初に対応している言語で出す
 * - 対応していない言語だけの人には英語を出す
 * - フッターの言語選択で選んだ言語は localStorage に残す
 * - HTML には日本語が入っている。日本語以外は i18n/<言語>.json を読んで差し替える
 * - 検索エンジンのクローラーには日本語をそのまま見せる
 *
 * ページ側の書き方:
 *   <p data-i18n="faq.012">日本語</p>            中身（HTML）を差し替える
 *   <meta data-i18n-content="index.002" ...>      content 属性を差し替える
 *   <img data-i18n-alt="index.054" data-shot="1">  alt と、その言語のスクショ（shots/<言語>/1.webp）
 *
 * <head> の中で、CSS より前に同期で読み込む（差し替え前の日本語が一瞬見えないように隠すため）。
 */
(function () {
    var KEY = 'oshiisland-lang';
    var VERSION = '1';
    var LANGS = {
        'ja': '日本語', 'en': 'English', 'ar': 'العربية', 'ca': 'Català', 'cs': 'Čeština',
        'da': 'Dansk', 'de': 'Deutsch', 'el': 'Ελληνικά', 'es': 'Español (España)',
        'es-MX': 'Español (México)', 'fi': 'Suomi', 'fr': 'Français', 'fr-CA': 'Français (Canada)',
        'he': 'עברית', 'hi': 'हिन्दी', 'hr': 'Hrvatski', 'hu': 'Magyar', 'id': 'Bahasa Indonesia',
        'it': 'Italiano', 'ko': '한국어', 'ms': 'Bahasa Melayu', 'nl': 'Nederlands', 'no': 'Norsk',
        'pl': 'Polski', 'pt-BR': 'Português (Brasil)', 'pt-PT': 'Português (Portugal)',
        'ro': 'Română', 'ru': 'Русский', 'sk': 'Slovenčina', 'sv': 'Svenska', 'sw': 'Kiswahili',
        'th': 'ไทย', 'tr': 'Türkçe', 'uk': 'Українська', 'vi': 'Tiếng Việt',
        'zh-Hans': '简体中文', 'zh-Hant': '繁體中文'
    };
    var RTL = { 'ar': true, 'he': true };
    var root = document.documentElement;

    // ブラウザの言語タグ（例: es-AR, zh-TW, nb-NO）を、対応している言語に寄せる。無ければ null
    function match(tag) {
        var t = String(tag || '').toLowerCase().replace(/_/g, '-');
        var p = t.split('-');
        var base = p[0];
        if (!base) return null;
        if (base === 'zh') {
            if (/hant|-tw|-hk|-mo/.test(t)) return 'zh-Hant';
            return 'zh-Hans';
        }
        if (base === 'es') {
            // スペイン以外のスペイン語圏（中南米・米国）は、メキシコ版に寄せる
            if (!p[1] || p[1] === 'es') return 'es';
            return 'es-MX';
        }
        if (base === 'fr') return p[1] === 'ca' ? 'fr-CA' : 'fr';
        if (base === 'pt') return p[1] === 'pt' ? 'pt-PT' : 'pt-BR';
        if (base === 'nb' || base === 'nn' || base === 'no') return 'no';
        if (base === 'iw') return 'he';
        if (base === 'in') return 'id';
        if (base === 'zsm') return 'ms';
        return LANGS.hasOwnProperty(base) ? base : null;
    }

    function detect() {
        var saved = null;
        try { saved = localStorage.getItem(KEY); } catch (e) {}
        if (saved && LANGS.hasOwnProperty(saved)) return saved;
        if (/bot|crawl|spider|slurp|lighthouse/i.test(navigator.userAgent || '')) return 'ja';
        var prefs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language];
        for (var i = 0; i < prefs.length; i++) {
            var m = match(prefs[i]);
            if (m) return m;
        }
        return 'en';
    }

    var lang = detect();
    window.oshiislandLang = lang;

    function setDocLang(l) {
        root.lang = l;
        root.setAttribute('data-lang', l);
        root.dir = RTL[l] ? 'rtl' : 'ltr';
    }

    var style = document.createElement('style');
    style.textContent = 'html.i18n-loading body{visibility:hidden}';
    (document.head || root).appendChild(style);

    function apply(dict) {
        var nodes = document.querySelectorAll('[data-i18n]');
        for (var i = 0; i < nodes.length; i++) {
            var v = dict[nodes[i].getAttribute('data-i18n')];
            if (typeof v === 'string') nodes[i].innerHTML = v;
        }
        nodes = document.querySelectorAll('[data-i18n-content]');
        for (i = 0; i < nodes.length; i++) {
            v = dict[nodes[i].getAttribute('data-i18n-content')];
            if (typeof v === 'string') nodes[i].setAttribute('content', v);
        }
        nodes = document.querySelectorAll('[data-i18n-alt]');
        for (i = 0; i < nodes.length; i++) {
            v = dict[nodes[i].getAttribute('data-i18n-alt')];
            if (typeof v === 'string') nodes[i].setAttribute('alt', v);
        }
        var t = document.querySelector('title[data-i18n]');
        if (t) document.title = t.textContent;
        setDocLang(lang);
    }

    function applyShots() {
        var imgs = document.querySelectorAll('img[data-shot]');
        for (var i = 0; i < imgs.length; i++) {
            imgs[i].src = 'shots/' + lang + '/' + imgs[i].getAttribute('data-shot') + '.webp';
        }
    }

    function reveal() { root.classList.remove('i18n-loading'); }

    function addPicker() {
        var slot = document.querySelector('[data-lang-picker]');
        if (!slot || slot.querySelector('select')) return;
        var sel = document.createElement('select');
        sel.setAttribute('aria-label', 'Language');
        for (var code in LANGS) {
            if (!LANGS.hasOwnProperty(code)) continue;
            var o = document.createElement('option');
            o.value = code;
            o.textContent = LANGS[code];
            if (code === lang) o.selected = true;
            sel.appendChild(o);
        }
        sel.addEventListener('change', function () {
            try { localStorage.setItem(KEY, sel.value); } catch (e) {}
            location.reload();
        });
        slot.appendChild(sel);
    }

    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }

    if (lang === 'ja') {
        setDocLang('ja');
        onReady(addPicker);
        return;
    }

    root.classList.add('i18n-loading');
    // 読み込みに失敗しても、3秒で日本語のまま見せる（真っ白のまま止めない）
    var giveUp = setTimeout(reveal, 3000);
    var dictPromise = fetch('/oshiisland/i18n/' + lang + '.json?v=' + VERSION)
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });

    onReady(function () {
        addPicker();
        applyShots();
        dictPromise.then(function (dict) {
            apply(dict);
            clearTimeout(giveUp);
            reveal();
        }).catch(function () {
            clearTimeout(giveUp);
            reveal();
        });
    });
})();
