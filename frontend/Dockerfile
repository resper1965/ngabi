FROM node:20-alpine

WORKDIR /app

# Criar usuário não-root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

COPY package*.json ./

RUN npm install

COPY . .

# Garantir permissões de escrita para o usuário
RUN mkdir -p /app/.vite && chown -R nextjs:nodejs /app/.vite

# Mudar propriedade para usuário não-root
RUN chown -R nextjs:nodejs /app

EXPOSE 3000

# Executar como root para evitar problemas de permissão com Vite
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"] 