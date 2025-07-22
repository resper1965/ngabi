FROM node:20-alpine

WORKDIR /app

# Criar usuário não-root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Copiar package files primeiro para cache de dependências
COPY package*.json ./

# Instalar todas as dependências (incluindo devDependencies)
RUN npm ci && npm cache clean --force

# Copiar código da aplicação
COPY . .

# Garantir permissões de escrita para o usuário
RUN mkdir -p /app/.vite && chown -R nextjs:nodejs /app/.vite

# Mudar propriedade para usuário não-root
RUN chown -R nextjs:nodejs /app

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Comando para iniciar a aplicação em modo de produção
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000", "--mode", "production"] 