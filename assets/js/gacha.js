/*
 * ガチャの見た目の共通の動き（全ページ）
 * - スマホのメニューの開け閉め（ボタン・外を押す・Esc・リンクを押す）
 * 古いページに残っている navToggle のインラインの処理より先に（capture で）受けて、
 * そちらは止める。開け閉めはここだけでやる。
 */
(function () {
    function init() {
        var btn = document.getElementById('navToggle');
        var menu = document.getElementById('navMenu');
        if (!btn || !menu || !btn.classList.contains('g-menu') || btn.dataset.gReady) return;
        btn.dataset.gReady = '1';
        function set(open) {
            menu.classList.toggle('active', open);
            btn.setAttribute('aria-expanded', open ? 'true' : 'false');
            btn.textContent = open ? 'CLOSE' : 'MENU';
        }
        btn.addEventListener('click', function (e) {
            e.stopImmediatePropagation();
            set(!menu.classList.contains('active'));
        }, true);
        document.addEventListener('click', function (e) {
            if (!menu.classList.contains('active')) return;
            if (menu.contains(e.target) && !e.target.closest('a')) return;
            if (btn.contains(e.target)) return;
            set(false);
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && menu.classList.contains('active')) { set(false); btn.focus(); }
        });
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
})();
