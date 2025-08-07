partnership-service
Backend com as API's do contexto de parcerias
Distribuited Generation
GETGET /distribuited-generation/plans Obter planos de geração distribuída
Retorna uma lista de planos de GD disponíveis, com base na distribuidora de energia informada OU
através da combinação de cidade e estado. Se informados tanto ID da distribuidora quanto estado e
cidade, a busca considerará o ID da distribuidora.
Try it out
Name Description
energy_utility_public_id
string
(query)
Public ID da distribuidora de energia. Deve ser um UUID válido.
Por exemplo, 123e4567-e89b-12d3-a456-426614174000.
Esse UUID pode ser obtido através do endpoint GET
/distribuited-generation/operation-areas
energy_utility_public_id
state
string
(query)
Sigla do estado (Unidade Federativa) para consultar as áreas
de operação. Deve ser fornecido junto com o parâmetro "city".
Por exemplo, "SP" para São Paulo.
state
city
string
(query)
Nome da cidade para consultar as áreas de operação. Deve ser
fornecido junto com o parâmetro "state". Por exemplo, "São
Paulo".
city
1.0 OAS
Parameters
Responses
Code Description Links
200
Media type
application/json
Controls Accept header.
Schema
No links
GETGET /distribuited-generation/operation-areas
Consultar áreas de operação de geração
distribuída
Retorna uma lista de áreas onde o serviço de GD está disponível. A consulta pode ser feita por estado
e cidade OU pelo código IBGE de um município.
Try it out
Name Description

state
string

(query)

Sigla do estado (Unidade Federativa) para consultar as áreas de operação.
Deve ser fornecido junto com o parâmetro "city". Por exemplo, "SP" para
São Paulo.
state
Example Value
[
{
"energyUtilityName": "ENEL SP",
"plans": [
{
"id": 1 ,
"name": "Plano Premium",
"fidelityMonths": 60 ,
"discount": "0.14",
"offeredBenefits": [
{
"description": "Primeira Fatura Grátis"
} ] } ] } ]
Parameters
Name Description
city
string
(query)
Nome da cidade para consultar as áreas de operação. Deve ser fornecido
junto com o parâmetro "state". Por exemplo, "São Paulo".
city
ibge_code
string
(query)
Código IBGE do município para consultar a área de operação. Este
parâmetro pode ser usado sozinho como alternativa aos parâmetros "state"
e "city". Exemplo: "3550308" para São Paulo.
ibge_code
Responses
Code Description Links
200
Media type
application/json
Controls Accept header.
Schema
No links
Sales Conversion
POSTPOST /sales-conversion/leads Cadastro de lead
Cadastra um lead na base da Serena.
O campo "companyName" é obrigatório apenas para lead do tipo pessoa jurídica.
O campo "personType" deve conter "juridical" para pessoa jurídica e "natural" quando pessoa física.
Example Value
[
{
"energyUtilityPublicId": "a06dcadc-fe16-44ee-b541-0c4658aa
d3e",
"energyUtilityName": "ENEL SP",
"energyUtilityQualified": true,
"ibgeCode": "Plano Premium",
"state": "SP",
"city": "São Paulo"
}
]
Os campos "nationality", "maritalStatus" e "profession" são obrigatórios apenas se o títular da conta de
luz for do tipo pessoa física.
O envio de plano não é obrigatório no momento da criação do lead, também pode ser enviado nas
rotas de atualização do lead OU criação do contrato
Try it out
No parameters
Request body application/json
Schema
Responses
Code Description Links
201 No links
GETGET /sales-conversion/leads Buscar informações de leads
Busca informações dos leads com base nos filtros fornecidos.
Parameters
required
Example Value

{
"fullName": "John Cena",
"personType": "natural",
"companyName": "Empresa Social LTDA",
"emailAddress": "another@mail.com",
"mobilePhone": "11999885544",
"utilityBillHolder": "natural",
"utilityBillingValue": 850. 15 ,
"identificationNumber": "41122255578",
"nationality": "Brasileiro",
"maritalStatus": "Solteiro",
"profession": "Mecânico",
"zipCode": "01111-999",
"state": "SP",
"city": "Campinas",
"street": "Rua Ladrilhos Dourados",
"number": "777",
"neighborhood": "Alphaville",
"complement": "Quadra 2",
"plan": {
"benefit": "Ganhou_1_Fatura_Gratis",
"discount": "10",
"loyaltyRequirement": "60",
"planName": "Premium"
}
Try it out
Name Description

page
number

(query)

page
limit
number

(query)

limit
filters
string

(query)

Uso de filtros para buscar os leads por: customer, seller_name, created_at,
status (não precisam ser mandados todos)
status enum: negociacao | indicado | desqualificado | assinado
Exemplo de uso: customer:18.928.199/0001-88,seller_name:John
Cena,created_at:2024-07-01,status:negociação
filters
Responses
Code Description Links
200
Resposta contendo a lista de leads e o total de leads encontrados
Media type
application/json
Controls Accept header.
Schema
No links
Parameters
Example Value
{
"leads": [
{
"fullName": "John Doe",
"personType": "PJ",
"companyName": "Empresa Social LTDA",
"emailAddress": "john.doe@mailinator.com",
"mobilePhone": "11999885544",
"utilityBillingValue": 850. 15 ,
"identificationNumber": "41122255578",
"nationality": "Brasileiro",
"maritalStatus": "Solteiro",
"profession": "Mecânico",
"zipCode": "01111-999",
"state": "SP",
Code Description Links
GETGET /sales-conversion/leads/qualification Consulta para validar a qualificação do lead.
Consulta para validar se um lead está qualificado para o produto de geração distribuída ou para
mercado livre.
Try it out
Name Description

city *
string

(query)

Nome da cidade para consultar as áreas de operação. Deve
ser fornecido junto com o parâmetro "state". Exemplo:
Belém
city
state *
string

(query)

Sigla do estado (Unidade Federativa) para consultar as
áreas de operação. Deve ser fornecido junto com o
parâmetro "city". Exemplo: PA
state
personType *
string

(query)

Categoria da pessoa associada ao lead, sendo necessário
especificar se é uma pessoa física ou jurídica. Para pessoa
física informe "natural" e para pessoa jurídica informe
"juridical".
personType
utilityBillingValue *
string

(query)

Valor da conta de luz por mês associada ao lead. Exemplo:
815.
utilityBillingValue
"city": "Campinas",
"street": "Rua Ladrilhos Dourados",
"number": "777",
"neighborhood": "Alphaville",
"complement": "Quadra 2",
"statusDetails": "string",
"status": "string",
"contractLink": "string",
"contractSignerLink": "string"
}
Parameters
required
required
required
required
Responses
Code Description Links
200
Media type
application/json
Controls Accept header.
Schema
No links
GETGET /sales-conversion/leads/{id} Buscar informações de um lead
Busca informações de um lead cadastrado baseado no ID fornecido.
Try it out
Name Description

id *
(path)

ID do lead
id
Responses
Code Description Links
200
Media type
application/json
Controls Accept header.
Schema
No links
Example Value
{
"product": "Geração Distribuída.",
"qualification": true
}
Parameters
required
Example Value
Code Description Links
PUTPUT /sales-conversion/leads/{id}
Atualiza as informações do lead de acordo com os dados
enviados.
O campo "personType" deve conter "juridical" caso seja pessoa jurídica e "natural" quando pessoa
física.
O campo "companyName" é obrigatório apenas para lead do tipo pessoa jurídica.
Os campos "nationality", "maritalStatus" e "profession" são obrigatórios apenas se o titular da conta de
luz for do tipo pessoa física.
Try it out
Name Description

id *
(path)

id
Request body application/json
Schema
{
"fullName": "John Doe",
"personType": "PJ",
"companyName": "Empresa Social LTDA",
"emailAddress": "john.doe@mailinator.com",
"mobilePhone": "11999885544",
"utilityBillingValue": 850. 15 ,
"identificationNumber": "41122255578",
"nationality": "Brasileiro",
"maritalStatus": "Solteiro",
"profession": "Mecânico",
"zipCode": "01111-999",
"state": "SP",
"city": "Campinas",
"street": "Rua Ladrilhos Dourados",
"number": "777",
"neighborhood": "Alphaville",
"complement": "Quadra 2",
"statusDetails": "string",
"status": "string",
"contractLink": "string",
"contractSignerLink": "string"
}
Parameters
required
required
Example Value

{
"fullName": "Claire Redfield",
"cnpj": "47526391000146",
"cpf": "12345678911",
"companyName": "Empresa Parceria",
Responses
Code Description Links
200 No links
PATCHPATCH
/sales-conversion/leads/{id}/energy-
utility-credentials
Adicionar ou atualizar o login e a senha da
distribuidora.
Atualiza ou adiciona dados das credenciais de acesso ao site da distribuidora.
Try it out
Name Description

id *
(path)

id
Request body application/json
Schema
"mobilePhone": "(11)90000-0000",
"personType": "juridical",
"utilityBillValue": 300. 67 ,
"installationNumber": "4324234432",
"birthDate": "1995-05-10",
"plan": {
"discount": "16",
"planName": "Premium",
"loyaltyRequirement": "60",
"benefit": "Ganhou_1_Fatura_Gratis"
},
"billingData": {
"identificationNumber": "47526391000146",
"nationality": "Brasileira",
"maritalStatus": "Solteira",
"profession": "Maratonista"
},
"address": {
"street": "Rua Duilio Aloi",
Parameters
required
required
Example Value

{
"utilityBillLogin": "login.distribuidora@teste.com",
"password": "qwer1234"
}
Responses
Code Description Links
200 No links
POSTPOST /sales-conversion/leads/{id}/utility-bill Upload de fatura de energia
Faz o envio da fatura de energia do cliente indicado após criação do lead
Try it out
Name Description

id *
(path)

id
Request body multipart/form-data
Arquivo a ser enviado com nome "utilityBill" no FormData
utilityBill
string($binary)
Responses
Code Description Links
201 No links
POSTPOST /sales-conversion/leads/{id}/document Upload de documento constitucional
Parameters
required
required
Faz o envio do documento constitucional do lead PJ indicado
Try it out
Name Description

id *
(path)

id
Request body multipart/form-data
Arquivo a ser enviado com nome "file" no FormData
file
string($binary)
Responses
Code Description Links
201 No links
PUTPUT /sales-conversion/leads/{id}/v2/document
Upload de documento pessoal e
constitucional (apenas para leads PJ)
Faz o envio de documento constitucional e pessoal do lead indicado, sendo que o envio de
documento constitucional (pode ser enviado duas vezes, o segundo irá opcional) se dá apenas para
lead PJ
Try it out
Parameters
required
required
Parameters
Name Description

id *
(path)

id
Request body multipart/form-data
Arquivos a serem enviados com nomes próprios no FormData, sendo um documento
constitucional e dois documentos (frente e verso) de identificação, que contenha o CPF (RG OU
CNH)
identificacaoFrente
string($binary)
Arquivo da frente do documento que contenha o CPF do lead
identificacaoVerso
string($binary)
Arquivo do verso do documento que contenha o CPF do lead
constitucional
string($binary)
Documento constitucional do lead (apenas para lead PJ)
Responses
Code Description Links
201
Documento (s) enviado com sucesso
No links
400
Erro no envio de documentos (exemplo: nome de arquivo muito
grande ou documentos já enviados)
No links
POSTPOST /sales-conversion/leads/{id}/contracts
Cria um contrato de geração distribuída
associado a um lead.
O envio do objeto "plan" é necessário somente se o plano não tiver sido informado previamente no
cadastro do lead; se um plano já tiver sido enviado anteriormente será lançada uma exceção 400.
O envio do array de objetos "legalRepresentatives" é obrigatório e permitido apenas se o lead for uma
pessoa jurídica; do contrário, será lançada uma exceção 400.
required
required
Parameters
Try it out
Name Description

id *
(path)

id
Request body application/json
Schema
Responses
Code Description Links
201
Documento enviado com sucesso
No links
400
Erro no envio de documentos (exemplo: nome de arquivo muito
grande ou documentos já enviados)
No links
required
required
Example Value

{
"plan": {
"benefit": "Ganhou_1_Fatura_Gratis",
"discount": "10",
"loyaltyRequirement": "60",
"planName": "Premium"
},
"legalRepresentatives": [
{
"name": "John Doe",
"identificationNumber": "60738456004",
"email": "john.doe@mailinator.com",
"cellphone": "11999885544",
"nationality": "Brasileiro",
"profession": "Diretor Comercial",
"maritalStatus": "Casado",
"address": {
"street": "Rua Ladrilhos Dourados",
"number": "777",
"complement": "Quadra 2",
"neighborhood": "Alphaville",
"zipCode": "01111-999",
"city": "Campinas",
"state": "SP"
}
Schemas
{
description*
[...]
}
OfferedBenefitsDto
{
id*
[...]
name*
[...]
fidelityMonths*
[...]
discount*
[...]
offeredBenefits*
[...]
}
PlansDto
{
energyUtilityName*
[...]
plans*
[...]
}
DistribuitedGenerationPlanDto
{
energyUtilityPublicId*
[...]
energyUtilityName*
[...]
energyUtilityQualified*
[...]
ibgeCode*
[...]
state*
[...]
city*
[...]
}
DistribuitedGenerationOperationAreaDto
{
benefit*
[...]
discount*
[...]
loyaltyRequirement*
[...]
planName*
[...]
}
PlanDTO
{
fullName*
[...]
personType*
[...]
companyName*
[...]
emailAddress*
[...]
mobilePhone*
[...]
utilityBillHolder*
[...]
utilityBillingValue*
[...]
identificationNumber*
[...]
nationality*
[...]
maritalStatus*
[...]
profession*
[...]
zipCode*
[...]
state*
[...]
city*
[...]
street*
[...]
number*
[...]
neighborhood*
[...]
complement*
[...]
plan*
{...}
}

CreateLeadDTO
PlanDTO
{
product*
[...]
qualification*
[...]
}

ResponseLeadQualificationDto
{
fullName*
[...]
personType*
[...]
companyName*
[...]
emailAddress*
[...]
mobilePhone*
[...]
utilityBillingValue*
[...]
identificationNumber*
[...]
nationality*
[...]
maritalStatus*
[...]
profession*
[...]
zipCode*
[...]
state*
[...]
city*
[...]
street*
[...]
number*
[...]
neighborhood*
[...]
complement*
[...]
statusDetails*
[...]
status*
[...]
contractLink*
[...]
contractSignerLink*
[...]
}

GetLeadDTO
{
leads*
[...]
total*
[...]
}

GetLeadsResponseDTO
{
discount*
[...]
planName*
[...]
loyaltyRequirement*
[...]
benefit*
[...]
}

Plan
{
identificationNumber*
[...]
nationality*
[...]
maritalStatus*
[...]
profession*
[...]
}

BillingData
{
street*
[...]
number*
[...]
complement*
[...]
neighborhood*
[...]
zipCode*
[...]
city*
[...]
state*
[...]
}

Address
{
fullName*
[...]
cnpj*
[...]
cpf*
[...]
companyName*
[...]
mobilePhone*
[...]
personType*
[...]
utilityBillValue*
[...]
installationNumber*
[...]
birthDate*
[...]
plan*
{...}
billingData*
{...}
address*
{...}
}

UpdateLeadDTO
Plan
BillingData
Address
{
utilityBillLogin*
[...]
password*
[...]
}

UpdateLeadEnergyUtilityCredentialsDTO
{
street*
[...]
number*
[...]
complement*
[...]
neighborhood*
[...]
zipCode*
[...]
city*
[...]
state*
[...]
}

AddressDto
{
name*
[...]
identificationNumber*
[...]
email*
[...]
cellphone*
[...]
nationality*
[...]
profession*
[...]
maritalStatus*
[...]
address*
{...}
}

LegalRepresentativesDTO
AddressDto
{
plan*
{...}
legalRepresentatives*
[...]
}

