document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.querySelector('#login-form');
    const loginButton = document.querySelector('#login-button');

    loginButton.addEventListener('click', function (event) {
        event.preventDefault();

        const usernameInput = document.querySelector('#username-input');
        const passwordInput = document.querySelector('#password-input');

        const userData = {
            username: usernameInput.value,
            password: passwordInput.value
        };

        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => {
            if (response.status === 200) {
                // Login successful
                console.log('Login successful');
                // You can redirect to the user's dashboard or perform other actions here
            } else if (response.status === 400) {
                // Bad request, e.g., missing or invalid data
                console.error('Invalid login data');
            } else if (response.status === 401) {
                // Unauthorized, login failed
                console.error('Login failed. Please check your credentials');
            } else {
                // Handle other error cases here
                console.error('Login failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
