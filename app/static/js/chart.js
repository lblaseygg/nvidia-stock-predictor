function updateUI(stockData, predictionData) {
    console.log('Updating UI with data:', stockData, predictionData);
    
    // Update timestamp
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('techTime').innerText = timeString;
    document.getElementById('predictionTime').innerText = timeString;

    // Update price section
    if (stockData) {
        // Current Price in Stats Section
        const currPriceElement = document.getElementById('currentPrice');
        currPriceElement.innerText = `$${stockData.current_price.toFixed(2)}`;
        
        // 24H Change in Stats Section
        const change24hElement = document.getElementById('change24h');
        const change24hValue = stockData.change_24h || 0;
        const isPositive = change24hValue > 0;
        const changeFormatted = `${isPositive ? '+' : ''}${change24hValue.toFixed(2)}%`;
        change24hElement.innerText = changeFormatted;
        change24hElement.className = `stat-value ${isPositive ? 'positive' : 'negative'}`;
        
        // Update Technical Indicators
        document.getElementById('volume').innerText = stockData.volume.toLocaleString();
        
        const rsi = stockData.rsi || 30;
        const rsiElement = document.getElementById('rsi');
        rsiElement.innerText = rsi.toFixed(2);
        
        if (rsi < 30) {
            rsiElement.className = 'indicator-value negative';
        } else if (rsi > 70) {
            rsiElement.className = 'indicator-value positive';
        } else {
            rsiElement.className = 'indicator-value neutral';
        }
        
        const macd = stockData.macd || 0.5;
        const macdElement = document.getElementById('macd');
        macdElement.innerText = macd.toFixed(4);
        macdElement.className = `indicator-value ${macd > 0 ? 'positive' : 'negative'}`;
        
        // Update navbar
        updateNavbarStats(stockData);

        // --- Update Hero Section ---
        const heroCurrentPrice = document.getElementById('heroCurrentPrice');
        if (heroCurrentPrice) {
            heroCurrentPrice.innerText = `$${stockData.current_price.toFixed(2)}`;
        }

        const heroPriceChange = document.getElementById('heroPriceChange');
        if (heroPriceChange) {
            const change24hValue = stockData.change_24h || 0;
            const isPositive = change24hValue > 0;
            heroPriceChange.innerText = `${isPositive ? '+' : ''}${change24hValue.toFixed(2)}%`;
            heroPriceChange.className = `stat-value ${isPositive ? 'positive' : 'negative'}`;
        }

        const heroRecommendation = document.getElementById('heroRecommendation');
        if (heroRecommendation && predictionData) {
            const recommendation = predictionData.recommendation || 'HOLD';
            heroRecommendation.innerText = recommendation;
            heroRecommendation.className =
                recommendation === 'BUY'
                    ? 'stat-value positive'
                    : recommendation === 'SELL'
                    ? 'stat-value negative'
                    : 'stat-value neutral';
        }
    }

    // Update prediction section
    if (predictionData) {
        // Predicted Price
        const predictedPrice = predictionData.predicted_price || stockData.current_price * 1.05;
        
        // Update all predicted price elements
        const predictedPriceElements = [
            document.getElementById('predictedPrice'),
            document.getElementById('statPredictedPrice')
        ];
        
        predictedPriceElements.forEach(elem => {
            if (elem) elem.innerText = `$${predictedPrice.toFixed(2)}`;
        });
        
        // Predicted Change
        const currentPrice = stockData ? stockData.current_price : 100; // Fallback value
        const predictedChange = ((predictedPrice - currentPrice) / currentPrice) * 100;
        const predictedChangeElement = document.getElementById('predictedChange');
        const changeFormatted = `${predictedChange > 0 ? '+' : ''}${predictedChange.toFixed(2)}%`;
        
        if (predictedChangeElement) {
            predictedChangeElement.innerText = changeFormatted;
            predictedChangeElement.className = `prediction-percentage ${predictedChange > 0 ? 'positive' : 'negative'}`;
        }
        
        // Recommendation
        const recommendation = predictionData.recommendation || (predictedChange > 0 ? 'BUY' : 'SELL');
        const recElement = document.getElementById('recommendation');
        if (recElement) {
            recElement.innerText = recommendation;
            recElement.className = `indicator-value ${recommendation === 'BUY' ? 'positive' : recommendation === 'SELL' ? 'negative' : 'neutral'}`;
        }
        
        // Confidence
        const confidence = predictionData.confidence || 75;
        
        // Update all confidence elements
        const confidenceElements = [
            document.getElementById('confidence'),
            document.getElementById('statConfidence')
        ];
        
        confidenceElements.forEach(elem => {
            if (elem) elem.innerText = `${confidence}%`;
        });
        
        // Update confidence meter
        const confidenceLevelElement = document.querySelector('.confidence-level');
        if (confidenceLevelElement) {
            confidenceLevelElement.style.width = `${confidence}%`;
            if (confidence < 50) {
                confidenceLevelElement.style.background = 'linear-gradient(90deg, #d02e5e, #ff6b81)';
            } else if (confidence < 75) {
                confidenceLevelElement.style.background = 'linear-gradient(90deg, #d0ae2e, #ffdd33)';
            } else {
                confidenceLevelElement.style.background = 'linear-gradient(90deg, #4facfe, #00f2fe)';
            }
        }
    }

    // Make sure we log statistics about all UI updates
    console.log('UI update complete. Elements updated:', {
        'navCurrentPrice': document.getElementById('navCurrentPrice')?.textContent,
        'navPriceChange': document.getElementById('navPriceChange')?.textContent,
        'currentPrice': document.getElementById('currentPrice')?.textContent,
        'heroCurrentPrice': document.getElementById('heroCurrentPrice')?.textContent,
        'heroPriceChange': document.getElementById('heroPriceChange')?.textContent,
        'predictedPrice': document.getElementById('predictedPrice')?.textContent,
        'confidence': document.getElementById('confidence')?.textContent
    });
}

// Fix fetchData function to handle separate data objects
async function fetchData() {
    try {
        const stockResponse = await fetch('/api/stock-data');
        console.log('Stock data response status:', stockResponse.status);
        
        const predictionResponse = await fetch('/api/prediction-data');
        console.log('Prediction data response status:', predictionResponse.status);
        
        if (!stockResponse.ok || !predictionResponse.ok) {
            console.error('Error fetching data:', 
                stockResponse.status, stockResponse.statusText,
                predictionResponse.status, predictionResponse.statusText);
            throw new Error(`Stock data: ${stockResponse.status}, Prediction data: ${predictionResponse.status}`);
        }
        
        const stockData = await stockResponse.json();
        const predictionData = await predictionResponse.json();
        
        console.log('Fetched stock data:', stockData);
        console.log('Fetched prediction data:', predictionData);
        
        const processedStockData = {
            current_price: stockData.current_price || 0,
            change_24h: stockData.price_change_percentage_24h || 0,
            volume: stockData.volume || 0,
            rsi: stockData.technical_indicators?.rsi || 65,
            macd: stockData.technical_indicators?.macd || 0.5,
            prices: stockData.prices || generateMockPrices(100),
            times: stockData.times || generateMockTimes(100)
        };
        
        const processedPredictionData = {
            predicted_price: predictionData.predicted_price || (processedStockData.current_price * 1.05),
            confidence: predictionData.confidence || 75,
            recommendation: predictionData.recommendation || 'BUY'
        };
        
        // Update the UI with the processed data
        updateUI(processedStockData, processedPredictionData);
        // Update the chart with real data
        updateChart(processedStockData.prices, processedStockData.times);
        
        // Update refresh button state
        const refreshButton = document.getElementById('refreshButton');
        if (refreshButton) {
            refreshButton.classList.remove('loading');
        }
        
    } catch (error) {
        console.error('Error in fetchData:', error);
        
        // Generate mock data for UI testing
        const mockStockData = {
            current_price: 546.78,
            change_24h: 2.35,
            volume: 12500000,
            rsi: 62,
            macd: 0.67,
            signal_strength: 78,
            technical_indicators: {
                rsi: 62,
                macd: 0.67
            },
            prices: generateMockPrices(100),
            times: generateMockTimes(100)
        };
        
        const mockPredictionData = {
            predicted_price: 579.25,
            confidence: 85,
            recommendation: 'BUY'
        };
        
        console.log('Using mock data due to API error:', mockStockData, mockPredictionData);
        updateUI(mockStockData, mockPredictionData);
    }
}

// Update navbar stats with correct IDs
function updateNavbarStats(stockData) {
    if (!stockData) return;
    const navCurrentPrice = document.getElementById('navCurrentPrice');
    if (navCurrentPrice) {
        navCurrentPrice.textContent = `$${stockData.current_price.toFixed(2)}`;
    }
    const navPriceChange = document.getElementById('navPriceChange');
    if (navPriceChange) {
        const change24h = stockData.change_24h || 0;
        navPriceChange.textContent = `${change24h > 0 ? '+' : ''}${change24h.toFixed(2)}%`;
        navPriceChange.className = 'stat-value ' + (change24h >= 0 ? 'positive' : 'negative');
    }
}

// Helper function to generate mock prices for testing
function generateMockPrices(count = 100) {
    const basePrice = 550;
    let price = basePrice;
    const prices = [];
    
    for (let i = 0; i < count; i++) {
        // Generate some realistic-looking price variations
        const change = (Math.random() - 0.48) * 5; // Slight upward bias
        price = Math.max(price + change, price * 0.995); // Prevent extreme drops
        prices.push(price);
    }
    
    return prices;
}

// Helper function to generate mock times for testing
function generateMockTimes(count = 100) {
    const times = [];
    const now = new Date();
    
    for (let i = 0; i < count; i++) {
        const time = new Date(now);
        // Go back in time, with each point representing 5 minutes
        time.setMinutes(now.getMinutes() - (count - i) * 5);
        times.push(time.toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        }));
    }
    
    return times;
}

// Initialize the chart
let priceChart;

function initializeChart() {
    const ctx = document.getElementById('priceChart');
    if (!ctx) {
        console.error('Price chart canvas not found!');
        return;
    }
    
    // Chart.js configuration
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'NVDA Price',
                data: [],
                borderColor: '#4facfe',
                backgroundColor: 'rgba(79, 172, 254, 0.1)',
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: '#4facfe',
                pointHoverBorderColor: '#ffffff',
                pointHoverBorderWidth: 2,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)',
                        tickLength: 0
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.6)',
                        font: {
                            size: 10
                        },
                        maxRotation: 0,
                        maxTicksLimit: 8,
                        callback: function(value, index, values) {
                            const time = value.toString();
                            if (time.includes(':')) {
                                return time; // Return the time string directly
                            }
                            return value;
                        }
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.6)',
                        font: {
                            size: 10
                        },
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(13, 17, 23, 0.9)',
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    titleFont: {
                        size: 12,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 12
                    },
                    padding: 12,
                    displayColors: false,
                    callbacks: {
                        label: function(context) {
                            return 'Price: $' + context.raw.toFixed(2);
                        }
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            },
            animation: {
                duration: 1000,
                easing: 'easeOutQuart'
            }
        }
    });
    
    return priceChart;
}

// Function to update the chart with new data
function updateChart(prices, times) {
    if (!priceChart) {
        priceChart = initializeChart();
        if (!priceChart) return; // Exit if chart initialization failed
    }
    
    // Update the chart data
    priceChart.data.labels = times;
    priceChart.data.datasets[0].data = prices;
    
    // Define gradient fill
    const ctx = document.getElementById('priceChart').getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(79, 172, 254, 0.2)');
    gradient.addColorStop(0.8, 'rgba(79, 172, 254, 0.0)');
    priceChart.data.datasets[0].backgroundColor = gradient;
    
    // Update the chart
    priceChart.update();
}

// Initialize refresh button
function initRefreshButton() {
    // Main nav refresh button
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            this.classList.add('loading');
            fetchData().then(() => {
                setTimeout(() => {
                    this.classList.remove('loading');
                }, 500);
            });
        });
    }
    
    // Chart refresh button - handles the newly renamed button
    const chartRefreshBtn = document.getElementById('chartRefreshBtn');
    if (chartRefreshBtn) {
        chartRefreshBtn.addEventListener('click', function() {
            this.classList.add('loading');
            fetchData().then(() => {
                setTimeout(() => {
                    this.classList.remove('loading');
                }, 500);
            });
        });
    }
    
    // Hero refresh button
    const heroRefreshBtn = document.getElementById('heroRefreshBtn');
    if (heroRefreshBtn) {
        heroRefreshBtn.addEventListener('click', function() {
            this.classList.add('loading');
            fetchData().then(() => {
                setTimeout(() => {
                    this.classList.remove('loading');
                }, 500);
            });
        });
    }
}

// Set up event listeners for time period buttons
document.addEventListener('DOMContentLoaded', function() {
    const timePeriodButtons = document.querySelectorAll('.time-period-btn');
    
    timePeriodButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            timePeriodButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Get the time period
            const period = this.getAttribute('data-period');
            console.log(`Changing time period to: ${period}`);
            
            // Here you would fetch data for the selected time period
            // For now, let's just simulate it with mock data
            const mockData = generateMockDataForPeriod(period);
            updateChart(mockData.prices, mockData.times);
        });
    });
    
    // Initialize chart and fetch data
    initializeChart();
    initRefreshButton();
    
    // Fetch data immediately when page loads
    fetchData();
});

// Generate mock data based on time period
function generateMockDataForPeriod(period) {
    let count, timeFormat;
    switch (period) {
        case '1h':
            count = 12;
            timeFormat = { hour: 'numeric', minute: '2-digit', hour12: true };
            break;
        case '1d':
            count = 24;
            timeFormat = { hour: 'numeric', hour12: true };
            break;
        case '1w':
            count = 7;
            timeFormat = { weekday: 'short' };
            break;
        case '1m':
            count = 30;
            timeFormat = { month: 'short', day: 'numeric' };
            break;
        case '1y':
            count = 12;
            timeFormat = { month: 'short', year: 'numeric' };
            break;
        default:
            count = 24;
            timeFormat = { hour: 'numeric', hour12: true };
    }
    
    const prices = generateMockPrices(count);
    const times = [];
    const now = new Date();
    
    for (let i = 0; i < count; i++) {
        const time = new Date(now);
        
        // Adjust time based on period
        switch (period) {
            case '1h':
                time.setMinutes(time.getMinutes() - (count - i) * 5);
                break;
            case '1d':
                time.setHours(time.getHours() - (count - i));
                break;
            case '1w':
                time.setDate(time.getDate() - (count - i));
                break;
            case '1m':
                time.setDate(time.getDate() - (count - i));
                break;
            case '1y':
                time.setMonth(time.getMonth() - (count - i));
                break;
        }
        
        times.push(time.toLocaleString('en-US', timeFormat));
    }
    
    return { prices, times };
}