// Function to loan a book to a customer
function loanBook(customerId, bookId, loanOption) {
    fetch('/api/loan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            customerId,
            bookId,
            loanOption,
        }),
    })
    .then(response => {
        if (response.ok) {
            // Book loaned successfully, you can update the UI
        } else {
            console.error('Error loaning book:', response.statusText);
        }
    })
    .catch(error => console.error('Error loaning book:', error));
}
