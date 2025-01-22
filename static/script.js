document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        // Ensure the response is handled correctly
        if (!response.ok) {
            const errorText = await response.text();
            document.getElementById('outputText').value = `Error: ${errorText}`;
        } else {
            const resultJson = await response.json();
            const { decision, credit_limit, justification, recommendations } = resultJson;

            const outputText = document.getElementById('outputText');
            outputText.innerHTML = `Decision: ${decision}
                Maximum sustainable EMI Limit: $${credit_limit}
                Justification: ${justification}
                Recommendation: ${recommendations}`;
            
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('outputText').value = `Error: ${error.message}`;
    }
});




// Get references to sliders and output elements (working)
const loanAmountSlider = document.getElementById('loanAmount');
const timeYearsSlider = document.getElementById('timeYears');
const interestRateSlider = document.getElementById('interestRate');

const loanAmountOutput = document.getElementById('loanAmountOutput');
const timeYearsOutput = document.getElementById('timeYearsOutput');
const interestRateOutput = document.getElementById('interestRateOutput');
const riskOutput = document.getElementById('riskOutput');

// Function to calculate and update the "Risk"
function updateEMI() {
    const loanAmount = parseFloat(loanAmountSlider.value); // Principal amount
    const timeYears = parseFloat(timeYearsSlider.value);   // Tenure in years
    const interestRate = parseFloat(interestRateSlider.value); // Annual interest rate

    // Convert annual interest rate to monthly rate and tenure to months
    const monthlyRate = interestRate / 12 / 100;
    const tenureMonths = timeYears * 12;

    // EMI formula
    const emi = (loanAmount * monthlyRate * Math.pow(1 + monthlyRate, tenureMonths)) / 
                (Math.pow(1 + monthlyRate, tenureMonths) - 1);


                
    // Display the EMI result
    riskOutput.textContent = emi.toFixed(2);
}


// Update the displayed slider values and recalculate the "Risk"
loanAmountSlider.addEventListener('input', () => {
    loanAmountOutput.textContent = loanAmountSlider.value;
    updateEMI();
});

timeYearsSlider.addEventListener('input', () => {
    timeYearsOutput.textContent = timeYearsSlider.value;
    updateEMI();
});

interestRateSlider.addEventListener('input', () => {
    interestRateOutput.textContent = interestRateSlider.value;
    updateEMI();
});

// Initialize the "Risk" value on page load
updateEMI();

// Red the credit limit:
