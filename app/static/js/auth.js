import { showToast, createBubbles } from './utils.js';


const btnSignIn = document.getElementById("sign-in"),
    btnSignUp = document.getElementById("sign-up"),
    formRegister = document.querySelector(".register"),
    formLogin = document.querySelector(".login");

btnSignIn.addEventListener("click", e => {
    resetRegisterFormValues()
    formRegister.classList.add("hide");
    formLogin.classList.remove("hide")
})

btnSignUp.addEventListener("click", e => {
    resetLoginFormValues()
    formLogin.classList.add("hide");
    formRegister.classList.remove("hide")
})

document.getElementById('register-form').addEventListener('submit', function (event) {
    console.log("holiiiiiiiiiiii")
    event.preventDefault();
    //register();
});

document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault();
    login();
});

function resetRegisterFormValues() {
    document.getElementById('fullname').value = ""
    document.getElementById('email-reg').value = ""
    document.getElementById('password-register').value = ""
    document.getElementById('password-confirm-register').value = ""
}

function resetLoginFormValues() {
    document.getElementById('email-log').value = ""
    document.getElementById('password-log').value = ""
}

function login() {
    var loginForm = document.getElementById('login-form');
    var formData = new FormData(loginForm);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/auth", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var userData = JSON.parse(xhr.response);
                if (userData.role != null && userData.role == "admin") {
                    window.location.replace("/admin");
                } else {
                    window.location.replace("/chat");
                }
            } else {
                var errorData = JSON.parse(xhr.responseText);
                showToast(errorData.message, "error");
            }
        }
    };
    xhr.send(setFormKeyInData(formData, true));
    return false;
}

function register() {
    console.log("lolazo")
    var registerForm = document.getElementById('register-form');
    var formData = new FormData(registerForm);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/auth", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var responseData = JSON.parse(xhr.responseText);
                showToast(responseData.message, "success");
                // Si se ha podido crear, se cierra la ventana y se abre la de login
                formRegister.classList.add("hide");
                formLogin.classList.remove("hide")
            } else {
                var errorData = JSON.parse(xhr.responseText);
                showToast(errorData.message, "error");
            }
        }
    };
    // xhr.send(setFormKeyInData(formData, false));
    return false;
}

function setFormKeyInData(formData, is_login) {
    var updatedFormData = new FormData();

    formData.forEach(function(value, key){
        if (key === "form_key"){
            if (is_login){
                updatedFormData.append(key, "form-login");
            } else {
                updatedFormData.append(key, "form-register");
            }
        } else {
            updatedFormData.append(key, value);
        }
    });
    return updatedFormData
}

createBubbles();


document.getElementById("social-btn").addEventListener("mouseover", function () {
    var socialIconsContainer = document.querySelector(".social-icons");
    socialIconsContainer.style.display = "block";
});

document.querySelector(".social-icons-container").addEventListener("mouseleave", function (event) {
    if (!event.relatedTarget || !event.relatedTarget.closest(".social-icons-container")) {
        var socialIconsContainer = document.querySelector(".social-icons");
        socialIconsContainer.style.display = "none";
    }
});

document.querySelector(".social-icons").addEventListener("mouseenter", function () {
    var socialIconsContainer = document.querySelector(".social-icons");
    socialIconsContainer.style.display = "block";
});
