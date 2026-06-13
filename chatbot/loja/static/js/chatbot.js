// pega os elementos html
const chatbotButton = document.getElementById("chatbot-button");
const chatbotWindow = document.getElementById("chatbot-window");

// abrir e fechar o chat
chatbotButton.addEventListener("click", () => {

    if (chatbotWindow.style.display === "flex") {
        chatbotWindow.style.display = "none";
    } else {
        chatbotWindow.style.display = "flex";
    }

});

// enviar mensagem

sendButton.addEventListener("click", async () => {

    const mensagem = userMessage.value;

    if (!mensagem) return;

    messages.innerHTML += `
        <div class="user-message">
            ${mensagem}
        </div>
    `;

    userMessage.value = "";

    try {

        const response = await fetch("/chatbot/", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                mensagem: mensagem
            })

        });

        const data = await response.json();

        messages.innerHTML += `
            <div class="bot-message">
                ${data.resposta}
            </div>
        `;

    }

    catch (error) {

        messages.innerHTML += `
            <div class="bot-message">
                Desculpe, tive um problema para responder 😥
            </div>
        `;

    }

});