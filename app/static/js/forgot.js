import { showToast, createBubbles } from './utils.js';

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

createBubbles();


