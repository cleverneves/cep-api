# API de Consulta de CEP

API REST para consulta de endereços brasileiros a partir do código de endereçamento postal (CEP). A API utiliza o serviço ViaCEP para obter as informações de endereço correspondentes.

## Visão Geral

Esta é uma aplicação backend experimental desenvolvida em **FastAPI** e containerizada com **Docker**. O aplicativo fornece um endpoint simples para consultar informações de endereço através do CEP, como logradouro, bairro, cidade e estado.

**Características:**
- Implementação assíncrona com FastAPI
- Integração com API ViaCEP
- Validação de formato de CEP
- Tratamento de erros estruturado
- Documentação automática com Swagger UI
- Containerização com Docker

## Requisitos

### Ambiente Local
- Python 3.11+
- pip (gerenciador de pacotes Python)

### Dependências
As dependências da aplicação estão listadas em `requirements.txt`:

```
fastapi      # Framework web assíncrono para construção de APIs
uvicorn      # Servidor ASGI de produção
httpx        # Cliente HTTP assíncrono
```

### Docker (Opcional)
- Docker 20+
- Docker Compose (opcional, para orquestração)

## Instalação e Setup

### Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/cleverneves/cep-api.git
cd cep-api
```

2. Crie um ambiente virtual Python:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Execute o servidor:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

O servidor estará disponível em `http://localhost:8000`

### Usando Docker

1. Construa a imagem Docker:
```bash
docker build -t cep-api:1.0 .
```

2. Execute o container:
```bash
docker run -p 8000:8000 cep-api:1.0
```

O servidor estará disponível em `http://localhost:8000`

## Documentação Interativa

A API fornece documentação interativa automática através do Swagger UI:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Endpoints

### Consultar CEP

Retorna as informações de endereço para um CEP específico.

**Endpoint:**
```
GET /cep/{cep}
```

**Parâmetros:**
- `cep` (path, required): O código de endereçamento postal a ser consultado
  - Formato aceito: `00000-000` ou `00000000` (com ou sem hífen)
  - Exemplo: `01001-000` ou `01001000`

**Resposta de Sucesso (200):**
```json
{
  "cep": "01001-000",
  "logradouro": "Praça da Sé",
  "complemento": "lado ímpar",
  "bairro": "Sé",
  "localidade": "São Paulo",
  "uf": "SP",
  "ibge": "3550308",
  "gia": "",
  "ddd": "11",
  "siafi": "7107"
}
```

**Campos de Resposta:**
- `cep`: CEP no formato com hífen
- `logradouro`: Nome da rua/avenida/praça
- `complemento`: Complemento do endereço (ex.: lado da rua)
- `bairro`: Nome do bairro
- `localidade`: Cidade/município
- `uf`: Unidade federativa (sigla do estado)
- `ibge`: Código IBGE do município
- `gia`: Código GIA (quando aplicável)
- `ddd`: Código DDD da região
- `siafi`: Código SIAFI do município

## Exemplos de Chamada

### JavaScript/Fetch API

```javascript
// Consultar CEP com hífen
fetch('http://localhost:8000/cep/01001-000')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Erro:', error));

// Consultar CEP sem hífen
fetch('http://localhost:8000/cep/01001000')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Erro:', error));
```

### Python (requests)

```python
import requests

url = 'http://localhost:8000/cep/01001-000'
response = requests.get(url)

if response.status_code == 200:
    dados = response.json()
    print(f"Logradouro: {dados['logradouro']}")
    print(f"Bairro: {dados['bairro']}")
    print(f"Cidade: {dados['localidade']}")
else:
    print(f"Erro: {response.status_code}")
    print(response.json())
```

### cURL

```bash
# Consultar CEP com hífen
curl http://localhost:8000/cep/01001-000

# Consultar CEP sem hífen
curl http://localhost:8000/cep/01001000

# Salvar resposta em arquivo
curl http://localhost:8000/cep/20040020 > endereco.json
```

### Axios (JavaScript)

```javascript
import axios from 'axios';

async function consultarCEP(cep) {
  try {
    const response = await axios.get(`http://localhost:8000/cep/${cep}`);
    console.log('Endereço encontrado:');
    console.log(response.data);
  } catch (error) {
    if (error.response?.status === 404) {
      console.log('CEP não encontrado');
    } else if (error.response?.status === 400) {
      console.log('Formato de CEP inválido');
    } else if (error.response?.status === 502) {
      console.log('Serviço ViaCEP indisponível');
    }
  }
}

consultarCEP('01001-000');
```

### Python (httpx) - Assíncrono

```python
import asyncio
import httpx

async def consultar_cep(cep: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'http://localhost:8000/cep/{cep}')
            response.raise_for_status()
            dados = response.json()
            print(f"Endereço: {dados['logradouro']}, {dados['bairro']}")
            return dados
        except httpx.HTTPStatusError as e:
            print(f"Erro HTTP {e.response.status_code}: {e.response.json()}")

# Executar
asyncio.run(consultar_cep('01001-000'))
```

### PowerShell

```powershell
# Usando Invoke-WebRequest
$response = Invoke-WebRequest -Uri 'http://localhost:8000/cep/01001-000' -Method Get
$dados = $response.Content | ConvertFrom-Json
Write-Host "Logradouro: $($dados.logradouro)"
Write-Host "Bairro: $($dados.bairro)"
Write-Host "Cidade: $($dados.localidade)"

# Ou com ConvertFrom-Json
$json = (Invoke-WebRequest -Uri 'http://localhost:8000/cep/20040020').Content
$json | ConvertFrom-Json | Format-Table
```

## Tratamento de Erros

A API retorna erros estruturados com status HTTP apropriados:

### 400 - Requisição Inválida (CEP malformado)

**Causa:** O CEP fornecido não possui 8 dígitos ou contém caracteres não numéricos (após remover hífen).

**Resposta:**
```json
{
  "detail": "CEP inválido."
}
```

**Exemplo de chamada que gera esse erro:**
```bash
# CEP com menos de 8 dígitos
curl http://localhost:8000/cep/0100

# CEP com caracteres inválidos
curl http://localhost:8000/cep/0100a000

# CEP vazio
curl http://localhost:8000/cep/
```

### 404 - Não Encontrado (CEP não existe)

**Causa:** O CEP possui formato válido, mas não foi encontrado na base de dados do ViaCEP.

**Resposta:**
```json
{
  "detail": "CEP não encontrado."
}
```

**Exemplo de chamada que gera esse erro:**
```bash
# CEP inválido (não existe)
curl http://localhost:8000/cep/00000000
```

### 502 - Bad Gateway (Erro na API ViaCEP)

**Causa:** A API ViaCEP está indisponível ou ocorreu um erro ao se comunicar com o serviço externo.

**Resposta:**
```json
{
  "detail": "Falha ao consultar o ViaCEP."
}
```

**Tratamento Recomendado:**
```python
import requests
import time

def consultar_cep_com_retry(cep: str, max_tentativas: int = 3):
    for tentativa in range(max_tentativas):
        try:
            response = requests.get(f'http://localhost:8000/cep/{cep}')
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                print("CEP inválido - não tente novamente")
                return None
            elif response.status_code == 404:
                print("CEP não encontrado - não tente novamente")
                return None
            elif response.status_code == 502:
                if tentativa < max_tentativas - 1:
                    tempo_espera = 2 ** tentativa  # Backoff exponencial
                    print(f"Serviço indisponível, tentando em {tempo_espera}s...")
                    time.sleep(tempo_espera)
                    continue
                
        except requests.exceptions.ConnectionError:
            if tentativa < max_tentativas - 1:
                print(f"Conexão recusada, tentando novamente...")
                time.sleep(2 ** tentativa)
                continue
    
    print("Todas as tentativas falharam")
    return None
```

## Arquitetura

### Fluxo de Requisição

```
Cliente (navegador/aplicação)
    |
    v
FastAPI (localhost:8000)
    |
    +-- Validação de CEP
    |
    +-- Normalização (remover hífen)
    |
    +-- Chamada HTTP para ViaCEP
    |   (https://viacep.com.br/ws/{cep}/json/)
    |
    +-- Tratamento de erros
    |
    v
JSON Response (endereço ou erro)
```

### Estrutura do Código

- **main.py**: Arquivo principal contendo a aplicação FastAPI
  - `consultar_cep()`: Função assíncrona que processa a requisição de consulta
  - Validação de CEP (8 dígitos numéricos)
  - Cliente HTTP assíncrono (httpx)
  - Tratamento de exceções

### Stack Tecnológico

| Componente | Tecnologia | Versão |
|-----------|-----------|--------|
| Framework Web | FastAPI | Latest |
| Servidor ASGI | Uvicorn | Latest |
| Cliente HTTP | httpx | Latest |
| Runtime | Python | 3.11+ |
| Containerização | Docker | 20+ |

## Desenvolvimento

### Executando em Modo de Desenvolvimento

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Flags:**
- `--reload`: Reinicia automaticamente quando houver mudanças no código
- `--host 0.0.0.0`: Aceita conexões de qualquer interface de rede
- `--port 8000`: Define a porta do servidor

### Testando a API

```python
# test_api.py
import pytest
import httpx

@pytest.mark.asyncio
async def test_consultar_cep_valido():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8000/cep/01001-000')
        assert response.status_code == 200
        assert 'logradouro' in response.json()

@pytest.mark.asyncio
async def test_cep_invalido():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8000/cep/0100')
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_cep_nao_encontrado():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://localhost:8000/cep/00000000')
        assert response.status_code == 404
```

## Deployment

### Deploy com Docker

1. Construir a imagem:
```bash
docker build -t cep-api:1.0 .
```

2. Executar o container:
```bash
docker run -d \
  --name cep-api \
  -p 8000:8000 \
  --restart unless-stopped \
  cep-api:1.0
```

3. Verificar status:
```bash
docker ps
docker logs cep-api
```

### Deploy em Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cep-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cep-api
  template:
    metadata:
      labels:
        app: cep-api
    spec:
      containers:
      - name: cep-api
        image: cep-api:1.0
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /docs
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: cep-api-service
spec:
  selector:
    app: cep-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## Melhores Práticas

### Implementadas nesta API

1. **Validação de Entrada**: Verificação rigorosa do formato do CEP antes de consultar a API externa
2. **Tratamento de Erros**: Respostas estruturadas com status HTTP apropriados
3. **Assincronismo**: Uso de async/await para melhor performance
4. **Cliente HTTP Eficiente**: httpx com gerenciamento automático de conexões
5. **Documentação Automática**: Swagger UI integrado via FastAPI
6. **Versionamento**: Definido no OpenAPI spec

### Recomendações para Extensão

1. **Rate Limiting**: Implementar limite de requisições por IP/usuário
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   @app.get("/cep/{cep}")
   @limiter.limit("30/minute")
   ```

2. **Cache**: Armazenar CEPs consultados frequentemente
   ```python
   from functools import lru_cache
   @lru_cache(maxsize=1000)
   def buscar_cep(cep: str):
       ...
   ```

3. **Logging**: Registrar requisições e erros
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.info(f"CEP consultado: {cep}")
   ```

4. **CORS**: Permitir requisições de outros domínios (se necessário)
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_methods=["*"],
   )
   ```

5. **Autenticação**: Implementar chaves de API para controle de acesso
6. **Monitoramento**: Adicionar métricas de performance e disponibilidade

## Solução de Problemas

### A API retorna erro 502

**Possíveis causas:**
- Serviço ViaCEP está fora do ar
- Conexão de internet instável
- Firewall bloqueando requisições externas

**Solução:**
- Verifique a disponibilidade do ViaCEP em https://viacep.com.br
- Tente novamente em alguns segundos
- Verifique configurações de firewall/proxy

### CEP válido retorna erro 404

**Possíveis causas:**
- CEP não existe na base de dados ViaCEP
- CEP é muito novo e ainda não foi registrado

**Solução:**
- Verifique se o CEP está correto
- Consulte os correios para validar o CEP

### Servidor não inicia

**Possíveis causas:**
- Porta 8000 já está em uso
- Dependências não estão instaladas

**Solução:**
```bash
# Verificar se a porta está em uso
netstat -ano | findstr :8000

# Usar porta diferente
uvicorn main:app --port 8001

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

## Informações Adicionais

- **Documentação FastAPI**: https://fastapi.tiangolo.com/
- **ViaCEP API**: https://viacep.com.br/
- **Documentação Docker**: https://docs.docker.com/
- **Repositório GitHub**: https://github.com/cleverneves/cep-api

## Suporte

Para reportar problemas ou sugerir melhorias, abra uma issue no repositório GitHub ou entre em contato com os mantenedores do projeto.
