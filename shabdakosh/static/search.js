const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');

let debounceTimer;

searchInput.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    const query = this.value.trim();

    if (query.length < 2) {
        searchResults.style.display = 'none';
        return;
    }

    debounceTimer = setTimeout(() => {
        fetch(`/api/search?q=${encodeURIComponent(query)}`)
            .then(res => res.json())
            .then(data => {
                if (data.results.length === 0) {
                    searchResults.style.display = 'none';
                    return;
                }

                searchResults.innerHTML = data.results.map(term => `
                    <div class="result-item" onclick="logAndGo(${term.id}, '${term.english}')">
                        <div>
                            <span class="term-english">${term.english}</span>
                            <span class="term-nepali">${term.nepali}</span>
                        </div>
                        <div class="term-subject">${term.subject}</div>
                    </div>
                `).join('');

                searchResults.style.display = 'block';
            });
    }, 300);
});

document.addEventListener('click', function(e) {
    if (!searchInput.contains(e.target)) {
        searchResults.style.display = 'none';
    }
});

function logAndGo(termId, query) {
    fetch(`/api/log?q=${encodeURIComponent(query)}&term_id=${termId}`)
        .then(() => {
            window.location = `/term/${termId}`;
        });
}