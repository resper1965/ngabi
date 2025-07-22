# 🔒 Segurança com gosu - n.Gabi

## 📋 Visão Geral

O **gosu** é uma ferramenta essencial para segurança em containers Docker. Ele permite executar comandos como usuário não-root de forma segura, eliminando vulnerabilidades de privilégios elevados.

## 🎯 Benefícios do gosu

### 1. **Execução Segura como Usuário Não-Root**
```bash
# ❌ Sem gosu (inseguro)
USER root
CMD ["python3", "-m", "uvicorn", "app.main:app"]

# ✅ Com gosu (seguro)
CMD ["gosu", "appuser", "python3", "-m", "uvicorn", "app.main:app"]
```

### 2. **Prevenção de Vulnerabilidades**
- **Container Escape**: Impede que processos maliciosos escapem do container
- **Privilege Escalation**: Elimina possibilidade de elevação de privilégios
- **File System Access**: Restringe acesso ao sistema de arquivos

### 3. **Compatibilidade Multi-Arquitetura**
O gosu suporta todas as arquiteturas principais:
- `x86_64` (AMD64)
- `aarch64` (ARM64)
- `armhf` (ARM32)
- `ppc64le` (PowerPC)
- `riscv64` (RISC-V)
- `s390x` (IBM S390)

## 🔧 Implementação no n.Gabi

### Backend (Python 3.13 + Alpine 3.22)
```dockerfile
# Instalar gosu com verificação de integridade
RUN set -eux; \
    apk add --no-cache --virtual .gosu-fetch gnupg; \
    arch="$(apk --print-arch)"; \
    case "$arch" in \
        'x86_64') \
            url='https://github.com/tianon/gosu/releases/download/1.17/gosu-amd64'; \
            sha256='bbc4136d03ab138b1ad66fa4fc051bafc6cc7ffae632b069a53657279a450de3' \
            ;; \
        # ... outras arquiteturas
    esac; \
    wget -O /usr/local/bin/gosu.asc "$url.asc"; \
    wget -O /usr/local/bin/gosu "$url"; \
    echo "$sha256 */usr/local/bin/gosu" | sha256sum -c -; \
    gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
    chmod +x /usr/local/bin/gosu

# Executar como usuário não-root
CMD ["gosu", "appuser", "python3", "-m", "uvicorn", "app.main:app"]
```

### Frontend (Node.js 20 + Alpine 3.22)
```dockerfile
# Instalar gosu (mesmo processo)
RUN set -eux; \
    apk add --no-cache --virtual .gosu-fetch gnupg; \
    # ... instalação do gosu

# Executar como usuário não-root
CMD ["gosu", "nextjs", "npm", "run", "dev"]
```

## 🛡️ Camadas de Segurança

### 1. **Base Segura**
- Alpine 3.22 (menor superfície de ataque)
- Python 3.13 (última versão estável)
- Node.js 20-alpine (LTS + Alpine)

### 2. **Usuários Não-Root**
- Backend: `appuser` (UID 1000)
- Frontend: `nextjs` (UID 1001)
- Redis: `redis` (usuário interno)

### 3. **Verificação de Integridade**
- SHA256 checksums para gosu
- GPG signature verification
- Arquitetura específica

### 4. **Isolamento de Rede**
- Rede dedicada: `172.20.0.0/16`
- Portas específicas expostas
- Redis com autenticação

## 📊 Comparação de Segurança

| Aspecto | Sem gosu | Com gosu |
|---------|----------|----------|
| **Execução** | Root | Usuário não-root |
| **Vulnerabilidades** | Alto risco | Baixo risco |
| **Container Escape** | Possível | Improvável |
| **File Access** | Total | Restrito |
| **Process Privileges** | Elevados | Mínimos |

## 🚀 Como Usar

### 1. **Construir e Executar**
```bash
# Construir versões ultra-seguras
docker-compose -f docker-compose.gosu.yml build --no-cache

# Executar
docker-compose -f docker-compose.gosu.yml up -d
```

### 2. **Testar Segurança**
```bash
# Executar script de teste
./scripts/test-gosu.sh
```

### 3. **Verificar Processos**
```bash
# Verificar usuários dos processos
docker exec ngabi-backend-gosu ps aux
docker exec ngabi-frontend-gosu ps aux
```

## 🔍 Verificações de Segurança

### 1. **Health Check**
```bash
curl -f http://localhost:8000/health
```

### 2. **Verificar gosu**
```bash
docker exec ngabi-backend-gosu gosu --version
```

### 3. **Verificar Usuários**
```bash
docker exec ngabi-backend-gosu whoami
docker exec ngabi-frontend-gosu whoami
```

## 📈 Impacto no Desempenho

### Vantagens
- ✅ **Menor overhead** que su/sudo
- ✅ **Inicialização rápida**
- ✅ **Baixo uso de memória**
- ✅ **Compatível com Alpine**

### Desvantagens
- ⚠️ **Imagem ligeiramente maior** (~2.4MB)
- ⚠️ **Build time aumentado** (download + verificação)

## 🎯 Recomendações

### 1. **Para Produção**
- Use sempre versões com gosu
- Configure Redis com senha
- Monitore logs de segurança
- Atualize regularmente

### 2. **Para Desenvolvimento**
- Use versões com gosu para consistência
- Mantenha volumes para hot-reload
- Configure debug logs

### 3. **Para CI/CD**
- Teste versões com gosu
- Verifique vulnerabilidades
- Use multi-stage builds

## 🔗 Referências

- [gosu GitHub](https://github.com/tianon/gosu)
- [Docker Security Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Alpine Linux Security](https://alpinelinux.org/about/)
- [OWASP Container Security](https://owasp.org/www-project-container-security/)

## ✅ Conclusão

O gosu é uma ferramenta essencial para segurança em containers. No n.Gabi, ele garante que:

1. **Todos os processos** rodem como usuário não-root
2. **Vulnerabilidades** sejam minimizadas
3. **Conformidade** com padrões de segurança
4. **Compatibilidade** com múltiplas arquiteturas

A implementação com Alpine 3.22 + Python 3.13 + Node.js 20 + gosu representa o estado da arte em segurança para containers Docker. 