import os
import streamlit as st
import base64
from openai import OpenAI

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Análisis de Imagen IA",
    page_icon="🤖",
    layout="centered"
)

# ---------------- ESTILO ----------------
st.markdown("""
<style>
.big-title {
    font-size: 38px;
    font-weight: bold;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}
.stButton>button {
    border-radius: 12px;
    background: linear-gradient(90deg, #6C63FF, #4CAF50);
    color: white;
    font-weight: bold;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<p class="big-title">🤖 Análisis Inteligente de Imágenes</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sube una imagen y deja que la IA la interprete por ti 🧠✨</p>', unsafe_allow_html=True)

# ---------------- API KEY (OCULTA) ----------------
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    st.error("⚠️ Falta configurar la API Key en secrets.toml")
    st.stop()

client = OpenAI(api_key=api_key)

# ---------------- FUNCION ----------------
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader("📸 Sube tu imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="🖼️ Imagen cargada", use_container_width=True)

# ---------------- OPCIONES ----------------
st.markdown("### ⚙️ Opciones")

show_details = st.toggle("🧠 Quiero hacer una pregunta específica", value=False)

if show_details:
    additional_details = st.text_area(
        "💬 Escribe tu pregunta o contexto:",
        placeholder="Ej: ¿Qué emoción transmite esta imagen?"
    )

# ---------------- BOTÓN ----------------
analyze_button = st.button("🚀 Analizar imagen")

# ---------------- PROCESO ----------------
if uploaded_file and analyze_button:

    with st.spinner("🔍 Analizando imagen..."):
        base64_image = encode_image(uploaded_file)

        prompt_text = "Describe detalladamente esta imagen en español de forma clara y natural."

        if show_details and additional_details:
            prompt_text += f"\n\nContexto del usuario:\n{additional_details}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ],
            }
        ]

        try:
            full_response = ""
            placeholder = st.empty()

            for completion in client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1200,
                stream=True
            ):
                if completion.choices[0].delta.content:
                    full_response += completion.choices[0].delta.content
                    placeholder.markdown("🤖 " + full_response + "▌")

            placeholder.markdown("🤖 " + full_response)

        except Exception as e:
            st.error(f"❌ Error: {e}")

# ---------------- MENSAJES ----------------
elif analyze_button and not uploaded_file:
    st.warning("⚠️ Primero sube una imagen")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("✨ Proyecto de visión con IA | Streamlit + OpenAI")
