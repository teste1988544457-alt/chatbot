import os
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

app = Flask(__name__)

# Inicializa cliente OpenAI usando variável de ambiente
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Chat com GPT-4o-mini</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .chat-container {
            width: 420px;
            background: #ffffff;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
        }
        .chat-header {
            background: #10a37f;
            color: white;
            padding: 15px;
            border-radius: 10px 10px 0 0;
            text-align: center;
            font-weight: bold;
        }
        .chat-messages {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }
        .message {
            margin-bottom: 10px;
            padding: 8px 12px;
            border-radius: 8px;
            max-width: 80%;
            word-wrap: break-word;
        }
        .user {
            background-color: #d1e7ff;
            align-self: flex-end;
            text-align: right;
        }
        .bot {
            background-color: #e2ffe2;
            align-self: flex-start;
            text-align: left;
        }
        .chat-input {
            display: flex;
            border-top: 1px solid #ddd;
        }
        .chat-input input {
            flex: 1;
            padding: 12px;
            border: none;
            outline: none;
            font-size: 14px;
            border-radius: 0 0 0 10px;
        }
        .chat-input button {
            padding: 12px 18px;
            border: none;
            background: #10a37f;
            color: white;
            cursor: pointer;
            font-weight: bold;
            border-radius: 0 0 10px 0;
        }
        .chat-input button:hover {
            background: #0e8c6a;
        }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">Chat com GPT-4o-mini</div>
    <div class="chat-messages" id="chatMessages"></div>
    <div class="chat-input">
        <input type="text" id="messageInput" placeholder="Digite sua mensagem..." onkeypress="if(event.key==='Enter'){sendMessage();}">
        <button onclick="sendMessage()">Enviar</button>
    </div>
</div>

<script>
function sendMessage() {
    const input = document.getElementById("messageInput");
    const message = input.value.trim();
    if (message === "") return;

    const chatMessages = document.getElementById("chatMessages");

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
    })
    .catch(error => {
        console.error("Erro:", error);
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

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente útil e direto."},
                {"role": "user", "content": mensagem}
            ],
            temperature=0.7,
        )

        resposta = response.choices[0].message.content

    except Exception as e:
        resposta = f"Erro ao consultar OpenAI: {str(e)}"

    return jsonify({"response": resposta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
