from flask import Flask, request, jsonify, make_response, render_template
from sql_manipulation import select, create_database, insert
import kpis
import google.generativeai as genai
import os
import json

os.environ["GEMINI_API_KEY"] = "AIzaSyDKgi7CmsqCBs2b2WwXKRPVkFj0aYnmt5s"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

feedback = {
    "id_feedback": "4042f20a-45f4-4647-8050-139ac16f610b",
   "sentiment": "POSITIVO",
   "code": "SEM SUGESTÃO",
   "reason": "O feedback não contém sugestões de funcionalidades.",
   "date_transaction": "2024-07-01T12:18:52.740000"
  }

app = Flask(__name__)

#@app.route("/feedbacks", methods=["GET"])
#def index():
#    return make_response(
#        jsonify(select())
#    )

@app.route('/')
def index():
    # Obter os dados do banco de dados
    df = select()

    percentagem_positivos = kpis.calculate_positive_feedbacks_kpi(df)
    percentagem_negativos = kpis.calculate_negative_feedbacks_kpi(df)
    percentagem_inconclusivos = kpis.calculate_inconclusive_kpi(df)
    feature_counts = kpis.calculate_features_kpi(df)

    return render_template(
        'index.html',
        positive_percentage=round(percentagem_positivos, 2),
        negative_percentage=round(percentagem_negativos, 2),
        inconclusive_percentage=round(percentagem_inconclusivos, 2),
        feature_counts=feature_counts
    )            
            
@app.route('/feedbacks', methods=['POST'])
def receive_feedback():
    
    feedbacks = request.json

    instruction = (
            "Sua tarefa é analisar os feedbacks vindos dos usuários, classificá-los a partir do seu sentimento e elencar as possíveis melhorias contidas neles." 
            "Cada feedback deve ser marcado como POSITIVO, NEGATIVO e INCONCLUSIVO." 
            "Cada feedback contém sugestões de funcionalidades feitas pelos usuários."
            "Cada funcionalidade sugerida deve ter um código que a identifica unicamente e uma descrição do porquê a funcionalidade é importante." 
            "O código da funcionalidade sugerida deve ser interpretável ao lê-lo." 
            "Crie opções que sejam facilmente entedidas como EDITAR PERFIL, DIFICULDADE DE CONTATO, MELHORA DE LAYOUT APP e outras opção. Para os feedbacks classificados com sentimento INCONCLUSIVO, categorize o código com INCONCLUSIVO e informe na descrição que não foi possível identificar a funcionalidade sugerida"
            "Se nenhuma sugestão de funcionalidade for descrita no feedback, classifique o código como SEM SUGESTÃO."
            "Exemplo de entrada: "
            "{'id': '4042f20a-45f4-4647-8050-139ac16f610b','feedback': 'Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só queria que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta'}."
            "Exemplo de saída: "
            "Requested_features = {code: str, reason: str} "
            "Feedback = {'id': str, sentiment: str, requested_features: list[Request_features]}"
            "Return: list[Recipe]"
        )

    version = 'models/gemini-1.5-flash'
    model = genai.GenerativeModel(version, 
                                system_instruction=instruction,
                                generation_config={"response_mime_type": "application/json"})

    prompt = f"""Analise o feedback abaixo, informe o sentimento e o recurso requisitado pelo usuário

    {feedbacks}"""

    response = model.generate_content(prompt)
    response = json.loads(response.text)

    create_database()

    insert(response)

    return response

if __name__ == "__main__":
    app.run(debug=True)