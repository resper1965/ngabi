# Dockerfile para Frontend n.Gabi
FROM node:18-alpine

# Definir variáveis de ambiente
ENV NODE_ENV=production
ENV NPM_CONFIG_LOGLEVEL=warn

# Instalar dependências do sistema
RUN apk add --no-cache \
    curl \
    && rm -rf /var/cache/apk/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências
RUN npm ci --only=production && npm cache clean --force

# Copiar código da aplicação
COPY . .

# Build da aplicação
RUN npm run build

# Instalar serve para produção
RUN npm install -g serve

# Criar usuário não-root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Mudar propriedade dos arquivos
RUN chown -R nextjs:nodejs /app

# Mudar para usuário não-root
USER nextjs

# Expor porta
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Comando para executar a aplicação
CMD ["serve", "-s", "dist", "-l", "3000"] 