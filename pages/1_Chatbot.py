import streamlit as st
import requests

#API_URL = "http://backend:8000/chat"

st.title("BioMistral-7B Chatbot Médical")

st.markdown("# Generalist BioMedical Chatbot")
st.sidebar.header("Generalist BioMedical Chatbot")

## TODO

## Make the first message of the chatbot more welcoming


# Liste de questions pour orienter l'utilisateur
questions = [
    "Quels sont vos symptômes principaux ?",
    "Depuis combien de temps ressentez-vous ces symptômes ?",
    "Avez-vous de la fièvre ? (oui/non)",
    "Avez-vous des antécédents médicaux ? (oui/non, précisez)"
]

# Initialisation de l'historique de chat et de la question courante
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "question_index" not in st.session_state:
    st.session_state.question_index = 0

# Affichage des messages précédents
for message in st.session_state.chat_history:
    st.text(message)

# Affichage de la question courante
if st.session_state.question_index < len(questions):
    st.text(f"AI: {questions[st.session_state.question_index]}")
    user_input = st.text_input("Vous:", "", key="input")
    
    if st.button("Envoyer") and user_input:
        st.session_state.chat_history.append(f"Vous: {user_input}")
        st.session_state.chat_history.append(f"AI: {questions[st.session_state.question_index]}")
        
        # Passer à la question suivante
        st.session_state.question_index += 1
        st.experimental_rerun()

# Envoi à l'API après toutes les questions
elif st.button("Analyser"):
    response = requests.post(API_URL, json={"conversation": st.session_state.chat_history})
    if response.status_code == 200:
        bot_reply = response.json().get("response", "[Erreur: Pas de réponse]")
        st.session_state.chat_history.append(f"AI: {bot_reply}")
    else:
        st.session_state.chat_history.append("AI: [Erreur: API injoignable]")
    st.experimental_rerun()
