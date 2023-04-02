import random
import math
import os

class ToTiTo:
    def __init__(self):
        self.tablero = ['-' for _ in range(9)]
        if random.randint(0, 1) == 1:
            self.humano = 'X'
            self.agente = "O"
        else:
            self.humano = "O"
            self.agente = "X"

    def mostrar_tablero(self):
        print("")
        for i in range(3):
            print("  ",self.tablero[0+(i*3)]," | ",self.tablero[1+(i*3)]," | ",self.tablero[2+(i*3)])
            print("")
            
    def tablero_lleno(self,state):
        return not "-" in state

    def es_ganador(self,state,jugador):
        if state[0]==state[1]==state[2] == jugador: return True
        if state[3]==state[4]==state[5] == jugador: return True
        if state[6]==state[7]==state[8] == jugador: return True
        if state[0]==state[3]==state[6] == jugador: return True
        if state[1]==state[4]==state[7] == jugador: return True
        if state[2]==state[5]==state[8] == jugador: return True
        if state[0]==state[4]==state[8] == jugador: return True
        if state[2]==state[4]==state[6] == jugador: return True

        return False

    def verGanador(self):
        if self.es_ganador(self.tablero,self.humano):
            os.system("cls")
            print(f"----------{self.humano} GANADOR----------")
            return True
            
        if self.es_ganador(self.tablero,self.agente):
            os.system("cls")
            print(f"---------- {self.agente} GANADOR----------")
            return True
        
        if self.tablero_lleno(self.tablero):
            os.system("cls")
            print("")
            print("----------Empate----------")
            return True
        return False

    def start(self):
        bot = ComputerPlayer(self.agente)
        human = humano(self.humano)
        while True:
            os.system("cls")
            print(f"   Turno de {self.humano} ")
            self.mostrar_tablero()

            cuadrado = human.human_move(self.tablero)
            self.tablero[cuadrado] = self.humano
            if self.verGanador():
                break
            cuadrado = bot.movimiento_agente(self.tablero)
            self.tablero[cuadrado] = self.agente
            if self.verGanador():
                break
        print()
        self.mostrar_tablero()

class humano:
    def __init__(self,letter):
        self.letter = letter
    
    def human_move(self,state):
        while True:
            cuadrado =  int(input("Ingrese un numero(1-9): "))
            if state[cuadrado-1] == "-":
                break
        return cuadrado-1

class ComputerPlayer(ToTiTo):
    def __init__(self,letter):
        self.agente = letter
        self.humano = "X" if letter == "O" else "O"

    def players(self,state):
        n = len(state)
        x = 0
        o = 0
        for i in range(9):
            if(state[i] == "X"):
                x = x+1
            if(state[i] == "O"):
                o = o+1
        if(self.humano == "X"):
            return "X" if x==o else "O"
        if(self.humano == "O"):
            return "O" if x==o else "X"
    
    def actions(self,state):
        return [i for i, x in enumerate(state) if x == "-"]
    
    def result(self,state,action):
        newState = state.copy()
        jugador = self.players(state)
        newState[action] = jugador
        return newState
    
    def terminal(self,state):
        if(self.es_ganador(state,"X")):
            return True
        if(self.es_ganador(state,"O")):
            return True
        return False

    def minimax(self, state, jugador):
        max_player = self.humano 
        otro_jugador = 'O' if jugador == 'X' else 'X'

        if self.terminal(state):
            return {'posicion': None, 'punteo': 1 * (len(self.actions(state)) + 1) if otro_jugador == max_player else -1 * (
                        len(self.actions(state)) + 1)}
        elif self.tablero_lleno(state):
            return {'posicion': None, 'punteo': 0}

        if jugador == max_player:
            mejor = {'posicion': None, 'punteo': -math.inf}  
        else:
            mejor = {'posicion': None, 'punteo': math.inf} 
        for posible_movimiento in self.actions(state):
            newState = self.result(state,posible_movimiento)
            s_punteo = self.minimax(newState, otro_jugador)  

            s_punteo['posicion'] = posible_movimiento  

            if jugador == max_player: 
                if s_punteo['punteo'] > mejor['punteo']:
                    mejor = s_punteo
            else:
                if s_punteo['punteo'] < mejor['punteo']:
                    mejor = s_punteo
        return mejor
    
    def movimiento_agente(self,state):
        cuadrado = self.minimax(state,self.agente)['posicion']
        return cuadrado

totito = ToTiTo()
totito.start()