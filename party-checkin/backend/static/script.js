let currentSignum = "";

async function lookup() {

    const signum = document
        .getElementById("signum")
        .value
        .trim()
        .toLowerCase();

    const result = document.getElementById("result");

    result.innerHTML = "";

    if (!signum) {
        alert("Please enter your Signum.");
        return;
    }

    currentSignum = signum;

    const response = await fetch(`/checkin/${signum}`);

    if (response.status === 404) {

        result.innerHTML = `
            <h3>User not found</h3>

            <p>Please register below.</p>

            <br>

            <input
                id="walkin_name"
                placeholder="Name"
            >

            <select id="walkin_meal">
                <option value="">Select Meal Preference</option>
                <option value="Vegetarian">Vegetarian</option>
                <option value="Non-Vegetarian">Non-Vegetarian</option>
            </select>

            <select id="walkin_beverage">
                <option value="">Select Beverage Preference</option>
                <option value="Alcoholic">Alcoholic</option>
                <option value="Non-Alcoholic">Non-Alcoholic</option>
            </select>

            <button onclick="registerWalkin()">
                Register
            </button>
        `;

        return;
    }

    const data = await response.json();

    if (data.checked_in) {

        result.innerHTML = `
            <h2>✅ Already Checked In</h2>

            <p>${data.name}</p>

            <p>${data.checkin_time}</p>
        `;

        return;
    }

    result.innerHTML = `
        <h2>${data.name}</h2>

        <p><b>Meal:</b> ${data.meal}</p>

        <p><b>Beverage:</b> ${data.beverage}</p>

        <br>

        <button onclick="confirmCheckin()">
            Confirm Check-In
        </button>
    `;
}

async function confirmCheckin() {

    const response = await fetch(`/checkin/${currentSignum}`, {
        method: "POST"
    });

    const data = await response.json();

    document.getElementById("result").innerHTML = `
        <h2>✅ Attendance Recorded</h2>

        <p>${data.time}</p>

        <br>

        <h3>Enjoy the party 🎉</h3>
        
    `;
    setTimeout(() => {

        document.getElementById("signum").value = "";

        document.getElementById("result").innerHTML = "";

        document.getElementById("signum").focus();

    }, 2000);
}

async function registerWalkin() {

    const name = document.getElementById("walkin_name").value.trim();
    const meal = document.getElementById("walkin_meal").value;
    const beverage = document.getElementById("walkin_beverage").value;

    if (!name || !meal || !beverage) {
        alert("Please fill all the details.");
        return;
    }

    const payload = {

        name: name
            .toLowerCase()
            .replace(/\b\w/g, c => c.toUpperCase()),

        signum: currentSignum,

        meal: meal,

        beverage: beverage

    };

    const response = await fetch("/checkin/register", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(payload)

    });

    const data = await response.json();

    document.getElementById("result").innerHTML = `
        <h2>✅ Registered Successfully</h2>

        <p>${data.name}</p>

        <p>${data.time}</p>

        <br>

        <h3>Enjoy the party 🎉</h3>
    `;

    setTimeout(() => {

        document.getElementById("signum").value = "";

        document.getElementById("result").innerHTML = "";

        document.getElementById("signum").focus();

    }, 2000);
}