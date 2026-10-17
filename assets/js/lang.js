/*
 * サイト共通の言語切り替え（日本語 / 英語）
 *
 * - ブラウザの第一言語が日本語なら日本語、それ以外は英語で表示する
 * - ?lang=ja / ?lang=en で明示指定でき、指定やボタンでの切り替えは localStorage に残す
 * - 検索エンジンのクローラーには既定の日本語を見せる
 *
 * ページ側の書き方:
 *   <span class="i18n-ja">日本語</span><span class="i18n-en">English</span>
 *   <meta name="title-en" content="English title">
 *   <meta name="description-en" content="English description">
 *   <input placeholder="検索" data-en-placeholder="Search">
 *   <img src="日本語のスクショ" data-en-src="英語のスクショ">
 *   JS から文言を出すときは window.tsuzukitLang（'ja' か 'en'）を見る
 *
 * <head> の中で、CSS より前に同期読み込みする（表示のちらつきを防ぐため）。
 */
(function () {
    var KEY = 'tsuzukit-lang';
    var root = document.documentElement;

    function detect() {
        var param = null;
        try { param = new URLSearchParams(location.search).get('lang'); } catch (e) {}
        if (param === 'ja' || param === 'en') {
            try { localStorage.setItem(KEY, param); } catch (e) {}
            return param;
        }
        var saved = null;
        try { saved = localStorage.getItem(KEY); } catch (e) {}
        if (saved === 'ja' || saved === 'en') return saved;
        if (/bot|crawl|spider|slurp|lighthouse/i.test(navigator.userAgent || '')) return 'ja';
        var first = (navigator.languages && navigator.languages[0]) || navigator.language || '';
        return String(first).toLowerCase().indexOf('ja') === 0 ? 'ja' : 'en';
    }

    var lang = detect();
    root.setAttribute('data-lang', lang);
    root.lang = lang;

    var style = document.createElement('style');
    style.textContent =
        'html[data-lang="en"] .i18n-ja{display:none!important}' +
        'html:not([data-lang="en"]) .i18n-en{display:none!important}' +
        '.lang-switch{font:inherit;cursor:pointer;background:none;border:0;padding:0;color:inherit}' +
        '.lang-switch--floating{position:fixed;right:16px;bottom:16px;z-index:9999;padding:8px 14px;' +
        'border-radius:999px;background:#14110c;color:#fff;font-size:13px;font-weight:700;' +
        'box-shadow:0 2px 8px rgba(0,0,0,.25)}';
    (document.head || root).appendChild(style);

    function meta(name) {
        var el = document.querySelector('meta[name="' + name + '"]');
        return el ? el.getAttribute('content') : null;
    }

    function applyHead() {
        if (lang !== 'en') return;
        var title = meta('title-en');
        if (title) document.title = title;
        var desc = meta('description-en');
        var descEl = document.querySelector('meta[name="description"]');
        if (desc && descEl) descEl.setAttribute('content', desc);
        // 属性の英語版: data-en-placeholder / data-en-alt / data-en-aria-label / data-en-title / data-en-src
        ['placeholder', 'alt', 'aria-label', 'title', 'src'].forEach(function (attr) {
            var nodes = document.querySelectorAll('[data-en-' + attr + ']');
            for (var i = 0; i < nodes.length; i++) {
                nodes[i].setAttribute(attr, nodes[i].getAttribute('data-en-' + attr));
            }
        });
    }

    function addSwitch() {
        if (document.querySelector('.lang-switch')) return;
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'lang-switch';
        btn.setAttribute('aria-label', 'Switch language / 言語を切り替え');
        btn.innerHTML = '<span class="i18n-ja">English</span><span class="i18n-en">日本語</span>';
        btn.addEventListener('click', function () {
            var next = lang === 'en' ? 'ja' : 'en';
            try { localStorage.setItem(KEY, next); } catch (e) {}
            var url = new URL(location.href);
            url.searchParams.delete('lang');
            location.replace(url.toString());
        });
        var menu = document.querySelector('.nav-menu');
        if (menu) {
            btn.classList.add('nav-link');
            menu.appendChild(btn);
        } else {
            btn.classList.add('lang-switch--floating');
            document.body.appendChild(btn);
        }
    }

    window.tsuzukitLang = lang;

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { applyHead(); addSwitch(); });
    } else {
        applyHead();
        addSwitch();
    }
})();
