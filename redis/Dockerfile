FROM redis:7-alpine

# Configurar Redis
RUN echo "daemonize no" >> /usr/local/etc/redis/redis.conf

# Expor porta
EXPOSE 6379

# Comando padrão
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"] 