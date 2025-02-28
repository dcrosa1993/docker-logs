FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Configuración de seguridad (cambiar estos valores en producción!)
ENV LOGIN_USERNAME=admin
ENV LOGIN_PASSWORD=admin123
ENV SECRET_KEY=supersecretkey

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]