# Servidor MCP para API de Parcerias Serena

## 📋 Visão Geral

Este é um servidor MCP (Model Context Protocol) que permite que assistentes de IA interajam com a API de Parcerias da Serena através de ferramentas estruturadas. O servidor está disponível no endpoint: **http://mwc8k8wk0wg8o8s4k0w8scc4.157.180.32.249.sslip.io/**

### 🎯 Objetivo
Fornecer uma interface padronizada para que agentes de IA possam:
- Consultar áreas de operação para Geração Distribuída (GD)
- Gerenciar leads de vendas
- Validar qualificação de clientes
- Criar contratos de energia solar
- Interagir com a API de Parcerias da Serena de forma estruturada

## 🛠️ Ferramentas Disponíveis

### 📍 Geração Distribuída (Distributed Generation)

#### 1. `consultar_areas_operacao_gd`
**Descrição**: Consulta áreas onde o serviço de Geração Distribuída está disponível

**Parâmetros**:
- `cidade` (string, opcional): Nome da cidade
- `estado` (string, opcional): Sigla do estado (ex: SP, RJ)
- `codigo_ibge` (string, opcional): Código IBGE da localidade

**Retorno**: Lista de áreas de operação disponíveis com informações de cobertura

**Exemplo de uso**:
```python
# Por cidade e estado
resultado = await consultar_areas_operacao_gd(
    cidade="São Paulo", 
    estado="SP"
)

# Por código IBGE
resultado = await consultar_areas_operacao_gd(
    codigo_ibge="3550308"
)
```

#### 2. `obter_planos_gd`
**Descrição**: Obtém planos de Geração Distribuída disponíveis para uma localidade

**Parâmetros**:
- `cidade` (string, obrigatório): Nome da cidade
- `estado` (string, obrigatório): Sigla do estado

**Retorno**: Lista de planos disponíveis com detalhes de potência, preços e condições

**Exemplo de uso**:
```python
resultado = await obter_planos_gd(
    cidade="São Paulo",
    estado="SP"
)
```

### 💼 Conversão de Vendas (Sales Conversion)

#### 3. `cadastrar_lead`
**Descrição**: Cadastra um novo lead na base de dados

**Parâmetros**:
- `fullName` (string, obrigatório): Nome completo
- `personType` (string, obrigatório): Tipo de pessoa ("natural" ou "legal")
- `emailAddress` (string, obrigatório): Email
- `mobilePhone` (string, obrigatório): Telefone celular
- `utilityBillingValue` (number, obrigatório): Valor da conta de energia
- `identificationNumber` (string, obrigatório): CPF/CNPJ
- `nationality` (string, obrigatório): Nacionalidade
- `maritalStatus` (string, obrigatório): Estado civil
- `profession` (string, obrigatório): Profissão
- `zipCode` (string, obrigatório): CEP
- `state` (string, obrigatório): Estado
- `city` (string, obrigatório): Cidade
- `street` (string, obrigatório): Rua
- `number` (string, obrigatório): Número
- `neighborhood` (string, obrigatório): Bairro
- `complement` (string, opcional): Complemento

**Retorno**: ID do lead criado e status da operação

**Exemplo de uso**:
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

#### 4. `buscar_leads`
**Descrição**: Busca leads com filtros e paginação

**Parâmetros**:
- `page` (number, opcional): Número da página (padrão: 1)
- `limit` (number, opcional): Limite de resultados por página (padrão: 10)
- `search` (string, opcional): Termo de busca
- `status` (string, opcional): Status do lead
- `personType` (string, opcional): Tipo de pessoa

**Retorno**: Lista paginada de leads com informações básicas

**Exemplo de uso**:
```python
resultado = await buscar_leads(
    page=1,
    limit=20,
    search="João Silva",
    status="active"
)
```

#### 5. `validar_qualificacao_lead`
**Descrição**: Valida se um lead está qualificado para produtos de energia solar

**Parâmetros**:
- `cidade` (string, obrigatório): Cidade do lead
- `estado` (string, obrigatório): Estado do lead
- `tipo_pessoa` (string, obrigatório): "natural" ou "legal"
- `valor_conta` (number, obrigatório): Valor da conta de energia

**Retorno**: Resultado da validação com detalhes de qualificação

**Exemplo de uso**:
```python
resultado = await validar_qualificacao_lead(
    cidade="São Paulo",
    estado="SP",
    tipo_pessoa="natural",
    valor_conta=500.00
)
```

#### 6. `buscar_lead_por_id`
**Descrição**: Busca informações detalhadas de um lead específico

**Parâmetros**:
- `lead_id` (string, obrigatório): ID único do lead

**Retorno**: Informações completas do lead incluindo histórico e status

**Exemplo de uso**:
```python
resultado = await buscar_lead_por_id("lead_123456")
```

#### 7. `atualizar_lead`
**Descrição**: Atualiza informações de um lead existente

**Parâmetros**:
- `lead_id` (string, obrigatório): ID do lead
- `dados_atualizacao` (object, obrigatório): Dados a serem atualizados

**Retorno**: Confirmação da atualização

**Exemplo de uso**:
```python
dados_atualizacao = {
    "emailAddress": "novo_email@email.com",
    "mobilePhone": "11988776655"
}

resultado = await atualizar_lead("lead_123456", dados_atualizacao)
```

#### 8. `atualizar_credenciais_distribuidora`
**Descrição**: Atualiza credenciais de acesso à distribuidora de energia

**Parâmetros**:
- `lead_id` (string, obrigatório): ID do lead
- `credenciais` (object, obrigatório): Credenciais da distribuidora

**Retorno**: Confirmação da atualização das credenciais

**Exemplo de uso**:
```python
credenciais = {
    "username": "usuario_distribuidora",
    "password": "senha_distribuidora"
}

resultado = await atualizar_credenciais_distribuidora("lead_123456", credenciais)
```

#### 9. `criar_contrato`
**Descrição**: Cria um contrato de geração distribuída para um lead

**Parâmetros**:
- `lead_id` (string, obrigatório): ID do lead
- `dados_contrato` (object, obrigatório): Dados do contrato

**Retorno**: ID do contrato criado e status

**Exemplo de uso**:
```python
dados_contrato = {
    "planId": "plan_123",
    "installationAddress": {
        "zipCode": "01234-567",
        "state": "SP",
        "city": "São Paulo",
        "street": "Rua das Flores",
        "number": "123",
        "neighborhood": "Centro"
    }
}

resultado = await criar_contrato("lead_123456", dados_contrato)
```

## 🔧 Configuração para Agentes de IA

### Configuração MCP

Para configurar este servidor MCP em um agente de IA, adicione a seguinte configuração:

```json
{
  "mcpServers": {
    "serena-partnerships": {
      "command": "python",
      "args": ["servidor_parcerias_mcp.py"],
      "env": {
        "PARTNERSHIP_API_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImQzNDBmZWEyLWM3ZTQtNGY1Ni1hYjdlLTAyMmE5ZDcwNTBiNiIsInBhcnRuZXJUeXBlIjoicGFydG5lcl9ncm91cCIsImlhdCI6MTc0NDgzNzEzOX0.YvvCD-I4GOSPmRduMoXit8Rw05c9ILoiCjhnPMgygO0",
        "PARTNERSHIP_API_ENDPOINT": "https://partnership-service-staging.api.srna.co/"
      }
    }
  }
}
```

### Configuração para Claude Desktop

1. Abra as configurações do Claude Desktop
2. Vá para a seção "MCP Servers"
3. Adicione um novo servidor com as seguintes configurações:
   - **Nome**: Serena Partnerships API
   - **Comando**: `python`
   - **Argumentos**: `servidor_parcerias_mcp.py`
   - **Diretório de trabalho**: Caminho para este projeto
   - **Variáveis de ambiente**: Configure as variáveis PARTNERSHIP_API_KEY e PARTNERSHIP_API_ENDPOINT

### Configuração para Ollama

Adicione ao arquivo de configuração do Ollama:

```yaml
mcp_servers:
  - name: serena-partnerships
    command: python
    args: [servidor_parcerias_mcp.py]
    env:
      PARTNERSHIP_API_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImQzNDBmZWEyLWM3ZTQtNGY1Ni1hYjdlLTAyMmE5ZDcwNTBiNiIsInBhcnRuZXJUeXBlIjoicGFydG5lcl9ncm91cCIsImlhdCI6MTc0NDgzNzEzOX0.YvvCD-I4GOSPmRduMoXit8Rw05c9ILoiCjhnPMgygO0"
      PARTNERSHIP_API_ENDPOINT: "https://partnership-service-staging.api.srna.co/"
```

## 🌐 Endpoints da API

### Base URL
- **Staging**: `https://partnership-service-staging.api.srna.co/`
- **Produção**: `https://partnership-service.api.srna.co/`

### Mapeamento de Endpoints

| Ferramenta MCP | Método HTTP | Endpoint | Descrição |
|----------------|-------------|----------|-----------|
| `consultar_areas_operacao_gd` | GET | `/distribuited-generation/operation-areas` | Consulta áreas de operação |
| `obter_planos_gd` | GET | `/distribuited-generation/plans` | Obtém planos disponíveis |
| `cadastrar_lead` | POST | `/sales-conversion/leads` | Cadastra novo lead |
| `buscar_leads` | GET | `/sales-conversion/leads` | Lista leads com filtros |
| `validar_qualificacao_lead` | GET | `/sales-conversion/leads/qualification` | Valida qualificação |
| `buscar_lead_por_id` | GET | `/sales-conversion/leads/{id}` | Busca lead específico |
| `atualizar_lead` | PUT | `/sales-conversion/leads/{id}` | Atualiza lead |
| `atualizar_credenciais_distribuidora` | PATCH | `/sales-conversion/leads/{id}/energy-utility-credentials` | Atualiza credenciais |
| `criar_contrato` | POST | `/sales-conversion/leads/{id}/contracts` | Cria contrato |

## 🔐 Autenticação

Todas as requisições utilizam autenticação Bearer Token:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 📊 Estrutura de Dados

### Lead (Pessoa Física)
```json
{
  "fullName": "string",
  "personType": "natural",
  "emailAddress": "string",
  "mobilePhone": "string",
  "utilityBillingValue": "number",
  "identificationNumber": "string",
  "nationality": "string",
  "maritalStatus": "string",
  "profession": "string",
  "zipCode": "string",
  "state": "string",
  "city": "string",
  "street": "string",
  "number": "string",
  "neighborhood": "string",
  "complement": "string"
}
```

### Lead (Pessoa Jurídica)
```json
{
  "fullName": "string",
  "personType": "legal",
  "emailAddress": "string",
  "mobilePhone": "string",
  "utilityBillingValue": "number",
  "identificationNumber": "string",
  "companyName": "string",
  "tradeName": "string",
  "zipCode": "string",
  "state": "string",
  "city": "string",
  "street": "string",
  "number": "string",
  "neighborhood": "string",
  "complement": "string"
}
```

## 🚀 Casos de Uso

### 1. Processo de Vendas Completo
```python
# 1. Verificar se a área tem cobertura
areas = await consultar_areas_operacao_gd(cidade="São Paulo", estado="SP")

# 2. Obter planos disponíveis
planos = await obter_planos_gd(cidade="São Paulo", estado="SP")

# 3. Cadastrar lead
lead_id = await cadastrar_lead(dados_cliente)

# 4. Validar qualificação
qualificacao = await validar_qualificacao_lead(
    cidade="São Paulo",
    estado="SP",
    tipo_pessoa="natural",
    valor_conta=500.00
)

# 5. Se qualificado, criar contrato
if qualificacao.qualificado:
    contrato = await criar_contrato(lead_id, dados_contrato)
```

### 2. Consulta de Leads Existentes
```python
# Buscar leads ativos
leads = await buscar_leads(status="active", limit=50)

# Para cada lead, buscar detalhes
for lead in leads:
    detalhes = await buscar_lead_por_id(lead.id)
    print(f"Lead: {detalhes.fullName} - Status: {detalhes.status}")
```

### 3. Atualização em Lote
```python
# Buscar leads que precisam de atualização
leads = await buscar_leads(status="pending_credentials")

# Atualizar credenciais
for lead in leads:
    await atualizar_credenciais_distribuidora(
        lead.id, 
        {"username": "novo_user", "password": "nova_senha"}
    )
```

## ⚠️ Tratamento de Erros

O servidor inclui tratamento robusto de erros:

### Códigos de Erro Comuns
- `400`: Dados inválidos ou obrigatórios ausentes
- `401`: Token de autenticação inválido
- `404`: Recurso não encontrado
- `422`: Dados de validação inválidos
- `500`: Erro interno do servidor

### Exemplo de Tratamento
```python
try:
    resultado = await cadastrar_lead(dados_lead)
    print(f"Lead criado com ID: {resultado.id}")
except Exception as e:
    print(f"Erro ao cadastrar lead: {e.message}")
    if e.status_code == 422:
        print("Dados de validação inválidos")
```

## 🔒 Segurança

### Boas Práticas
- ✅ A chave de API é carregada de variável de ambiente
- ✅ Todas as requisições incluem autenticação Bearer Token
- ✅ Não armazene credenciais no código fonte
- ✅ Use HTTPS para todas as comunicações
- ✅ Valide todos os dados de entrada

### Configuração de Segurança
```bash
# Configure as variáveis de ambiente
export PARTNERSHIP_API_KEY="sua_chave_aqui"
export PARTNERSHIP_API_ENDPOINT="https://partnership-service-staging.api.srna.co/"
```

## 📈 Monitoramento e Logs

### Logs Disponíveis
- Requisições HTTP com timestamps
- Erros de validação
- Tempo de resposta das APIs
- Status de autenticação

### Exemplo de Log
```
[2024-01-15 10:30:45] INFO: Requisição para /sales-conversion/leads
[2024-01-15 10:30:46] INFO: Lead criado com sucesso - ID: lead_123456
[2024-01-15 10:30:47] INFO: Tempo de resposta: 1.2s
```

## 🧪 Testes

### Testando as Ferramentas
```python
# Teste básico de conectividade
areas = await consultar_areas_operacao_gd(cidade="São Paulo", estado="SP")
assert areas is not None
assert len(areas) > 0

# Teste de cadastro de lead
lead_data = {
    "fullName": "Teste MCP",
    "personType": "natural",
    "emailAddress": "teste@mcp.com",
    # ... outros campos obrigatórios
}
lead = await cadastrar_lead(lead_data)
assert lead.id is not None
```

## 📞 Suporte

### Recursos de Ajuda
- **Documentação da API**: Consulte `api-documentation.md`
- **Issues**: Abra issues no repositório para bugs ou melhorias
- **Equipe de Desenvolvimento**: Entre em contato para suporte técnico

### Informações de Contato
- **Email**: dev@serena.co
- **Slack**: #serena-partnerships-api
- **Documentação**: https://docs.serena.co/partnerships

## 🔄 Versões e Changelog

### v1.0.0 (Atual)
- ✅ Implementação completa das 9 ferramentas MCP
- ✅ Suporte a leads pessoa física e jurídica
- ✅ Validação de qualificação
- ✅ Criação de contratos
- ✅ Tratamento robusto de erros

### Próximas Versões
- 🔄 Suporte a webhooks
- 🔄 Cache de consultas frequentes
- 🔄 Métricas de performance
- 🔄 Suporte a múltiplos ambientes

---

**Desenvolvido pela Equipe Serena** 🚀 