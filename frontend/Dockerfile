FROM node:18-alpine

WORKDIR /app

# Criar usuário não-root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

COPY package*.json ./

RUN npm install

COPY . .

# Mudar propriedade para usuário não-root
RUN chown -R nextjs:nodejs /app
USER nextjs

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"] 