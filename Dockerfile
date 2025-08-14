
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV DB_PATH=/data/urls.db
ENV BASE_URL=http://localhost:8000
ENV SECRET_KEY=change-me
EXPOSE 8000
RUN mkdir -p /data
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "wsgi:app"]
