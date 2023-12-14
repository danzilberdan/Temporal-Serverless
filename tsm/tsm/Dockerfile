FROM tsbase

WORKDIR /app

COPY . .

RUN poetry export -f requirements.txt --output requirements.txt && \
    pip install -r requirements.txt
