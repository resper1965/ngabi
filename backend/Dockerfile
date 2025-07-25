# Dockerfile otimizado e seguro para Python 3.13
# n.Gabi - Chat Multi-Agente (Versão Hardened + Otimizada)

# Usar Alpine 3.22 (mais recente e seguro)
FROM alpine:3.22

# Instalar Python 3.13 e dependências essenciais
RUN apk add --no-cache \
    python3 \
    python3-dev \
    py3-pip \
    gcc \
    musl-dev \
    postgresql-dev \
    curl \
    && rm -rf /var/cache/apk/*

# Criar usuário não-root para segurança
RUN adduser -D -s /bin/sh appuser

# Definir diretório de trabalho
WORKDIR /app

# Definir variáveis de ambiente para segurança
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONHASHSEED=random
ENV PYTHONPATH=/app

# Copiar requirements e instalar dependências Python
COPY requirements-python313.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip --break-system-packages && \
    pip3 install --no-cache-dir -r requirements.txt --break-system-packages && \
    rm -rf /root/.cache/pip

# Copiar código da aplicação
COPY . .

# Mudar propriedade para usuário não-root
RUN chown -R appuser:appuser /app

# Mudar para usuário não-root
USER appuser

# Expor porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando para iniciar a aplicação
CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"] 