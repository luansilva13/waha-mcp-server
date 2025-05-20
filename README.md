# Servidor MCP para envio de mensagens via WhatsApp com WAHA

## Nome da Tarefa

Construir um servidor MCP para envio de mensagens no WhatsApp utilizando o WAHA.

---

## Descrição

Este projeto implementa um servidor MCP com uma ferramenta (`tool`) e um recurso (`resource`) para envio de mensagens via WhatsApp utilizando o **WAHA**.

### Tool: `send_message`

Esta ferramenta recebe como parâmetros:

- **número** (no formato internacional: +5511...)
- **mensagem** a ser enviada

A `tool` se comunica com um servidor local WAHA, realizando uma requisição **POST** na rota `/api/sendText`.

### Exemplo de chamada em Python

```python
import requests

url = "http://localhost:3000/api/sendText"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
data = {
    "chatId": "123123@c.us",
    "text": "Hi there!",
    "session": "default"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

---

### Como instanciar o servidor WAHA

1. Siga os passos do vídeo: [YouTube - Dev Like a Pro](https://www.youtube.com/watch?v=RFerMyAUPRg)
2. Consulte a documentação oficial: [WAHA Quick Start](https://waha.devlike.pro/docs/overview/quick-start/)

---

## Resource: `contatos`

O recurso `contatos` vem pré-carregado com 3 números de telefone e nomes associados, por exemplo:

- João - +5511999999999
- Maria - +5511888888888
- Pedro - +5511777777777

Este recurso permite chamadas como:

> "Envie uma mensagem de bom dia para o João"

---

## Entregável

- Repositório no GitHub (ou outro)
- Relatório básico de uso
- Print de funcionalidade:
  - Servidor funcional com:
    - 1 Tool: `send_message`
    - 1 Resource: `contatos`

---

## Relatório básico de uso
Temos duas estruturas: serviço WAHA(disponível na porta 3000) e o servidor mcp (servidor e cliente).
Primeiramente inicie o servico WAHA e autentique através com o QR CODE gerado.
```
docker run -it -p 3000:3000/tcp devlikeapro/waha
```
- Para a implementação do cliente mcp vamos usar o https://www.anthropic.com/
- Gere uma chave dentro da api e adicione no .env na pasta mcp-client
- Exemplo de .env
```
ANTHROPIC_API_KEY=YOUR_KEY
```
Criando o ambiente
```
# Create project directory
uv init mcp-client
cd mcp-client

# Create virtual environment
uv venv

# Activate virtual environment
# On Unix or MacOS:
source .venv/bin/activate

# Install required packages
uv add mcp anthropic python-dotenv

# On Unix or MacOS:
rm main.py

# Create our main file
touch client.py
```
Ref: https://modelcontextprotocol.io/quickstart/client
Inicie o projeto mcp com: 
```
uv run mcp-client/client.py /message/message.py
```
## Referências

- [WAHA Quick Start](https://waha.devlike.pro/docs/overview/quick-start/)
- [YouTube: Dev Like a Pro](https://www.youtube.com/watch?v=RFerMyAUPRg&ab_channel=devlikeapro)
- [Model Context Protocol - Quickstart](https://modelcontextprotocol.io/quickstart/server)
