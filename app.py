import os
import streamlit as st
import base64
from openai import OpenAI

# ---------------- FUNCIONES ----------------
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Análisis de Imagen",
    page_icon="🤖",
    layout="centered"
)

# ---------------- ESTILOS ----------------
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}
.stButton>button {
    background-color: #6C63FF;
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<p class="title">🤖 Análisis de Imagen</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sube una imagen y descubre lo que la IA puede interpretar 🧠</p>', unsafe_allow_html=True)

# ---------------- API KEY ----------------
api_key = st.text_input("🔑 Ingresa tu API Key de OpenAI", type="password")

client = None
if api_key:
    client = OpenAI(api_key=api_key)

# ---------------- SUBIDA ----------------
st.markdown("### 📂 Cargar imagen")
uploaded_file = st.file_uploader("Elige una imagen", type=["jpg", "png", "jpeg"])

# ---------------- MOSTRAR IMAGEN ----------------
if uploaded_file:
    st.image(uploaded_file, caption="🖼️ Imagen cargada", use_container_width=True)

# ---------------- OPCIONES ----------------
st.markdown("### ⚙️ Opciones")

show_details = st.checkbox("✍️ Quiero hacer una pregunta específica sobre la imagen")

additional_details = ""
if show_details:
    additional_details = st.text_area(
        "💬 Escribe tu pregunta o contexto:",
        placeholder="Ej: ¿Qué emoción transmite esta imagen?"
    )

# ---------------- BOTÓN ----------------
st.markdown(" ")
analyze_button = st.button("🚀 Analizar imagen")

# ---------------- PROCESO ----------------
if analyze_button:

    if not uploaded_file:
        st.warning("⚠️ Sube una imagen primero")
    
    elif not api_key:
        st.warning("⚠️ Ingresa tu API Key")
    
    else:
        with st.spinner("🧠 Analizando imagen..."):

            base64_image = encode_image(uploaded_file)

            prompt_text = "Describe detalladamente lo que ves en la imagen en español."

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

                for chunk in client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    max_tokens=1200,
                    stream=True
                ):
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        placeholder.markdown(full_response + "▌")

                placeholder.markdown(full_response)

                st.success("✅ Análisis completado")

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("✨ Hecho con IA + Streamlit")
