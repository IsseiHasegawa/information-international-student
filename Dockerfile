FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ backend/
COPY frontend/ frontend/

EXPOSE 5000
CMD ["sh", "-c", "python backend/src/init_db.py && gunicorn --chdir backend/src --bind 0.0.0.0:5000 app:app"]