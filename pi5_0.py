"""
Antes de executar, rode os seguintes comandos:

pip install requests

e

pip install urllib3

Nome dos labirintos: 'large-maze', 'maze-sample-2', 'maze-sample', 'medium-maze', 'very-large-maze'

Labirintos concluidos:
-   maze-sample
-   maze-sample-2
-   medium-maze


"""
import sys
import requests
import urllib3
from collections import deque

def obter_labirinto():
    urllib3.disable_warnings()
    response = requests.get('https://gtm.delary.dev/labirintos', verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"A solicitação falhou com o código de status {response.status_code}")
        return None

def iniciar_labirinto(nome_labirinto, id_jogador):
    urllib3.disable_warnings()
    url_iniciar = "https://gtm.delary.dev/iniciar"
    dados_requisicao = {
        "id": id_jogador,
        "labirinto": nome_labirinto
    }
    resposta_iniciar = requests.post(url_iniciar, json=dados_requisicao, verify=False)

    if resposta_iniciar.status_code == 200:
        print("Resposta do /iniciar:")
        return resposta_iniciar.json()
    else:
        print(f"A solicitação falhou com o código de status: {resposta_iniciar.status_code}")
        print('Dados da requisição: ', dados_requisicao)
        return None

def movimentar_labirinto(nome_labirinto, id_jogador, nova_posicao):
    urllib3.disable_warnings()
    url_movimentar = "https://gtm.delary.dev/movimentar"
    dados_requisicao = {
        "id": id_jogador,
        "labirinto": nome_labirinto,
        "nova_posicao": nova_posicao
    }
    resposta_movimentar = requests.post(url_movimentar, json=dados_requisicao, verify=False)

    if resposta_movimentar.status_code == 200:
        print("\nResposta do /movimentar:")
        print(resposta_movimentar.json())
        return resposta_movimentar.json()
    else:
        print(f"A solicitação falhou com o código de status: {resposta_movimentar.status_code} > {resposta_movimentar.reason}")
        print('Dados da requisição: ', dados_requisicao)
        return None

# Iniciar Labirinto
nome_labirinto = "" 
if len(sys.argv) > 1:
    nome_labirinto = sys.argv[1]
else:
    nome_labirinto = 'large-maze'

print("Labirinto: ", nome_labirinto)

inicio_lab = iniciar_labirinto(nome_labirinto, 'Aaron')
visitados = set()
caminho = [inicio_lab['pos_atual']]
pilha = [inicio_lab['pos_atual']]
pilha.extend(inicio_lab.get('movimentos'))
visitados.add(inicio_lab['pos_atual'])
movimentos_visitados = set()

while pilha:
    posicao_atual = pilha[-1]
    visitados.add(posicao_atual)
    caminho.append(posicao_atual)

    if posicao_atual in movimentos_visitados:
        pilha.pop()
        caminho.pop()
        continue

    mov_lab = movimentar_labirinto('large-maze', 'Aaron', posicao_atual)
    if mov_lab is None:
        print("Erro!")
        break

    movimentos = mov_lab.get('movimentos', [])

    if mov_lab.get('final') == True:
        print(f'Caminho final {caminho}')
        print(f'Posição final: {posicao_atual}')
        break

    movimentos_visitados.add(posicao_atual)

    novos_movimentos = [movimento for movimento in movimentos if movimento not in visitados and movimento not in movimentos_visitados]
    pilha.extend(novos_movimentos)

    print(f'Posição atual: {posicao_atual}')
    print(f'Pilha: {pilha}')
    print(f'Caminho({len(caminho)}): {caminho}')
    print(f'Visitados: {visitados}')


