// Dashboard async data loader
document.addEventListener('DOMContentLoaded', function() {
    // Show loading indicators
    showLoadingStates();
    
    // Load dashboard data asynchronously
    loadDashboardData();
});

function showLoadingStates() {
    // Show loading spinners for different sections
    const sections = ['weather-section', 'market-section', 'alerts-section'];
    sections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            section.innerHTML = '<div class="text-center p-4"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
        }
    });
}

function loadDashboardData() {
    // Load main dashboard data
    fetch('/api/dashboard-data')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateWeatherSection(data.weather);
                updateMarketSection(data.market_data);
                
                // Load additional data after main data loads
                setTimeout(() => {
                    loadAlerts();
                    loadMarketInsights();
                }, 1000);
            } else {
                showError('Failed to load dashboard data');
            }
        })
        .catch(error => {
            console.error('Dashboard loading error:', error);
            showError('Network error loading dashboard');
        });
}

function loadAlerts() {
    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateAlertsSection(data.alerts, data.summary);
            }
        })
        .catch(error => console.error('Alerts loading error:', error));
}

function loadMarketInsights() {
    fetch('/api/market-insights')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateInsightsSection(data.insights);
            }
        })
        .catch(error => console.error('Insights loading error:', error));
}

function updateWeatherSection(weather) {
    const section = document.getElementById('weather-section');
    if (section && weather) {
        section.innerHTML = `
            <div class="weather-card">
                <h3>${weather.city || 'Your Location'}</h3>
                <div class="temperature">${weather.temperature || 'N/A'}°C</div>
                <div class="condition">${weather.condition || 'Loading...'}</div>
                <div class="humidity">Humidity: ${weather.humidity || 'N/A'}%</div>
            </div>
        `;
    }
}

function updateMarketSection(marketData) {
    const section = document.getElementById('market-section');
    if (section && marketData) {
        let html = '<h3>Market Prices</h3>';
        if (marketData.length > 0) {
            marketData.forEach(crop => {
                html += `
                    <div class="market-item">
                        <span class="crop-name">${crop.commodity}</span>
                        <span class="price">₹${crop.modal_price}/kg</span>
                    </div>
                `;
            });
        } else {
            html += '<p>No market data available</p>';
        }
        section.innerHTML = html;
    }
}

function updateAlertsSection(alerts, summary) {
    const section = document.getElementById('alerts-section');
    if (section) {
        let html = '<h3>Price Alerts</h3>';
        if (alerts && alerts.length > 0) {
            alerts.forEach(alert => {
                html += `
                    <div class="alert-item ${alert.type}">
                        <i class="fas fa-bell"></i> ${alert.message}
                    </div>
                `;
            });
        } else {
            html += '<p>No active alerts</p>';
        }
        section.innerHTML = html;
    }
}

function updateInsightsSection(insights) {
    const section = document.getElementById('insights-section');
    if (section && insights) {
        let html = '<h3>Market Insights</h3>';
        if (insights.length > 0) {
            insights.forEach(insight => {
                html += `
                    <div class="insight-item">
                        <strong>${insight.crop}</strong>: ${insight.recommendation}
                    </div>
                `;
            });
        } else {
            html += '<p>No insights available</p>';
        }
        section.innerHTML = html;
    }
}

function showError(message) {
    const sections = ['weather-section', 'market-section', 'alerts-section'];
    sections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (section) {
            section.innerHTML = `<div class="alert alert-warning">${message}</div>`;
        }
    });
}