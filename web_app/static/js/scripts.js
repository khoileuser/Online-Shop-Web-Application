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
    if (window.scrollY > 75) {
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
    if (quantity <= 0) {
        return;
    }
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
    var stock = document.querySelector('.pd-stock-' + productid);
    var updateQuantity = null;
    var reload = false;

    if (action == 'add') {
        if (parseInt(quantity.value) < parseInt(stock.innerHTML.trim())) {
            quantity.value = parseInt(quantity.value) + parseInt(_quantity);
            updateQuantity = _quantity;
        }
        else {
            customAlert("You cannot add more than the available stock.", "alert-warning")
            return;
        }
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
        updateQuantity = _quantity;
    }
    else if (action == 'edit') {
        if (parseInt(quantity.value) > parseInt(quantity.oldvalue)) {
            const calcQuantity = (parseInt(quantity.value) - parseInt(quantity.oldvalue));
            var action = 'add';
            updateQuantity = calcQuantity;
            if (parseInt(quantity.value) >= parseInt(stock.innerHTML.trim())) {
                quantity.value = stock.innerHTML.trim();
                customAlert("You cannot add more than the available stock.", "alert-warning")
                updateQuantity = parseInt(stock.innerHTML.trim()) - parseInt(quantity.oldvalue);
            }
        }
        else if (parseInt(quantity.value) < parseInt(quantity.oldvalue)) {
            const calcQuantity = (parseInt(quantity.oldvalue) - parseInt(quantity.value));
            var action = 'remove';
            updateCartCount();
            reload = true;
            updateQuantity = calcQuantity;
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
            const calced = (parseFloat(cartPrice.innerHTML.trim()) - updateQuantity * pdPrice).toFixed(2);
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
    try {
        var fetchPromise = fetch('/cart/add/' + productid + '/quantity/' + _quantity, {
            method: 'POST'
        });

        var animationPromise = new Promise(function (resolve) {
            var button = document.querySelector('.add-cart-btn');
            button.classList.add("clicked");
            setTimeout(function () {
                button.classList.remove('clicked');
            }, 2500);
            resolve();
        });

        Promise.all([fetchPromise, animationPromise]).then(function (values) {
            var response = values[0];
            if (response.ok) {
                response.json().then(function (data) {
                    if (data.cart_plus) {
                        var quantity = document.querySelector('.cart-count');
                        quantity.innerHTML = parseInt(quantity.innerHTML.trim()) + 1;
                    }
                });
            }
        });
    }
    catch {
        window.location.href = '/signin';
    }
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
    var pdPrice = parseFloat(document.querySelector('.pd-price-' + product_id).innerHTML.trim());
    var pdQuantity = parseInt(document.querySelector('.pd-quantity-input-box-' + product_id).value);
    var cartTotalPrice = document.querySelector('.total-price');

    if (calledCheckbox.checked) {
        if (!productIds.value.includes(product_id)) {
            productIds.value = productIds.value + product_id + ',';
        }
        document.querySelector('.checkout-btn').removeAttribute("disabled");

        // update total price
        cartTotalPrice.innerHTML = (parseFloat(cartTotalPrice.innerHTML.trim()) + pdPrice * pdQuantity).toFixed(2);

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

        // update total price
        cartTotalPrice.innerHTML = (parseFloat(cartTotalPrice.innerHTML.trim()) - pdPrice * pdQuantity).toFixed(2);

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
    var cartTotalPrice = document.querySelector('.total-price');

    if (selectAllCheckbox.checked) {
        var checkoutMode = 'all';
        var newProductIds = "";
        pdCheckboxes.forEach(function checkCheckbox(checkbox) {
            if (checkbox.value == 'out-of-stock') {
                checkoutMode = 'selected';
            }
            else {
                var pdRow = checkbox.parentElement.parentElement;
                var pdPrice = parseFloat(pdRow.querySelector('.pd-price-span').innerHTML.trim());
                var pdQuantity = parseInt(pdRow.querySelector('.input-number').value);
                cartTotalPrice.innerHTML = (parseFloat(cartTotalPrice.innerHTML.trim()) + pdPrice * pdQuantity).toFixed(2);
                checkbox.checked = true;
                newProductIds = newProductIds + checkbox.value + ',';
            }
        })
        if (checkoutMode == 'selected') {
            productIds.value = newProductIds;
        }
        if (pdCheckboxes.length != 0) {
            document.querySelector('.checkout-btn').removeAttribute("disabled");
            document.querySelector('.checkout-mode').value = checkoutMode;
        }
    }
    else {
        productIds.value = "";
        pdCheckboxes.forEach(function uncheckCheckbox(checkbox) {
            checkbox.checked = false;
        })
        cartTotalPrice.innerHTML = "0.00";
        document.querySelector('.checkout-btn').setAttribute("disabled", "");
        document.querySelector('.checkout-mode').value = 'none';
    }
}

function checkOutCart() {
    const selectAllCheckbox = document.querySelector('.select-all');
    if (selectAllCheckbox.checked) {
        try {
            document.querySelector('.out-of-stock-warning');
            document.querySelector('.checkout-mode').value = 'selected';
        }
        catch {
            document.querySelector('.checkout-mode').value = 'all';
        }
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
 * The function removes diacritics (accent marks) from a given string.
 * @param str - The parameter "str" is a string that represents the input text.
 * @returns a string with diacritics (accent marks) removed.
 */
function removeDiacritics(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

/**
 * The function `doFilter` takes an array `a` and a filter string, and filters the array based on fuzzy
 * matching with the filter string.
 * @param a - The parameter "a" is an array of elements that you want to filter. These elements can be
 * HTML elements or any other objects that have a "textContent" or "innerText" property.
 * @param filter - The `filter` parameter is a string that represents the filter criteria. It is used
 * to match against the elements in the `a` array.
 * @returns The function `doFilter` does not have a return statement, so it does not explicitly return
 * anything.
 */
function doFilter(a, filter) {
    var prepared = a.map(function (el) {
        return { target: fuzzysort.prepare(removeDiacritics(el.textContent || el.innerText)), el: el };
    });
    var result = fuzzysort.go(filter, prepared, {
        key: 'target'
    });

    a.forEach(function (el) {
        el.style.display = "none";
    });
    result.forEach(function (res) {
        res.obj.el.style.display = "";
    });
}

/**
 * The function filters a list of countries based on user input.
 */
function filterCountry() {
    var input = document.querySelector(".country");
    var div = document.querySelector(".country-dropdown");
    var a = Array.from(div.getElementsByTagName("a"));
    doFilter(a, input.value);
}

/**
 * The function filters a dropdown list of phone number codes based on user input.
 */
function filterNumberCode() {
    var input = document.querySelector(".phone_number_code");
    var div = document.querySelector(".number-code-dropdown");
    var a = Array.from(div.getElementsByTagName("a"));
    doFilter(a, input.value);
}

/**
 * The function filters a dropdown list of states based on user input.
 */
function filterState() {
    var input = document.querySelector(".state");
    var div = document.querySelector(".state-dropdown");
    var a = Array.from(div.getElementsByTagName("a"));
    doFilter(a, input.value);
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
 * The function `addAddress` checks if all the required address fields are filled out and submits the
 * form if they are.
 */
function addAddress() {
    var country = document.querySelector(".country_input");
    var code = document.querySelector(".phone_number_code_input");
    var state = document.querySelector(".state_input");
    var phoneNumber = document.querySelector(".phone-number-input");
    var address = document.querySelector(".address-input");
    var city = document.querySelector(".city-input");
    var postalCode = document.querySelector(".postal-code-input");

    if (country.value == "Country") {
        customAlert("Please select country.", "alert-warning");
    }
    else if (code.value == "Code") {
        customAlert("Please select phone number code.", "alert-warning");
    }
    else if (phoneNumber.value.trim() == "") {
        customAlert("Please enter your phone number.", "alert-warning");
    }
    else if (address.value.trim() == "") {
        customAlert("Please enter your address.", "alert-warning");
    }
    else if (city.value.trim() == "") {
        customAlert("Please enter your city.", "alert-warning");
    }
    else if (state.value == "State") {
        customAlert("Please select state.", "alert-warning");
    }
    else if (postalCode.value.trim() == "") {
        customAlert("Please enter your postal code.", "alert-warning");
    }
    else {
        document.querySelector(".add-address-form").submit();
    }
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
        input.value = '0' + input.value;
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

/**
 * The function `preventFirstSpace` removes the first space character from the value of an input field
 * if it exists.
 * @param input - The input parameter is a reference to an HTML input element.
 */
function preventFirstSpace(input) {
    if (input.value.charAt(0) == ' ') {
        input.value = input.value.slice(0, -1);
    }
}

/**
 * The function filters a category based on the input checkbox value and updates the URL accordingly.
 * @param input - The input parameter is the checkbox element that triggered the function.
 */
function filterCategory(input) {
    if (input.checked) {
        var checkboxes = document.querySelectorAll('.category-checkbox');
        checkboxes.forEach(function uncheckCheckbox(checkbox) {
            if (checkbox.value != input.value) {
                checkbox.checked = false;
            }
        })
        if (window.location.href.includes('search=')) {
            var paramString = window.location.href.split('?')[1];
            var queryString = new URLSearchParams(paramString);
            var search = queryString.get('search');
            window.location.href = '?filter=' + input.value + '&search=' + search;
        }
        else {
            window.location.href = '?filter=' + input.value;
        }
    }
    else {
        window.location.href = '?page=1';
    }
}

/**
 * The function filters product cards on a webpage based on their price range.
 * @param min - The minimum price value to filter the products by.
 * @param max - The maximum price value that you want to filter the products by.
 * @returns nothing (undefined).
 */
function filterProductPrice(min, max) {
    if (window.location.href.includes('filter=') || window.location.href.includes('search=')) {
        if (min == 0 && max == 0) {
            var products = document.querySelectorAll('.pd-card');
            products.forEach(function filterProduct(product) {
                product.style.display = "block";
            })
        }
        else {
            var products = document.querySelectorAll('.pd-card');
            products.forEach(function filterProduct(product) {
                var price = parseFloat(product.querySelector('.card-price').innerHTML.trim().replace('$', ''));
                if (price < min || price > max) {
                    product.style.display = "none";
                }
                else {
                    product.style.display = "block";
                }
            })
        }
    }
}

/**
 * The function `editMinPrice` updates the minimum price value on a webpage and calls another function
 * to filter products based on the updated minimum price.
 * @param input - The input parameter is the HTML input element that represents the minimum price
 * value.
 */
function editMinPrice(input) {
    var min = parseInt(input.value);
    document.querySelector(".min-price-txt").innerHTML = "$" + min;
    filterProductPrice(min, parseInt(document.querySelector('.max-price').value))
}

/**
 * The function `editMaxPrice` updates the maximum price value and filters the product price based on
 * the new maximum value.
 * @param input - The input parameter is the HTML input element that represents the maximum price
 * value.
 */
function editMaxPrice(input) {
    var max = parseInt(input.value);
    document.querySelector(".max-price-txt").innerHTML = "$" + max;
    filterProductPrice(parseInt(document.querySelector('.min-price').value), max)
}

/**
 * The function `resetFilterPrice` resets the filter for product prices to the default values of 
 * minimum and  maximum.
 */
function resetFilterPrice() {
    document.querySelector('.min-price').value = "0";
    document.querySelector(".min-price-txt").innerHTML = "$0";

    var maxPriceFilter = document.querySelector('.max-price').max;
    document.querySelector('.max-price').value = maxPriceFilter;
    document.querySelector(".max-price-txt").innerHTML = "$" + maxPriceFilter;
    filterProductPrice(0, 0);
}

/**
 * The function `submitFilterPrice` takes the values of the minimum and maximum price inputs, and
 * updates the URL with the filter parameters.
 */
function submitFilterPrice() {
    var min = parseInt(document.querySelector('.min-price').value);
    var max = parseInt(document.querySelector('.max-price').value);
    if (window.location.href.includes('search=')) {
        var paramString = window.location.href.split('?')[1];
        var queryString = new URLSearchParams(paramString);
        var search = queryString.get('search');
        window.location.href = '?filter=price&min=' + min + '&max=' + max + '&search=' + search;
    }
    else {
        window.location.href = '?filter=price&min=' + min + '&max=' + max;
    }
}

/**
 * The function "handleKeyPress" checks if the key pressed is the Enter key and calls the
 * "submitSearch" function if it is.
 * @param event - The event parameter is an object that represents the event that occurred, in this
 * case, a key press event. It contains information about the event, such as the key that was pressed.
 */
function handleKeyPress(event, input) {
    if (event.key === 'Enter') {
        if (input == 'search') {
            submitSearch();
        }
        else if (input == 'auth') {
            signIn();
        }
    }
}

/**
 * The function `submitSearch` redirects the user to a search page with the search query as a parameter
 * in the URL.
 */
function submitSearch() {
    var search = document.querySelector('.search-input');
    if (search.value.trim() == "") {
        customAlert("Please enter a search query.", "alert-warning");
        return;
    }
    else if (window.location.pathname.includes('/products')) {
        if (window.location.href.includes('filter=')) {
            var paramString = window.location.href.split('?')[1];
            var queryString = new URLSearchParams(paramString);
            var filter = queryString.get('filter');
            if (filter == 'price') {
                var min = queryString.get('min');
                var max = queryString.get('max');
                window.location.href = '?filter=' + filter + '&min=' + min + '&max=' + max + '&search=' + search.value;
            }
            else {
                window.location.href = '?filter=' + filter + '&search=' + search.value;
            }
        }
        else {
            window.location.href = '?search=' + search.value;
        }
    }
    else {
        window.location.href = '/products?search=' + search.value;
    }
}

/**
 * The function enables the input field for category if the value is 'other'.
 * @param input - The input parameter is the HTML input element that triggered the event.
 */
function editCategory(input) {
    if (input.value == 'other') {
        document.querySelector('.pd-category').removeAttribute("disabled");
    }
}

/**
 * The function removes an image element from the DOM and updates the value of an input range element.
 * @param col - The `col` parameter represents the column element that needs to be removed from the
 * DOM.
 */
function removeImg(col) {
    col.remove();
    const imgRange = parseInt(document.querySelector('.img-range').value);
    document.querySelector('.img-range').value = imgRange - 1;

    var previewRow = document.querySelector('.preview-img');
    var previewCols = previewRow.querySelectorAll('.col-2');
    for (i = 0; i < previewCols.length; i++) {
        previewCols[i].querySelector('.img-input-hidden').name = 'preview-img-' + i;
    }
}

/**
 * The function `addImg` is used to add an image preview to a specified container element.
 * @param input - The `input` parameter is the file input element that the user interacts with to
 * select an image file.
 */
function addImg(input) {
    var previewRow = document.querySelector('.preview-img');

    var previewCol = document.createElement('div');
    previewCol.classList.add('col-2');
    previewCol.classList.add('d-flex');
    previewCol.classList.add('justify-content-center');
    previewCol.classList.add('align-items-center');
    previewCol.style.position = 'relative';

    var deleteButton = document.createElement('button');
    deleteButton.innerHTML = 'X';
    deleteButton.classList.add('btn');
    deleteButton.classList.add('btn-primary');
    deleteButton.classList.add('del-col-btn');
    deleteButton.setAttribute('onclick', 'removeImg(' + previewCol + ')');
    previewCol.appendChild(deleteButton);

    var previewImg = document.createElement('img');
    previewImg.src = URL.createObjectURL(input.files[0]);
    previewImg.setAttribute('alt', 'preview image')
    previewImg.classList.add('img-fluid');
    previewImg.classList.add('rounded');

    var previewInput = document.createElement('input');
    previewInput.classList.add('d-none');
    previewInput.classList.add('img-input-hidden');
    previewInput.type = 'file';
    previewInput.name = 'preview-img-' + previewRow.childElementCount;
    previewInput.files = input.files;

    document.querySelector('.img-range').value = previewRow.childElementCount + 1;
    previewCol.appendChild(previewImg);
    previewCol.appendChild(previewInput);
    previewRow.appendChild(previewCol);
}

/**
 * The function `editAvatar` updates the source of an HTML image element with the selected file from an
 * input element.
 * @param input - The input parameter is the file input element that allows the user to select an image
 * file from their device.
 */
function editAvatar(input) {
    var avatar = document.querySelector('.avatar-img');
    avatar.src = URL.createObjectURL(input.files[0]);
}

/**
 * The function `copyURL` copies the current URL to the clipboard and updates the sharing status on the
 * wishlist if it is set to false.
 */
function copyURL() {
    var sharing = document.querySelector('.sharing').value
    if (sharing == 'false') {
        fetch('/wishlist/share/true', {
            method: 'POST'
        })
            .then(() => {
                location.reload();
                navigator.clipboard.writeText(window.location.href);
                customAlert("URL copied to clipboard!", "alert-success");
            })
            .catch(err => console.error(err));
    }
    else {
        navigator.clipboard.writeText(window.location.href);
        customAlert("URL copied to clipboard!", "alert-success");
    }
}

/**
 * The function toggles the state of a review input and updates the icon accordingly.
 * @param input - The input parameter is expected to be an HTML element that contains a review toggle.
 */
function toggleReview(input) {
    var current = input.querySelector('.current');
    if (current.value == 'off') {
        current.value = 'on';
        input.querySelector('.icon').innerHTML = '<i class="bi bi-chevron-up"></i>';
    }
    else {
        current.value = 'off';
        input.querySelector('.icon').innerHTML = '<i class="bi bi-chevron-down"></i>';
    }
}

/**
 * The `placeOrderBtn` function is responsible for handling the click event on a button, triggering an
 * animation and sending a form data to a server.
 * @param button - The `button` parameter is the HTML button element that triggers the place order
 * action.
 */
function placeOrderBtn(button) {
    var box = button.querySelector('.box');
    var truck = button.querySelector('.truck');

    var form = button.parentElement;
    var formData = new FormData(form);

    var fetchPromise = fetch(form.action, {
        method: form.method,
        body: formData
    });

    var animationPromise = new Promise(function (resolve) {
        if (!button.classList.contains('done')) {
            if (!button.classList.contains('animation')) {
                button.classList.add('animation');

                gsap.to(button, {
                    '--box-s': 1,
                    '--box-o': 1,
                    duration: .3,
                    delay: .5
                });

                gsap.to(box, {
                    x: 0,
                    duration: .4,
                    delay: .7
                });

                gsap.to(button, {
                    '--hx': -5,
                    '--bx': 50,
                    duration: .18,
                    delay: .92
                });

                gsap.to(box, {
                    y: 0,
                    duration: .1,
                    delay: 1.15
                });

                gsap.set(button, {
                    '--truck-y': 0,
                    '--truck-y-n': -26
                });

                gsap.to(button, {
                    '--truck-y': 1,
                    '--truck-y-n': -25,
                    duration: .2,
                    delay: 1.25,
                    onComplete() {
                        gsap.timeline({
                            onComplete() {
                                button.classList.add('done');
                            }
                        }).to(truck, {
                            x: 0,
                            duration: .4
                        }).to(truck, {
                            x: 40,
                            duration: 1
                        }).to(truck, {
                            x: 20,
                            duration: .6
                        }).to(truck, {
                            x: 96,
                            duration: .4
                        });
                        gsap.to(button, {
                            '--progress': 1,
                            duration: 2.4,
                            ease: "power2.in"
                        });

                        resolve()
                    }
                });

            }

        } else {
            button.classList.remove('animation', 'done');
            gsap.set(truck, {
                x: 4
            });
            gsap.set(button, {
                '--progress': 0,
                '--hx': 0,
                '--bx': 0,
                '--box-s': .5,
                '--box-o': 0,
                '--truck-y': 0,
                '--truck-y-n': -26
            });
            gsap.set(box, {
                x: -24,
                y: -6
            });
        }
    });

    Promise.all([fetchPromise, animationPromise]).then(function (values) {
        var response = values[0];
        if (response.ok) {
            // If the response is done, redirect the user
            response.json().then(function (data) {
                window.location.href = data.redirectUrl;
            });
        }
    });
}

/**
 * The function `updateAccount` validates the username and password input fields and submits the form
 * if the inputs are valid.
 * @param user_id - The user_id parameter is the unique identifier for the user account that needs to
 * be updated.
 * @returns nothing (undefined) if the username or password does not meet the specified criteria.
 */
function updateAccount(user_id) {
    const username = document.getElementById('floatingUsername-' + user_id);
    if (username.value.length < 4 || username.value.length > 25 || ! /^[a-zA-Z0-9]+$/.test(username.value)) {
        customAlert("Username must be between 4 and 25 characters long and can only contain letters and numbers.", "alert-warning");
        return;
    }

    const password = document.getElementById('floatingPassword-' + user_id);
    if (! /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,255}$/.test(password.value)) {
        customAlert("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number and one special character.", "alert-warning");
        return;
    }

    var form = username.parentElement.parentElement.parentElement.parentElement;
    console.log(form)
    form.submit();
}


/* Executed when the window loads. It checks the current URL and performs different actions based on the URL. */
window.onload = function () {
    if (window.location.href.includes('filter=price')) {
        var paramString = window.location.href.split('?')[1];
        var queryString = new URLSearchParams(paramString);
        var min = queryString.get('min');
        var max = queryString.get('max');
        filterProductPrice(min, max);
    }
    else if (window.location.href.includes('search=')) {
        var paramString = window.location.href.split('?')[1];
        var queryString = new URLSearchParams(paramString);
        var search = queryString.get('search');
        document.querySelector('.search-input').value = search;
    }
    else if (window.location.href.includes('/checkout')) {
        var address = document.querySelector('.no-address-btn');
        var card = document.querySelector('.no-card-btn');
        if (address == null && card == null) {
            document.querySelector('.place-order-btn').removeAttribute("disabled");
        }
    }
    else if (window.location.href.includes('/product/')) {
        var sliderContainer = document.getElementById('slider-container');
        var sliderImages = document.getElementsByClassName('slider-image-img');

        if (sliderImages.length <= 4) {
            sliderContainer.style.overflowX = 'hidden';
        }

        else {
            var scrollAmount = 0;
            function autoSlide() {
                if (scrollAmount < sliderContainer.scrollWidth - sliderContainer.clientWidth) {
                    scrollAmount += sliderContainer.clientWidth / 4;
                } else {
                    scrollAmount = 0;
                }

                sliderContainer.scrollTo({
                    top: 0,
                    left: scrollAmount,
                    behavior: 'smooth'
                });
            }
            setInterval(autoSlide, 2500);
        }
    }
}