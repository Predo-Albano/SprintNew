from flask import Blueprint, request, jsonify
from services.agendamento_service import AgendamentoService
import google.generativeai as genai
import os

# Configuração da API Gemini
GEMINI_API_KEY = "AIzaSyBg4dxUtFQc9YFaR1F-zedZ0YB0Ry-1AZs"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")  

chatbot_bp = Blueprint("chatbot", __name__)
agendamento_service = AgendamentoService()

@chatbot_bp.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_message = data.get("message", "").lower()

    if "horários disponíveis" in user_message or "quais horários" in user_message:
        try:
            horarios_ocupados = agendamento_service.obter_todos_agendamentos()
            if horarios_ocupados:
                resposta = f"Os horários já ocupados são: {', '.join([str(horario) for horario in horarios_ocupados])}. Escolha um horário disponível!"
            else:
                resposta = "Todos os horários estão livres no momento!"
        except Exception as e:
            print(f"Erro ao buscar horários: {e}")
            resposta = "Ocorreu um erro ao consultar os horários. Tente novamente mais tarde."

    elif "oi" in user_message or "olá" in user_message:
        resposta = "Olá! Como posso ajudar no seu agendamento?"

    elif "agendar" in user_message:
        resposta = "Para agendar, informe a data, horário e o serviço que deseja."

    # Se nenhuma das palavras-chave , usa o Gemini para gerar uma resposta
    else:
        try:
           
            generation_config = {
                "temperature": 0.7,
                "max_output_tokens": 256
            }
            gemini_response = model.generate_content(user_message, generation_config=generation_config)
            resposta = gemini_response.text  
        except Exception as e:
            print(f"Erro ao usar Gemini: {e}")
            resposta = "Desculpe, não entendi e não consegui gerar uma resposta usando o Gemini."

    return jsonify({"response": resposta})
