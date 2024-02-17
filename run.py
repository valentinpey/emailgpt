
import streamlit as st
from AnswerGPT import AnswerGPT
from email_gpt import EmailGPT
from fct import *

# Set up the title of the web application
#st.title("🦜🔗  - AnswerGPT")
# Page d'accueil


# Barre latérale
sidebar_options = {
    "Accueil": home,
    "AnswerGPT": answer_gpt,
    "EmailGPT": email_gpt
}
selected_option = st.sidebar.selectbox("Sélectionnez une option", list(sidebar_options.keys()))

# Affiche la page correspondante à l'option sélectionnée
sidebar_options[selected_option]()
