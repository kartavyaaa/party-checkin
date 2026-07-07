// CHANGE THIS TO YOUR OWN PASSWORD
const ADMIN_PASSWORD = "bandar123";

function login() {

    const password = document.getElementById("password").value;

    if (password !== ADMIN_PASSWORD) {

        alert("Incorrect password.");

        return;

    }

    document.getElementById("loginScreen").style.display = "none";

    document.getElementById("dashboard").style.display = "block";

    loadData();

    setInterval(loadData, 5000);

}

async function uploadExcel() {

    const fileInput = document.getElementById("excelFile");

    if (fileInput.files.length === 0) {

        alert("Please choose an Excel file.");

        return;

    }

    const formData = new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    document.getElementById("uploadStatus").innerText =
        "Uploading...";

    const response = await fetch("/upload/excel", {

        method: "POST",

        body: formData

    });

    const data = await response.json();

    if (response.ok) {

        document.getElementById("uploadStatus").innerText =
            "✅ Upload Successful";

        loadData();

    } else {

        document.getElementById("uploadStatus").innerText =
            "❌ Upload Failed";

        alert(data.detail);

    }

}

async function loadData() {

    const response = await fetch("/admin/summary");

    const data = await response.json();

    document.getElementById("total").innerText = data.total;

    document.getElementById("checked").innerText = data.checked_in;

    document.getElementById("pending").innerText = data.pending;

    document.getElementById("walkins").innerText = data.walkins;

    const table = document.getElementById("tableBody");

    table.innerHTML = "";

    data.attendees.forEach(person => {

        table.innerHTML += `

        <tr>

            <td>${person.name}</td>

            <td>${person.signum}</td>

            <td class="${person.checked_in ? 'yes' : 'no'}">

                ${person.checked_in ? 'Checked In' : 'Pending'}

            </td>

            <td>${person.time}</td>

            <td>${person.source}</td>

        </tr>

        `;

    });

}