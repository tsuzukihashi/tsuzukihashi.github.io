/**
 * Portfolio Filter & Sort Functionality
 * Provides search, category filter, and sort functionality for the portfolio page
 */

(function() {
  'use strict';

  let appsData = [];
  let appCards = [];
  let originalOrder = [];

  const searchInput = document.getElementById('searchInput');
  const categoryFilter = document.getElementById('categoryFilter');
  const sortFilter = document.getElementById('sortFilter');
  const filterResults = document.getElementById('filterResults');
  const filterClear = document.getElementById('filterClear');
  const appGrid = document.getElementById('appGrid');

  /**
   * Initialize the filter functionality
   */
  function init(apps) {
    if (!appGrid) return;

    appsData = apps || [];

    appCards = Array.from(document.querySelectorAll('#appGrid .app-card-store:not(.app-card-archived)'));
    originalOrder = appCards.map(card => card);

    addDataAttributesToCards();

    if (searchInput) {
      searchInput.addEventListener('input', debounce(applyFilters, 200));
    }
    if (categoryFilter) {
      categoryFilter.addEventListener('change', applyFilters);
    }
    if (sortFilter) {
      sortFilter.addEventListener('change', applyFilters);
    }
    if (filterClear) {
      filterClear.addEventListener('click', clearFilters);
    }

    updateResultsCount();
  }

  /**
   * Add data attributes to app cards for filtering/sorting
   */
  function addDataAttributesToCards() {
    appCards.forEach((card, index) => {
      card.dataset.originalIndex = index;

      let appUrl = card.getAttribute('href') || '';
      if (!appUrl) {
        const iosLink = card.querySelector('.store-btn-ios');
        if (iosLink) appUrl = iosLink.getAttribute('href') || '';
      }
      const appIdMatch = appUrl.match(/\/id(\d+)/);
      const appId = appIdMatch ? parseInt(appIdMatch[1]) : null;

      const appData = appsData.find(app => app.id === appId);

      if (appData) {
        card.dataset.appId = appData.id;
        card.dataset.name = appData.name || '';
        card.dataset.category = appData.primary_genre || '';
        card.dataset.releaseDate = appData.release_date || '';
        card.dataset.updateDate = appData.current_version_release_date || '';
        card.dataset.ratingCount = appData.rating_count || 0;
        card.dataset.rating = appData.rating || 0;
        card.dataset.downloadCount = appData.download_count || 0;

        injectReleaseDate(card, appData.release_date);
      } else {
        const nameEl = card.querySelector('.app-name');
        const categoryEl = card.querySelector('.app-subtitle');

        card.dataset.name = nameEl ? nameEl.textContent.trim() : '';
        card.dataset.category = categoryEl ? categoryEl.textContent.trim() : '';
        card.dataset.releaseDate = '';
        card.dataset.updateDate = '';
        card.dataset.ratingCount = 0;
        card.dataset.rating = 0;
        card.dataset.downloadCount = 0;
      }
    });
  }

  function injectReleaseDate(card, releaseDate) {
    if (!releaseDate) return;

    const metaEl = card.querySelector('.app-meta');
    if (!metaEl) return;

    const date = new Date(releaseDate);
    if (isNaN(date.getTime())) return;

    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const formatted = `${year}.${month}.${day}`;

    metaEl.textContent = `${metaEl.textContent} · ${formatted}`;
  }

  function applyFilters() {
    const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const category = categoryFilter ? categoryFilter.value : '';
    const sortOption = sortFilter ? sortFilter.value : 'default';

    let visibleCards = [];

    appCards.forEach(card => {
      const name = (card.dataset.name || '').toLowerCase();
      const cardCategory = card.dataset.category || '';

      const matchesSearch = !searchTerm || name.includes(searchTerm);
      const matchesCategory = !category || cardCategory === category;

      if (matchesSearch && matchesCategory) {
        card.classList.remove('hidden');
        visibleCards.push(card);
      } else {
        card.classList.add('hidden');
      }
    });

    sortCards(visibleCards, sortOption);
    updateResultsCount(visibleCards.length);
  }

  function sortCards(cards, sortOption) {
    if (!appGrid) return;

    let sortedCards;

    switch (sortOption) {
      case 'release-desc':
        sortedCards = cards.sort((a, b) => {
          return new Date(b.dataset.releaseDate || '1970-01-01') - new Date(a.dataset.releaseDate || '1970-01-01');
        });
        break;
      case 'release-asc':
        sortedCards = cards.sort((a, b) => {
          return new Date(a.dataset.releaseDate || '1970-01-01') - new Date(b.dataset.releaseDate || '1970-01-01');
        });
        break;
      case 'update-desc':
        sortedCards = cards.sort((a, b) => {
          return new Date(b.dataset.updateDate || b.dataset.releaseDate || '1970-01-01') - new Date(a.dataset.updateDate || a.dataset.releaseDate || '1970-01-01');
        });
        break;
      case 'update-asc':
        sortedCards = cards.sort((a, b) => {
          return new Date(a.dataset.updateDate || a.dataset.releaseDate || '1970-01-01') - new Date(b.dataset.updateDate || b.dataset.releaseDate || '1970-01-01');
        });
        break;
      case 'popular':
        sortedCards = cards.sort((a, b) => {
          return (parseInt(b.dataset.ratingCount) || 0) - (parseInt(a.dataset.ratingCount) || 0);
        });
        break;
      case 'name-asc':
        sortedCards = cards.sort((a, b) => {
          return (a.dataset.name || '').toLowerCase().localeCompare((b.dataset.name || '').toLowerCase(), 'ja');
        });
        break;
      case 'name-desc':
        sortedCards = cards.sort((a, b) => {
          return (b.dataset.name || '').toLowerCase().localeCompare((a.dataset.name || '').toLowerCase(), 'ja');
        });
        break;
      case 'default':
      default:
        sortedCards = cards.sort((a, b) => {
          return parseInt(a.dataset.originalIndex) - parseInt(b.dataset.originalIndex);
        });
        break;
    }

    sortedCards.forEach(card => {
      appGrid.appendChild(card);
    });

    appCards.forEach(card => {
      if (card.classList.contains('hidden')) {
        appGrid.appendChild(card);
      }
    });
  }

  function clearFilters() {
    if (searchInput) searchInput.value = '';
    if (categoryFilter) categoryFilter.value = '';
    if (sortFilter) sortFilter.value = 'default';

    appCards.forEach(card => {
      card.classList.remove('hidden');
    });

    originalOrder.forEach(card => {
      appGrid.appendChild(card);
    });

    updateResultsCount();
  }

  function updateResultsCount(count) {
    if (!filterResults) return;

    const total = appCards.length;
    const visible = count !== undefined ? count : total;

    if (visible === total) {
      filterResults.textContent = `${total}件表示中`;
    } else {
      filterResults.textContent = `${visible}/${total}件表示中`;
    }

    showNoResultsMessage(visible === 0);
  }

  function showNoResultsMessage(show) {
    let noResultsEl = document.querySelector('.no-results');

    if (show) {
      if (!noResultsEl) {
        noResultsEl = document.createElement('div');
        noResultsEl.className = 'no-results';
        noResultsEl.innerHTML = `
          <h3>検索結果がありません</h3>
          <p>別のキーワードやカテゴリで検索してみてください</p>
        `;
        appGrid.parentNode.insertBefore(noResultsEl, appGrid.nextSibling);
      }
      noResultsEl.style.display = 'block';
    } else if (noResultsEl) {
      noResultsEl.style.display = 'none';
    }
  }

  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // portfolio-renderer.js のレンダリング完了イベントを待つ
  document.addEventListener('portfolio-rendered', function(e) {
    init(e.detail.apps);
  });
})();
