from dotenv import load_dotenv, find_dotenv
from sql_manipulation import select
import google.generativeai as genai
import smtplib
import email.message
import datetime
import smtplib
import kpis
import os

load_dotenv(dotenv_path=find_dotenv(),  # Or BASE_DIR/'.env',
            verbose=True,               # Print verbose output for debugging purposes
            override=True)

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def data_semana_anterior():

    """
        Essa função extrai a data inicial e final da última semana, para informar o período analisado no email enviado aos Stackholders. Também pode ser usado para filtrar os dados no banco de dados.
    """

    data_atual = datetime.datetime.now()
    semana_atual = data_atual.isocalendar()[1]

    semana_passada = semana_atual - 1

    data_inicio_semana = data_atual - datetime.timedelta(days=data_atual.weekday(), weeks=1)
    data_fim_semana = data_inicio_semana + datetime.timedelta(days=6)

    data_inicio_semana = data_inicio_semana.strftime('%Y-%m-%d')
    data_fim_semana = data_fim_semana.strftime('%Y-%m-%d')

    return data_inicio_semana, data_fim_semana

def gera_corpo_email():

    """
        Essa função gera o email enviado aos Stackholders.  
    """
    
    df = select()

    positivos = kpis.calculate_positive_feedbacks_kpi(df)
    negativos = kpis.calculate_negative_feedbacks_kpi(df)
    inconclusivos = kpis.calculate_inconclusive_kpi(df)
    recursos = df["code"].unique()

    data_inicio_semana, data_fim_semana = data_semana_anterior()

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    instruction = (
        "A AluMind é uma startup que oferece um aplicativo focado em bem-estar e saúde mental, proporcionando aos usuários acesso a meditações guiadas, sessões de terapia, e conteúdos educativos sobre saúde mental"
        "Você, como um assistente que cria e-mails, tem a tarefa de criar e-mails com um breve resumo dos principais feedbacks da semana, que serão enviados aos Stackholders da empresa. Estes feedbacks são disponibilizados pelos usuários da plataforma e são armazenados em nosso banco de dados. Os emails se referem a semana anterior, portanto, serão passadas duas datas. A menor se refere ao inicio da semana e a maior se refere ao último dia da semana."
        "Serão passadas 3 informações: porcentagem de feedbacks positivos, porcentagem de feedbacks negativos e Principais funcionalidades pedidas."
        "Para informar quais são as funcionalidades pedidas, dê destaque a cada funcionalidade usando a tag <strong>. Em sequência, explique o porquê cada uma das funcionalidades são importantes para a evolução do app."
        "Não é preciso criar um assunto para o email. Comece o email com uma saudação para os Stackholders. E termine com uma despedida da equipe AluMind."
        
    )

    version = 'models/gemini-1.5-flash'
    model = genai.GenerativeModel(version, 
                                system_instruction=instruction,
                                )


    prompt = f"""Crie o email. Porcentagem de feedbacks positivos: {positivos}; Porcentagem de feedbacks negativos: {negativos}; Porcentagem de feedbacks inconclusivos: {inconclusivos}; Principais funcionalidades: {recursos}; Inicio da semana: {data_inicio_semana}; Fim da semana: {data_fim_semana}"""
                
                
    response = model.generate_content(prompt)

    return response.text

def send_email(recipient_email, sender_email=EMAIL, sender_password=EMAIL_PASSWORD, subject="[AluMind] - Resumo de feedbacks"):
    
    body = gera_corpo_email()

    # Criação da mensagem
    msg = email.message.Message()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    print(msg['From'])

    # Corpo do e-mail
    msg.add_header('Contet-Type', 'text/html')
    msg.set_payload(body)

    # Configurações do servidor SMTP
    smtp_server = smtplib.SMTP('smtp.gmail.com: 587')
    smtp_server.starttls()

    smtp_server.login(msg["From"], sender_password)
    smtp_server.sendmail(msg["From"], [msg["To"]], msg.as_string().encode('utf-8'))

    print(f"E-mail enviado com sucesso para {recipient_email}")

send_email(recipient_email="carlosrobertoh2000@gmail.com")