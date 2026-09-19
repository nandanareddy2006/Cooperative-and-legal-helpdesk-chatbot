const API_URL = "http://127.0.0.1:8000";
const CHAT_ENDPOINT = "/chat";

const input = document.getElementById("message");
const send = document.getElementById("send");

function sendQuestion(text) {

    if (!text) return;

    input.value = "";
    input.placeholder = "Thinking...";

    fetch(API_URL + CHAT_ENDPOINT, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: text,
            language: document.getElementById("language").value
        })

    })

    .then(response => {

        if (!response.ok) {
            throw new Error("HTTP " + response.status);
        }

        return response.json();

    })

    .then(data => {

        const answer =
            data.answer ||
            data.response ||
            data.message ||
            "Response received from Sahakaar-Saathi.";

        input.placeholder = answer;

    })

    .catch(error => {

        console.error(error);

        input.placeholder =
            "Backend connection failed. Check FastAPI /chat endpoint.";

    });
}


/* QUICK CARDS */

document.querySelectorAll("[data-question]").forEach(button => {

    button.addEventListener("click", () => {

        sendQuestion(button.dataset.question);

    });

});


/* SEND BUTTON */

send.addEventListener("click", () => {

    sendQuestion(input.value.trim());

});


/* ENTER TO SEND */

input.addEventListener("keydown", event => {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendQuestion(input.value.trim());

    }

});


/* PROCEDURE BUTTON */

document.getElementById("nextStep").addEventListener("click", () => {

    alert(
        "Step 2: Please keep relevant notices, receipts, membership records and other evidence ready."
    );

});