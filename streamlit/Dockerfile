# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create a /static folder in the /app directory
RUN mkdir -p /app/static

# Copy requirements and install dependencies
COPY requirements_2.txt .
RUN pip install -r requirements_2.txt

# Copy the rest of the Streamlit app
COPY . .

# Set environment variables
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_PORT=9000

# Run Streamlit app
CMD ["streamlit", "run", "Login.py"]
