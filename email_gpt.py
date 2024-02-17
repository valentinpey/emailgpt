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
from openai import OpenAIError


class EmailGPT:
    def __init__(self, api_key, synthetic_level, tone, nom_destinataire, main_objective, key_points, signature):
        self.api_key = api_key
        self.synthetic_level = synthetic_level
        self.tone = tone
        self.nom_destinataire = nom_destinataire
        self.main_objective = main_objective
        self.key_points = key_points
        self.signature = signature

    def define_instructions(self):
        # Define the common instructions for the language model
        system_instructions = """
            You are a helpful AI assistant with expertise in crafting email.
            Your responses should be clear, utilizing proper structured techniques like bullet points, and paragraph breaks where needed.
            You will respond in the tone precised in the following.
        """
        # Define the specific instructions based on user input
        system_instructions += "\n{synthetic_level}"
        system_instructions += "\nMaintain a {tone} tone."
        system_instructions +="- Recipient's Name: {nom_destinataire}\n"
        system_instructions +="- Main objective of the email: {main_objective}\n"
        if self.key_points:
            system_instructions += "\nEnsure to include these key points in your response: {key_points}."
        system_instructions +="- Signature (name, position, contact information): {signature}\n"

        system_message_prompt = SystemMessagePromptTemplate.from_template(system_instructions)
        chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt])
        return chat_prompt

    def answer_message(self):
        try:
            # Initialize the language model
            chat = ChatOpenAI(openai_api_key=self.api_key)
            # Combine the common and specific instructions
            chat_prompt = self.define_instructions()
            # Prepare the prompt for the language model
            request = chat_prompt.format_prompt(nom_destinataire=self.nom_destinataire,
                                        main_objective=self.main_objective,
                                        synthetic_level=self.synthetic_level,
                                        signature=self.signature,
                                        tone=self.tone,
                                        key_points=self.key_points
                                        ).to_messages()
            response = chat(request)
            return response.content
        except OpenAIError as e:
            return e
        except Exception as e:
            return e