import { showToast, createBubbles } from './utiasls.js';

document.getElementById('change-password').addEventListener('click', function changePassword(params) {
    var form = document.getElementById('container-form');
    var passwordForm = document.getElementById('container-form-password');

    form.classList.add("hide");
    passwordForm.classList.remove("hide");
});

document.getElementById('email').readOnly = true

document.getElementById('change-main').addEventListener('click', function changePassword(params) {
    var form = document.getElementById('container-form');
    var passwordForm = document.getElementById('container-form-password')

    form.classList.remove("hide");
    passwordForm.classList.add("hide");
});

document.getElementById('form-settings').addEventListener('submit', function (event) {
    event.preventDefault();
    changeSettings("form-settings");
});

document.getElementById('form-settings-password').addEventListener('submit', function (event) {
    event.preventDefault();
    changeSettings("form-settings-password");
});

function changeSettings(formId) {
    var loginForm = document.getElementById(formId);
    var formData = new FormData(loginForm);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/settings", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var userData = JSON.parse(xhr.response)
                showToast(userData.message, "success")
            } else {
                //TODO: mostrar un dialog wapo
                var errorData = JSON.parse(xhr.response);
                showToast(errorData.message, "error");
            }
        }
    };
    xhr.send(setFormKeyInData(formData, formId));
    return false
}



function setFormKeyInData(formData, formId) {
    var updatedFormData = new FormData();

    formData.forEach(function (value, key) {
        if (key === "form_key") {
            if (formId == "form-settings") {
                updatedFormData.append(key, "form-settings");
            } else {
                updatedFormData.append(key, "form-password");
            }
        } else {
            updatedFormData.append(key, value);
        }
    });

    return updatedFormData
}