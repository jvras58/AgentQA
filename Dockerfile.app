FROM python:3.12-slim

# Instalar uv
RUN pip install uv

# Copiar arquivos do projeto
WORKDIR /app
COPY . .

# Instalar dependências
RUN uv sync --no-install-project

# Comando para executar
CMD ["uv", "run", "python", "-m", "src.main"]
