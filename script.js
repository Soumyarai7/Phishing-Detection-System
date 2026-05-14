document.addEventListener('DOMContentLoaded', () => {
    const scanForm = document.getElementById('scanForm');
    const urlInput = document.getElementById('urlInput');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');

    scanForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const urlToScan = urlInput.value.trim();
        if (!urlToScan) return;

        // Reset UI
        results.classList.add('hidden');
        loading.classList.remove('hidden');

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: urlToScan })
            });

            const data = await response.json();
            
            if (response.ok) {
                displayResults(data);
            } else {
                displayError(data.error || "An unknown error occurred during analysis.");
            }
            
        } catch (error) {
            console.error("Error scanning URL:", error);
            displayError("Failed to connect to the analysis engine. Please try again later.");
        } finally {
            loading.classList.add('hidden');
        }
    });

    function displayResults(data) {
        let statusIcon = '';
        let statusClass = '';
        let listClass = '';

        if (data.classification === 'Safe') {
            statusIcon = '<i class="fa-solid fa-shield-check"></i>';
            statusClass = 'status-safe';
            listClass = 'safe-list';
            if (data.reasons.length === 0) {
                data.reasons.push("No suspicious indicators found.");
            }
        } else if (data.classification === 'Suspicious') {
            statusIcon = '<i class="fa-solid fa-triangle-exclamation"></i>';
            statusClass = 'status-suspicious';
            listClass = 'suspicious-list';
        } else {
            statusIcon = '<i class="fa-solid fa-skull-crossbones"></i>';
            statusClass = 'status-phishing';
            listClass = 'phishing-list';
        }

        let reasonsHtml = `<ul class="reasons-list ${listClass}">`;
        data.reasons.forEach(reason => {
            reasonsHtml += `<li><i class="fa-solid fa-circle-info"></i><span>${reason}</span></li>`;
        });
        reasonsHtml += '</ul>';

        results.innerHTML = `
            <div class="result-header">
                <div class="status-icon ${statusClass}">
                    ${statusIcon}
                </div>
                <div>
                    <div class="result-title ${statusClass}">${data.classification} Domain</div>
                    <div class="result-score">Threat Score: ${data.score}</div>
                </div>
            </div>
            ${reasonsHtml}
        `;
        
        results.classList.remove('hidden');
    }

    function displayError(message) {
        results.innerHTML = `
            <div class="result-header">
                <div class="status-icon status-suspicious">
                    <i class="fa-solid fa-circle-exclamation"></i>
                </div>
                <div>
                    <div class="result-title status-suspicious">Analysis Failed</div>
                </div>
            </div>
            <ul class="reasons-list suspicious-list">
                <li><i class="fa-solid fa-circle-info"></i><span>${message}</span></li>
            </ul>
        `;
        results.classList.remove('hidden');
    }
});
