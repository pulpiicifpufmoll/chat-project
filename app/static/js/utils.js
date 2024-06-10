function showToast(message, type) {
    var toast = document.createElement("div");
    toast.classList.add("toast", type);

    var icon = document.createElement("i");
    icon.classList.add("toast-icon");

    if (type === "success") {
        icon.classList.add("bx", "bx-check-circle");
    } else if (type === "error") {
        icon.classList.add("bx", "bx-error-circle");
    }

    var toastMessage = document.createElement("div");
    toastMessage.textContent = message;

    toast.appendChild(icon);
    toast.appendChild(toastMessage);

    var toastContainer = document.getElementById("toast-container");

    // Eliminar Toast existente antes de agreagar otro
    while (toastContainer != undefined && toastContainer.firstChild) {
        toastContainer.removeChild(toastContainer.firstChild);
    }

    toastContainer.appendChild(toast);

    setTimeout(function () {
        toast.classList.remove("slideIn");
        toast.classList.add("slideOut");
        setTimeout(function () {
            toast.remove();
        }, 6000);
    }, 6000);
}


export default showToast;
