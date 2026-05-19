FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r api/requirements.txt

EXPOSE 8000

CMD ["gunicorn", "api.index:app", "--bind", "0.0.0.0:8000"]