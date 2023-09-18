document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.querySelector('#register-form');
    const registerButton = document.querySelector('#register-button');

    registerButton.addEventListener('click', function (event) {
        event.preventDefault();

        const usernameInput = document.querySelector('#username-input');
        const passwordInput = document.querySelector('#password-input');

        const userData = {
            username: usernameInput.value,
            password: passwordInput.value
        };

        fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        })
        .then(response => {
            if (response.status === 201) {
                // Registration successful
                console.log('Registration successful');
                // You can redirect to the login page or perform other actions here
            } else if (response.status === 400) {
                // Bad request, e.g., missing or invalid data
                console.error('Invalid registration data');
            } else {
                // Handle other error cases here
                console.error('Registration failed');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
