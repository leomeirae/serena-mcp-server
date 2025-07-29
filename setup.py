#!/usr/bin/env python3
"""
Script de configuração para o servidor MCP de parcerias.
Este script ajuda a configurar o ambiente e testar a conexão.
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Imprime o banner do projeto."""
    print("=" * 60)
    print("🚀 Configuração do Servidor MCP para API de Parcerias")
    print("=" * 60)

def check_python_version():
    """Verifica se a versão do Python é compatível."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 ou superior é necessário!")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def create_virtual_environment():
    """Cria um ambiente virtual Python."""
    if os.path.exists("mcp_env"):
        print("✅ Ambiente virtual já existe")
        return True
    
    print("📦 Criando ambiente virtual...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "mcp_env"], check=True)
        print("✅ Ambiente virtual criado com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao criar ambiente virtual")
        return False

def install_dependencies():
    """Instala as dependências do projeto."""
    print("📦 Instalando dependências...")
    
    # Determina o comando pip correto baseado no sistema operacional
    if platform.system() == "Windows":
        pip_cmd = "mcp_env\\Scripts\\pip"
    else:
        pip_cmd = "mcp_env/bin/pip"
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False

def setup_environment_variable():
    """Configura a variável de ambiente."""
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImQzNDBmZWEyLWM3ZTQtNGY1Ni1hYjdlLTAyMmE5ZDcwNTBiNiIsInBhcnRuZXJUeXBlIjoicGFydG5lcl9ncm91cCIsImlhdCI6MTc0NDgzNzEzOX0.YvvCD-I4GOSPmRduMoXit8Rw05c9ILoiCjhnPMgygO0"
    
    print("🔑 Configurando variável de ambiente...")
    
    if platform.system() == "Windows":
        # Windows
        os.environ["PARTNERSHIP_API_KEY"] = api_key
        print("✅ Variável de ambiente configurada para esta sessão")
        print("💡 Para configurar permanentemente, execute:")
        print(f'   setx PARTNERSHIP_API_KEY "{api_key}"')
    else:
        # Linux/macOS
        os.environ["PARTNERSHIP_API_KEY"] = api_key
        print("✅ Variável de ambiente configurada para esta sessão")
        print("💡 Para configurar permanentemente, adicione ao seu ~/.bashrc ou ~/.zshrc:")
        print(f'   export PARTNERSHIP_API_KEY="{api_key}"')
    
    return True

def run_tests():
    """Executa os testes do servidor."""
    print("🧪 Executando testes...")
    
    # Determina o comando python correto baseado no sistema operacional
    if platform.system() == "Windows":
        python_cmd = "mcp_env\\Scripts\\python"
    else:
        python_cmd = "mcp_env/bin/python"
    
    try:
        result = subprocess.run([python_cmd, "test_server.py"], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        print("❌ Erro ao executar testes")
        return False

def print_next_steps():
    """Imprime os próximos passos para o usuário."""
    print("\n" + "=" * 60)
    print("🎉 Configuração concluída!")
    print("=" * 60)
    print("\n📋 Próximos passos:")
    print("1. Para executar o servidor:")
    if platform.system() == "Windows":
        print("   mcp_env\\Scripts\\python servidor_parcerias_mcp.py")
    else:
        print("   mcp_env/bin/python servidor_parcerias_mcp.py")
    
    print("\n2. Para conectar a um cliente MCP (ex: Claude Desktop):")
    print("   - Nome: API de Parcerias")
    print("   - Comando: python")
    print("   - Argumentos: servidor_parcerias_mcp.py")
    print("   - Diretório: " + os.getcwd())
    
    print("\n3. Para mais informações, consulte o README.md")
    print("\n" + "=" * 60)

def main():
    """Função principal de configuração."""
    print_banner()
    
    # Verifica versão do Python
    if not check_python_version():
        return False
    
    print()
    
    # Cria ambiente virtual
    if not create_virtual_environment():
        return False
    
    # Instala dependências
    if not install_dependencies():
        return False
    
    # Configura variável de ambiente
    if not setup_environment_variable():
        return False
    
    # Executa testes
    if not run_tests():
        print("⚠️ Testes falharam, mas a configuração básica foi concluída")
    
    print_next_steps()
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 