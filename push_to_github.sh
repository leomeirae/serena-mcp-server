#!/bin/bash

# Script para fazer push do repositório para o GitHub
# Uso: ./push_to_github.sh YOUR_USERNAME

if [ $# -eq 0 ]; then
    echo "❌ Erro: Você precisa fornecer seu username do GitHub"
    echo "Uso: ./push_to_github.sh YOUR_USERNAME"
    echo ""
    echo "Exemplo: ./push_to_github.sh joaosilva"
    exit 1
fi

USERNAME=$1

echo "🚀 Configurando repositório remoto para GitHub..."
echo "Username: $USERNAME"
echo ""

# Verificar se já existe um remote
if git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  Repositório remoto já configurado:"
    git remote -v
    echo ""
    read -p "Deseja sobrescrever? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Operação cancelada"
        exit 1
    fi
    git remote remove origin
fi

# Adicionar repositório remoto
echo "📡 Adicionando repositório remoto..."
git remote add origin https://github.com/$USERNAME/serena-mcp-server.git

# Verificar se foi adicionado corretamente
if [ $? -eq 0 ]; then
    echo "✅ Repositório remoto adicionado com sucesso!"
    git remote -v
else
    echo "❌ Erro ao adicionar repositório remoto"
    exit 1
fi

echo ""
echo "🔄 Configurando branch main..."
git branch -M main

echo ""
echo "📤 Fazendo push para o GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCESSO! Repositório enviado para o GitHub!"
    echo ""
    echo "📋 Próximos passos:"
    echo "1. Acesse: https://github.com/$USERNAME/serena-mcp-server"
    echo "2. Configure tópicos: mcp, model-context-protocol, api-server, python"
    echo "3. Ative GitHub Pages (opcional)"
    echo "4. Configure Actions para testes automáticos"
    echo ""
    echo "📚 Consulte o arquivo GITHUB_SETUP.md para instruções detalhadas"
else
    echo ""
    echo "❌ Erro ao fazer push"
    echo "Verifique se:"
    echo "1. O repositório foi criado no GitHub"
    echo "2. O username está correto"
    echo "3. Você tem permissão para fazer push"
    exit 1
fi 