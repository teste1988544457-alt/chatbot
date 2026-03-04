import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Respostas simples do chatbot
def responder(mensagem):
    mensagem = mensagem.lower()

    if "rende" in mensagem:
        return "A Rende é uma plataforma feita para ajudar você com informações e suporte."
    elif "contato" in mensagem:
        return "Você pode entrar em contato pelo email suporte@rende.com."
    elif "como funciona" in mensagem:
        return "A Rende funciona oferecendo suporte online e ferramentas digitais."
    elif "preço" in mensagem or "valor" in mensagem:
        return "Você pode consultar os planos disponíveis na página oficial."
    else:
        return "Desculpe, ainda estou aprendendo. Pode reformular sua pergunta?"

# Página principal
@app.route("/")
def home():
    return """
    <h1>Chatbot Rende</h1>
    <p>Use POST /chat para conversar com o bot.</p>
    """

# Endpoint do chatbot
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "mensagem" not in data:
        return jsonify({"erro": "Envie JSON com campo 'mensagem'"}), 400

    resposta = responder(data["mensagem"])
    return jsonify({"resposta": resposta})

# Necessário para rodar localmente
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
