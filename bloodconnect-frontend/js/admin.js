const savedUser = localStorage.getItem("loggedInUser");
const loggedInUser = JSON.parse(savedUser);

if (!loggedInUser || loggedInUser.role !== "Admin") {
    window.location.href = "login.html";
}

function loadPendingUsers() {
fetch("http://127.0.0.1:8000/admin/pending-users?admin_id=" + loggedInUser.id)
    .then(response => response.json())
    .then(pendingUsers => {
        console.log(pendingUsers);
        const listHTML = pendingUsers.map(user => {
            return `<div>
                <p>${user.name} (${user.role}) - ${user.email}</p>
                    <button onclick="approveUser(${user.id})">Approve</button>
                    <button onclick="rejectUser(${user.id})">Reject</button>
            </div>`;
        });
        document.getElementById("pending-list").innerHTML = listHTML.join("");
    });
}

loadPendingUsers();

function approveUser(userId) {
    fetch("http://127.0.0.1:8000/admin/approve/" + userId + "?admin_id=" + loggedInUser.id, {
        method: "POST"
    })
        .then(response => response.json())
        .then(updatedUser => {
            console.log(updatedUser);
            loadPendingUsers();
        });
}

function rejectUser(userId) {
    fetch("http://127.0.0.1:8000/admin/reject/" + userId + "?admin_id=" + loggedInUser.id, {
        method: "POST"
    })
        .then(response => response.json())
        .then(updatedUser => {
            console.log(updatedUser);
            loadPendingUsers();
        });
}

