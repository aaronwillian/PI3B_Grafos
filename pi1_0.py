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

labirinto = obter_labirinto()
print(labirinto)

def iniciar_labirinto(nome_labirinto, id_jogador):
  urllib3.disable_warnings()
  url_iniciar = "https://gtm.delary.dev/iniciar"

  dados_requisicao = {
      "id": id_jogador,
      "labirinto": nome_labirinto
  }

  resposta_iniciar = requests.post(url_iniciar, json=dados_requisicao, verify = False)

  if resposta_iniciar.status_code == 200:
      print("Resposta do /iniciar:")
      return resposta_iniciar.json()
  else:
      print(f"A solicitação falhou com o código de status {resposta_iniciar.status_code}")
      return None
  
def movimentar_labirinto(nome_labirinto,id_jogador, nova_posicao):
  urllib3.disable_warnings()
  url_movimentar = "https://gtm.delary.dev/movimentar"

  dados_requisicao = {
      "id": id_jogador,
      "labirinto": nome_labirinto,
      "nova_posicao": nova_posicao
  }
  resposta_movimentar = requests.post(url_movimentar, json=dados_requisicao, verify = False)

  if resposta_movimentar.status_code == 200:
      print("Resposta do /movimentar:")
      return resposta_movimentar.json()
  else:
      print(f"A solicitação falhou com o código de status {resposta_movimentar.status_code}")
      return None
  
inicio_lab = iniciar_labirinto('maze-sample','Lucas')
print(inicio_lab)

mov_lab = movimentar_labirinto('maze-sample', 'Lucas',3)['movimentos']
print(mov_lab)


# ---------------  Iniciar Lab -------------------------------------------
inicio_lab = iniciar_labirinto('maze-sample','Lucas')
visitados = set()
caminho = [(inicio_lab['pos_atual'])]
pilha = [(inicio_lab['pos_atual'])]
pilha.extend(inicio_lab.get('movimentos'))
visitados.add((inicio_lab['pos_atual']))
print(pilha)
movimentos_visitados = {}
while pilha:
  posicao_atual = pilha[-1]
  visitados.add(posicao_atual)
  caminho.append(posicao_atual)
  mov_lab = movimentar_labirinto('maze-sample', 'Lucas', posicao_atual)
  movimentos = mov_lab.get('movimentos')

  if mov_lab.get('final') == True:
    print(f'Caminho final {caminho}')
    break
  if all(movimento in visitados for movimento in movimentos):
    caminho.pop()
    pilha.pop()
    movimento_anterior = pilha.pop()
    posicao_atual = caminho[-1]
    pilha.append(movimento_anterior)
    movimentar_labirinto('maze-sample', 'Lucas', posicao_atual)
    movimentos_visitados[posicao_atual] = movimento_anterior

  for movimento in movimentos:
    if movimento not in visitados and movimento not in movimentos_visitados:
      pilha.append(movimento)
    else:
      continue
  print(f'Posição atual: {posicao_atual}')
  print(f'Pilha{pilha}')
  print(f'Caminho{caminho}')
  print(f'Visitados: {visitados}')

def dfs_retrocesso(posicao_atual, visitados, caminho):
    # Adicione a posição atual ao caminho e aos visitados
    caminho.append(posicao_atual)
    visitados.add(posicao_atual)

    # Obtenha os movimentos disponíveis a partir da posição atual
    mov_lab = movimentar_labirinto('maze-sample', 'Lucas', posicao_atual)['movimentos']

    # Recursivamente explore os movimentos disponíveis
    for movimento in mov_lab:
        if movimento not in visitados:
            dfs_retrocesso(movimento, visitados, caminho)

    # Se todas as posições adjacentes já foram visitadas e não encontrou a saída, retroceda no caminho
    if posicao_atual != inicio_lab['pos_saida']:
        caminho.pop()
        
inicio_lab = iniciar_labirinto('maze-sample','Lucas')
print(inicio_lab)
visitados = set()
fila = deque([(inicio_lab['pos_atual'])])
fila.extend(inicio_lab.get('movimentos'))
while fila:
  posicao_atual = fila.popleft()
  print(posicao_atual)
  print(fila)
  visitados.add(posicao_atual)
  print(visitados)
  no_pai = posicao_atual
  nova_posicao = fila[0]
  mover = movimentar_labirinto('maze-sample', 'Lucas', nova_posicao)
  fila.extend(mover.get('movimentos'))
  for movimento in mover.get('movimentos'):
    if no_pai in mover.get('movimentos'):
      print(no_pai)
      mover = movimentar_labirinto('maze-sample','Lucas', no_pai)