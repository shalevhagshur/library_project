// Function to fetch and display a list of all books
function displayBooks() {
    fetch('/api/books')
        .then(response => response.json())
        .then(data => {
            // Handle the data and display it in your HTML
            // For example, you can append book information to a table or list
        })
        .catch(error => console.error('Error fetching books:', error));
}

// Function to add a new book
function addBook(bookData) {
    fetch('/api/books', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookData),
    })
    .then(response => {
        if (response.ok) {
            // Book added successfully, you can update the UI
        } else {
            console.error('Error adding book:', response.statusText);
        }
    })
    .catch(error => console.error('Error adding book:', error));
}
