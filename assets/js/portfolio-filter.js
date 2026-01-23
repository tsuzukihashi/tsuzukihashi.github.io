/**
 * Portfolio Filter & Sort Functionality
 * Provides search, category filter, and sort functionality for the portfolio page
 */

(function() {
  'use strict';

  // App data loaded from JSON
  let appsData = [];
  let appCards = [];
  let originalOrder = [];

  // DOM Elements
  const searchInput = document.getElementById('searchInput');
  const categoryFilter = document.getElementById('categoryFilter');
  const sortFilter = document.getElementById('sortFilter');
  const filterResults = document.getElementById('filterResults');
  const filterClear = document.getElementById('filterClear');
  const appGrid = document.getElementById('appGrid');

  /**
   * Initialize the filter functionality
   */
  async function init() {
    if (!appGrid) return;

    // Load app data from JSON
    try {
      const response = await fetch('/assets/data/apps.json');
      const data = await response.json();
      appsData = data.apps || [];
    } catch (error) {
      console.warn('Could not load apps.json, using fallback data extraction');
      appsData = [];
    }

    // Get all app cards
    appCards = Array.from(document.querySelectorAll('.app-card-store'));

    // Store original order
    originalOrder = appCards.map(card => card);

    // Add data attributes to cards
    addDataAttributesToCards();

    // Add event listeners
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

    // Initial update
    updateResultsCount();
  }

  /**
   * Add data attributes to app cards for filtering/sorting
   */
  function addDataAttributesToCards() {
    appCards.forEach((card, index) => {
      // Store original index
      card.dataset.originalIndex = index;

      // Try to find matching app data
      const appUrl = card.getAttribute('href') || '';
      const appIdMatch = appUrl.match(/\/id(\d+)/);
      const appId = appIdMatch ? parseInt(appIdMatch[1]) : null;

      // Find app in data
      const appData = appsData.find(app => app.id === appId);

      if (appData) {
        // Add data attributes from JSON
        card.dataset.appId = appData.id;
        card.dataset.name = appData.name || '';
        card.dataset.category = appData.primary_genre || '';
        card.dataset.releaseDate = appData.release_date || '';
        card.dataset.updateDate = appData.current_version_release_date || '';
      } else {
        // Fallback: extract data from card HTML
        const nameEl = card.querySelector('.app-name');
        const categoryEl = card.querySelector('.app-subtitle');

        card.dataset.name = nameEl ? nameEl.textContent.trim() : '';
        card.dataset.category = categoryEl ? categoryEl.textContent.trim() : '';
        card.dataset.releaseDate = '';
        card.dataset.updateDate = '';
      }
    });
  }

  /**
   * Apply all filters and sorting
   */
  function applyFilters() {
    const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const category = categoryFilter ? categoryFilter.value : '';
    const sortOption = sortFilter ? sortFilter.value : 'default';

    let visibleCards = [];

    appCards.forEach(card => {
      const name = (card.dataset.name || '').toLowerCase();
      const cardCategory = card.dataset.category || '';

      // Check search match
      const matchesSearch = !searchTerm || name.includes(searchTerm);

      // Check category match
      const matchesCategory = !category || cardCategory === category;

      // Show/hide card
      if (matchesSearch && matchesCategory) {
        card.classList.remove('hidden');
        visibleCards.push(card);
      } else {
        card.classList.add('hidden');
      }
    });

    // Sort visible cards
    sortCards(visibleCards, sortOption);

    // Update results count
    updateResultsCount(visibleCards.length);
  }

  /**
   * Sort cards based on selected option
   */
  function sortCards(cards, sortOption) {
    if (!appGrid) return;

    let sortedCards;

    switch (sortOption) {
      case 'release-desc':
        sortedCards = cards.sort((a, b) => {
          const dateA = new Date(a.dataset.releaseDate || '1970-01-01');
          const dateB = new Date(b.dataset.releaseDate || '1970-01-01');
          return dateB - dateA;
        });
        break;

      case 'release-asc':
        sortedCards = cards.sort((a, b) => {
          const dateA = new Date(a.dataset.releaseDate || '1970-01-01');
          const dateB = new Date(b.dataset.releaseDate || '1970-01-01');
          return dateA - dateB;
        });
        break;

      case 'update-desc':
        sortedCards = cards.sort((a, b) => {
          const dateA = new Date(a.dataset.updateDate || a.dataset.releaseDate || '1970-01-01');
          const dateB = new Date(b.dataset.updateDate || b.dataset.releaseDate || '1970-01-01');
          return dateB - dateA;
        });
        break;

      case 'update-asc':
        sortedCards = cards.sort((a, b) => {
          const dateA = new Date(a.dataset.updateDate || a.dataset.releaseDate || '1970-01-01');
          const dateB = new Date(b.dataset.updateDate || b.dataset.releaseDate || '1970-01-01');
          return dateA - dateB;
        });
        break;

      case 'name-asc':
        sortedCards = cards.sort((a, b) => {
          const nameA = (a.dataset.name || '').toLowerCase();
          const nameB = (b.dataset.name || '').toLowerCase();
          return nameA.localeCompare(nameB, 'ja');
        });
        break;

      case 'name-desc':
        sortedCards = cards.sort((a, b) => {
          const nameA = (a.dataset.name || '').toLowerCase();
          const nameB = (b.dataset.name || '').toLowerCase();
          return nameB.localeCompare(nameA, 'ja');
        });
        break;

      case 'default':
      default:
        // Restore original order for visible cards
        sortedCards = cards.sort((a, b) => {
          return parseInt(a.dataset.originalIndex) - parseInt(b.dataset.originalIndex);
        });
        break;
    }

    // Re-append cards in sorted order
    sortedCards.forEach(card => {
      appGrid.appendChild(card);
    });

    // Also append hidden cards at the end
    appCards.forEach(card => {
      if (card.classList.contains('hidden')) {
        appGrid.appendChild(card);
      }
    });
  }

  /**
   * Clear all filters
   */
  function clearFilters() {
    if (searchInput) searchInput.value = '';
    if (categoryFilter) categoryFilter.value = '';
    if (sortFilter) sortFilter.value = 'default';

    // Show all cards
    appCards.forEach(card => {
      card.classList.remove('hidden');
    });

    // Restore original order
    originalOrder.forEach(card => {
      appGrid.appendChild(card);
    });

    updateResultsCount();
  }

  /**
   * Update the results count display
   */
  function updateResultsCount(count) {
    if (!filterResults) return;

    const total = appCards.length;
    const visible = count !== undefined ? count : total;

    if (visible === total) {
      filterResults.textContent = `${total}件表示中`;
    } else {
      filterResults.textContent = `${visible}/${total}件表示中`;
    }

    // Show/hide no results message
    showNoResultsMessage(visible === 0);
  }

  /**
   * Show/hide no results message
   */
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

  /**
   * Debounce function for search input
   */
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

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
