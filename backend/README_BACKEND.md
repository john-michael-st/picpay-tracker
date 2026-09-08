# PicPay Tracker - Backend

Este é o backend do projeto PicPay Tracker, construído com FastAPI, SQLAlchemy, PostgreSQL e integração com a IA do Google Gemini.

## Pré-requisitos e Serviços Externos

Para rodar em produção (ex: no Render), você precisará de:
1. **Banco de Dados (PostgreSQL)**: Pode ser criado gratuitamente no [Neon.tech](https://neon.tech/).
2. **API Key do Google Gemini**: Obtida no [Google AI Studio](https://aistudio.google.com/).
3. **Token de Autenticação**: Qualquer string segura (ex: um UUID gerado aleatoriamente) para proteger suas rotas de escrita.

## Executando Localmente

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure o arquivo `.env`:
Copie o arquivo `.env.example` para `.env` e preencha com suas credenciais. Se deixar o `DATABASE_URL` padrão vazio ou não configurado, um erro pode ocorrer (ou você pode trocar para SQLite local para testar).

3. Rode o servidor:
```bash
uvicorn main:app --reload
```

## Deploy no Render.com

1. Crie uma conta no [Render.com](https://render.com/).
2. Conecte ao seu repositório GitHub que contém este código.
3. Crie um novo "Web Service".
4. O Render detectará automaticamente o arquivo `render.yaml` ou `Dockerfile`.
5. Adicione as seguintes variáveis de ambiente (`Environment Variables`) no painel do Render:
   - `DATABASE_URL`
   - `GEMINI_API_KEY`
   - `SECRET_TOKEN`
6. O deploy acontecerá automaticamente. O Render usa o `/health` como rota de verificação de saúde.
