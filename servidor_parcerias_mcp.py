# servidor_parcerias_mcp.py
import os
import httpx
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Carregue sua chave de API de variáveis de ambiente (prioridade) ou arquivo .env
API_KEY = os.getenv("PARTNERSHIP_API_KEY")
API_BASE_URL = os.getenv("PARTNERSHIP_API_ENDPOINT", "https://partnership-service-staging.api.srna.co").rstrip('/')

print(f"DEBUG: API_KEY from env: {'SET' if API_KEY else 'NOT SET'}")
print(f"DEBUG: API_BASE_URL from env: {API_BASE_URL}")

# Se não encontrou nas variáveis de ambiente, tenta carregar do .env
if not API_KEY:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        API_KEY = os.getenv("PARTNERSHIP_API_KEY")
        if not API_BASE_URL or API_BASE_URL == "https://partnership-service-staging.api.srna.co":
            API_BASE_URL = os.getenv("PARTNERSHIP_API_ENDPOINT", "https://partnership-service-staging.api.srna.co").rstrip('/')
        print(f"DEBUG: After .env load - API_KEY: {'SET' if API_KEY else 'NOT SET'}")
    except ImportError:
        print("DEBUG: dotenv not available")
        pass

# Fallback hardcoded para Coolify (REMOVER EM PRODUÇÃO)
if not API_KEY:
    print("DEBUG: Using hardcoded fallback for Coolify")
    API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImQzNDBmZWEyLWM3ZTQtNGY1Ni1hYjdlLTAyMmE5ZDcwNTBiNiIsInBhcnRuZXJUeXBlIjoicGFydG5lcl9ncm91cCIsImlhdCI6MTc0NDgzNzEzOX0.YvvCD-I4GOSPmRduMoXit8Rw05c9ILoiCjhnPMgygO0"
    API_BASE_URL = "https://partnership-service-staging.api.srna.co"

print(f"DEBUG: Final API_KEY: {'SET' if API_KEY else 'NOT SET'}")
print(f"DEBUG: Final API_BASE_URL: {API_BASE_URL}")

# Função auxiliar para criar os cabeçalhos de autenticação
def get_auth_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

# Configuração do servidor
SERVER_NAME = "servidor_api_parcerias"
SERVER_INSTRUCTIONS = "Servidor para API de Parcerias da Serena"

# --- Ferramentas de Geração Distribuída ---

async def consultar_areas_operacao_gd(cidade: Optional[str] = None, estado: Optional[str] = None, codigo_ibge: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retorna uma lista de áreas onde o serviço de Geração Distribuída (GD) está disponível.
    A consulta pode ser feita por estado e cidade OU pelo código IBGE do município.
    
    Args:
        cidade: Nome da cidade a ser consultada. Deve ser fornecido junto com o estado. Ex: "São Paulo".
        estado: Sigla do estado (UF). Deve ser fornecido junto com a cidade. Ex: "SP".
        codigo_ibge: Código IBGE do município. Pode ser usado como alternativa a cidade/estado. Ex: "3550308".
        
    Returns:
        Uma lista de dicionários, cada um representando uma área de operação com dados da distribuidora.
    """
    params = {}
    if cidade and estado:
        params['city'] = cidade
        params['state'] = estado
    elif codigo_ibge:
        params['ibge_code'] = codigo_ibge
    else:
        return {"error": "Forneça 'cidade' e 'estado' ou 'codigo_ibge'."}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/distribuited-generation/operation-areas",
            params=params,
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()

async def obter_planos_gd(id_distribuidora: Optional[str] = None, cidade: Optional[str] = None, estado: Optional[str] = None) -> Dict[str, Any]:
    """
    Retorna os planos de Geração Distribuída (GD) disponíveis para uma localidade.
    A busca pode ser por ID da distribuidora ou pela combinação de cidade e estado.
    Se o ID da distribuidora for informado, ele terá prioridade.

    Args:
        id_distribuidora: O ID público da distribuidora (UUID). Pode ser obtido pela ferramenta 'consultar_areas_operacao_gd'.
        cidade: Nome da cidade a ser consultada. Ex: "São Paulo".
        estado: Sigla do estado (UF). Ex: "SP".
        
    Returns:
        Um dicionário contendo o nome da distribuidora e a lista de planos.
    """
    params = {}
    if id_distribuidora:
        params['energy_utility_public_id'] = id_distribuidora
    elif cidade and estado:
        params['city'] = cidade
        params['state'] = estado
    else:
        return {"error": "Forneça 'id_distribuidora' ou a combinação 'cidade' e 'estado'."}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/distribuited-generation/plans",
            params=params,
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()

# --- Ferramentas de Conversão de Vendas (Leads) ---

async def cadastrar_lead(dados_lead: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cadastra um novo lead na base de dados.
    O campo 'companyName' é obrigatório para pessoa jurídica ('juridical').
    O campo 'personType' deve ser 'natural' (pessoa física) ou 'juridical' (pessoa jurídica).

    Args:
        dados_lead: Um dicionário contendo todos os dados do lead, conforme a documentação. Veja o schema CreateLeadDTO.
        
    Returns:
        A resposta da API após o cadastro do lead.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/sales-conversion/leads",
            json=dados_lead,
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json() if response.status_code != 204 else {"status": "success", "statusCode": 204}

async def buscar_leads(filtros: Optional[str] = None, pagina: int = 1, limite: int = 10) -> Dict[str, Any]:
    """
    Busca uma lista de leads com base em filtros fornecidos.
    
    Args:
        filtros: String com filtros para a busca. 
                 Ex: 'customer:18.928.199/0001-88,seller_name:John Cena,status:negociacao'.
                 Status válidos: negociacao, indicado, desqualificado, assinado.
        pagina: O número da página para a paginação.
        limite: O número de resultados por página.
        
    Returns:
        Um dicionário com a lista de leads e o total de resultados.
    """
    params = {'page': pagina, 'limit': limite}
    if filtros:
        params['filters'] = filtros

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/sales-conversion/leads",
            params=params,
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()

async def validar_qualificacao_lead(cidade: str, estado: str, tipo_pessoa: str, valor_conta: float) -> Dict[str, Any]:
    """
    Valida se um lead está qualificado para o produto de geração distribuída ou mercado livre.

    Args:
        cidade: Nome da cidade para a consulta.
        estado: Sigla do estado (UF).
        tipo_pessoa: Categoria da pessoa, 'natural' para física ou 'juridical' para jurídica.
        valor_conta: O valor mensal da conta de luz do lead.
        
    Returns:
        Um dicionário indicando o produto e se o lead está qualificado.
    """
    params = {
        'city': cidade,
        'state': estado,
        'personType': tipo_pessoa,
        'utilityBillingValue': valor_conta
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/sales-conversion/leads/qualification",
            params=params,
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()
        
async def buscar_lead_por_id(id_lead: str) -> Dict[str, Any]:
    """
    Busca as informações de um lead específico cadastrado, baseado no seu ID.

    Args:
        id_lead: O ID do lead a ser buscado.
        
    Returns:
        Um dicionário com todos os dados do lead.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_BASE_URL}/sales-conversion/leads/{id_lead}",
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()

async def atualizar_lead(id_lead: str, dados_atualizacao: Dict[str, Any]) -> Dict[str, Any]:
    """
    Atualiza as informações do lead de acordo com os dados enviados.
    O campo "personType" deve conter "juridical" caso seja pessoa jurídica e "natural" quando pessoa física.
    O campo "companyName" é obrigatório apenas para lead do tipo pessoa jurídica.

    Args:
        id_lead: O ID do lead a ser atualizado.
        dados_atualizacao: Dicionário com os dados a serem atualizados.
        
    Returns:
        A resposta da API após a atualização do lead.
    """
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{API_BASE_URL}/sales-conversion/leads/{id_lead}",
            json=dados_atualizacao,
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json() if response.status_code != 204 else {"status": "success", "statusCode": 204}

async def atualizar_credenciais_distribuidora(id_lead: str, login: str, senha: str) -> Dict[str, Any]:
    """
    Adicionar ou atualizar o login e a senha da distribuidora.
    Atualiza ou adiciona dados das credenciais de acesso ao site da distribuidora.

    Args:
        id_lead: O ID do lead.
        login: Login da distribuidora.
        senha: Senha da distribuidora.
        
    Returns:
        A resposta da API após a atualização das credenciais.
    """
    dados_credenciais = {
        "utilityBillLogin": login,
        "password": senha
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{API_BASE_URL}/sales-conversion/leads/{id_lead}/energy-utility-credentials",
            json=dados_credenciais,
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json() if response.status_code != 204 else {"status": "success", "statusCode": 204}

async def criar_contrato(id_lead: str, plano: Optional[Dict[str, Any]] = None, representantes_legais: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Cria um contrato de geração distribuída associado a um lead.
    O envio do objeto "plan" é necessário somente se o plano não tiver sido informado previamente no cadastro do lead.
    O envio do array de objetos "legalRepresentatives" é obrigatório e permitido apenas se o lead for uma pessoa jurídica.

    Args:
        id_lead: O ID do lead.
        plano: Dicionário com os dados do plano (opcional se já informado no cadastro).
        representantes_legais: Lista de representantes legais (obrigatório para pessoa jurídica).
        
    Returns:
        A resposta da API após a criação do contrato.
    """
    dados_contrato = {}
    
    if plano:
        dados_contrato["plan"] = plano
    
    if representantes_legais:
        dados_contrato["legalRepresentatives"] = representantes_legais
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/sales-conversion/leads/{id_lead}/contracts",
            json=dados_contrato,
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json() if response.status_code != 204 else {"status": "success", "statusCode": 204}

# Código para executar o servidor
if __name__ == "__main__":
    try:
        print("Iniciando o Servidor MCP para a API de Parcerias...")
        print(f"DEBUG: Server name: {SERVER_NAME}")
        print(f"DEBUG: Server instructions: {SERVER_INSTRUCTIONS}")
        
        # Verificar se há conexão stdio disponível
        import sys
        print(f"DEBUG: stdin: {sys.stdin}")
        print(f"DEBUG: stdout: {sys.stdout}")
        print(f"DEBUG: stderr: {sys.stderr}")
        
        # Criar servidor HTTP simples para expor as ferramentas
        from fastapi import FastAPI, HTTPException
        import uvicorn
        import json
        from typing import Dict, Any
        
        app = FastAPI(title="Serena MCP Server", version="1.0.0")
        
        @app.get("/")
        async def root():
            return {
                "message": "Serena MCP Server",
                "version": "1.0.0",
                "tools": ["consultar_areas_operacao_gd", "obter_planos_gd", "cadastrar_lead", "buscar_leads", "validar_qualificacao_lead", "buscar_lead_por_id", "atualizar_lead", "atualizar_credenciais_distribuidora", "criar_contrato"]
            }
        
        @app.get("/health")
        async def health():
            return {"status": "healthy", "api_key": "SET" if API_KEY else "NOT SET"}
        
        @app.get("/tools")
        async def list_tools():
            return {"tools": ["consultar_areas_operacao_gd", "obter_planos_gd", "cadastrar_lead", "buscar_leads", "validar_qualificacao_lead", "buscar_lead_por_id", "atualizar_lead", "atualizar_credenciais_distribuidora", "criar_contrato"]}
        
        @app.post("/tools/{tool_name}")
        async def execute_tool(tool_name: str, params: Dict[str, Any] = None):
            # Mapeamento direto das ferramentas para funções
            tool_functions = {
                "consultar_areas_operacao_gd": consultar_areas_operacao_gd,
                "obter_planos_gd": obter_planos_gd,
                "cadastrar_lead": cadastrar_lead,
                "buscar_leads": buscar_leads,
                "validar_qualificacao_lead": validar_qualificacao_lead,
                "buscar_lead_por_id": buscar_lead_por_id,
                "atualizar_lead": atualizar_lead,
                "atualizar_credenciais_distribuidora": atualizar_credenciais_distribuidora,
                "criar_contrato": criar_contrato
            }
            
            if tool_name not in tool_functions:
                raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
            
            try:
                func = tool_functions[tool_name]
                result = await func(**(params or {}))
                return {"result": result}
            except Exception as e:
                print(f"DEBUG: Error executing tool {tool_name}: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        print("DEBUG: Starting HTTP server on port 54321...")
        uvicorn.run(app, host="0.0.0.0", port=54321)
        
    except Exception as e:
        print(f"ERROR: Failed to start server: {e}")
        print(f"ERROR: Exception type: {type(e)}")
        import traceback
        print(f"ERROR: Traceback: {traceback.format_exc()}")
        
        # Em vez de falhar, manter o container rodando
        print("DEBUG: Keeping container alive for debugging...")
        import time
        while True:
            time.sleep(10)
            print("DEBUG: Container still alive...") 