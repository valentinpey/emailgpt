import streamlit as st

from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from datetime import datetime
from langchain.llms import OpenAI
from langchain.output_parsers import DatetimeOutputParser
from langchain.chat_models import ChatOpenAI
from AnswerGPT import AnswerGPT
from email_gpt import EmailGPT

from openai import OpenAIError
import time

import os


def home():
    st.title("🔥  - Home")
    st.markdown("Welcome to the email interface of Prometee!")
    st.markdown("This interface allows you to generate email responses using OpenAI's GPT language model.")
    st.markdown("You can choose between two options:")
    st.markdown("- **AnswerGPT**: Generate a response to an email.")
    st.markdown("- **EmailGPT**: Generate a new email.")
    # Add your home page content here


def answer_gpt():
    # Add a brief user guide
    
    st.title("🦜🔗  - AnswerGPT2")
    st.write("Welcome to AnswerGPT of Prometee !")

    # Add a brief user guide
    st.sidebar.markdown("""
    ### User Guide
    1. **Enter the original email that you want to reply to.**
    2. **Enter key points that should be included in the email response.**
    3. **Select the tone of the email response.**
    4. **Adjust the length of the response.**
    5. **Click "Submit" to generate the email response.** You can copy and modify the response in the "Email Response" box.
    """)

    # Add a slider for the user to select the synthetic level
    synthetic_level = st.sidebar.slider(
        "Select the length of the answer:", min_value=0, max_value=6)

    synthetic_level_instructions = {
        6: "Use complex sentence structures, longer sentences, and more details. ",
        5: "Make the response relatively detailed. ",
        4: "Make the response somewhat detailed, but still fairly concise. ",
        3: "Balance conciseness and detail in the response. ",
        2: "Make the response somewhat concise, but with some detail. ",
        1: "Make the response concise. ",
        0: "Make the response extremely concise, straightforward and very short. "
    }
    synthetic_level = synthetic_level_instructions[synthetic_level]

    # Get the OpenAI API key directly from ours
    #openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    openai_api_key = st.secrets["openai_secret"]
    os.environ['OPENAI_API_KEY'] = openai_api_key # Pass the API key into an environment variable.

    # Get the tone of the message from the user
    tone = st.sidebar.selectbox(
        "Select the tone of the message:", options=['Casual', 'Formal']
    )

    if 'email_summary' not in st.session_state or 'email' not in st.session_state or 'gpt' not in st.session_state:
        answerGPT = None
        email_summary = None

        with st.form("form"):
            # Get the original message from the user
            original_message = st.text_area("Email to answer:",
                                            help="Enter the original message that you want to reply to.")
            # Add a submit button to the form
            submitted = st.form_submit_button("Next")
            # if not openai_api_key:
            #    st.info("Please add your OpenAI API key to continue.")
            if not original_message:
                st.info("Please enter an original message.")
            # If the form is submitted, generate the email response
            elif submitted:
                answerGPT = AnswerGPT(api_key=openai_api_key, synthetic_level=synthetic_level, tone=tone,
                                    original_message=original_message)
                with st.spinner('Generating summary...'):
                    email_summary = answerGPT.generate_summary()

                st.text_area("Email Summary:", value=email_summary, height=150)

                st.session_state['gpt'] = answerGPT
                st.session_state['email_summary'] = email_summary
                st.session_state['email'] = original_message

    else:
        st.text_area("Email", st.session_state['email'])
        st.text_area("Email summary", st.session_state['email_summary'])
        answerGPT = st.session_state['gpt']

        if "messages" not in st.session_state:
            st.session_state.messages = []

        if len(st.session_state.messages) == 5:
            st.session_state.messages = None
            st.text_area("Email Answer", value=answerGPT.craft_answer(), height=400)

        # Display chat messages from history on app rerun
        if st.session_state.messages is not None:
            if prompt := st.chat_input("Answer:"):  # Prompt for user input and save to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                question = st.session_state.messages[-1]["content"]
                answerGPT.chain.memory.save_context(
                    {"query": question},
                    {"output": prompt},
                )

            for message in st.session_state.messages:  # Display the prior chat messages
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            # If last message is not from assistant, ask a new question
            if len(st.session_state.messages) < 5:
                if len(st.session_state.messages) == 0 or st.session_state.messages[-1]["role"] != "assistant":
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            response = answerGPT.ask_question()
                            st.write(response)
                            message = {"role": "assistant", "content": response}
                            st.session_state.messages.append(message)  # Add response to message history

# Page EmailGPT
def email_gpt():

    st.title("🦄🔗  - EmailGPT")
    st.write("Welcome in the interface EmailGPT of Prometee !")

    # Add a slider for the user to select the synthetic level
    synthetic_level = st.sidebar.slider(
        "Select the length of the email:", min_value=0, max_value=6)

    synthetic_level_instructions = {
        6: "Use complex sentence structures, longer sentences, and more details. ",
        5: "Make the response relatively detailed. ",
        4: "Make the response somewhat detailed, but still fairly concise. ",
        3: "Balance conciseness and detail in the response. ",
        2: "Make the response somewhat concise, but with some detail. ",
        1: "Make the response concise. ",
        0: "Make the response extremely concise, straightforward and very short. "
    }
    synthetic_level = synthetic_level_instructions[synthetic_level]

    # Get the OpenAI API key directly from ours
    #openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    
    openai_api_key = st.secrets["openai_secret"]
    os.environ['OPENAI_API_KEY'] = openai_api_key # Pass the API key into an environment variable.

    # Get the tone of the message from the user
    tone = st.sidebar.selectbox(
        "Select the tone of the message:", options = ["Slang", "Casual",  "Professional", "Legal/Official"] #["Slang", "Colloquial", "Casual", "Informal", "Friendly", "Neutral", "Professional", "Business Formal", "Formal", "Legal/Official"]
    )

    # Set up the form for user input
    with st.form("myform"):
      #Création des champs pour collecter les entrées de l'utilisateur
        nom_destinataire = st.text_input("Recipient's Name:")
        #sujet_email = st.text_input("Sujet de l'email:")
        main_objective = st.text_area("Main objective of the email:", help="Enter the main objective of the email, the main reason for sending the email.")
        key_points = st.text_area("Key points to include:", help="Enter the key points that should be included in the email response, gives the important information that should be included in the email.")
        #action_souhaitée = st.text_input("Action souhaitée de la part du destinataire:")
        #date_limite = st.text_input("Date limite pour l'action ou la réponse:")
        signature = st.text_input("Signature:", help="Enter your name or the name of the sender. (name, position, informations of contact)")

        # Add a submit button to the form
        submitted = st.form_submit_button("Submit")
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
        elif not nom_destinataire or not main_objective or not key_points or not signature:
                st.info("Please enter all required information.")
        # If the form is submitted, generate the email response
        elif submitted:
            emailGPT = EmailGPT(api_key=openai_api_key, synthetic_level=synthetic_level, tone=tone, nom_destinataire = nom_destinataire, main_objective = main_objective, key_points=key_points, signature=signature)
            # Generate the email response
            progress_bar = st.progress(0)
            with st.spinner('Generating response...'):
                response = emailGPT.answer_message()
            for i in range(100):
                # Update progress bar
                progress_bar.progress(i + 1)
                # Pause for effect
                time.sleep(0.01)
            # Display the response
            if type(response) == OpenAIError:
                st.error(f"An OpenAI API error occurred: {str(response)}")
            elif type(response) == Exception:
                st.error(f"An OpenAI API error occurred: {str(response)}")
            else:
                st.text_area("Email Response:", value=response, height=300)
