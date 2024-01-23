FROM pytorch/pytorch:2.1.1-cuda12.1-cudnn8-runtime

WORKDIR /home

RUN mkdir -p /home/api

COPY ./api/requirements.txt /home/

RUN pip3 install -r requirements.txt

COPY ./api/*.py /home/api/

EXPOSE 8000
HEALTHCHECK CMD curl --fail http://localhost:8000/_stcore/health

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]