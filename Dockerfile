# ---------- Base Python image ----------
FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------- System dependencies ----------
# These cover unstructured, PDFs, docx, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmagic1 \
    poppler-utils \
    tesseract-ocr \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ---------- App setup ----------
WORKDIR /app

# 1) Install Python deps
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy the rest of your code
COPY . .

# Cloud Run injects $PORT, but set a default for local runs
ENV PORT=8080

# ---------- Start FastAPI with Uvicorn ----------
# Entry point: app/main.py -> app = FastAPI()
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
