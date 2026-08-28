const roleRadios = document.querySelectorAll('input[name="role"]');
const donorFields = document.getElementById("donor-fields");
const form = document.getElementById("register-form");

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(form);

    const data = {
        role: formData.get("role"),
        name: formData.get("name"),
        email: formData.get("email"),
        phone: formData.get("phone"),
        password: formData.get("password"),
        blood_type: formData.get("blood_type") || null,
        date_of_birth: formData.get("date_of_birth") || null
    };

        fetch("http://127.0.0.1:8000/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json().then(body => ({ status: response.status, body })))
        .then(({ status, body }) => {
            const message = document.getElementById("register-message");
            if (status === 200) {
                message.textContent = "Registration successful! Your account is pending for approval.";
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


// a function that shows/hides based on what's currently selected
function updateFormFields() {
    const selectedRole = document.querySelector('input[name="role"]:checked').value;

    if (selectedRole === "Donor") {
        donorFields.style.display = "block";
    } else {
        donorFields.style.display = "none";
    }

    const nameInput = document.querySelector('input[name="name"]');
    if (selectedRole === "Hospital") {
        nameInput.placeholder = "Institution Name";
    } else {
        nameInput.placeholder = "Full Name";
    }
}

// actually run this function whenever someone clicks a different role
roleRadios.forEach(radio => {
    radio.addEventListener("change", updateFormFields);
});

updateFormFields();

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