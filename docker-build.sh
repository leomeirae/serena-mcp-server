#!/bin/bash

# Script para build e execução do Docker para o Servidor MCP da Serena
# Uso: ./docker-build.sh [build|run|dev|stop|clean]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações
IMAGE_NAME="serena-mcp-server"
CONTAINER_NAME="serena-mcp-server"
TAG="latest"

# Função para imprimir mensagens coloridas
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Serena MCP Server Docker${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Função para verificar se o Docker está rodando
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker não está rodando. Inicie o Docker e tente novamente."
        exit 1
    fi
}

# Função para verificar se o arquivo .env existe
check_env_file() {
    if [ ! -f ".env" ]; then
        print_warning "Arquivo .env não encontrado!"
        print_message "Copiando env.example para .env..."
        cp env.example .env
        print_warning "Por favor, edite o arquivo .env com suas credenciais antes de continuar."
        exit 1
    fi
}

# Função para build da imagem
build_image() {
    print_header
    print_message "Construindo imagem Docker..."
    
    check_docker
    check_env_file
    
    docker build -t ${IMAGE_NAME}:${TAG} .
    
    print_message "Imagem construída com sucesso!"
    print_message "Tamanho da imagem:"
    docker images ${IMAGE_NAME}:${TAG} --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
}

# Função para executar o container
run_container() {
    print_header
    print_message "Executando container..."
    
    check_docker
    check_env_file
    
    # Parar container se estiver rodando
    if docker ps -q -f name=${CONTAINER_NAME} | grep -q .; then
        print_warning "Container já está rodando. Parando..."
        docker stop ${CONTAINER_NAME}
    fi
    
    # Remover container se existir
    if docker ps -aq -f name=${CONTAINER_NAME} | grep -q .; then
        print_warning "Removendo container existente..."
        docker rm ${CONTAINER_NAME}
    fi
    
    # Executar container
    docker run -d \
        --name ${CONTAINER_NAME} \
        --env-file .env \
        -p 8000:8000 \
        --restart unless-stopped \
        ${IMAGE_NAME}:${TAG}
    
    print_message "Container iniciado com sucesso!"
    print_message "Logs do container:"
    docker logs ${CONTAINER_NAME}
}

# Função para modo desenvolvimento
run_dev() {
    print_header
    print_message "Executando em modo desenvolvimento..."
    
    check_docker
    check_env_file
    
    # Usar docker-compose para desenvolvimento
    docker-compose --profile dev up -d serena-mcp-dev
    
    print_message "Container de desenvolvimento iniciado!"
    print_message "Logs do container:"
    docker-compose --profile dev logs -f serena-mcp-dev
}

# Função para parar containers
stop_containers() {
    print_header
    print_message "Parando containers..."
    
    # Parar container Docker
    if docker ps -q -f name=${CONTAINER_NAME} | grep -q .; then
        docker stop ${CONTAINER_NAME}
        print_message "Container ${CONTAINER_NAME} parado."
    else
        print_warning "Container ${CONTAINER_NAME} não está rodando."
    fi
    
    # Parar containers do docker-compose
    if docker-compose ps | grep -q "serena-mcp"; then
        docker-compose down
        print_message "Containers do docker-compose parados."
    fi
}

# Função para limpeza
clean_up() {
    print_header
    print_message "Limpando recursos Docker..."
    
    # Parar e remover containers
    stop_containers
    
    # Remover containers parados
    if docker ps -aq -f name=${CONTAINER_NAME} | grep -q .; then
        docker rm ${CONTAINER_NAME}
        print_message "Container ${CONTAINER_NAME} removido."
    fi
    
    # Remover imagem
    if docker images ${IMAGE_NAME}:${TAG} | grep -q ${IMAGE_NAME}; then
        docker rmi ${IMAGE_NAME}:${TAG}
        print_message "Imagem ${IMAGE_NAME}:${TAG} removida."
    fi
    
    # Limpar volumes não utilizados
    docker volume prune -f
    
    print_message "Limpeza concluída!"
}

# Função para mostrar logs
show_logs() {
    print_header
    print_message "Mostrando logs do container..."
    
    if docker ps -q -f name=${CONTAINER_NAME} | grep -q .; then
        docker logs -f ${CONTAINER_NAME}
    else
        print_error "Container ${CONTAINER_NAME} não está rodando."
    fi
}

# Função para mostrar status
show_status() {
    print_header
    print_message "Status dos containers:"
    
    echo -e "\n${BLUE}Containers Docker:${NC}"
    docker ps -a --filter name=${CONTAINER_NAME} --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    echo -e "\n${BLUE}Containers Docker Compose:${NC}"
    docker-compose ps
    
    echo -e "\n${BLUE}Imagens:${NC}"
    docker images ${IMAGE_NAME} --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
}

# Função para mostrar ajuda
show_help() {
    print_header
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  build   - Construir a imagem Docker"
    echo "  run     - Executar o container"
    echo "  dev     - Executar em modo desenvolvimento"
    echo "  stop    - Parar todos os containers"
    echo "  clean   - Limpar containers e imagens"
    echo "  logs    - Mostrar logs do container"
    echo "  status  - Mostrar status dos containers"
    echo "  help    - Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 build    # Construir imagem"
    echo "  $0 run      # Executar container"
    echo "  $0 dev      # Modo desenvolvimento"
    echo "  $0 stop     # Parar containers"
}

# Main script
case "${1:-help}" in
    build)
        build_image
        ;;
    run)
        run_container
        ;;
    dev)
        run_dev
        ;;
    stop)
        stop_containers
        ;;
    clean)
        clean_up
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Comando inválido: $1"
        show_help
        exit 1
        ;;
esac 