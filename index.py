import threading
import time
from rich.panel import Panel
from rich.console import Console
from rich import print

title_style = "bold underline"
option_style = "bold cyan"
success_style = "bold green"

travessa = 0
semaforo_travessa = threading.Semaphore(1)
semaforo_cozinheiro = threading.Semaphore(0)

console = Console()

texto = "\nA aplicação desenvolvida em Python faz a criação de N threads/canibais que irão se alimentar unicamente de travessas (de pessoas, possivelmente...) cozinhadas pelo renomado chefe Érick Jacquin. Sem mais enrolações digite o número de threads/canibais que irão se alimentar e o número de travessas que Érick Jacquin irá cozinhar após cada cochilo interrompido por um canibal faminto 😡\n"
print(Panel(
    texto, title=f"[{title_style}]🤨 Alimentando Canibais com Felipe e Jonas 🤨[/{title_style}]"))

N_CANIBAIS = int(console.input(
    f'[{title_style}] Digite a quantidade de canibais: '))
CAPACIDADE_TRAVESSA = int(console.input(
    f'[{title_style}] Digite a quantidade de travessas cozinhadas após cada cochilo: '))

nome_canibais = {
    0: "Picolino",
    1: "Estapafúrdio",
    2: "Tremendão",
    3: "Zé Preguiça",
    4: "Cabeça de Melão",
    5: "Risadinha",
    6: "Lunático",
    7: "Fuzuê",
    8: "Esparrela",
    9: "Chicleteiro"
}


def cozinheiro(st=False):
    global travessa
    while True:
        semaforo_cozinheiro.acquire()  # Espera até que seja necessário cozinhar
        console.print(f'[{option_style}]Érick Jacquin acordando... 😴🥱')
        # time.sleep(1)
        console.print(f'[{option_style}]Colocando tâmpero na travessa...')
        # time.sleep(1)
        console.print(f'[{option_style}]Travessas cozinhadas 😎')
        travessa = CAPACIDADE_TRAVESSA  # Enche a travessa

        semaforo_travessa.release()  # Garante acesso exclusivo à travessa


def comer(id, travessa):
    console.print(
        f'[{option_style}]Canibal {nome_canibais[id]}-({id}) está se alimentando... Respeitam o momento dele!')
    # time.sleep(1)
    console.print(
        f'[{option_style}]Canibal {nome_canibais[id]}-({id}) se alimentou 😋')
    return travessa-1


def canibal(id):
    global travessa
    while True:
        semaforo_travessa.acquire()
        if travessa == 0:
            time.sleep(2)
            console.print(
                f'[{option_style}]Canibal {nome_canibais[id]}-({id}) está com muita fome 😢')
            semaforo_cozinheiro.release()
            semaforo_travessa.acquire()
            travessa = comer(id, travessa)
            console.print(
                f'[{option_style}]Restam apenas {travessa} travessas\n')
            semaforo_travessa.release()
        else:
            travessa = comer(id, travessa)
            console.print(
                f'[{option_style}]Restam apenas {travessa} travessas\n')
            semaforo_travessa.release()

        time.sleep(2)


threading.Thread(target=cozinheiro, args=[True]).start()
for i in range(N_CANIBAIS):
    threading.Thread(target=canibal, args=[i]).start()
