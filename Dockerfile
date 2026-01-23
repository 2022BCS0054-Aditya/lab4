FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY app.py .
COPY outputs/ ./outputs/ 

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m pip install scikit-learn

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]