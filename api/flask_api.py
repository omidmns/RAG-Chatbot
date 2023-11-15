from flask import Flask, request, jsonify
from model import RAGModel
import os

app = Flask(__name__)
model = RAGModel()


@app.route("/config", methods=["POST"])
def config():

    huggingfacehub_api_token = request.json.get('huggingfacehub_api_token', 0)
    url = request.json.get('url', 0)
    repo_id = request.json.get('repo_id', 0)
    model_temp = request.json.get('temperature', 0)
    model_top_k = request.json.get('top_k', 0)
    model_top_p = request.json.get('top_p', 0)

    if huggingfacehub_api_token:
        model_updated = model.update_llm(huggingfacehub_api_token=huggingfacehub_api_token)

    if url:
        model_updated = model.load_url(url)

    if repo_id:
        model_updated = model.update_llm(repo_id=repo_id)

    if model_temp:
        model_updated = model.update_llm(model_kwargs={'temperature': model_temp})

    if model_top_k:
        model_updated = model.update_llm(model_kwargs={'top_k': model_top_k})

    if model_top_p:
        model_updated = model.update_llm(model_kwargs={'top_p': model_top_p})

    return str(model_updated)


@app.route("/chat", methods=["POST"])
def chat():
    question = request.json['question']
    response = model.retrieve_response(question)

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
