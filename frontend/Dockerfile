# Dockerfile para Frontend n.Gabi (multi-stage)

# ==========================
# Stage 1: Builder
# ==========================
FROM node:20-alpine AS builder

ENV NODE_ENV=production
ENV NPM_CONFIG_LOGLEVEL=warn

# Dependências úteis
RUN apk add --no-cache \
    curl \
    bash \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Cache de dependências
COPY package*.json ./
RUN npm ci

# Copiar código da aplicação
COPY . .

# Build-time args vindos do EasyPanel
ARG VITE_API_BASE_URL
ARG VITE_PRODUCTION_API_URL
ARG VITE_SUPABASE_URL
ARG VITE_SUPABASE_ANON_KEY
ARG NODE_ENV
ARG GIT_SHA

# Tornar disponíveis para o Vite no build
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
ENV VITE_PRODUCTION_API_URL=${VITE_PRODUCTION_API_URL:-${VITE_API_BASE_URL}}
ENV VITE_SUPABASE_URL=${VITE_SUPABASE_URL}
ENV VITE_SUPABASE_ANON_KEY=${VITE_SUPABASE_ANON_KEY}
ENV VITE_GIT_SHA=${GIT_SHA}

# Build da aplicação (precisa de devDependencies: vite/tsc)
RUN npm run build

# ==========================
# Stage 2: Runner
# ==========================
FROM node:20-alpine AS runner

ENV NODE_ENV=production
ENV NPM_CONFIG_LOGLEVEL=warn

RUN apk add --no-cache curl && rm -rf /var/cache/apk/*

WORKDIR /app

# Copiar artefatos do build
COPY --from=builder /app/dist ./dist

# Servir estáticos
RUN npm install -g serve

# Criar usuário não-root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

RUN chown -R nextjs:nodejs /app
USER nextjs

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000 || exit 1

CMD ["serve", "-s", "dist", "-l", "3000"] 