from mcp.server.fastmcp import FastMCP
from mcp import types
from typing import Any, Dict, List
import requests
from datetime import datetime
import sys
import json
from pathlib import Path
import os



app = FastMCP('message')
# WAHA API configuration
WAHA_URL = os.environ.get('WAHA_URL', 'http://localhost:3000')
WAHA_SESSION = os.environ.get('WAHA_SESSION', 'default')

CONTACTS_FILE = Path(os.environ.get('CONTACTS_FILE', '/home/luan-silva/ufg/atividades/tarefa_2/tarefa_luan/message/contatos.json'))

# Tool: send_message
@app.tool(description="Envia uma mensagem de texto via WhatsApp com o número de telefone e o texto fornecidos")
async def send_message(number: str, text: str) -> Dict[str, Any]:
    """
    Envia uma mensagem via WhatsApp para o número especificado.
    
    Args:
        number: Número de telefone com código do país (ex: 5511999999999)
        text: Texto da mensagem a ser enviada
    
    Returns:
        Resultado da operação de envio
    """
    try:
        # Format the phone number properly
        # Remove any non-digit characters to ensure correct format
        clean_number = ''.join(filter(str.isdigit, number))
        
        url = f"{WAHA_URL}/api/{WAHA_SESSION}/sendText"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        data = {
            "chatId": f"{clean_number}@c.us",
            "text": text
        }
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        result = response.json()
        print(f"Mensagem enviada para {number}: {result}")
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição HTTP: {e}")
        return {"status": "error", "message": f"Erro na requisição: {str(e)}"}
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return {"status": "error", "message": str(e)}
#Resource: contatos.json

@app.resource('file:///contatos.json', name='contatos', description="Lista de contatos pré-carregados")
async def list_contacts() -> List[Dict[str, Any]]:
    """
    Retorna a lista de contatos pré-carregados.
    """
    contacts = load_contacts()
    print(f"Retornando {len(contacts)} contatos")
    return contacts


# Load contacts with proper error handling
def load_contacts() -> List[Dict[str, Any]]:
    """Load contacts from JSON file with error handling"""
    try:
        with open(CONTACTS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo de contatos não encontrado: {CONTACTS_FILE}")
        # Create a default contacts file if it doesn't exist
        sample_contacts = [
            {"name": "Exemplo", "phoneNumber": "5511999999999"},
            {"name": "Teste", "phoneNumber": "5511888888888"}
        ]
        with open(CONTACTS_FILE, 'w', encoding="utf-8") as f:
            json.dump(sample_contacts, f, indent=2, ensure_ascii=False)
        return sample_contacts
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo JSON: {CONTACTS_FILE}")
        return []
    except Exception as e:
        print(f"Erro ao carregar o arquivo JSON: {e}")
        return []
# Tool: get_contacts
@app.tool(description="Retorna a lista de contatos disponíveis")
async def get_contacts() -> Dict[str, Any]:
    """
    Obtém a lista de contatos disponíveis.
    
    Returns:
        Lista de contatos com seus detalhes
    """
    contacts = load_contacts()
    return {
        "status": "success",
        "contacts": contacts,
        "count": len(contacts)
    }


if __name__ == "__main__":
    # Initialize and run the server
    app.run(transport='stdio')
    