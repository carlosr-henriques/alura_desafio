from flask import Flask, request, render_template
from sql_manipulation import select, create_database, insert
import kpis
import google.generativeai as genai
import os
import json

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

app = Flask(__name__)


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
        positive_percentage=percentagem_positivos,
        negative_percentage=percentagem_negativos,
        inconclusive_percentage=percentagem_inconclusivos,
        feature_counts=feature_counts
    )            
            
@app.route('/feedbacks', methods=['POST'])
def receive_feedback():
    
    feedbacks = request.json

    check_instruction = (
        "Você é um analisador dos feedbacks enviados pelos usuários do app AluMind. Sua tarefa é verificar se o valor da chave 'feedback' na estrutura JSON apresentada pode ser classificado de acordo com o seu sentimento (positivo, negativo ou neutro) e identificar as funcionalidades sugeridas no feedback, se houver. Se não for possível classificar o feedback ou identificar funcionalidades sugeridas, gere a resposta: 'Ilegítimo'. Caso contrário, gere a resposta: 'Legítimo'."
    )

    version = 'models/gemini-1.5-flash'
    model = genai.GenerativeModel(version, 
                                  system_instruction=check_instruction)

    prompt = f"""Analise se o feedback abaixo é legítico ou ilegítimo.

    {feedbacks}"""

    response = model.generate_content(prompt)
    response = response.text

    if response.lower() == "legítimo":

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
    else:
        return "O feedback não foi armazenado e processado. A I.A marcou o feedback como ilegítimo"

if __name__ == "__main__":
    app.run(debug=True)