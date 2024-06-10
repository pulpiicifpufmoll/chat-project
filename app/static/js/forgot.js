document.getElementById('forgot-pass-form').addEventListener('submit', function (event) {
    event.preventDefault();
    forgotPassword();
});
function forgotPassword() {
    var forgotPassForm = document.getElementById('forgot-pass-form');
    var formData = new FormData(forgotPassForm)
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/forgot-password", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var responseData = JSON.parse(xhr.responseText);
                showToast(responseData.message, "success");
            } else {
                var errorData = JSON.parse(xhr.responseText);
                showToast(errorData.message, "error");
            }
        }
    };
    xhr.send(formData);
    return false
}
document.getElementById('change-password-btn').addEventListener('click', function (event) {
    event.preventDefault();
    var token = document.getElementById('input-token').value
    changePassword(token)
})

function changePassword(token) {
    var forgotPassForm = document.getElementById('change-password-form');
    var formData = new FormData(forgotPassForm)
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/change-password/" + token, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var responseData = JSON.parse(xhr.responseText);
                showToast(responseData.message, "success");
                // Redirigir a otra página o realizar otras acciones según sea necesario
            } else {
                0
                var errorData = JSON.parse(xhr.responseText);
                showToast(errorData.message, "error");
            }
        }
    };
    xhr.send(formData);
    return false
}
