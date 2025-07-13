FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["uvicorn", "src.api.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
