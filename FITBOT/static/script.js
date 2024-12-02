const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');

function addMessage(message, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
    const messageParagraph = document.createElement('p');
    messageParagraph.textContent = message;
    messageDiv.appendChild(messageParagraph);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Desplazar al final
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (message === '') return;

    addMessage(message, 'user'); // Mostrar mensaje del usuario

    try {
        const response = await fetch('/get_response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await response.json();
        addMessage(data.response, 'bot'); // Mostrar respuesta del bot
    } catch (error) {
        console.error('Error:', error);
        addMessage('Hubo un problema al conectar con el servidor.', 'bot');
    }

    userInput.value = ''; // Limpiar el campo de entrada
}
