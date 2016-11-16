import random
import math

class Cuatro_en_linea():
    def __init__(self, jugador1, jugador2,width=8, height=8):
        self.width = width
        self.height = height
        self.tablero = [[] for i in range(width)]
        self.player1 = jugador1
        self.player2 = jugador2
        self.player1_turn = random.choice([True, False])
        self.pieza_player_1 = '1'
        self.pieza_player_2 = '0'

    def jugar_ficha(self,color,posicion):
        if posicion > -1 and posicion < self.width:
            if len(self.tablero[posicion]) < self.height:
                self.tablero[posicion].append(color)
            else:
                print "error"
        else:
            print "error"

    def jugador_gano(self,color):
        for i in range(len(self.tablero)):
            for j in range(self.width):
                try:
                    if all(self.tablero[i][j+k] == color for k in range(4)):
                        return True
                except IndexError:
                    pass
                try:
                    if all(self.tablero[i+k][j] == color for k in range(4)):
                        return True
                except IndexError:
                    pass
                try:
                    if all(self.tablero[i+k][j+k] == color for k in range(4)):
                        return True
                except IndexError:
                    pass
        return False

    def imprimir_tablero(self):
        for i in range(self.height-1, -1, -1):
            colores = []
            for j in range(len(self.tablero)):
                try:
                    color = self.tablero[j][i]
                except IndexError:
                    color = '-'

                colores.append(color)
            print "".join(colores)

    def tablero_lleno(self):
        return not any([len(columna) < self.height for columna in self.tablero])

    def jugar(self):
        self.player1.start_game(self.pieza_player_1)
        self.player2.start_game(self.pieza_player_2)
        while True:
            if self.player1_turn:
                player, char, other_player = self.player1, self.pieza_player_1, self.player2
            else:
                player, char, other_player = self.player2, self.pieza_player_2, self.player1
            space = player.move(self.tablero)
            self.jugar_ficha(char,space)
            #for columna in self.tablero:
            #    print columna
            if self.jugador_gano(char):
                player.reward(1, self.tablero)
                other_player.reward(-1, self.tablero)
                return char
            if self.tablero_lleno(): # tie game
                player.reward(0.5, self.tablero)
                other_player.reward(0.5, self.tablero)
                return ' '
            other_player.reward(0, self.tablero)
            self.player1_turn = not self.player1_turn

class Player(object):
    def __init__(self,height=8, width=8):
        self.breed = "random"
        self.height = height
        self.width = width

    def reward(self, value, tablero):
        pass

    def start_game(self, char):
        pass

    def move(self, tablero):
        return random.choice(self.available_moves(tablero))

    def available_moves(self, tablero):
        return [i for i in range(self.width) if len(tablero[i]) < self.height]


class QLearningPlayer(Player):
    def __init__(self,estrategia,height=8, width=8, alpha=0.3, gamma=0.9):
        self.breed = "Qlearner"
        self.harm_humans = False
        self.q = {} # (state, action) keys: Q values
        #self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for future rewards
        self.height = height
        self.width = width
        self.estrategia = estrategia

    def start_game(self, char):
        self.last_board = (' ',)*9
        self.last_move = None

    def getQ(self, state, action):
        # encourage exploration; "optimistic" 1.0 initial values
        if self.q.get((state, action)) is None:
            self.q[(state, action)] = 1.0
        return self.q.get((state, action))

    def move(self, board):
        self.last_board = tuple(tuple(x) for x in board)
        actions = self.available_moves(board)
        qs = [self.getQ(self.last_board, a) for a in actions]
        i = self.estrategia.elegir_accion(qs)
        self.last_move = actions[i]
        return actions[i]

    def reward(self, value, board):
        if self.last_move:
            self.learn(self.last_board, self.last_move, value, tuple(tuple(x) for x in board))

    def learn(self, state, action, reward, result_state):
        prev = self.getQ(state, action)
        maxqnew = max([self.getQ(result_state, a) for a in self.available_moves(state)])
        self.q[(state, action)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev)


class estrategia_greedy():
    def __init__(self,epsilon=0.1):
        self.epsilon = epsilon

    def elegir_accion(self, qs):
        if random.random() < self.epsilon: # explore!
            return random.choice(range(len(qs)))
        maxQ = max(qs)
        if qs.count(maxQ) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(qs)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)
        return i

class estrategia_e_first():
    def __init__(self,epsilon=0.1,cantidad_trials=10000):
        self.epsilon = epsilon
        self.cantidad_trials = cantidad_trials
        self.contador = 0

    def elegir_accion(self, qs):
        if self.contador < (self.epsilon*self.cantidad_trials)/100: # explore!
            self.contador += 1
            return random.choice(range(len(qs)))
        maxQ = max(qs)
        if qs.count(maxQ) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(qs)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)
        return i

class estrategia_softmax():
    def __init__(self,temperatura_inicial=0.1):
        self.temperatura_inicial = temperatura_inicial
        self.contador = 1

    def elegir_accion(self, qs):
        #levemente turbio
        #calculo la temperatura
        self.contador += 1
        temperatura = self.temperatura_inicial / math.log(self.contador)
        #calculo la probabilidad de tomar cada accion
        probabilidades = [math.exp(qs[i]/(temperatura*1.0)) for i in range(len(qs))]
        probabilidad_total = sum(probabilidades)
        probabilidades = [probabilidad/probabilidad_total for probabilidad in probabilidades]
        r = random.random()
        index = 0
        while r >= 0 and index < len(probabilidades):
            r -= probabilidades[index]
            index += 1
        return index -1

def print_promedios(resultados):
    contador = 0
    suma = 0
    VELOCIDAD_DE_SAMPLEO = 40
    limite = len(resultados) // VELOCIDAD_DE_SAMPLEO
    for resultado in resultados:
        contador += 1
        suma += resultado
        if contador == limite:
            print suma
            suma = 0
            contador = 0



if __name__ == "__main__":
    resultado_X = 0
    resultado_O = 0
    p1 = QLearningPlayer(estrategia_greedy())
    p2 = Player()
    resultados = []
    for i in range(10000):
        t = Cuatro_en_linea(p1, p2)
        resultado = t.jugar()
        if resultado == '1':
            resultados.append(1)
            resultado_X += 1
        if resultado == '0':
            resultados.append(0)
            resultado_O += 1
    print_promedios(resultados)
    #print "Cantidad De Veces que gano Qlearner: " + str(resultado_X)
    #print "Cantidad De Veces que gano Random: " + str(resultado_O)

