#!/usr/bin/env python3
"""
Script de teste para verificar se o servidor MCP está funcionando corretamente.
Este script testa a importação e verifica se as ferramentas estão registradas.
"""

import os
import sys
import asyncio
from servidor_parcerias_mcp import server

def test_server_import():
    """Testa se o servidor pode ser importado corretamente."""
    print("✅ Servidor importado com sucesso!")
    print(f"📋 Nome do servidor: {server.name}")
    print(f"📋 Instruções: {server.instructions}")
    return True

def test_tools_registration():
    """Testa se as ferramentas estão registradas corretamente."""
    print(f"\n🔧 Testando ferramentas...")
    
    expected_tools = [
        "consultar_areas_operacao_gd",
        "obter_planos_gd", 
        "cadastrar_lead",
        "buscar_leads",
        "validar_qualificacao_lead",
        "buscar_lead_por_id",
        "atualizar_lead",
        "atualizar_credenciais_distribuidora",
        "criar_contrato"
    ]
    
    # Para FastMCP, vamos verificar se as ferramentas foram registradas
    # no tool manager
    registered_tools = list(server._tool_manager._tools.keys())
    
    for tool_name in expected_tools:
        if tool_name in registered_tools:
            print(f"  ✅ {tool_name}")
        else:
            print(f"  ❌ {tool_name} (não encontrado)")
            return False
    
    return True

def test_environment():
    """Testa se a variável de ambiente está configurada."""
    api_key = os.getenv("PARTNERSHIP_API_KEY")
    if api_key:
        print(f"\n🔑 API Key configurada: {api_key[:20]}...")
        return True
    else:
        print("\n❌ API Key não configurada!")
        print("Configure a variável de ambiente PARTNERSHIP_API_KEY")
        return False

async def test_api_connection():
    """Testa a conexão com a API."""
    try:
        from servidor_parcerias_mcp import API_BASE_URL, get_auth_headers
        import httpx
        
        print(f"\n🌐 Testando conexão com: {API_BASE_URL}")
        
        async with httpx.AsyncClient() as client:
            # Testa um endpoint simples para verificar se a API está acessível
            response = await client.get(
                f"{API_BASE_URL}/distribuited-generation/operation-areas",
                params={"city": "São Paulo", "state": "SP"},
                headers=get_auth_headers(),
                timeout=10.0
            )
            
            if response.status_code == 200:
                print("✅ Conexão com a API estabelecida com sucesso!")
                return True
            else:
                print(f"⚠️ API retornou status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Erro ao conectar com a API: {e}")
        return False

def main():
    """Função principal de teste."""
    print("🧪 Iniciando testes do servidor MCP...\n")
    
    # Teste 1: Importação
    if not test_server_import():
        print("❌ Falha no teste de importação")
        return False
    
    # Teste 2: Registro de ferramentas
    if not test_tools_registration():
        print("❌ Falha no teste de registro de ferramentas")
        return False
    
    # Teste 3: Variável de ambiente
    if not test_environment():
        print("❌ Falha no teste de ambiente")
        return False
    
    # Teste 4: Conexão com API (opcional)
    print("\n🌐 Testando conexão com a API...")
    try:
        api_ok = asyncio.run(test_api_connection())
        if api_ok:
            print("✅ Todos os testes passaram!")
        else:
            print("⚠️ Testes básicos passaram, mas há problemas com a API")
    except Exception as e:
        print(f"⚠️ Não foi possível testar a API: {e}")
        print("✅ Testes básicos passaram!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 