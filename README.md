# Servidor MCP para API de Parcerias

Este é um servidor MCP (Model Context Protocol) que permite que assistentes de IA interajam com a API de Parcerias da Serena através de ferramentas estruturadas.

## Funcionalidades

O servidor MCP oferece as seguintes ferramentas:

### Geração Distribuída (Distributed Generation)
- **consultar_areas_operacao_gd**: Consulta áreas onde o serviço de GD está disponível
- **obter_planos_gd**: Obtém planos de GD disponíveis para uma localidade

### Conversão de Vendas (Sales Conversion)
- **cadastrar_lead**: Cadastra um novo lead na base de dados
- **buscar_leads**: Busca leads com filtros e paginação
- **validar_qualificacao_lead**: Valida se um lead está qualificado para produtos
- **buscar_lead_por_id**: Busca informações de um lead específico
- **atualizar_lead**: Atualiza informações de um lead
- **atualizar_credenciais_distribuidora**: Atualiza credenciais de acesso à distribuidora
- **criar_contrato**: Cria um contrato de geração distribuída

## Instalação

1. **Clone ou baixe este repositório**

2. **Crie um ambiente virtual Python:**
   ```bash
   python -m venv mcp_env
   source mcp_env/bin/activate  # No Windows: mcp_env\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as credenciais no arquivo .env:**
   
   O arquivo `.env` já está configurado com as credenciais necessárias:
   ```
   PARTNERSHIP_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImQzNDBmZWEyLWM3ZTQtNGY1Ni1hYjdlLTAyMmE5ZDcwNTBiNiIsInBhcnRuZXJUeXBlIjoicGFydG5lcl9ncm91cCIsImlhdCI6MTc0NDgzNzEzOX0.YvvCD-I4GOSPmRduMoXit8Rw05c9ILoiCjhnPMgygO0
   PARTNERSHIP_API_ENDPOINT=https://partnership-service-staging.api.srna.co/
   ```

## Uso

### Executando o Servidor

```bash
python servidor_parcerias_mcp.py
```

O servidor será iniciado e aguardará conexões via stdio.

### Conectando a um Cliente MCP

Para conectar este servidor a um cliente MCP (como Claude Desktop, Ollama, etc.), você precisará configurar o cliente para usar este servidor local.

#### Exemplo de configuração para Claude Desktop:

1. Abra as configurações do Claude Desktop
2. Vá para a seção de servidores MCP
3. Adicione um novo servidor com as seguintes configurações:
   - **Nome**: API de Parcerias
   - **Comando**: `python`
   - **Argumentos**: `servidor_parcerias_mcp.py`
   - **Diretório de trabalho**: Caminho para este projeto

## Exemplos de Uso

### Consultando Áreas de Operação

```python
# Consultar por cidade e estado
resultado = await consultar_areas_operacao_gd(
    cidade="São Paulo", 
    estado="SP"
)

# Consultar por código IBGE
resultado = await consultar_areas_operacao_gd(
    codigo_ibge="3550308"
)
```

### Cadastrando um Lead

```python
dados_lead = {
    "fullName": "João Silva",
    "personType": "natural",
    "emailAddress": "joao@email.com",
    "mobilePhone": "11999885544",
    "utilityBillingValue": 500.00,
    "identificationNumber": "12345678901",
    "nationality": "Brasileiro",
    "maritalStatus": "Solteiro",
    "profession": "Engenheiro",
    "zipCode": "01234-567",
    "state": "SP",
    "city": "São Paulo",
    "street": "Rua das Flores",
    "number": "123",
    "neighborhood": "Centro",
    "complement": "Apto 45"
}

resultado = await cadastrar_lead(dados_lead)
```

### Validando Qualificação de Lead

```python
resultado = await validar_qualificacao_lead(
    cidade="São Paulo",
    estado="SP",
    tipo_pessoa="natural",
    valor_conta=500.00
)
```

## Estrutura da API

### Endpoint Base
- **URL**: `https://partnership-service-staging.api.srna.co/`
- **Autenticação**: Bearer Token

### Principais Endpoints Mapeados

1. **GET /distribuited-generation/operation-areas** → `consultar_areas_operacao_gd`
2. **GET /distribuited-generation/plans** → `obter_planos_gd`
3. **POST /sales-conversion/leads** → `cadastrar_lead`
4. **GET /sales-conversion/leads** → `buscar_leads`
5. **GET /sales-conversion/leads/qualification** → `validar_qualificacao_lead`
6. **GET /sales-conversion/leads/{id}** → `buscar_lead_por_id`
7. **PUT /sales-conversion/leads/{id}** → `atualizar_lead`
8. **PATCH /sales-conversion/leads/{id}/energy-utility-credentials** → `atualizar_credenciais_distribuidora`
9. **POST /sales-conversion/leads/{id}/contracts** → `criar_contrato`

## Tratamento de Erros

O servidor inclui tratamento básico de erros HTTP. Em caso de falha na API, o erro será propagado com informações sobre o que deu errado.

## Segurança

- A chave de API é carregada de uma variável de ambiente para evitar exposição acidental
- Todas as requisições incluem autenticação Bearer Token
- Não armazene a chave de API no código fonte

## Suporte

Para dúvidas ou problemas, consulte a documentação da API em `api-documentation.md` ou entre em contato com a equipe de desenvolvimento. 