/*
 * 記事の広告枠（Google AdSense）
 *
 * 広告を出す場所は HTML 側で決める。本文の区切りに次の目印を置いたところにだけ出す:
 *   <div class="ad-slot" data-ad="mid"></div>   記事の途中（見出しの手前）
 *   <div class="ad-slot" data-ad="end"></div>   本文を読み終えたところ
 * 置き場所の決まりは docs/ads.md。自動広告は AdSense の管理画面でオフにしてある。
 *
 * - 日本語と英語の本文を二重に持つページでは、見えている側の目印にだけ入れる
 * - 広告が埋まらなかった枠は消す（空の箱を残さない）
 * - localhost では AdSense を読まず、大きさの見本だけ出す（開発中に広告を表示させない）
 */
(function () {
    var CLIENT = 'ca-pub-8240751277462688';
    var UNITS = {
        mid: '3182306220', // tsuzukit.com ブログ 記事の途中
        end: '2754930814'  // tsuzukit.com ブログ 記事の終わり
    };
    var LOCAL = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);

    function label() {
        return window.tsuzukitLang === 'en' ? 'Advertisement' : '広告';
    }

    function loadLibrary() {
        if (document.querySelector('script[src*="adsbygoogle.js"]')) return;
        var s = document.createElement('script');
        s.async = true;
        s.crossOrigin = 'anonymous';
        s.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + CLIENT;
        document.head.appendChild(s);
    }

    // 埋まらなかったら枠ごと消す
    function hideWhenUnfilled(slot, ins) {
        if (!('MutationObserver' in window)) return;
        new MutationObserver(function (records, observer) {
            if (ins.getAttribute('data-ad-status') === 'unfilled') {
                slot.hidden = true;
                observer.disconnect();
            } else if (ins.getAttribute('data-ad-status') === 'filled') {
                observer.disconnect();
            }
        }).observe(ins, { attributes: true, attributeFilter: ['data-ad-status'] });
    }

    function fill() {
        var slots = document.querySelectorAll('.ad-slot[data-ad]');
        var filled = 0;
        for (var i = 0; i < slots.length; i++) {
            var slot = slots[i];
            var unit = UNITS[slot.getAttribute('data-ad')];
            // 隠れている言語の本文の中にある目印は飛ばす
            if (!unit || slot.classList.contains('is-filled') || slot.getClientRects().length === 0) continue;

            var box = document.createElement('div');
            box.className = 'ad-slot-box';
            var tag = document.createElement('div');
            tag.className = 'ad-slot-label';
            tag.textContent = label();
            box.appendChild(tag);

            if (LOCAL) {
                var sample = document.createElement('div');
                sample.className = 'ad-slot-sample';
                sample.textContent = 'AdSense ' + slot.getAttribute('data-ad') + ' (' + unit + ')';
                box.appendChild(sample);
            } else {
                var ins = document.createElement('ins');
                ins.className = 'adsbygoogle';
                ins.style.display = 'block';
                ins.setAttribute('data-ad-client', CLIENT);
                ins.setAttribute('data-ad-slot', unit);
                ins.setAttribute('data-ad-format', 'rectangle');
                ins.setAttribute('data-full-width-responsive', 'false');
                box.appendChild(ins);
                hideWhenUnfilled(slot, ins);
            }

            slot.appendChild(box);
            slot.classList.add('is-filled');
            if (!LOCAL) (window.adsbygoogle = window.adsbygoogle || []).push({});
            filled++;
        }
        if (filled > 0 && !LOCAL) loadLibrary();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fill);
    } else {
        fill();
    }
})();
