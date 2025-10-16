# Usa una imagen ligera de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala dependencias
RUN pip install --no-cache-dir fastapi uvicorn requests pytest

# Expone el puerto donde corre FastAPI
EXPOSE 8000

# Comando por defecto para ejecutar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
