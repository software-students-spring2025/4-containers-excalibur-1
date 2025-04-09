FROM python:3.10-slim
RUN apt-get update && apt-get install -y build-essential gcc
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --dev --system
COPY . .
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
