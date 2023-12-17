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

function accountTypeCheck() {
  const accounttype = document.getElementsByName('accounttype');
  for (i = 0; i < accounttype.length; i++) {
    if (accounttype[i].checked) {
      return true;
    }
  }
  return false;
}

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

function signUpEditType() {
  document.querySelector('.signup-btn').setAttribute("disabled", "");
  if (accountTypeCheck() == true) {
    if (document.querySelector('.name-danger').style.display == "none" & document.querySelector('.username-danger').style.display == "none" & document.querySelector('.password-danger').style.display == "none") {
      document.querySelector('.signup-btn').removeAttribute("disabled");
    }
  }
}

function signInEdit() {
  document.querySelector('.signin-btn').setAttribute("disabled", "");
  if (document.querySelector('.username').value.length > 0 & document.querySelector('.password').value.length > 0) {
    document.querySelector('.signin-btn').removeAttribute("disabled");
  }
}

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