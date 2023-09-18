// Function to fetch and display a list of all customers
function displayCustomers() {
    fetch('/api/customers')
        .then(response => response.json())
        .then(data => {
            // Handle the data and display it in your HTML
            // For example, you can append customer information to a table or list
        })
        .catch(error => console.error('Error fetching customers:', error));
}

// Function to add a new customer
function addCustomer(customerData) {
    fetch('/api/customers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(customerData),
    })
    .then(response => {
        if (response.ok) {
            // Customer added successfully, you can update the UI
        } else {
            console.error('Error adding customer:', response.statusText);
        }
    })
    .catch(error => console.error('Error adding customer:', error));
}
