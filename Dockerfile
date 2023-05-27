FROM python:3.12.0b1-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt --user
CMD ["python", "main.py"]
