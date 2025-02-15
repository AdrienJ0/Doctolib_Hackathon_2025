# Backend Dockerfile
FROM python:3.11
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# Streamlit Dockerfile
FROM python:3.11
WORKDIR /app
COPY streamlit/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY streamlit/ ./
CMD ["streamlit", "run", "app_streamlit.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
