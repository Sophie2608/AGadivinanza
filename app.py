pip install requests
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Lista de adivinanzas (pregunta y respuesta)
adivinanzas = [
    {"question": "¿Cuál es el animal más grande del mundo?", "answer": "ballena azul"},
    {"question": "¿Cuántos planetas tiene el sistema solar?", "answer": "8"},
    {"question": "¿En qué año llegó el hombre a la luna?", "answer": "1969"},
    {"question": "¿Cuál es la capital de Francia?", "answer": "parís"},
    {"question": "¿Cuántos continentes hay en el mundo?", "answer": "7"}
]

# Estado de sesión para mantener las respuestas y el puntaje
if "puntaje" not in st.session_state:
    st.session_state.puntaje = 0
    st.session_state.index_adivinanza = 0
    st.session_state.respuesta_usuario = ""
    st.session_state.respuesta_verificada = False  # Para verificar si ya se respondió

# Función para verificar la respuesta
def verificar_respuesta(respuesta_usuario, respuesta_correcta):
    return respuesta_usuario.strip().lower() == respuesta_correcta.strip().lower()

# Mostrar título
st.title("Juego de Adivinanzas")

# Obtener la adivinanza actual
adivinanza_actual = adivinanzas[st.session_state.index_adivinanza]

# Mostrar la adivinanza
st.subheader("Adivina la respuesta:")
st.write(adivinanza_actual["question"])

# Campo de entrada para la respuesta
if not st.session_state.respuesta_verificada:  # Solo mostrar el input si no se ha respondido
    st.session_state.respuesta_usuario = st.text_input("Tu respuesta:")

# Verificar respuesta
if st.button("Verificar respuesta") and not st.session_state.respuesta_verificada:
    if verificar_respuesta(st.session_state.respuesta_usuario, adivinanza_actual["answer"]):
        st.success("¡Correcto! 🎉")
        st.markdown(":star: :star: :star:")  # Mostrar estrellas
        st.session_state.puntaje += 1  # Incrementar puntaje
    else:
        st.error("¡Incorrecto! Intenta de nuevo.")
    
    st.session_state.respuesta_verificada = True  # Marcar que la respuesta ya fue verificada

# Siguiente adivinanza
if st.button("Siguiente pregunta") and st.session_state.respuesta_verificada:
    # Avanzar al siguiente índice
    if st.session_state.index_adivinanza < len(adivinanzas) - 1:
        st.session_state.index_adivinanza += 1
        st.session_state.respuesta_usuario = ""  # Limpiar respuesta
        st.session_state.respuesta_verificada = False  # Resetear estado para la siguiente pregunta
    else:
        # Juego terminado
        st.session_state.respuesta_verificada = False  # Terminar el juego, reseteando la verificación para mostrar el resultado final
        st.session_state.respuesta_usuario = ""  # Limpiar respuesta

# Mostrar puntuación final al terminar el juego
if st.session_state.index_adivinanza == len(adivinanzas) - 1 and not st.session_state.respuesta_verificada:
    st.subheader("¡Juego terminado!")
    st.write(f"Puntuación: {st.session_state.puntaje}/{len(adivinanzas)}")

    # Determinar el apodo según la puntuación
    if st.session_state.puntaje == len(adivinanzas):
        apodo = "Genio"
    elif st.session_state.puntaje == len(adivinanzas) - 1:
        apodo = "¡Casi Genio!"
    elif st.session_state.puntaje >= len(adivinanzas) - 2:
        apodo = "Buena respuesta"
    else:
        apodo = "¡Sigue practicando!"

    # Mostrar apodo
    st.write(f"¡{apodo}!")

    # Mostrar imagen contenta si la puntuación es alta
    if st.session_state.puntaje == len(adivinanzas):
        # Descargar la imagen desde la URL
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Emoji_u1f60a.svg/1024px-Emoji_u1f60a.svg.png"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))  # Abrir la imagen desde los datos descargados

        # Mostrar la imagen
        st.image(img, caption="¡Genio!")
