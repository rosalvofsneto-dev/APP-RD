import streamlit as st
import json
import os
from google import genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Meu App de Treino", 
    page_icon="🏋️", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- META TAGS E ESTILO PARA SAFARI / iOS (PWA MODE) ---
st.markdown(
    """
    <head>
      <!-- Habilita execução em tela cheia no iOS (sem barra de URL) -->
      <meta name="apple-mobile-web-app-capable" content="yes">
      <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
      <meta name="apple-mobile-web-app-title" content="Meu Treino">
      <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
      <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/twitter/twemoji/master/assets/192x192/1f3cb.png">
    </head>
    <style>
      /* Ajustes de espaçamento e toque para telas de celular */
      .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
      }
      button {
        width: 100% !important;
        border-radius: 10px !important;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# --- CONFIGURAÇÃO DA API DO GOOGLE AI STUDIO ---
# Tenta buscar via Secrets (deploy online) ou fallback para a variável de ambiente / chave local
API_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6KIDrgSTvRdjVNUVraodK-EJUGxAMe0K2MknXM0hFCSAw"))
client = genai.Client(api_key=API_KEY)

# --- BASES DE DADOS / FICHA DE TREINO E DIRETRIZES ---
DIRETRIZES_CARDIO = """
🏃 **AERÓBICO OBRIGATÓRIO (Pós-treino):** 
35 minutos de Caminhada Acelerada na Esteira (Inclinação de 3% a 6%).
"""

FICHA_TREINO = {
    "PUSH A": [
        {"exercicio": "Dumbbell Press Inclinado", "series": "3", "reps": "10 a 12", "descanso": "2,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Dumbbell+Press+Inclinado"},
        {"exercicio": "Dumbbell Press Reto", "series": "3", "reps": "10 a 12", "descanso": "2,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Dumbbell+Press+Reto"},
        {"exercicio": "Crossover na Polia", "series": "3", "reps": "12 a 15", "descanso": "1,5 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Crossover+na+Polia"},
        {"exercicio": "Desenvolvimento com Halteres", "series": "3", "reps": "10 a 12", "descanso": "2,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Desenvolvimento+com+Halteres"},
        {"exercicio": "Elevação Lateral com Halteres", "series": "4", "reps": "12 a 15", "descanso": "1,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Elevacao+Lateral+com+Halteres"},
        {"exercicio": "Tríceps Testa na Polia", "series": "3", "reps": "12 a 15", "descanso": "1,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Triceps+Testa+na+Polia"}
    ],
    "PULL A": [
        {"exercicio": "Pulley Frente Pronado e Aberto", "series": "3", "reps": "8 a 10", "descanso": "2,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Pulley+Frente+Pronado+e+Aberto"},
        {"exercicio": "Pulley Frente Supinado e Fechado", "series": "3", "reps": "10 a 12", "descanso": "2,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Pulley+Frente+Supinado"},
        {"exercicio": "Remada do Lalá (Unilateral)", "series": "3", "reps": "10 a 12", "descanso": "1,5 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Remada+do+Lala"},
        {"exercicio": "Crucifixo Inverso", "series": "3", "reps": "12 a 15", "descanso": "1,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Crucifixo+Inverso"},
        {"exercicio": "Rosca Direta com Barra", "series": "3", "reps": "8 a 10", "descanso": "1,5 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Rosca+Direta+com+Barra"},
        {"exercicio": "Rosca 45° com Halteres", "series": "3", "reps": "10 a 12", "descanso": "1,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Rosca+45+com+Halteres"}
    ],
    "LEGS": [
        {"exercicio": "Agachamento Livre", "series": "4", "reps": "8 a 10", "descanso": "2,5 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Agachamento+Livre"},
        {"exercicio": "Leg Press 45º", "series": "4", "reps": "10 a 12", "descanso": "2,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Leg+Press+45"},
        {"exercicio": "Cadeira Flexora", "series": "4", "reps": "12 a 15", "descanso": "1,5 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Cadeira+Flexora"},
        {"exercicio": "Panturrilha (Em pé / Leg)", "series": "4", "reps": "15 a 20", "descanso": "1,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Panturrilha"}
    ],
    "PUSH B (Semana 1)": [
        {"exercicio": "Pull Over com Halter", "series": "3", "reps": "10 a 12", "descanso": "1,5 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Pull+Over+com+Halter"},
        {"exercicio": "Crossover de Baixo para Cima", "series": "3", "reps": "12 a 15", "descanso": "1,5 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Crossover+de+Baixo+para+Cima"},
        {"exercicio": "Elevação Lateral na Polia", "series": "4", "reps": "12 a 15", "descanso": "1,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Elevacao+Lateral+na+Polia"},
        {"exercicio": "Tríceps Francês", "series": "3", "reps": "10 a 12", "descanso": "1,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Triceps+Frances"}
    ],
    "PULL B (Semana 2)": [
        {"exercicio": "Remada Curvada Aberta", "series": "3", "reps": "10 a 12", "descanso": "2,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Remada+Curvada+Aberta"},
        {"exercicio": "Remada do Lalá (Unilateral)", "series": "3", "reps": "10 a 12", "descanso": "1,5 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Remada+do+Lala"},
        {"exercicio": "Banco Romano (Lombar)", "series": "3", "reps": "12 a 15", "descanso": "1,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Banco+Romano+Lombar"},
        {"exercicio": "Rosca Martelo", "series": "3", "reps": "10 a 12", "descanso": "1,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Rosca+Martelo"}
    ],
    "SÁBADO QUINZENAL": [
        {"exercicio": "Banco Romano (Lombar)", "series": "3", "reps": "15", "descanso": "1,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Banco+Romano+Lombar"},
        {"exercicio": "Elevação Lateral", "series": "4", "reps": "15", "descanso": "1,0 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Elevacao+Lateral"},
        {"exercicio": "Cadeira Flexora ou Passada", "series": "3", "reps": "12", "descanso": "1,5 min", "video": "https://www.youtube.com/results?search_query=Laercio+Refundini+Cadeira+Flexora"}
    ]
}

# --- CABEÇALHO DO APP ---
st.title("🏋️ Meu Treino")
st.info(DIRETRIZES_CARDIO)

# --- MENU LATERAL DE NAVEGAÇÃO ---
st.sidebar.header("📅 Planejamento")
treino_selecionado = st.sidebar.selectbox("Selecione o Treino:", list(FICHA_TREINO.keys()))

st.subheader(f"🔴 Ficha: {treino_selecionado}")

# --- EXIBIÇÃO DA FICHA COMPLETA COM VÍDEOS ---
for idx, item in enumerate(FICHA_TREINO[treino_selecionado], 1):
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.checkbox(f"**{idx}. {item['exercicio']}**", key=f"ex_{treino_selecionado}_{idx}")
            st.caption(f"📊 {item['series']}x ({item['reps']}) | ⏱️ {item['descanso']}")
        with col2:
            st.link_button("🎥 Vídeo", item["video"])
        st.divider()

# --- INTEGRAÇÃO COM IA DO GOOGLE AI STUDIO (GEMINI 2.5) ---
st.subheader("🤖 Personal Trainer AI")

tempo_disponivel = st.slider("Tempo disponível hoje (minutos):", 20, 90, 60)
duvida_usuario = st.text_input("Observações ou dores hoje? (ex: 'dor no ombro', 'pouco tempo')", "")

if st.button("✨ Gerar Ajuste / Dica com Gemini"):
    with st.spinner("Analisando sua ficha..."):
        prompt = f"""
        Você é um Personal Trainer de elite focado em hipertrofia e musculação técnica.
        O aluno selecionou o treino: {treino_selecionado}.
        A ficha oficial deste treino é: {json.dumps(FICHA_TREINO[treino_selecionado], ensure_ascii=False)}
        
        Condições informadas:
        - Tempo disponível: {tempo_disponivel} minutos.
        - Observação/Dúvida do aluno: '{duvida_usuario}'.
        
        Responda de forma direta e estruturada:
        1. Como otimizar as séries/descansos para fechar nos {tempo_disponivel} minutos.
        2. Recomendações técnicas para a observação mencionada, mantendo o foco nos exercícios da ficha.
        """
        
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            st.markdown("### 📝 Orientação do Gemini:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Erro ao conectar com a IA: {e}")