const chatButton = document.getElementById("ai-chat-button");
const chatBox = document.getElementById("ai-chat-box");
const closeChat = document.getElementById("close-chat");
const sendButton = document.getElementById("send-message");
const chatInput = document.getElementById("chat-input");
const messagesContainer = document.getElementById("chat-messages");

chatButton.addEventListener("click", () => {
    chatBox.style.display = "flex";
});

closeChat.addEventListener("click", () => {
    chatBox.style.display = "none";
});

sendButton.addEventListener("click", async () => {

    const message = chatInput.value.trim();

    if (!message) {
        return;
    }

    messagesContainer.innerHTML += `
        <div class="user-message">
            ${message}
        </div>
    `;

    chatInput.value = "";

    const response = await fetch("/cars/ai-chat/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({
            message: message
        })
    });

    const data = await response.json();

    console.log(data)

    let carsHtml = "";

    data.cars.forEach(car => {

        carsHtml += `
        
            <div class="car-card">
                <img src="${car.image}" alt="car">

                <div class="car-info">
                    <h5>${car.name}</h5>

                    <p>${car.price} DH / jour</p>

                   <p>
                   Compatibilité IA :
                               ${car.score}
                   </p>
                    

                    <a href="/reservations/create/${car.id}/" class="btn btn-dark">
                        Réserver
                    </a>
                </div>
            </div>
        `;
    });

    messagesContainer.innerHTML += `
        <div class="ai-message">
            Voici les voitures trouvées 😊
            ${carsHtml}
        </div>
    `;

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
});

function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {

                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;
            }
        }
    }

    return cookieValue;
}