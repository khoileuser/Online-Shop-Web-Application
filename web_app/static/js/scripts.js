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

// Clears the value of a file input element and sets the source of an image element to a default image.
function clearImage() {
  document.getElementById('formFile').value = "";
  frame.src = "/images/profiles/default.jpg";
}

function showProvinces() {

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

function changeLargeImg(image) {
  largeImage = document.querySelector('.large-image');
  largeImage.src = image.src;
}

function doFetch(action, productid, quantity, reload = false) {
  return fetch('/cart/' + action + '/' + productid + '/quantity/' + quantity, {
    method: 'POST'
  }).then(function (response) {
    if (reload == true) {
      location.reload()
    }
  }).catch(function (err) {
    console.log(`Error: ${err}`)
  });
}

function updateCartCount() {
  var cartQuantity = document.querySelector('.cart-count');
  if (parseInt(cartQuantity.innerHTML.trim()) - 1 >= 0) {
    cartQuantity.innerHTML = parseInt(cartQuantity.innerHTML.trim()) - 1;
  }
}

function editQuantity(productid, action, _quantity, noUpdate = false, limit = false) {
  var quantity = document.querySelector('.pd-quantity-input-box-' + productid);
  var updateQuantity = null;
  var reload = false;

  if (action == 'add') {
    quantity.value = parseInt(quantity.value) + parseInt(_quantity);
    updateQuantity = _quantity
  }
  else if (action == 'remove') {
    if (_quantity == 'all') {
      reload = true;
    }
    else {
      if (!limit & quantity.value == '1') {
        updateCartCount();
        reload = true;
      }
      if (limit & quantity.value == '1') {
        return;
      }
      quantity.value = parseInt(quantity.value) - parseInt(_quantity);
    }
    updateQuantity = _quantity
  }
  else if (action == 'edit') {
    if (parseInt(quantity.value) > parseInt(quantity.oldvalue)) {
      const calcQuantity = (parseInt(quantity.value) - parseInt(quantity.oldvalue))
      var action = 'add';
      updateQuantity = calcQuantity
    }
    else if (parseInt(quantity.value) < parseInt(quantity.oldvalue)) {
      const calcQuantity = (parseInt(quantity.oldvalue) - parseInt(quantity.value))
      var action = 'remove';
      updateCartCount();
      reload = true;
      updateQuantity = calcQuantity
    }
  }

  if (!noUpdate) { doFetch(action, productid, updateQuantity, reload) }

  try {
    const pdPrice = parseFloat(document.querySelector('.pd-price-' + productid).innerHTML.trim());
    const totalPrice = parseFloat(quantity.value) * pdPrice;
    document.querySelector('.pd-total-price-' + productid).innerHTML = totalPrice.toFixed(2);

    var cartPrice = document.querySelector('.total-price');
    if (action == 'add') {
      cartPrice.innerHTML = (parseFloat(cartPrice.innerHTML.trim()) + updateQuantity * pdPrice).toFixed(2);
    }
    else if (action == 'remove') {
      const calced = (parseFloat(cartPrice.innerHTML.trim()) - updateQuantity * pdPrice).toFixed(2)
      if (calced <= 0 || calced == 'NaN') {
        cartPrice.innerHTML = 0;
      }
      else {
        cartPrice.innerHTML = calced;
      }
    }
  }
  catch (error) {
    if (error.name != "TypeError") {
      console.log(error);
    }
  }
}

function addToCart(productid, getQuantity = false) {
  var _quantity = 1;
  if (getQuantity) {
    _quantity = document.querySelector('.pd-quantity-input-box-' + productid).value;
  }
  fetch('/cart/add/' + productid + '/quantity/' + _quantity, {
    method: 'POST'
  });
  var quantity = document.querySelector('.cart-count');
  quantity.innerHTML = parseInt(quantity.innerHTML.trim()) + 1;
}

function checkOutProduct(product_id) {
  const quantity = document.querySelector('.pd-quantity-input-box-' + product_id).value;
  document.querySelector('.checkout-quantity').value = quantity;
  document.querySelector('.checkout-form').submit();
}

function selectOne(product_id) {
  const calledCheckbox = document.querySelector('.pd-checkbox-' + product_id);
  var productIds = document.querySelector('.checkout-pd-ids');

  if (calledCheckbox.checked) {
    if (!productIds.value.includes(product_id)) {
      productIds.value = productIds.value + product_id + ',';
    }
    document.querySelector('.checkout-btn').removeAttribute("disabled");

    // check if all product checkboxes is checked, check select all
    var allChecked = false;
    var pdCheckboxes = document.querySelectorAll('.product-checkbox');
    for (i = 0; i < pdCheckboxes.length; i++) {
      if (!pdCheckboxes[i].checked) {
        break;
      }
      if (i == pdCheckboxes.length - 1) {
        allChecked = true;
      }
    }
    if (allChecked) {
      document.querySelector('.select-all').checked = true;
      document.querySelector('.checkout-mode').value = 'all';
    }
    else {
      document.querySelector('.checkout-mode').value = 'selected';
    }
  }
  else {
    productIds.value = productIds.value.replace(product_id + ',', '');

    // check if there is no checked checkboxes, disable checkout button
    var anyChecked = false;
    var pdCheckboxes = document.querySelectorAll('.product-checkbox');
    for (i = 0; i < pdCheckboxes.length; i++) {
      if (pdCheckboxes[i].checked) {
        anyChecked = true;
        break;
      }
    }
    if (!anyChecked) {
      document.querySelector('.checkout-btn').setAttribute("disabled", "");
      document.querySelector('.checkout-mode').value = 'none';
    }
    else {
      document.querySelector('.checkout-mode').value = 'selected';
    }
    document.querySelector('.select-all').checked = false;
  }
}

function selectAll() {
  const selectAllCheckbox = document.querySelector('.select-all');
  var pdCheckboxes = document.querySelectorAll('.product-checkbox');
  var productIds = document.querySelector('.checkout-pd-ids');

  if (selectAllCheckbox.checked) {
    pdCheckboxes.forEach(function checkCheckbox(checkbox) {
      checkbox.checked = true;
    })
    document.querySelector('.checkout-btn').removeAttribute("disabled");
    document.querySelector('.checkout-mode').value = 'all';
  }
  else {
    productIds.value = "";
    pdCheckboxes.forEach(function uncheckCheckbox(checkbox) {
      checkbox.checked = false;
    })
    document.querySelector('.checkout-btn').setAttribute("disabled", "");
    document.querySelector('.checkout-mode').value = 'none';
  }
}

function checkOutCart() {
  const selectAllCheckbox = document.querySelector('.select-all');
  if (selectAllCheckbox.checked) {
    document.querySelector('.checkout-mode').value = 'all';
  }
  else {
    document.querySelector('.checkout-mode').value = 'selected';
  }
  document.querySelector('.checkout-form').submit();
}