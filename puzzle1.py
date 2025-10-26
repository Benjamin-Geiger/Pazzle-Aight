import random
import time
import  statistics
from heapq import heappush, heappop
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




#gnerate random 9 numbers that are solvable
def generatePuzzle():

    """
    This method generates random puzzle arrangements of length 9,
     it also checks if the puzzle is solvable using the previous method.
    :return: returns the solvable puzzle as list of integers
    """
    while True:
        puzzle= list(range (9))
        random.shuffle(puzzle)
        if solvablePuzzle(puzzle):
            return puzzle




#Hamming distance
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


#Tests
#tempTest =[2,3,1,4,5,6,7,8,0]
#print ("Hamming: ", hamming(generatePuzzle(), Goal))
#print ("solvable: ", solvablePuzzle(tempTest))
#print ("Hamming: ", hamming(tempTest, Goal))



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

            #test output
            #if value != goal[position]:
                #print(f"Kachel {value}: aktuell idx={position} -> ziel idx={gid}  d={distance}")

    return total



#next move = cost now + evaluation of distanc(manhattan/ hamming)
#--possible moves
def get_neighbors(state):

    """
    Generates all possible next puzzle states by moving the empty tile (0)
    one step up, down, left, or right, if possible.
    Used by the A* algorithm to explore the search tree.
    :param state: current state of the puzzle
    :return: list of all valid successor states (each also a list of 9 numbers).
    """
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
def astar(start, goal, heuristic):

    """
    Performs the A* search algorithm to find the shortest path
    from a start state to the goal state using the given heuristic.
    :param start: starting configuration of 8-puzzle
    :param goal: goal state of 8-puzzle
    :param heuristic:  heuristic function used (manhattan or hamming)
    :return:contains steps, number of expanded nodes, and runtime
    """
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
            return {"steps": g_cost[current_t], "expanded": len(closed), "runtime": round(totaltime, 5)}



        for neighbor in get_neighbors(current):
            new_t = tuple(neighbor)
            if new_t not in closed:
                # Calculate the cost to reach the neighbor
                new_g = g_cost[current_t] + 1
                f = new_g + heuristic(neighbor, goal)
                # Push new state to open list
                heappush(open_list, (f, neighbor))
                g_cost[new_t] = new_g


    return None

#Tests
#print( algo_a(tempTest, Goal, manhatten))
#print (astar(tempTest, Goal, manhatten))


def test_100 (heuristic, test):

    """
    Tests the A* algorithm on 100 random solvable 8-puzzles using the heuristic it gests as input .
    And measures and calculates average runtime and memory usage, of the  A* with the given heuristic..
    :param heuristic: either manhatten or hamming
    :param test: the number of test done in the function
    :return: average and standard deviation of runtime and expanded nodes
    """
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

input("Press Enter to exit...")
