import Env
import threading
import time
import random
import cPickle as pickle



f = open('Q.pckl', 'rb')
Q = pickle.load(f)

f = open('Q.pckl', 'wb')


discount = 0.3
actions = Env.actions
states = []

for i in range(Env.x):
    for j in range(Env.y):
        states.append((i, j))

def do_action(action):
    s = Env.player
    r = -Env.score
    if action == actions[0]:
        Env.try_move(0, -1)
    elif action == actions[1]:
        Env.try_move(0, 1)
    elif action == actions[2]:
        Env.try_move(-1, 0)
    elif action == actions[3]:
        Env.try_move(1, 0)
    else:
        return
    s2 = Env.player
    r += Env.score
    return s, action, r, s2


def max_Q(s):
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc
    pickle.dump(Q, f)
    print Q

def run():
    global discount
    time.sleep(1)
    alpha = 1
    t = 1
    while True:
        # Pick the right action
        s = Env.player
        max_act, max_val = max_Q(s)
        (s, a, r, s2) = do_action(max_act)

        # Update Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + discount * max_val)


        # Check if the game has restarted
        t += 1.0
        if Env.has_restarted():
            Env.restart_game()
            time.sleep(0.01)
            t = 1.0

        # Update the learning rate
        alpha = pow(t, -0.1)

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(0.1)


t = threading.Thread(target=run)
t.daemon = True
t.start()
Env.start_game()
f.close()
