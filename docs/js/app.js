/**
 * Claude Skills Registry - Search Application
 * Fast client-side search for 67,000+ skills
 */

const CONFIG = {
    INDEX_URL: 'search-index.json',
    FEATURED_URL: 'featured.json',
    CATEGORIES_URL: 'categories/index.json',
    PAGE_SIZE: 20,
    DEBOUNCE_MS: 300,
    FUSE_OPTIONS: {
        keys: [
            { name: 'n', weight: 0.4 },  // name
            { name: 'd', weight: 0.3 },  // description
            { name: 'g', weight: 0.2 },  // tags
            { name: 'c', weight: 0.1 }   // category
        ],
        threshold: 0.4,
        includeScore: true,
        ignoreLocation: true,
        minMatchCharLength: 2
    }
};

// Category code to full name mapping
const CATEGORY_NAMES = {
    'dev': 'Development',
    'ops': 'DevOps',
    'sec': 'Security',
    'doc': 'Documents',
    'des': 'Design',
    'tst': 'Testing',
    'prd': 'Product',
    'mkt': 'Marketing',
    'pro': 'Productivity',
    'dat': 'Data',
    'off': 'Official',
    'oth': 'Other'
};

// State
let state = {
    index: null,
    fuse: null,
    featured: [],
    categories: [],
    results: [],
    displayedCount: 0,
    currentQuery: '',
    currentCategory: '',
    currentSort: 'relevance',
    isLoading: true
};

// DOM Elements
const elements = {
    searchInput: document.getElementById('search-input'),
    categoryFilter: document.getElementById('category-filter'),
    sortFilter: document.getElementById('sort-filter'),
    totalCount: document.getElementById('total-count'),
    resultCount: document.getElementById('result-count'),
    searchTime: document.getElementById('search-time'),
    loading: document.getElementById('loading'),
    featuredSection: document.getElementById('featured-section'),
    featuredList: document.getElementById('featured-list'),
    searchResults: document.getElementById('search-results'),
    emptyState: document.getElementById('empty-state'),
    loadMore: document.getElementById('load-more'),
    loadMoreBtn: document.getElementById('load-more-btn'),
    lastUpdated: document.getElementById('last-updated'),
    quickTags: document.getElementById('quick-tags'),
    modal: document.getElementById('skill-modal'),
    modalClose: document.getElementById('modal-close'),
    modalBody: document.getElementById('modal-body')
};

// Initialize
async function init() {
    try {
        // Load index and featured in parallel
        const [indexData, featuredData, categoriesData] = await Promise.all([
            fetch(CONFIG.INDEX_URL).then(r => r.json()),
            fetch(CONFIG.FEATURED_URL).then(r => r.json()).catch(() => ({ skills: [] })),
            fetch(CONFIG.CATEGORIES_URL).then(r => r.json()).catch(() => ({ categories: [] }))
        ]);

        state.index = indexData;
        state.featured = featuredData.skills || [];
        state.categories = categoriesData.categories || [];

        // Initialize Fuse.js
        state.fuse = new Fuse(state.index.s, CONFIG.FUSE_OPTIONS);

        // Update UI
        elements.totalCount.textContent = state.index.t.toLocaleString();
        elements.lastUpdated.textContent = `Updated: ${state.index.v}`;

        // Populate category filter
        populateCategoryFilter();

        // Show featured
        showFeatured();

        // Hide loading
        elements.loading.classList.add('hidden');
        state.isLoading = false;

    } catch (error) {
        console.error('Failed to load index:', error);
        elements.loading.innerHTML = `
            <span style="font-size: 2rem;">❌</span>
            <p>Failed to load skills index</p>
            <p style="font-size: 0.9rem; color: var(--text-muted);">${error.message}</p>
        `;
    }
}

// Populate category filter
function populateCategoryFilter() {
    state.categories.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.code;
        option.textContent = `${cat.name} (${cat.count.toLocaleString()})`;
        elements.categoryFilter.appendChild(option);
    });
}

// Show featured skills
function showFeatured() {
    elements.featuredSection.classList.remove('hidden');
    elements.featuredList.innerHTML = state.featured.slice(0, 12).map(skill =>
        createSkillCard(skill, true)
    ).join('');
}

// Create skill card HTML
function createSkillCard(skill, isFeatured = false) {
    const name = isFeatured ? skill.name : skill.n;
    const description = isFeatured ? skill.description : skill.d;
    const category = isFeatured ? skill.category : CATEGORY_NAMES[skill.c] || skill.c;
    const categoryCode = isFeatured ? skill.category : skill.c;
    const tags = isFeatured ? (skill.tags || []) : (skill.g || []);
    const stars = isFeatured ? skill.stars : skill.r;
    const install = isFeatured ? skill.install : skill.i;

    const tagsHtml = tags.slice(0, 3).map(tag =>
        `<span class="skill-tag">#${tag}</span>`
    ).join('');

    return `
        <div class="skill-card" data-install="${escapeHtml(install)}" onclick="showSkillDetail(this)">
            <div class="skill-header">
                <span class="skill-name">${escapeHtml(name)}</span>
                ${stars > 0 ? `<span class="skill-stars">⭐ ${stars.toLocaleString()}</span>` : ''}
            </div>
            <p class="skill-description">${escapeHtml(description)}</p>
            <div class="skill-meta">
                <span class="skill-category">${escapeHtml(category)}</span>
                <div class="skill-tags">${tagsHtml}</div>
            </div>
            <div class="skill-install">
                <div class="install-cmd">
                    <span class="prefix">$</span>
                    <span>sk install ${escapeHtml(install)}</span>
                    <button class="copy-btn" onclick="copyInstall(event, '${escapeHtml(install)}')" title="Copy">📋</button>
                </div>
            </div>
        </div>
    `;
}

// Search
function search(query) {
    const startTime = performance.now();

    state.currentQuery = query.trim().toLowerCase();
    state.displayedCount = 0;

    if (!state.currentQuery) {
        showFeatured();
        elements.searchResults.classList.add('hidden');
        elements.emptyState.classList.add('hidden');
        elements.loadMore.classList.add('hidden');
        elements.resultCount.textContent = '';
        elements.searchTime.textContent = '';
        return;
    }

    // Hide featured, show search results
    elements.featuredSection.classList.add('hidden');
    elements.searchResults.classList.remove('hidden');

    // Perform search
    let results = state.fuse.search(state.currentQuery);

    // Apply category filter
    if (state.currentCategory) {
        results = results.filter(r => r.item.c === state.currentCategory);
    }

    // Apply sort
    if (state.currentSort === 'stars') {
        results.sort((a, b) => (b.item.r || 0) - (a.item.r || 0));
    } else if (state.currentSort === 'name') {
        results.sort((a, b) => a.item.n.localeCompare(b.item.n));
    }

    state.results = results;

    const endTime = performance.now();
    const searchTimeMs = (endTime - startTime).toFixed(1);

    // Update UI
    elements.resultCount.textContent = `${results.length.toLocaleString()} results`;
    elements.searchTime.textContent = `${searchTimeMs}ms`;

    if (results.length === 0) {
        elements.searchResults.classList.add('hidden');
        elements.emptyState.classList.remove('hidden');
        elements.loadMore.classList.add('hidden');
    } else {
        elements.emptyState.classList.add('hidden');
        displayResults();
    }
}

// Display results with pagination
function displayResults() {
    const start = state.displayedCount;
    const end = start + CONFIG.PAGE_SIZE;
    const pageResults = state.results.slice(start, end);

    const html = pageResults.map(result => createSkillCard(result.item)).join('');

    if (start === 0) {
        elements.searchResults.innerHTML = html;
    } else {
        elements.searchResults.insertAdjacentHTML('beforeend', html);
    }

    state.displayedCount = end;

    // Show/hide load more
    if (state.displayedCount < state.results.length) {
        elements.loadMore.classList.remove('hidden');
    } else {
        elements.loadMore.classList.add('hidden');
    }
}

// Show skill detail modal
function showSkillDetail(card) {
    const install = card.dataset.install;

    // Find skill in index
    const skill = state.index.s.find(s => s.i === install);
    if (!skill) return;

    const tagsHtml = (skill.g || []).map(tag =>
        `<span class="tag">#${tag}</span>`
    ).join(' ');

    elements.modalBody.innerHTML = `
        <h2 style="margin-bottom: 1rem; color: var(--accent-primary);">${escapeHtml(skill.n)}</h2>
        <p style="margin-bottom: 1rem; color: var(--text-secondary);">${escapeHtml(skill.d)}</p>

        <div style="margin-bottom: 1rem;">
            <strong>Category:</strong> ${CATEGORY_NAMES[skill.c] || skill.c}<br>
            <strong>Stars:</strong> ${skill.r > 0 ? '⭐ ' + skill.r.toLocaleString() : 'N/A'}
        </div>

        ${tagsHtml ? `<div style="margin-bottom: 1rem;">${tagsHtml}</div>` : ''}

        <div style="margin-top: 1.5rem;">
            <strong>Install:</strong>
            <div class="install-cmd" style="margin-top: 0.5rem;">
                <span class="prefix">$</span>
                <span>sk install ${escapeHtml(install)}</span>
                <button class="copy-btn" onclick="copyInstall(event, '${escapeHtml(install)}')" title="Copy">📋</button>
            </div>
        </div>

        <div style="margin-top: 1rem;">
            <a href="https://github.com/${install}" target="_blank" style="color: var(--accent-primary);">
                View on GitHub →
            </a>
        </div>
    `;

    elements.modal.classList.remove('hidden');
}

// Copy install command
function copyInstall(event, install) {
    event.stopPropagation();
    const cmd = `sk install ${install}`;
    navigator.clipboard.writeText(cmd).then(() => {
        const btn = event.target;
        btn.textContent = '✓';
        setTimeout(() => btn.textContent = '📋', 1500);
    });
}

// Escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Debounce
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Event Listeners
elements.searchInput.addEventListener('input', debounce((e) => {
    search(e.target.value);
}, CONFIG.DEBOUNCE_MS));

elements.searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        search(e.target.value);
    }
});

elements.categoryFilter.addEventListener('change', (e) => {
    state.currentCategory = e.target.value;
    if (state.currentQuery) {
        search(state.currentQuery);
    }
});

elements.sortFilter.addEventListener('change', (e) => {
    state.currentSort = e.target.value;
    if (state.currentQuery) {
        search(state.currentQuery);
    }
});

elements.loadMoreBtn.addEventListener('click', displayResults);

// Quick tags
elements.quickTags.addEventListener('click', (e) => {
    if (e.target.classList.contains('tag')) {
        const query = e.target.dataset.query;
        elements.searchInput.value = query;
        search(query);
    }
});

// Modal
elements.modalClose.addEventListener('click', () => {
    elements.modal.classList.add('hidden');
});

elements.modal.querySelector('.modal-backdrop').addEventListener('click', () => {
    elements.modal.classList.add('hidden');
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        elements.modal.classList.add('hidden');
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Focus search on '/'
    if (e.key === '/' && document.activeElement !== elements.searchInput) {
        e.preventDefault();
        elements.searchInput.focus();
    }
});

// Initialize
init();
