// Sets the source of a frame element to the URL of the selected file.
function preview() {
    frame.src = URL.createObjectURL(event.target.files[0]);
}

// Clears the value of a file input element and sets the source of an image element to a default image.
function clearImage() {
    document.getElementById('formFile').value = "";
    frame.src = "/images/profiles/default.jpg";
}