# 1. Puxa um "mini-computador" Linux que já vem com Python instalado
FROM python:3.11-slim

# 2. Cria uma pasta chamada /app lá dentro e entra nela
WORKDIR /app

# 3. Copia a nossa lista de bibliotecas para dentro do container
COPY requirements.txt .

# 4. Instala as bibliotecas lá dentro
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todos os nossos scripts e o banco de dados para o container
COPY . .

# 6. O comando que o container vai executar quando for ligado
CMD ["python", "etl_brasileirao.py"]