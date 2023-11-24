import requests
import urllib3
from collections import deque

urllib3.disable_warnings()

MAZE_NAME = 'large-maze'
PLAYER_NAME = 'Aaron'

# Reuse a session for better performance
session = requests.Session()


def obter_labirinto():
    response = session.get('https://gtm.delary.dev/labirintos', verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"A solicitação falhou com o código de status {response.status_code}")
        return None


labirinto = obter_labirinto()
print(labirinto)


def iniciar_labirinto(nome_labirinto, id_jogador):
    url_iniciar = "https://gtm.delary.dev/iniciar"
    dados_requisicao = {"id": id_jogador, "labirinto": nome_labirinto}
    resposta_iniciar = session.post(url_iniciar, json=dados_requisicao, verify=False)

    if resposta_iniciar.status_code == 200:
        print("Resposta do /iniciar:")
        return resposta_iniciar.json()
    else:
        print(f"A solicitação falhou com o código de status {resposta_iniciar.status_code}")
        return None


def movimentar_labirinto(nome_labirinto, id_jogador, nova_posicao):
    url_movimentar = "https://gtm.delary.dev/movimentar"
    dados_requisicao = {
        "id": id_jogador,
        "labirinto": nome_labirinto,
        "nova_posicao": nova_posicao
    }
    resposta_movimentar = session.post(url_movimentar, json=dados_requisicao, verify=False)

    if resposta_movimentar.status_code == 200:
        print("Resposta do /movimentar:")
        return resposta_movimentar.json()
    else:
        print(f"A solicitação falhou com o código de status {resposta_movimentar.status_code}")
        return None


def bfs(grafo, inicio, fim):
    fila = deque([(inicio, [inicio])])
    visitados = set()

    while fila:
        vertice, caminho = fila.popleft()
        if vertice not in visitados:
            visitados.add(vertice)

            # Verifica se a chave existe no dicionário e se tem vizinhos
            if vertice in grafo and grafo[vertice]:
                for vizinho in grafo[vertice]:
                    if vizinho == fim:
                        return caminho + [vizinho]
                    else:
                        fila.append((vizinho, caminho + [vizinho]))

    # Se não encontrar caminho, retorna None
    return None


inicio_lab = iniciar_labirinto(MAZE_NAME, PLAYER_NAME)
visitados = set()
p_atual = inicio_lab
pilha = [inicio_lab['pos_atual']]
final_lab = None
visitados.add(inicio_lab['pos_atual'])
grafo = {}

# Lista de adjacência e elementos visitados
lista_adjacencia = {}
elementos_visitados = set()

while True:
    movs = 0
    for movimento in p_atual['movimentos']:
        if movimento not in visitados:
            # Adiciona a aresta ao grafo
            if p_atual['pos_atual'] not in lista_adjacencia:
                lista_adjacencia[p_atual['pos_atual']] = []
            lista_adjacencia[p_atual['pos_atual']].append(movimento)

            p_atual = movimentar_labirinto(MAZE_NAME, PLAYER_NAME, movimento)
            if p_atual['final']:
                final_lab = p_atual['pos_atual']
            pilha.append(p_atual['pos_atual'])
            visitados.add(p_atual['pos_atual'])
            elementos_visitados.add(p_atual['pos_atual'])
            movs = 1
            break
    print(p_atual)
    print(visitados)

    if movs == 0 and len(pilha) > 1:
        pilha.pop()
        novo_ponto = movimentar_labirinto(MAZE_NAME, PLAYER_NAME, pilha[-1])
        p_atual = novo_ponto
    else:
        if len(pilha) > 1:
            continue
        else:
            break



# Imprime a lista de adjacência
print("Lista de Adjacência:")
for vertice, vizinhos in lista_adjacencia.items():
    print(f"{vertice}: {vizinhos}")

# Executa o BFS
inicio_bfs = inicio_lab['pos_atual']
fim_bfs = final_lab
MenorCaminho = bfs(lista_adjacencia, inicio_bfs, fim_bfs)
print("Menor Caminho:")
print(MenorCaminho)

# Verifica se a quantidade de elementos do menor caminho não muda após percorrer a lista duas vezes
for _ in range(2):
    MenorCaminho = bfs(lista_adjacencia, inicio_bfs, fim_bfs)

if len(MenorCaminho) == len(set(MenorCaminho)):
    print("O menor caminho não mudou após percorrer a lista duas vezes.")
else:
    print("O menor caminho mudou após percorrer a lista duas vezes.")
    
# Adicione esta verificação após o término do loop
if final_lab:
    print(f"A casa onde Final = True é: {final_lab}")
else:
    print("Não foi encontrada nenhuma casa onde Final = True.")
