FROM python:3.13-slim

# Instalar dependencias necesarias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    pkg-config \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Generar e instalar el locale es_PE.UTF-8
RUN echo "es_PE.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=es_PE.UTF-8

# Establecer el locale en las variables de entorno
ENV LANG=es_PE.UTF-8  
ENV LANGUAGE=es_PE:es  
ENV LC_ALL=es_PE.UTF-8

# Establecer zona horaria (opcional)
ENV TZ=America/Lima

# Variables para optimizar Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear y trabajar desde el directorio del proyecto
WORKDIR /personal-webpage

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar el servidor
CMD ["/bin/bash", "-c", "python manage.py collectstatic --noinput; gunicorn --bind :8000 --workers 1 coding_journal.wsgi"]
