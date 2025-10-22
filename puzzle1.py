import random
from contextlib import nullcontext
from fileinput import close
import time
import  statistics

import heapq
# Ubung 1 AI


Goal= [1,2,3,4,5,6,7,8,0] #for global usa

def solvablePuzzle(input):
    """
    :param input: array containing the puzzle layout and
    checks it for solvability based on the inversion count (even number == true).
    :return: returns a boolean value indicating whether the puzzle is solvable or not
    """


    arr=[x for x in input if x != 0]
    length = len(arr)
    inv= 0

    for i in range(length):
        for j in range(i+1, length):
            if arr[i] > arr[j]:
                inv= inv +1

    return (inv % 2) == 0


#Tests
#print ("Ergebnis:", solvablePuzzle([2,1,3,4,5,6,7,8,0]))
#print ("Ergebnis:", solvablePuzzle([2,3,1,4,5,6,7,8,0]))


#gnerate random 9 numbers that are solvable
def generatePuzzle():

    """
    This method generates random puzzle arrangements of length 9,
     it also checks if the puzzle is solvable using the previous method.
    :return: returns the solvable puzzle as list of integers.
    """
    while True:
        puzzle= list(range (9))
        random.shuffle(puzzle)
        if solvablePuzzle(puzzle):
            return puzzle


print ("Generated Puzzle: ", generatePuzzle())


#Hamming distance -->

def hamming (puzzle, goal):

    """
    The hamming functions is a heuristic that calculates the hamming distance
    (number of misplaced tiles) that are not in their goal state, excluding the empty tile.
    :param puzzle: the random and solvable puzzle
    :param goal: the predefined goal state
    :return: returns the count of the number of misplaced tiles
    """
    count = 0
    #for i in range(len(puzzle)):
    for i, value in enumerate(puzzle):      # enumerate returns position with the value on it
        if value != goal[i] and value != 0:
            count += 1

    return count


tempTest =[2,3,1,4,5,6,7,8,0]





#print ("Hamming: ", hamming(generatePuzzle(), Goal))
print ("solvable: ", solvablePuzzle(tempTest))
print ("Hamming: ", hamming(tempTest, Goal))



#Manhatten-> abs(currentR - goalR) + abs(currentC - goalC)
def manhattan(puzzle, goal):

    """
    The manhattan distance calculates the sum of vertical and horizontal differences between each tile and it's goal state
    :param puzzle: the random and solvable puzzle
    :param goal: the goal state that was predefined
    :return: the total manhattan distance
    """

    total = 0
    size=3
    # list of postions of goal
    # [0/1 , 1/2 , 2/3 ,.....8/0]
    posG=list(enumerate(goal))
    #print ("Positions goal:2", posG)

    #faster lookup then goal.index[value] -> lookup table
    goalPos = {val: id for id, val in posG}

    for position, value in enumerate(puzzle):
        if value != 0:
            #current
            currentR= position //size
            currentC= position %size

            #goal
            gid= goalPos[value]
            goalR= gid //size
            goalC= gid %size

            #manhattan
            distance = abs(currentR - goalR)+abs(currentC - goalC)
            total = total + distance

            #if value != goal[position]:
                #print(f"Kachel {value}: aktuell idx={position} -> ziel idx={gid}  d={distance}")

    return total

print("Manhattan Dist.: ", manhattan(tempTest, Goal))



#netxt move = cost now + evaluation of distanc(manhattan/ hamming)


#--possible moves
def get_neighbors(state):
    #all possilbe neigbors moves
    neighbors = []
    size = 3
    zero = state.index(0)
    r, c = divmod(zero, size)
    moves = [(-1,0),(1,0),(0,-1),(0,1)]  # oben, unten, links, rechts

    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < size and 0 <= nc < size:
            new = state[:]
            new_idx = nr * size + nc
            new[zero], new[new_idx] = new[new_idx], new[zero]
            neighbors.append(new)
    return neighbors




#g(x) =Cost
#h(x) = estimate to goal
#f(x) = total estimate cost
def algo_a(start,goal, heuristic):
    open_list = []
    # save as tupel with priority 0
    heapq.heappush(open_list, (0, start))
    # dictionary g -> lists not hashable
    g = {tuple(start): 0}
    expanded = 0

    while open_list:
        _, current = heapq.heappop(open_list)
        expanded += 1

        if current == goal:
            return {"steps": g[tuple(current)], "expanded": expanded}

        for neighbor in get_neighbors(current):
            new_g = g[tuple(current)] + 1
            if tuple(neighbor) not in g or new_g < g[tuple(neighbor)]:
                g[tuple(neighbor)] = new_g
                f = new_g + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f, neighbor))

    return {"steps": -1, "expanded": expanded}


print( "algo a_*: ")

#print (algo_a(tempTest, Goal, manhattan))

# second try

from heapq import heappush, heappop


def astar(start, goal, heuristic):
    open_list = []
    heappush(open_list, (0, start))
    closed = set()

    g_cost = {tuple(start): 0}

    #def heuristic(state):
        #return sum(abs((val - 1) % 3 - i % 3) + abs((val - 1) // 3 - i // 3)
                  # for i, val in enumerate(state) if val != 0)
    starttime = time.time()
    while open_list:
        f, current = heappop(open_list)
        current_t = tuple(current)

        if current_t in closed:
            continue
        closed.add(current_t)

        if current == goal:
            endtime = time.time()
            totaltime = endtime - starttime
            #print(f"Time needed: {totaltime:.5f} seconds ")
            return {"steps": g_cost[current_t], "expanded": len(closed), "runtime": round(totaltime, 5)}



        zero = current.index(0)
        x, y = divmod(zero, 3)
        moves = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = current[:]
                new_zero = nx * 3 + ny
                new_state[zero], new_state[new_zero] = new_state[new_zero], new_state[zero]
                new_t = tuple(new_state)
                if new_t not in closed:
                    new_g = g_cost[current_t] + 1
                    f = new_g + heuristic(new_state,goal)
                    heappush(open_list, (f, new_state))
                    g_cost[new_t] = new_g

    return None




#print( algo_a(tempTest, Goal, manhattan))
#print (astar(tempTest, Goal, manhattan))


def test_100 (heuristic, test):

    runtimes=[]
    expanded_nodes=[]


    for y in range(test):
        randomPuzzle= generatePuzzle()
        print(randomPuzzle)

        if solvablePuzzle(randomPuzzle):
            result= astar(randomPuzzle, Goal,heuristic)

            runtimes.append(result["runtime"])
            expanded_nodes.append(result["expanded"])

    avg_time = statistics.mean(runtimes)
    std_time = statistics.stdev(runtimes)
    avg_expanded = statistics.mean(expanded_nodes)
    std_expanded = statistics.stdev(expanded_nodes)

    print(f"--- Results for {heuristic.__name__} ---")
    print(f"Average Runtime: {avg_time:.5f}s ± {std_time:.5f}")
    print(f"Average expanded Nodes: {avg_expanded:.2f} ± {std_expanded:.2f}")
    print()

    return {
        "heuristic": heuristic.__name__,
        "avg_time": avg_time,
        "std_time": std_time,
        "avg_expanded": avg_expanded,
        "std_expanded": std_expanded
    }



test_100(manhattan, 100)
test_100(hamming, 100)

