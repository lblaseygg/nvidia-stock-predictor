// This trading.js file is for updating predictions and technical analysis
// It complements chart.js which handles chart rendering and UI updates

// Function to update trading signals
async function updateTradingSignals() {
    try {
        const response = await fetch('/api/prediction');
        if (!response.ok) {
            console.warn(`Prediction API returned status: ${response.status}`);
            return null; // Return null to indicate failure
        }
        
        const data = await response.json();
        
        if (data.error) {
            console.warn('Prediction API returned error:', data.error);
            return null; // Return null to indicate failure
        }

        console.log('Successfully fetched trading signals:', data);
        return data; // Return the data for potential use by other functions
    } catch (error) {
        console.error('Error updating trading signals:', error);
        return null; // Return null to indicate failure
    }
}

// Function to update model and get new predictions
async function updateModel() {
    console.log('Updating AI model...');
    try {
        // Update model and get new predictions
        const response = await fetch('/api/update-model', {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }

        console.log('Model updated successfully:', data);
        return data;
    } catch (error) {
        console.error('Error updating model:', error);
        return null;
    }
}

// Initialize when DOM is loaded but avoid duplicate initialization
// We're not adding event listeners here to avoid conflicts with chart.js
document.addEventListener('DOMContentLoaded', () => {
    console.log('Trading.js initialized');
    
    // Initial signal update (if not handled by chart.js)
    // Only do this if chart.js hasn't initialized the data
    if (typeof window.dataInitialized === 'undefined') {
        setTimeout(() => {
            // After 2 seconds, check if data is still not initialized
            if (typeof window.dataInitialized === 'undefined') {
                console.log('Initializing data from trading.js');
                updateTradingSignals();
                window.dataInitialized = true;
            }
        }, 2000);
    }
});

// Scroll to explore functionality
document.addEventListener('DOMContentLoaded', function() {
    const scrollIndicator = document.getElementById('scrollIndicator');
    const mainContent = document.getElementById('main-content');

    if (scrollIndicator && mainContent) {
        scrollIndicator.addEventListener('click', function() {
            mainContent.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
            });
        });

        // Hide scroll indicator when user scrolls past hero section
        window.addEventListener('scroll', function() {
            const heroSection = document.querySelector('.hero-section');
            if (heroSection) {
                const heroBottom = heroSection.getBoundingClientRect().bottom;
                if (heroBottom <= 0) {
                    scrollIndicator.style.opacity = '0';
                    scrollIndicator.style.visibility = 'hidden';
                } else {
                    scrollIndicator.style.opacity = '1';
                    scrollIndicator.style.visibility = 'visible';
                }
            }
        });
    }
});

// Stock dropdown functionality
document.addEventListener('DOMContentLoaded', function() {
    const stockButton = document.querySelector('.stock-button');
    const stockDropdown = document.querySelector('.stock-dropdown');

    if (stockButton && stockDropdown) {
        stockButton.addEventListener('click', function() {
            stockButton.classList.toggle('active');
            stockDropdown.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(event) {
            if (!stockButton.contains(event.target) && !stockDropdown.contains(event.target)) {
                stockButton.classList.remove('active');
                stockDropdown.classList.remove('active');
            }
        });

        // Handle stock option clicks
        const stockOptions = document.querySelectorAll('.stock-option:not(.disabled)');
        stockOptions.forEach(option => {
            option.addEventListener('click', function() {
                const symbol = this.querySelector('.stock-symbol').textContent;
                const name = this.querySelector('.stock-name').textContent;
                
                // Update the button text
                stockButton.querySelector('h2').textContent = name;
                
                // Update active state
                stockOptions.forEach(opt => opt.classList.remove('active'));
                this.classList.add('active');
                
                // Close dropdown
                stockButton.classList.remove('active');
                stockDropdown.classList.remove('active');
                
                // Navigate to the stock page
                window.location.href = `/stock/${symbol}`;
            });
        });
    }
});

// Export functions for use by other scripts
window.tradingModule = {
    updateTradingSignals,
    updateModel
}; 