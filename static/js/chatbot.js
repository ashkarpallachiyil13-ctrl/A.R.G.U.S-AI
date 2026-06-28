const menuBtn = document.getElementById("menuBtn");
const dropdown = document.getElementById("dropdown");
const chatArea = document.getElementById("chatArea");
const msgInput = document.getElementById("msgInput");
const sendBtn = document.getElementById("sendBtn");

// ===========================
// Dropdown Menu
// ===========================

menuBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    dropdown.classList.toggle("open");
});

document.addEventListener("click", () => {
    dropdown.classList.remove("open");
});

chatArea.appendChild(row);

    chatArea.scrollTop = chatArea.scrollHeight;
}

// ===========================
// Send Message
// ===========================

async function handleSend() {

    const text = msgInput.value.trim();

    if (!text) return;

    addMessage(text, "user");

    msgInput.value = "";

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: text
            })

        });

        const data = await response.json();

        addMessage(data.reply, "bot");

    }

    catch (error) {

        addMessage(
            "Connection error.",
            "bot"
        );

        console.error(error);

    }

}

// ===========================
// Event Listeners
// ===========================

sendBtn.addEventListener("click", handleSend);

msgInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter") {
        handleSend();
    }

});