FROM python:3.10-slim

WORKDIR /app
ADD frontend_server.py .

CMD ["python", "frontend_server.py"]
