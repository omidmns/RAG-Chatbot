FROM pytorch/pytorch:latest

WORKDIR /app

RUN mkdir -p /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY flask_api.py /app
COPY model.py /app

EXPOSE 5000
HEALTHCHECK CMD curl --fail http://localhost:5000/_stcore/health

ENTRYPOINT ["python", "flask_api.py"]