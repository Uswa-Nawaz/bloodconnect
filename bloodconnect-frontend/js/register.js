const roleRadios = document.querySelectorAll('input[name="role"]');
const donorFields = document.getElementById("donor-fields");

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