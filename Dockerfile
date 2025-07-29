# Dockerfile para o Servidor MCP da Serena
# Usando Python 3.11 slim para reduzir o tamanho da imagem

FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Criar usuário não-root para segurança
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências primeiro (para cache do Docker)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY servidor_parcerias_mcp.py .
COPY env.example .
COPY .env .

# Criar diretório para logs e dados
RUN mkdir -p /app/logs && chown -R mcpuser:mcpuser /app

# Mudar para usuário não-root
USER mcpuser

# Expor porta (se necessário para debugging)
EXPOSE 54321

# Health check (comentado temporariamente para debug)
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD curl -f http://localhost:54321/health || exit 1

# Comando padrão
CMD ["python", "servidor_parcerias_mcp.py"]

# Labels para documentação
LABEL maintainer="Serena MCP Server Team" \
      description="MCP Server for Serena Partnership API" \
      version="1.0.0" \
      org.opencontainers.image.source="https://github.com/leomeirae/serena-mcp-server" 