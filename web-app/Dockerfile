FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install pipenv && pipenv install --dev --system
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]