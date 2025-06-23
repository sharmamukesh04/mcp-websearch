FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System packages (you may need curl/git if using private repos)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Verify streamlit was installed
RUN python -m pip show streamlit || (echo "❌ Streamlit NOT installed" && exit 1)

# Copy your app code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
ENTRYPOINT ["python", "-m", "streamlit"]
CMD ["run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

