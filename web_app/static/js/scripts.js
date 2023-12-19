/**
 * The customAlert function displays a message in an alert container for a specified duration of time.
 * @param message - The message parameter is a string that represents the message you want to display
 * in the alert.
 */
function customAlert(message) {
  var alertContainer = document.querySelector('.alert-container');
  var alertMsg = document.querySelector('.alert-msg');
  alertMsg.innerHTML = message;
  alertContainer.style.display = 'block';

  setTimeout(function () {
    alertContainer.style.display = 'none';
    alertMsg.innerHTML = "";
  }, 10000);
}

/* The code is adding an event listener to the window object for the scroll event. When the user
scrolls the page, the function is triggered. */
window.onscroll = function () {
  var navbar = document.querySelector('.navbar')
  if (window.scrollY > 100) {
    navbar.classList.add('navbar-scrolled')
  }
  else {
    navbar.classList.remove('navbar-scrolled')
  }
}


/**
 * The `signIn` function sends a POST request to the server to check the user's credentials and if they
 * are valid, it submits the sign-in form.
 */
function signIn() {
  document.querySelector('.signin-btn').setAttribute("disabled", "");
  document.querySelector('.spinner').style.display = "flex";
  const username = document.querySelector('.username').value;
  const password = document.querySelector('.password').value;
  fetch('/check/signin/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
      'username': username,
      'password': password
    })
  })
    .then(response => response.text())
    .then(data => {
      if (data == "false") {
        customAlert("Login failed! Please check your credentials.");
        document.querySelector('.signin-btn').removeAttribute("disabled");
        document.querySelector('.spinner').style.display = "none";
      }
      else {
        // submit form if all is passed
        document.querySelector('.signin-form').submit();
      }
    });
}

/**
 * The function checks if any account type is selected in a form.
 * @returns a boolean value. It returns true if at least one of the radio buttons with the name
 * 'accounttype' is checked, and false otherwise.
 */
function accountTypeCheck() {
  const accounttype = document.getElementsByName('accounttype');
  for (i = 0; i < accounttype.length; i++) {
    if (accounttype[i].checked) {
      return true;
    }
  }
  return false;
}

/**
 * The function checks if the length of the name input is empty or exceeds 255 characters, and displays
 * an error message and disables the signup button if it does.
 */
function signUpEditName() {
  const _name = document.querySelector('.name');
  if (_name.value.length == "" || _name.value.length > 255) {
    document.querySelector('.name-danger').style.display = "block";
    document.querySelector('.signup-btn').setAttribute("disabled", "");
  }
  else {
    document.querySelector('.name-danger').style.display = "none";
    if (document.querySelector('.username-danger').style.display == "none" & document.querySelector('.password-danger').style.display == "none") {
      if (accountTypeCheck() == true) {
        document.querySelector('.signup-btn').removeAttribute("disabled");
      }
    }
  }
}

/**
 * The function checks if the username input meets certain criteria and enables or disables the signup
 * button accordingly.
 */
function signUpEditUsername() {
  const username = document.querySelector('.username');
  if (username.value.length < 4 || username.value.length > 25 || ! /^[a-zA-Z0-9]+$/.test(username.value)) {
    document.querySelector('.username-danger').style.display = "block";
    document.querySelector('.signup-btn').setAttribute("disabled", "");
  }
  else {
    document.querySelector('.username-danger').style.display = "none";
    if (document.querySelector('.name-danger').style.display == "none" & document.querySelector('.password-danger').style.display == "none") {
      if (accountTypeCheck() == true) {
        document.querySelector('.signup-btn').removeAttribute("disabled");
      }
    }
  }
}

/**
 * The function checks if the password entered meets certain criteria and enables the signup button if
 * all other required fields are also filled.
 */
function signUpEditPassword() {
  const password = document.querySelector('.password')
  if (! /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,255}$/.test(password.value)) {
    document.querySelector('.password-danger').style.display = "block";
    document.querySelector('.signup-btn').setAttribute("disabled", "");
  }
  else {
    document.querySelector('.password-danger').style.display = "none";
    if (document.querySelector('.name-danger').style.display == "none" & document.querySelector('.username-danger').style.display == "none") {
      if (accountTypeCheck() == true) {
        document.querySelector('.signup-btn').removeAttribute("disabled");
      }
    }
  }
}

/**
 * The function "signUpEditType" disables the signup button and enables it only if the account type is
 * checked and there are no errors in the name, username, and password fields.
 */
function signUpEditType() {
  document.querySelector('.signup-btn').setAttribute("disabled", "");
  if (accountTypeCheck() == true) {
    if (document.querySelector('.name-danger').style.display == "none" & document.querySelector('.username-danger').style.display == "none" & document.querySelector('.password-danger').style.display == "none") {
      document.querySelector('.signup-btn').removeAttribute("disabled");
    }
  }
}

/**
 * The function "signInEdit" disables the sign-in button if either the username or password input
 * fields are empty, and enables it otherwise.
 */
function signInEdit() {
  document.querySelector('.signin-btn').setAttribute("disabled", "");
  if (document.querySelector('.username').value.length > 0 & document.querySelector('.password').value.length > 0) {
    document.querySelector('.signin-btn').removeAttribute("disabled");
  }
}

/**
 * The function `signUp()` is used to handle the sign-up process by checking if a username is already
 * taken and submitting the form if it is not.
 */
function signUp() {
  document.querySelector('.signup-btn').setAttribute("disabled", "");
  document.querySelector('.spinner').style.display = "flex";
  const username = document.querySelector('.username').value;
  fetch('/check/signup/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
      'username': username
    })
  })
    .then(response => response.text())
    .then(data => {
      if (data == "true") {
        customAlert("Username is already used, please try another username.");
        document.querySelector('.signup-btn').removeAttribute("disabled");
        document.querySelector('.spinner').style.display = "none";
      }
      else {
        // submit form if all is passed
        document.querySelector('.signup-form').submit();
      }
    });
}

function toggleCreditCardFields() {
  var paymentMethod = document.getElementById('payment');
  var creditCardFields = document.getElementById('creditCardFields');

  if (paymentMethod.value === 'credit') {
    creditCardFields.style.display = 'block';
  } else {
    creditCardFields.style.display = 'none';
  }
}