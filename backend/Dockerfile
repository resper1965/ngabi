# Usar uma imagem base que suporte múltiplos serviços
FROM ubuntu:22.04

# Evitar prompts interativos durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-pip \
    python3.11-dev \
    curl \
    wget \
    gnupg2 \
    lsb-release \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Configurar Python
RUN ln -s /usr/bin/python3.11 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

# Instalar PostgreSQL
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update \
    && apt-get install -y postgresql-15 postgresql-contrib-15 \
    && rm -rf /var/lib/apt/lists/*

# Instalar Redis
RUN apt-get update \
    && apt-get install -y redis-server \
    && rm -rf /var/lib/apt/lists/*

# Instalar Java (necessário para Elasticsearch)
RUN apt-get update \
    && apt-get install -y openjdk-11-jdk \
    && rm -rf /var/lib/apt/lists/*

# Instalar Elasticsearch
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - \
    && echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-7.x.list \
    && apt-get update \
    && apt-get install -y elasticsearch=7.17.0 \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretórios de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Tornar o script de inicialização executável
RUN chmod +x docker-entrypoint.sh

# Criar diretórios necessários
RUN mkdir -p /var/lib/postgresql/data /var/log/postgresql /var/lib/redis /var/lib/elasticsearch

# Configurar PostgreSQL
RUN chown -R postgres:postgres /var/lib/postgresql /var/log/postgresql
RUN su - postgres -c "initdb -D /var/lib/postgresql/data"

# Configurar Redis
RUN mkdir -p /etc/redis && echo "daemonize yes" > /etc/redis/redis.conf

# Configurar Elasticsearch
RUN chown -R elasticsearch:elasticsearch /var/lib/elasticsearch

# Expor portas
EXPOSE 8000 5432 6379 9200

# Usar o script de inicialização
ENTRYPOINT ["./docker-entrypoint.sh"] 