from langchain.schema import ChatMessage
import streamlit as st
import requests


url = "http://api:5000/"
model_api_conf = url + "config"
model_api_chat = url + "chat"


def update_model(kwargs):
    api_response = requests.post(model_api_conf, json=kwargs)
    if api_response.status_code == 200:
        print(f'model updated with data {kwargs}!')
    else:
        print("Error: Unable to get an answer from the model.")


def get_answer(question):
    data = {"question": question}
    model_response = requests.post(model_api_chat, json=data)
    if model_response.status_code == 200:
        answer = model_response.json().get("response")
        return answer
    else:
        return "Error: Unable to get an answer from the model."


with st.sidebar:
    data_url = st.text_input("Webpage url")
    url_button = st.button("submit url")

if url_button:
    if data_url:
        update_model({'url': f'{data_url}'})

with st.sidebar:
    repo_id = st.text_input("HuggingFace repo id; e.g. google/flan-t5-base")
    repo_button = st.button("submit repo_id")

if repo_button:
    if repo_id:
        update_model({'repo_id': f'{repo_id}'})

with st.sidebar:
    model_temperature = st.slider('LLM parameter: temperature',
                                  min_value=0.01, max_value=2.0,
                                  value=0.01)
    update_model({'temperature': f'{model_temperature}'})

with st.sidebar:
    model_top_k = st.slider('LLM parameter: top_k', step=1,
                                  min_value=1, max_value=100,
                                  value=5)
    update_model({'top_k': model_top_k})

with st.sidebar:
    model_top_p = st.slider('LLM parameter: top_p',
                                  min_value=0.0, max_value=1.0,
                                  value=.25)
    update_model({'top_p': model_top_p})

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="")]

if prompt := st.chat_input():

    if not data_url:
        st.info("Please provide a webpage url!")
        st.stop()

    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    response = get_answer(st.session_state.messages[-1].content)
    st.session_state.messages.append(ChatMessage(role="assistant", content=response))

for msg in st.session_state.messages[1:]:
    st.chat_message(msg.role).write(msg.content)
