/**
 * The function `customAlert` displays a message with a specified type (e.g., success, error) in an
 * alert container for a certain duration before hiding it.
 * @param message - The message parameter is a string that represents the content of the alert message
 * that will be displayed.
 * @param type - The "type" parameter is used to specify the type of alert message. It can be a string
 * value representing different types of alerts such as "success", "error", "warning", etc.
 */
function customAlert(message, type) {
  var alertContainer = document.querySelector('.alert-container');
  var alertMsg = document.querySelector('.alert-msg');
  alertContainer.classList.add(type)
  alertMsg.innerHTML = message;
  alertContainer.style.display = 'block';

  setTimeout(function () {
    alertContainer.style.display = 'none';
    alertContainer.classList.remove(type)
    alertMsg.innerHTML = "";
  }, 10000);
}

// Clears the value of a file input element and sets the source of an image element to a default image.
function clearImage() {
  document.getElementById('formFile').value = "";
  frame.src = "/images/profiles/default.jpg";
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
        customAlert("Login failed! Please check your credentials.", "alert-warning");
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
    if (document.querySelector('.username-danger').style.display == "none" & document.querySelector('.password-danger').style.display == "none" & document.querySelector('.confirm-password-danger').style.display == "none") {
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
    if (document.querySelector('.name-danger').style.display == "none" & document.querySelector('.password-danger').style.display == "none" & document.querySelector('.confirm-password-danger').style.display == "none") {
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
  const password = document.querySelector('.password');
  const confirmPassword = document.querySelector('.confirm-password');
  if (! /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,255}$/.test(password.value)) {
    document.querySelector('.password-danger').style.display = "block";
    document.querySelector('.signup-btn').setAttribute("disabled", "");
  }
  else if (password.value != confirmPassword.value) {
    document.querySelector('.password-danger').style.display = "none";
    document.querySelector('.confirm-password-danger').style.display = "block";
    document.querySelector('.signup-btn').setAttribute("disabled", "");
  }
  else {
    document.querySelector('.password-danger').style.display = "none";
    document.querySelector('.confirm-password-danger').style.display = "none";
    if (document.querySelector('.name-danger').style.display == "none" & document.querySelector('.username-danger').style.display == "none" & document.querySelector('.confirm-password-danger').style.display == "none") {
      if (accountTypeCheck() == true) {
        document.querySelector('.signup-btn').removeAttribute("disabled");
      }
    }
  }
}

/**
 * The function checks if the password and confirm password fields match, and enables the signup button
 * if all other validation checks pass.
 */
function signUpConfirmPassword() {
  const password = document.querySelector('.password');
  const confirmPassword = document.querySelector('.confirm-password');
  if (password.value != confirmPassword.value) {
    document.querySelector('.confirm-password-danger').style.display = "block";
    document.querySelector('.signup-btn').setAttribute("disabled", "");
  }
  else {
    document.querySelector('.confirm-password-danger').style.display = "none";
    if (document.querySelector('.name-danger').style.display == "none" & document.querySelector('.username-danger').style.display == "none" & document.querySelector('.password-danger').style.display == "none") {
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
    if (document.querySelector('.name-danger').style.display == "none" & document.querySelector('.username-danger').style.display == "none" & document.querySelector('.password-danger').style.display == "none" & document.querySelector('.confirm-password-danger').style.display == "none") {
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
        customAlert("Username is already used, please try another username.", "alert-warning");
        document.querySelector('.signup-btn').removeAttribute("disabled");
        document.querySelector('.spinner').style.display = "none";
      }
      else {
        // submit form if all is passed
        document.querySelector('.signup-form').submit();
      }
    });
}

/**
 * The function changes the source of a large image element to the source of the clicked image.
 * @param image - The `image` parameter is the reference to the image element that triggered the
 * function.
 */
function changeLargeImg(image) {
  largeImage = document.querySelector('.large-image');
  largeImage.src = image.src;
}

/**
 * The function `doFetch` sends a POST request to the server to perform an action on a product in the
 * cart, and optionally reloads the page after the request is completed.
 * @param action - The "action" parameter represents the action to be performed on the cart. It could
 * be "add" to add a product to the cart, "remove" to remove a product from the cart, or any other
 * action that is supported by the server-side code.
 * @param productid - The productid parameter is the unique identifier of the product that you want to
 * perform the action on.
 * @param quantity - The `quantity` parameter represents the quantity of the product being added or
 * removed from the cart.
 * @param [reload=false] - The `reload` parameter is a boolean value that determines whether the page
 * should be reloaded after the fetch request is completed. If `reload` is set to `true`, the
 * `location.reload()` method is called to reload the page. If `reload` is set to `false` or not
 * @returns The fetch request is being returned.
 */
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

/**
 * The function updates the cart count by decreasing it by 1 if it is greater than or equal to 0.
 */
function updateCartCount() {
  var cartQuantity = document.querySelector('.cart-count');
  if (parseInt(cartQuantity.innerHTML.trim()) - 1 >= 0) {
    cartQuantity.innerHTML = parseInt(cartQuantity.innerHTML.trim()) - 1;
  }
}

/**
 * The function `editQuantity` is used to update the quantity of a product in a shopping cart and
 * perform related calculations and updates.
 * @param productid - The productid parameter is the unique identifier of the product. It is used to
 * select the quantity input box and other elements related to the specific product.
 * @param action - The "action" parameter determines the action to be performed on the quantity of the
 * product. It can have three possible values: "add", "remove", or "edit".
 * @param _quantity - The _quantity parameter represents the quantity of the product that needs to be
 * added, removed, or edited. It is a numeric value.
 * @param [noUpdate=false] - The `noUpdate` parameter is a boolean value that determines whether or not
 * to perform an update action. If `noUpdate` is set to `true`, the function will not perform any
 * update action. If `noUpdate` is set to `false` (or not provided), the function will
 * @param [limit=false] - The `limit` parameter is a boolean value that determines whether there is a
 * limit on the quantity of the product. If `limit` is set to `true`, it means there is a limit and the
 * quantity cannot be reduced below 1. If `limit` is set to `false`, there
 * @returns The function does not have a return statement, so it does not explicitly return anything.
 */
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

/**
 * The function addToCart is used to add a product to the cart and update the cart count.
 * @param productid - The productid parameter is the unique identifier of the product that is being
 * added to the cart.
 * @param [getQuantity=false] - The `getQuantity` parameter is a boolean value that determines whether
 * to retrieve the quantity of the product from the DOM or use a default quantity of 1. If
 * `getQuantity` is `true`, the function will retrieve the quantity from the DOM using the product ID.
 * If `getQuantity`
 */
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

/**
 * The function `checkOutProduct` retrieves the quantity of a product selected by the user and submits
 * it to the checkout form.
 * @param product_id - The product_id parameter is the unique identifier of the product that the user
 * wants to check out.
 */
function checkOutProduct(product_id) {
  const quantity = document.querySelector('.pd-quantity-input-box-' + product_id).value;
  document.querySelector('.checkout-quantity').value = quantity;
  document.querySelector('.checkout-form').submit();
}

/**
 * The function `selectOne` is used to handle the selection and deselection of checkboxes for
 * individual products, updating the state of the checkout button and select all checkbox accordingly.
 * @param product_id - The `product_id` parameter is the unique identifier of a product. It is used to
 * select or deselect a checkbox associated with that product.
 */
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

/**
 * The above code defines two functions in JavaScript, one for selecting all checkboxes and another for
 * checking out the cart.
 */
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

/**
 * The function checks if the password entered meets certain criteria and enables the signup button if
 * all other required fields are also filled.
 */
function profileEditPassword() {
  const password = document.querySelector('.password');
  const confirmPassword = document.querySelector('.confirm-password');
  if (! /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,255}$/.test(password.value)) {
    document.querySelector('.password-danger').style.display = "block";
    document.querySelector('.password-save-btn').setAttribute("disabled", "");
  }
  else if (password.value != confirmPassword.value) {
    document.querySelector('.password-danger').style.display = "none";
    document.querySelector('.confirm-password-danger').style.display = "block";
    document.querySelector('.password-save-btn').setAttribute("disabled", "");
  }
  else {
    document.querySelector('.password-danger').style.display = "none";
    document.querySelector('.confirm-password-danger').style.display = "none";
    document.querySelector('.password-save-btn').removeAttribute("disabled");
  }
}

/**
 * The function checks if the password and confirm password fields match, and enables the signup button
 * if all other validation checks pass.
 */
function profileConfirmPassword() {
  const password = document.querySelector('.password');
  const confirmPassword = document.querySelector('.confirm-password');
  if (password.value != confirmPassword.value) {
    document.querySelector('.confirm-password-danger').style.display = "block";
    document.querySelector('.password-save-btn').setAttribute("disabled", "");
  }
  else {
    document.querySelector('.confirm-password-danger').style.display = "none";
    if (document.querySelector('.password-danger').style.display == "none") {
      document.querySelector('.password-save-btn').removeAttribute("disabled");
    }
  }
}

/**
 * The function `profileSavePassword` sends a POST request to update the user's password and displays a
 * success or error message based on the response.
 */
function profileSavePassword() {
  const oldPassword = document.querySelector('.old-password');
  const newPassword = document.querySelector('.new-password');
  fetch('/me/update/password', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
      'old-password': oldPassword.value,
      'new-password': newPassword.value
    })
  })
    .then(response => response.text())
    .then(data => {
      if (data == "wrong password") {
        customAlert("Old password is not correct.", "alert-warning");
      }
      else {
        customAlert("New password saved!", "alert-success");
      }
    });
}

/**
 * The function filters a list of countries based on user input.
 */
function filterCountry() {
  var input, filter, ul, li, a, i, txtValue;
  input = document.querySelector(".country");
  filter = input.value.toUpperCase();
  div = document.querySelector(".country-dropdown");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

/**
 * The function filters a dropdown list of phone number codes based on user input.
 */
function filterNumberCode() {
  var input, filter, ul, li, a, i, txtValue;
  input = document.querySelector(".phone_number_code");
  filter = input.value.toUpperCase();
  div = document.querySelector(".number-code-dropdown");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

/**
 * The function filters a dropdown list of states based on user input.
 */
function filterState() {
  var input, filter, ul, li, a, i, txtValue;
  input = document.querySelector(".state");
  filter = input.value.toUpperCase();
  div = document.querySelector(".state-dropdown");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

/**
 * The function "choseState" updates the value of a button and an input field with the provided state
 * value.
 * @param state - The `state` parameter is a string representing the chosen state.
 */
function choseState(state) {
  document.querySelector(".state-btn").innerHTML = state;
  document.querySelector(".state_input").value = state;
}

/**
 * The `editCardNumber` function formats and validates a credit card number input field, and updates
 * the card type and visibility of error messages accordingly.
 * @param input - The `input` parameter is a reference to an HTML input element.
 */
function editCardNumber(input) {
  input.value = input.value.replace(/\D+/g, '');
  var trimmed = input.value.replace(/\s+/g, '');
  var formatted = trimmed.replace(/(\d{4})/g, '$1 ').trim();
  input.value = formatted;

  var addCardBtn = document.querySelector('.add-card-btn');
  var cardType = document.querySelector(".card_type");
  var visaLogo = document.querySelector(".visa-logo");
  var mastercardLogo = document.querySelector(".mastercard-logo");
  var alert = document.querySelector(".wrong-card-alert");

  // visa
  if (formatted.charAt(0) == '4') {
    visaLogo.classList.add("border");
    visaLogo.classList.add("border-primary");

    mastercardLogo.classList.remove("border");
    mastercardLogo.classList.remove("border-primary");

    cardType.value = "VISA";
    addCardBtn.removeAttribute("disabled");
    alert.classList.add("d-none");
  }
  // mastercard 
  else if (formatted.charAt(0) == '5') {
    mastercardLogo.classList.add("border");
    mastercardLogo.classList.add("border-primary");

    visaLogo.classList.remove("border");
    visaLogo.classList.remove("border-primary");

    cardType.value = "MC";
    addCardBtn.removeAttribute("disabled");
    alert.classList.add("d-none");
  }
  else {
    mastercardLogo.classList.remove("border");
    mastercardLogo.classList.remove("border-primary");

    visaLogo.classList.remove("border");
    visaLogo.classList.remove("border-primary");

    cardType.value = "";
    addCardBtn.setAttribute("disabled", "");
    alert.classList.remove("d-none");
  }
}

/**
 * The function `editExpireDate` is used to format and validate an input field for an expiration date.
 * @param input - The input parameter is a reference to an HTML input element.
 */
function editExpireDate(input) {
  input.value = input.value.replace(/\D+/g, '');

  if (parseInt(input.value.charAt(0)) > 1) {
    input.value = '0' + input.value
  }
  else if (parseInt(input.value.charAt(0)) == 1) {
    if (parseInt(input.value.charAt(1)) > 2) {
      input.value = input.value.slice(0, -1);
    }
  }

  if (input.value.length >= 2) {
    input.value = input.value.slice(0, 2) + '/' + input.value.slice(2);
    if (parseInt(input.value.charAt(3)) < 2) {
      input.value = input.value.slice(0, -1);
    }
    else if (parseInt(input.value.charAt(4)) < 4) {
      input.value = input.value.slice(0, -1);
    }
  }
}