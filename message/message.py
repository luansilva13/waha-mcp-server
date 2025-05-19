from mcp.server.fastmcp import FastMCP
from typing import Any
import requests
from datetime import datetime
import sys
import json
app = FastMCP('message')


try:
    with open('/home/luan-silva/ufg/atividades/tarefa_2/tarefa_luan/message/contatos.json', encoding="utf-8") as f:
        contatos: list[dict[str, str]] = json.load(f)
except Exception as e:
    print(f"Erro ao carregar o arquivo JSON: {e}")

# Tool: send_message
@app.tool()
async def send_message(number: str, text: str)-> dict[str, Any]:
    try:
        url = "http://waha:3000/api/sendText"  # usando nome do serviço Docker
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "chatId": f"{number.replace('+', '')}@c.us",
            "text": text,
            "session": "default"
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return {"status": "error", "message": str(e)}

@app.tool()
async def list_contacts() -> list[dict[str, str]]:
    """
    Retorna a lista de contatos pré-carregados.
    """
    return contatos



if __name__ == "__main__":
    # Initialize and run the server
    app.run(transport='stdio')
    