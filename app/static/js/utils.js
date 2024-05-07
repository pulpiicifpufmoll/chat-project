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
    while (toastContainer.firstChild) {
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

function createBubbles() {
    const numBubbles = 30;
    const bubbleContainer = document.querySelector(".bubble-container");

    for (let i = 0; i < numBubbles; i++) {
        const bubble = document.createElement("div");
        bubble.classList.add("bubble");
        bubble.style.left = `${Math.random() * 100}%`;
        bubble.style.animationDuration = `${Math.random() * 30 + 15}s`;

        const size = Math.random() * 10 + 5;
        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;

        bubbleContainer.appendChild(bubble);
    }
}

export default showToast;

export { showToast, createBubbles }