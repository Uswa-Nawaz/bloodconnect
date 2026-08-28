const form = document.getElementById("login-form");

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(form);

    const data = {
        email: formData.get("email"),
        password: formData.get("password")
    };

    fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json().then(body => ({ status: response.status, body })))
        .then(({ status, body }) => {
            const message = document.getElementById("login-message");
            if (status === 200) {
                message.textContent = "Login successful! Welcome, " + body.name + ".";
                message.style.color = "green";
            } else {
                message.textContent = body.detail;
                message.style.color = "red";
            }
        })
        .catch(error => {
            console.log("Error:", error);
        });
});

function togglePassword(fieldId, toggleElement) {
    const field = document.getElementById(fieldId);

    if (field.type === "password") {
        field.type = "text";
        toggleElement.textContent = "Hide";
    } else {
        field.type = "password";
        toggleElement.textContent = "Show";
    }
}