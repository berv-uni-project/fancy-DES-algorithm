FROM python:3.14.2-alpine AS build
WORKDIR /app
COPY requirements.txt .
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
RUN apk --no-cache add musl-dev linux-headers g++
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


FROM python:3.14.2-alpine AS final
WORKDIR /app
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . .
CMD ["python", "main.py"]
