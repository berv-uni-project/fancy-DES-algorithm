FROM python:3.10.4-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt --user
CMD ["python", "main.py"]
