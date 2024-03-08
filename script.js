function authenticateUser() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Add your authentication logic here
    if (username.trim() !== "" && password.trim() !== "") {
        // Check if the user exists in creds.csv
        if (checkUserExists(username, password)) {
            alert("Login successful!");
            // Add code to redirect or perform actions after successful login
        } else {
            alert("Login failed. Please try again.");
        }
    } else {
        alert("Please enter both username and password.");
    }
}

function createOrUpdateCreds(username, password) {
    // Read creds.csv and update it with the new user
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'creds.csv', false);
    xhr.send();

    var newCsvLine = username + ',' + password;

    if (xhr.status === 200) {
        // Update the existing CSV content
        var updatedCsv = xhr.responseText + '\n' + newCsvLine;
        xhr.open('POST', 'update_creds.php', false); // Use a server-side script to update the file
        xhr.setRequestHeader('Content-Type', 'text/csv');
        xhr.send(updatedCsv);
    } else {
        // Create a new CSV file
        xhr.open('POST', 'create_creds.php', false); // Use a server-side script to create the file
        xhr.setRequestHeader('Content-Type', 'text/csv');
        xhr.send('Username,Password\n' + newCsvLine);
    }
}

function createUserFolder(username) {
    // Assume this is an asynchronous operation (e.g., using fetch or XMLHttpRequest)
    // For simplicity, using a synchronous XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'check_folder.php?username=' + username, false);
    xhr.send();

    if (xhr.status === 404) {
        // User folder does not exist, create it
        xhr.open('POST', 'create_folder.php', false); // Use a server-side script to create the folder
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send('username=' + username);
    } else {
        // User folder exists
        alert("User folder already exists.");
    }
}

function createNewUser() {
    var newUsername = document.getElementById('new-username').value;
    var newPassword = document.getElementById('new-password').value;

    // Add your signup logic here
    if (newUsername.trim() !== "" && newPassword.trim() !== "") {
        // Check if the user already exists
        if (!checkUserExists(newUsername)) {
            // Save the new user to localStorage
            saveUserToLocalStorage(newUsername, newPassword);

            // Create a user folder
            createUserFolder(newUsername);

            alert("Sign up successful!");

            // Redirect to the login page
            window.location.href = 'index.html';
        } else {
            alert("User already exists. Choose a different username.");
        }
    } else {
        alert("Please enter both username and password.");
    }
}

function checkUserExists(username) {
    // Check if the user already exists in localStorage
    var storedUsers = localStorage.getItem('users');
    if (storedUsers) {
        var users = JSON.parse(storedUsers);
        return users.hasOwnProperty(username);
    }
    return false;
}

function saveUserToLocalStorage(username, password) {
    // Save the new user to localStorage
    var storedUsers = localStorage.getItem('users');
    var users = storedUsers ? JSON.parse(storedUsers) : {};
    users[username] = password;
    localStorage.setItem('users', JSON.stringify(users));
}
function createUserFolder(username) {
    // Assume this is an asynchronous operation (e.g., using fetch or XMLHttpRequest)
    // For simplicity, using a synchronous XMLHttpRequest
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'check_folder.php?username=' + username, false);
    xhr.send();

    if (xhr.status === 404) {
        // User folder does not exist, create it
        xhr.open('POST', 'create_folder.php', false); // Use a server-side script to create the folder
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send('username=' + username);
    } else {
        // User folder exists
        alert("User folder already exists.");
    }
}

