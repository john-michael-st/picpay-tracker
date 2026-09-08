import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def categorizar_gasto(texto: str) -> str:
    """
    Usa o modelo Gemini para categorizar um gasto baseado no texto da notificação.
    Categorias permitidas: Alimentação, Assinaturas, Transporte, Saúde, Lazer, Outros.
    """
    if not GEMINI_API_KEY:
        return "Outros"
        
    prompt = (
        f"Analise o seguinte texto de notificação de pagamento: '{texto}'. "
        "Classifique este gasto em exatamente UMA das seguintes categorias: "
        "Alimentação, Assinaturas, Transporte, Saúde, Lazer, Outros. "
        "Retorne APENAS o nome da categoria, sem aspas, pontuação ou texto adicional."
    )
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        categoria = response.text.strip()
        
        categorias_validas = ["Alimentação", "Assinaturas", "Transporte", "Saúde", "Lazer", "Outros"]
        if categoria in categorias_validas:
            return categoria
        else:
            return "Outros"
    except Exception as e:
        print(f"Erro ao categorizar gasto com Gemini: {e}")
        return "Outros"
