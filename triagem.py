from dotenv import load_dotenv, find_dotenv
import os
import smtplib
from email.message import EmailMessage
from pypdf import PdfReader 
from google import genai

load_dotenv(find_dotenv())
# ====================================================================================
# Função que irá analisar o currículo enviado, irá enumerar as páginas
# e juntar todos os textos presentes em uma variável chamada "texto_completo_do_pdf"
# ====================================================================================
def extrair_curriculo_pdf(Curriculo):
    texto_completo_do_pdf = ""
    try:
        leitor_pdf = PdfReader(Curriculo)
        for i, pagina in enumerate(leitor_pdf.pages):
            texto_se_tiver_na_pagina = pagina.extract_text()
            if texto_se_tiver_na_pagina:
                texto_completo_do_pdf += texto_se_tiver_na_pagina
        return texto_completo_do_pdf
    except FileNotFoundError:
        print(f"Arquivo {Curriculo} não encontrado no sistema")
        return ""    
    except Exception as erro_leitura:
        print(f"ERRO: Não foi possível ler o arquivo\n MOTIVO: {erro_leitura}")
    return ""
# =============================================================================================================
#Função que irá enviar o texto completo coletado na primeira função, para a IA analisar e retornar a resposta
# =============================================================================================================
def analise_do_currilo_pela_ia(texto_completo_do_pdf, exigencias_vaga):
    print("A inteligência artificial irá analisar o currículo...")
    token_api = os.getenv("GEMINI_API_KEY")
    if not token_api:
        return "ERRO: A chave API não foi configurada"
    client = genai.Client(api_key=token_api)
    prompt = f"""
    Você é um Recrutador Sênior especialista em Recursos Humanos e Seleção de Talentos.
    Sua missão é fazer a triagem detalhada do currículo fornecido abaixo, avaliando-o com base nas exigências da vaga especificadas.

    EXIGÊNCIAS / COMPETÊNCIAS DA VAGA:
    {competencias_vaga}

    Por favor, estruture sua análise exatamente nos seguintes tópicos:
    1. **Resumo do Perfil:** Um parágrafo curto resumindo a experiência e a formação do candidato.
    2. **Principais Competências:** Liste as principais Hard Skills e Soft Skills identificadas no currículo.
    3. **Pontos Fortes:** O que mais se destaca positivamente no currículo.
    4. **Adequação para Vagas:** Avalie criticamente se o perfil se encaixa bem nas exigências da vaga informadas acima, cruzando os requisitos com a trajetória do candidato.
    5. **Nota de Adequação (0 a 10):** Atribua uma nota final fundamentada no alinhamento com os requisitos da vaga.

    Aqui está o texto do currículo para análise:
    {texto_completo_do_pdf}
    """
    try:
        resposta = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
        )
        resposta_ia = resposta.text
        return resposta_ia
    except Exception as erro_ia:
        if "503" in str(erro_ia):
            return "Os servidores do Google estão temporariamente sobrecarregados"
        else: 
            return f"Ocorreu um erro ao comunicar com a IA {erro_ia}"
def enviar_analise_via_email(email_destino, parecer_ia):
    print("Enviando o currículo para a IA")
    email_remetente = os.getenv("EMAIL_PARA_RECEBER_ANALISE_IA")
    if email_remetente:
        email_remetente = email_remetente.strip()
    if email_destino:
        email_destino = email_destino.strip()
    senha_app = os.getenv("SENHA_PROPRIA_EMAIL")
    if senha_app:
        senha_app = senha_app.strip()

    if not email_remetente or not senha_app:
        print("Não existem email's ou senhas do app configuradas nessa máquina (.env)")
        return

    mensagem = EmailMessage()
    mensagem["Subject"] = "Feedback Geral e Análise de Currículo pela IA"
    mensagem["From"] = email_remetente
    mensagem["To"] = email_destino
    mensagem.set_content(parecer_ia)

    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(email_remetente, senha_app)
        servidor.send_message(mensagem)
        servidor.quit()

        print(f"Email enviado com sucesso para {email_destino}")
    except Exception as erro_email:
        print(f"Erro ao enviar o email: {erro_email}")    


if __name__ == "__main__":
    arquivo_pdf = "Curriculo.pdf"
    meu_email_para_receber = os.getenv("EMAIL_PARA_RECEBER_ANALISE_IA")
    competencias_vaga = "MBA, formação em veterinária, boa comunicação, inglês intermediário, experiência na Adimax"
    print("Iniciando a triagem...")

    texto_extraido = extrair_curriculo_pdf(arquivo_pdf)
    if texto_extraido:
        parecer_ia = analise_do_currilo_pela_ia(texto_extraido, competencias_vaga)
        print("----RESUMO DA ANÁLISE----")
        print(parecer_ia)   

        enviar_analise_via_email(meu_email_para_receber, parecer_ia)
    else:
        print("Processo interrompido devido a falhas na leitura do currículo")