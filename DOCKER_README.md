# 🐳 Docker para Servidor MCP da Serena

Este documento explica como executar o servidor MCP da Serena usando Docker.

## 📋 **Pré-requisitos**

- Docker instalado e rodando
- Docker Compose (opcional, para desenvolvimento)
- Arquivo `.env` configurado com suas credenciais

## 🚀 **Início Rápido**

### 1. **Configurar credenciais**
```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar com suas credenciais
nano .env
```

### 2. **Construir e executar**
```bash
# Usar script automatizado
./docker-build.sh build
./docker-build.sh run

# Ou usar comandos Docker diretamente
docker build -t serena-mcp-server .
docker run -d --name serena-mcp-server --env-file .env -p 8000:8000 serena-mcp-server
```

## 🛠️ **Métodos de Execução**

### **Método 1: Script Automatizado (Recomendado)**

O script `docker-build.sh` automatiza todo o processo:

```bash
# Construir imagem
./docker-build.sh build

# Executar container
./docker-build.sh run

# Modo desenvolvimento
./docker-build.sh dev

# Parar containers
./docker-build.sh stop

# Limpar tudo
./docker-build.sh clean

# Ver logs
./docker-build.sh logs

# Ver status
./docker-build.sh status
```

### **Método 2: Docker Compose**

```bash
# Executar em produção
docker-compose up -d

# Executar em desenvolvimento
docker-compose --profile dev up -d

# Parar
docker-compose down

# Ver logs
docker-compose logs -f
```

### **Método 3: Comandos Docker Diretos**

```bash
# Construir imagem
docker build -t serena-mcp-server .

# Executar container
docker run -d \
  --name serena-mcp-server \
  --env-file .env \
  -p 8000:8000 \
  --restart unless-stopped \
  serena-mcp-server

# Ver logs
docker logs -f serena-mcp-server

# Parar container
docker stop serena-mcp-server

# Remover container
docker rm serena-mcp-server
```

## 🔧 **Configuração**

### **Variáveis de Ambiente**

Crie um arquivo `.env` com suas credenciais:

```env
# Configuração da API de Parcerias
PARTNERSHIP_API_KEY=sua_chave_api_aqui
PARTNERSHIP_API_ENDPOINT=https://partnership-service-staging.api.srna.co/
```

### **Portas**

- **8000**: Porta padrão para debugging (se necessário)
- **8001**: Porta para desenvolvimento (docker-compose dev)

### **Volumes**

- `./logs:/app/logs`: Volume para logs (opcional)
- `./servidor_parcerias_mcp.py:/app/servidor_parcerias_mcp.py`: Volume para desenvolvimento

## 📊 **Otimizações da Imagem**

### **Características da Imagem**

- **Base**: `python:3.11-slim` (~45MB)
- **Usuário**: Não-root (`mcpuser`) para segurança
- **Cache**: Otimizado para dependências Python
- **Health Check**: Verificação automática de saúde
- **Labels**: Metadados para documentação

### **Tamanho Estimado**

```
python:3.11-slim     ~45MB
+ dependências       ~15MB
+ código             ~1MB
= Total              ~61MB
```

## 🔍 **Monitoramento**

### **Health Check**

O container inclui health check automático:

```bash
# Verificar saúde
docker inspect serena-mcp-server | grep Health -A 10

# Ver logs de health check
docker logs serena-mcp-server 2>&1 | grep health
```

### **Logs**

```bash
# Logs em tempo real
docker logs -f serena-mcp-server

# Logs com timestamp
docker logs -t serena-mcp-server

# Últimas 100 linhas
docker logs --tail 100 serena-mcp-server
```

## 🐛 **Troubleshooting**

### **Problemas Comuns**

#### 1. **Container não inicia**
```bash
# Verificar logs
docker logs serena-mcp-server

# Verificar se .env existe
ls -la .env

# Verificar variáveis de ambiente
docker exec serena-mcp-server env | grep PARTNERSHIP
```

#### 2. **Erro de permissão**
```bash
# Verificar permissões do .env
chmod 600 .env

# Verificar usuário do container
docker exec serena-mcp-server whoami
```

#### 3. **Problemas de rede**
```bash
# Verificar conectividade
docker exec serena-mcp-server curl -I https://partnership-service-staging.api.srna.co

# Verificar DNS
docker exec serena-mcp-server nslookup partnership-service-staging.api.srna.co
```

### **Comandos de Debug**

```bash
# Entrar no container
docker exec -it serena-mcp-server /bin/bash

# Verificar processos
docker exec serena-mcp-server ps aux

# Verificar arquivos
docker exec serena-mcp-server ls -la /app

# Testar Python
docker exec serena-mcp-server python -c "import mcp; print('MCP OK')"
```

## 🔒 **Segurança**

### **Boas Práticas Implementadas**

- ✅ Usuário não-root (`mcpuser`)
- ✅ Arquivo `.env` no `.dockerignore`
- ✅ Health check para monitoramento
- ✅ Restart policy configurada
- ✅ Volumes somente leitura quando possível

### **Recomendações Adicionais**

```bash
# Usar secrets do Docker (produção)
echo "sua_chave_api" | docker secret create partnership_api_key -

# Usar rede customizada
docker network create mcp-network

# Executar com recursos limitados
docker run --memory=512m --cpus=1 serena-mcp-server
```

## 📈 **Produção**

### **Deploy em Produção**

```bash
# Build para produção
docker build -t serena-mcp-server:prod .

# Executar com restart automático
docker run -d \
  --name serena-mcp-server-prod \
  --env-file .env.prod \
  --restart always \
  --memory=1g \
  --cpus=2 \
  serena-mcp-server:prod
```

### **Monitoramento**

```bash
# Verificar recursos
docker stats serena-mcp-server

# Verificar logs
docker logs --tail 1000 serena-mcp-server | grep ERROR

# Backup de configuração
docker cp serena-mcp-server:/app/.env ./backup.env
```

## 🔄 **Atualizações**

### **Atualizar Imagem**

```bash
# Parar container
./docker-build.sh stop

# Rebuild
./docker-build.sh build

# Executar nova versão
./docker-build.sh run
```

### **Rollback**

```bash
# Voltar para versão anterior
docker tag serena-mcp-server:previous serena-mcp-server:latest
./docker-build.sh run
```

## 📚 **Comandos Úteis**

```bash
# Ver todas as imagens
docker images serena-mcp-server

# Ver containers
docker ps -a --filter name=serena-mcp

# Limpar recursos não utilizados
docker system prune -f

# Ver uso de disco
docker system df

# Exportar imagem
docker save serena-mcp-server:latest | gzip > serena-mcp-server.tar.gz

# Importar imagem
docker load < serena-mcp-server.tar.gz
```

## 🆘 **Suporte**

Se encontrar problemas:

1. Verifique os logs: `./docker-build.sh logs`
2. Verifique o status: `./docker-build.sh status`
3. Teste a conectividade: `docker exec serena-mcp-server curl -I https://partnership-service-staging.api.srna.co`
4. Verifique as variáveis de ambiente: `docker exec serena-mcp-server env`

---

**🎉 Agora você pode executar o servidor MCP da Serena em qualquer ambiente com Docker!** 