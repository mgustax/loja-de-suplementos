import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

modelo = genai.GenerativeModel(
    "gemini-2.5-flash"
)


@csrf_exempt
def chatbot_view(request):

    if request.method == 'POST':

        try:

            data = json.loads(request.body)

            mensagem = data.get('mensagem')

            if not mensagem:

                return JsonResponse({
                    'erro': 'Digite uma pergunta para que eu possa te ajudar! 💪'
                })

            prompt = f"""
            voce é marombilda, assistente virtual de uma loja de suplementos.
            seja simpática, divertida e profissional.
            Responda sempre em português.
            Explique de forma simples.
            ajude com dúvidas sobre academia, whey, creatina e pré-treino.
            Não substitua orientação médica.
            pergunta do cliente:

            {mensagem}
            """

            resposta = modelo.generate_content(prompt)

            return JsonResponse({
                'resposta': resposta.text
            })

        except Exception as erro:

            return JsonResponse({
                'erro': str(erro)
            })

    return JsonResponse({
        'erro': 'Método não permitido'
    })