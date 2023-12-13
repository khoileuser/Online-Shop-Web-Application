// Sets the source of a frame element to the URL of the selected file.
function preview() {
  frame.src = URL.createObjectURL(event.target.files[0]);
}

// Clears the value of a file input element and sets the source of an image element to a default image.
function clearImage() {
  document.getElementById('formFile').value = "";
  frame.src = "/images/profiles/default.jpg";
}

function accountTypeCheck() {
  const accounttype = document.getElementsByName('accounttype');
  var accountTypeCheck = false;
  for (i = 0; i < accounttype.length; i++) {
    if (accounttype[i].checked) {
      return true;
    }
  }
  return false;
}

function signInEditName() {
  const _name = document.querySelector('.name');
  if (_name.value.length == "" || _name.value.length > 255) {
    document.querySelector('.name-danger').style.display = "block";
    document.querySelector('.signin-btn').setAttribute("disabled", "");
  }
  else {
    document.querySelector('.name-danger').style.display = "none";
    if (document.querySelector('.username-danger').style.display == "none" & document.querySelector('.password-danger').style.display == "none") {
      if (accountTypeCheck() == true) {
        document.querySelector('.signin-btn').removeAttribute("disabled");
      }
    }
  }
}

function signInEditUsername() {
  const username = document.querySelector('.username');
  if (username.value.length < 4 || username.value.length > 25 || ! /^[a-zA-Z0-9]+$/.test(username.value)) {
    document.querySelector('.username-danger').style.display = "block";
    document.querySelector('.signin-btn').setAttribute("disabled", "");
  }
  else {
    document.querySelector('.username-danger').style.display = "none";
    if (document.querySelector('.name-danger').style.display == "none" & document.querySelector('.password-danger').style.display == "none") {
      if (accountTypeCheck() == true) {
        document.querySelector('.signin-btn').removeAttribute("disabled");
      }
    }
  }
}

function signInEditPassword() {
  const password = document.querySelector('.password')
  if (! /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,255}$/.test(password.value)) {
    document.querySelector('.password-danger').style.display = "block";
    document.querySelector('.signin-btn').setAttribute("disabled", "");
  }
  else {
    document.querySelector('.password-danger').style.display = "none";
    if (document.querySelector('.name-danger').style.display == "none" & document.querySelector('.username-danger').style.display == "none") {
      if (accountTypeCheck() == true) {
        document.querySelector('.signin-btn').removeAttribute("disabled");
      }
    }
  }
}

function signInEditType() {
  document.querySelector('.signin-btn').setAttribute("disabled", "");
  if (accountTypeCheck() == true) {
    if (document.querySelector('.name-danger').style.display == "none" & document.querySelector('.username-danger').style.display == "none" & document.querySelector('.password-danger').style.display == "none") {
      document.querySelector('.signin-btn').removeAttribute("disabled");
    }
  }
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