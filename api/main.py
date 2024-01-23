from fastapi import FastAPI, Body, Request
from api.model import RAGModel


app = FastAPI()
model = RAGModel()


@app.post("/config")
async def config(request: Request):
    model_updated = False

    req = await request.json()

    if "url" in req:
        model_updated = model.load_url(req.pop("url"))

    if req:
        model_updated = model.update_llm(**req)

    return str(model_updated)


@app.post("/chat")
async def chat(question: str = Body(..., embed=True)):
    response = model.retrieve_response(question)
    return {"response": response}
