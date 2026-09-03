const savedUser = localStorage.getItem("loggedInUser");
const loggedInUser = JSON.parse(savedUser);

if (!loggedInUser || loggedInUser.role !== "Admin") {
    window.location.href = "login.html";
}

fetch("http://127.0.0.1:8000/admin/pending-users?admin_id=" + loggedInUser.id)
    .then(response => response.json())
    .then(pendingUsers => {
        console.log(pendingUsers);
        const listHTML = pendingUsers.map(user => {
            return `<div>
                <p>${user.name} (${user.role}) - ${user.email}</p>
            </div>`;
        });
        document.getElementById("pending-list").innerHTML = listHTML.join("");
    });