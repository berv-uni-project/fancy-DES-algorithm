FROM python:3.11.0rc2-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt --user
CMD ["python", "main.py"]
