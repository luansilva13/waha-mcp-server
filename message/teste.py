import json

def ler_nome_do_json(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            print("TESTE")
            print(dados.get("lizandra"))
            return dados.get("lizandra")
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON no arquivo: {caminho_arquivo}")
    return None
ler_nome_do_json('/home/luan-silva/ufg/atividades/tarefa_2/tarefa_luan/message/contatos.json')