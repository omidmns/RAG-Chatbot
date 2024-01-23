from langchain.schema import ChatMessage
from urllib.parse import urljoin
import streamlit as st
import requests
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE_URL = os.environ.get("API_BASE_URL")


def update_model(**kwargs):
    api_response = requests.post(urljoin(API_BASE_URL, "config"), json=kwargs)
    if api_response.status_code == 200:
        # not printing api_token in log
        if "huggingfacehub_api_token" not in kwargs:
            logger.info(f"model updated with {kwargs}!")
    else:
        api_response.raise_for_status()


def get_answer(**kwargs):
    model_response = requests.post(urljoin(API_BASE_URL, "chat"), json=kwargs)
    if model_response.status_code == 200:
        answer = model_response.json().get("response")
        return answer
    else:
        model_response.raise_for_status()


def main():
    with st.sidebar:
        huggingfacehub_api_token = st.text_input(
            "huggingfacehub_api_token", type="password"
        )
        if st.button("Submit token"):
            update_model(huggingfacehub_api_token=huggingfacehub_api_token)

    if not huggingfacehub_api_token:
        st.info("Please provide huggingfacehub_api_token!")
        st.stop()

    with st.sidebar:
        data_url = st.text_input("Webpage url")
        if st.button("Update URL"):
            update_model(url=data_url)

    if not data_url:
        st.info("Please provide a webpage url!")
        st.stop()

    with st.sidebar:
        repo_id = st.text_input("HuggingFace repo id; default: google/flan-t5-large")
        if st.button("Update Repo ID"):
            update_model(repo_id=repo_id)

        model_temperature = st.slider(
            "LLM parameter: temperature", min_value=0.01, max_value=2.0, value=0.01
        )

        model_top_k = st.slider(
            "LLM parameter: top_k", step=1, min_value=1, max_value=100, value=5
        )

        model_top_p = st.slider(
            "LLM parameter: top_p", min_value=0.0, max_value=1.0, value=0.25
        )

        if st.button("Update Model"):
            update_model(
                top_p=model_top_p, top_k=model_top_k, temperature=model_temperature
            )

    if "messages" not in st.session_state:
        st.session_state["messages"] = [ChatMessage(role="assistant", content="")]

    if prompt := st.chat_input():
        st.session_state.messages.append(ChatMessage(role="user", content=prompt))
        response = get_answer(question=st.session_state.messages[-1].content)
        st.session_state.messages.append(
            ChatMessage(role="assistant", content=response)
        )

    for msg in st.session_state.messages[1:]:
        st.chat_message(msg.role).write(msg.content)


if __name__ == "__main__":
    main()
