FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml alembic.ini /app/

COPY ./app /app/app
COPY ./scripts /app/scripts

RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache -e .

ENV PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK=True
RUN python -c "from paddleocr import PaddleOCR; PaddleOCR(use_angle_cls=True, lang='ro', ocr_version='PP-OCRv3')"

RUN mkdir -p /app/uploads && chmod 777 /app/uploads
ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]