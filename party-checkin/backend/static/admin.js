async function loadData(){

    const response = await fetch("/admin/summary");

    const data = await response.json();

    document.getElementById("total").innerText = data.total;
    document.getElementById("checked").innerText = data.checked_in;
    document.getElementById("pending").innerText = data.pending;
    document.getElementById("walkins").innerText = data.walkins;

    const table = document.getElementById("tableBody");

    table.innerHTML = "";

    data.attendees.forEach(person=>{

        table.innerHTML += `

        <tr>

            <td>${person.name}</td>

            <td>${person.signum}</td>

            <td class="${person.checked_in ? 'yes':'no'}">

                ${person.checked_in ? 'Checked In' : 'Pending'}

            </td>

            <td>${person.time}</td>

            <td>${person.source}</td>

        </tr>

        `;

    });

}

loadData();

/* Refresh every 5 seconds */

setInterval(loadData,5000);