from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Chat Flask</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .chat-container {
            width: 400px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
        }
        .chat-header {
            background: #4CAF50;
            color: white;
            padding: 15px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            text-align: center;
            font-weight: bold;
        }
        .chat-messages {
            flex: 1;
            padding: 10px;
            overflow-y: auto;
        }
        .message {
            margin-bottom: 10px;
        }
        .user {
            text-align: right;
            color: blue;
        }
        .bot {
            text-align: left;
            color: green;
        }
        .chat-input {
            display: flex;
            border-top: 1px solid #ddd;
        }
        .chat-input input {
            flex: 1;
            padding: 10px;
            border: none;
            border-bottom-left-radius: 10px;
            outline: none;
        }
        .chat-input button {
            padding: 10px;
            border: none;
            background: #4CAF50;
            color: white;
            cursor: pointer;
            border-bottom-right-radius: 10px;
        }
        .chat-input button:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">Chat Flask</div>
        <div class="chat-messages" id="chatMessages"></div>
        <div class="chat-input">
            <input type="text" id="messageInput" placeholder="Digite sua mensagem..." />
            <button onclick="sendMessage()">Enviar</button>
        </div>
    </div>

<script>
function sendMessage() {
    const input = document.getElementById("messageInput");
    const message = input.value.trim();
    if (message === "") return;

    const chatMessages = document.getElementById("chatMessages");

    // Mostrar mensagem do usuário
    const userDiv = document.createElement("div");
    userDiv.className = "message user";
    userDiv.innerText = message;
    chatMessages.appendChild(userDiv);

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        const botDiv = document.createElement("div");
        botDiv.className = "message bot";
        botDiv.innerText = data.response;
        chatMessages.appendChild(botDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });

    input.value = "";
}
</script>

</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    mensagem = data.get("message", "")
    resposta = f"você disse: {mensagem}"
    return jsonify({"response": resposta})

if __name__ == "__main__":
    app.run(debug=True)
