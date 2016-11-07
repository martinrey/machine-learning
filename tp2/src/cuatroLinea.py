import random

class Cuatro_en_linea():
    def __init__(self, jugador1, jugador2,width=8, height=8):
        self.width = width
        self.height = height
        self.tablero = [[] for i in range(width)]
        self.player1 = jugador1
        self.player2 = jugador2
        self.player1_turn = random.choice([True, False])

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
            contador = 0
            for j in range(len(self.tablero[i])):
                if self.tablero[i][j] == color:
                    contador += 1
                else:
                    contador = 0
                if contador == 4:
                    print "Gano " + color
                    return True
        #TODO: falta chequear si en una fila hay cuatro en linea y si en las diagonales hay
        return False

    def tablero_lleno(self):
        return not any([len(columna) < self.height for columna in self.tablero])

    def jugar(self):
        self.player1.start_game('X')
        self.player2.start_game('O')
        while True:
            if self.player1_turn:
                player, char, other_player = self.player1, 'X', self.player2
            else:
                player, char, other_player = self.player2, 'O', self.player1
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
    def __init__(self,height=8, width=8, epsilon=0.2, alpha=0.3, gamma=0.9):
        self.breed = "Qlearner"
        self.harm_humans = False
        self.q = {} # (state, action) keys: Q values
        self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for future rewards
        self.height = height
        self.width = width

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

        if random.random() < self.epsilon: # explore!
            self.last_move = random.choice(actions)
            return self.last_move
        qs = [self.getQ(self.last_board, a) for a in actions]
        maxQ = max(qs)

        if qs.count(maxQ) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        self.last_move = actions[i]
        return actions[i]

    def reward(self, value, board):
        if self.last_move:
            self.learn(self.last_board, self.last_move, value, tuple(tuple(x) for x in board))

    def learn(self, state, action, reward, result_state):
        prev = self.getQ(state, action)
        maxqnew = max([self.getQ(result_state, a) for a in self.available_moves(state)])
        self.q[(state, action)] = prev + self.alpha * ((reward + self.gamma*maxqnew) - prev)

if __name__ == "__main__":
    resultado_X = 0
    resultado_O = 0
    p1 = QLearningPlayer()
    p2 = Player()
    for i in range(1000):
        t = Cuatro_en_linea(p1, p2)
        resutlado = t.jugar()
        if resutlado == 'X':
            resultado_X += 1
        if resutlado == 'O':
            resultado_O += 1
    print "Cantidad De Veces que gano Qlerner: " + str(resultado_X)
    print "Cantidad De Veces que gano Random: " + str(resultado_O)
