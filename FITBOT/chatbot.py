from flask import Flask, request, jsonify
import cohere
import json
import math
import re
import random

conversation_history = []

app = Flask(__name__)

co = cohere.Client('uxoUOT8yxWg4PEtEphJUJN75Kk0llh6ezLrHuUQl')

def load_intents():
    with open("intents.json", "r", encoding="utf-8") as file:
        return json.load(file)

intents = load_intents()  

def get_response_from_cohere(message):
    try:
        prompt = f"{message}"
        
        response = co.generate(
            model='command-r-08-2024',  
            prompt=prompt,  
            max_tokens=200,  
            temperature=0.7  
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"Error al generar respuesta con IA: {str(e)}"

def get_response(intent, intents):
    for i in intents["intents"]:
        if i["tag"] == intent:
            return random.choice(i["responses"])
    return "No entiendo tu pregunta, ¿puedes reformularla?"

def detect_intent(message, intents):
    for i in intents["intents"]:
        for pattern in i["patterns"]:
            if pattern.lower() in message.lower():
                return i["tag"]
    return None

def solve_advanced_math_expression(message):
    try:
        if any(op in message for op in ['+', '-', '*', '/', '^', 'raíz', 'seno', 'coseno', 'tangente']):
            if "raíz" in message:
                number = float(re.search(r"\d+", message).group())
                return str(math.sqrt(number))
            if "potencia" in message or "^" in message:
                numbers = re.findall(r"\d+", message)
                base, exponent = map(float, numbers[:2])
                return str(math.pow(base, exponent))
            if "seno" in message:
                angle = float(re.search(r"\d+", message).group())
                return str(math.sin(math.radians(angle)))
            if "coseno" in message:
                angle = float(re.search(r"\d+", message).group())
                return str(math.cos(math.radians(angle)))
            if "tangente" in message:
                angle = float(re.search(r"\d+", message).group())
                return str(math.tan(math.radians(angle)))
            return str(eval(message))
        return None
    except Exception:
        return "Hubo un error al intentar resolver la operación."

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/get_response", methods=["POST"])
def handle_message():
    data = request.json
    user_message = data.get("message", "")
    print(f"Mensaje recibido: {user_message}")

    if not user_message:
        return jsonify({"response": "Por favor, envía un mensaje válido."})

    math_response = solve_advanced_math_expression(user_message)
    if math_response:
        print(f"Respuesta matemática generada: {math_response}")
        return jsonify({"response": math_response})

    intent = detect_intent(user_message, intents)
    if intent:
        response = get_response(intent, intents)
        print(f"Intención detectada: {intent}, Respuesta: {response}")
        return jsonify({"response": response})

    response = get_response_from_cohere(user_message)
    print(f"Respuesta generada con Cohere: {response}")
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
