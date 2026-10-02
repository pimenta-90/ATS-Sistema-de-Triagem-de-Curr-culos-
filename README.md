Projeto: ATS (Sistema de Triagem de Currículos) com IA

Olá! Bem-vindo ao meu primeiro projeto de programação!
Este é um Sistema de Triagem de Currículos (ATS) simples, mas muito poderoso, que criei usando Python. A ideia principal surgiu da vontade de unir duas áreas que estudo: Recursos Humanos e Tecnologia.
O objetivo do script é facilitar a vida de quem faz recrutamento, lendo um currículo em PDF, pedindo para a inteligência artificial do Google (Gemini) analisá-lo com base nos requisitos da vaga, e enviando um relatório completinho direto para o e-mail do recrutador.

💡 O que o código faz exatamente?
Lê o PDF: Ele pega o arquivo do currículo (ex: Curriculo.pdf) e extrai todo o texto lá de dentro.
Pensa como um Recrutador Sênior: Envia esse texto para a IA do Google Gemini, junto com as exigências da vaga, e pede uma análise crítica e uma nota de 0 a 10.
Manda um E-mail: Assim que a IA termina de pensar, o script pega a resposta e envia automaticamente para o e-mail configurado.

🛠️ Ferramentas que usei (Tecnologias)
Python 3 (A base de tudo)
google-genai: Para conversar com a Inteligência Artificial do Google.
pypdf: Para conseguir ler os arquivos de currículo.
python-dotenv: Para esconder as minhas senhas e chaves de API (segurança em primeiro lugar!).
smtplib: A biblioteca nativa do Python que faz a mágica de enviar o e-mail.

⚙️ Como testar no seu computador
Se você quiser rodar o meu código aí na sua máquina, é bem simples:
1. Faça o clone do repositório

git clone https://github.com/pimenta-90/ATS-Sistema-de-Triagem-de-Curr-culos.git
cd ATS-Sistema-de-Triagem-de-Curr-culos

2. Instale as bibliotecas necessárias

pip install google-genai pypdf python-dotenv

3. Crie o seu arquivo de senhas (MUITO IMPORTANTE)
Crie um arquivo chamado .env na mesma pasta do projeto e coloque as suas informações:

GEMINI_API_KEY=cola_aqui_a_sua_chave_do_google_studio
EMAIL_PARA_RECEBER_ANALISE_IA=seu_email@gmail.com
SENHA_PROPRIA_EMAIL=sua_senha_de_aplicativo_do_gmail

4. Rode o projeto!
Coloque um currículo em PDF com o nome Curriculo.pdf na pasta, ajuste as exigências da vaga no final do código, e rode no seu terminal:

python nome_do_seu_arquivo.py

Feito por Vinícius Ribeiro Pimenta. Sinta-se à vontade para dar dicas e sugestões!
