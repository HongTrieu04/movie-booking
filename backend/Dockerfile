# Python slim cho FastAPI
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Cài đặt deps hệ thống tối thiểu
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements trước để cache layer
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy mã nguồn
COPY app /app

# Mặc định chạy uvicorn (prod)
# Nếu bạn dùng app/main.py với FastAPI instance tên "app":
# uvicorn main:app --host 0.0.0.0 --port 8000
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
