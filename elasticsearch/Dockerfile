FROM elasticsearch:7.17.0

# Configurar Elasticsearch
ENV discovery.type=single-node
ENV xpack.security.enabled=false
ENV cluster.name=ngabi-cluster

# Expor porta
EXPOSE 9200

# Comando padrão
CMD ["elasticsearch"] 