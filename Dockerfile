FROM python:3.9-slim

# Instalar dependencias para Docker CLI
RUN apt-get update && \
    apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker CLI
RUN apt-get update && \
    apt-get install -y docker-ce-cli

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Configuración de seguridad (personaliza estos valores!)
ENV LOGIN_USERNAME=admin
ENV LOGIN_PASSWORD=admin123
ENV SECRET_KEY=tu_clave_secreta_aqui

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]