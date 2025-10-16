import heapq

array = [2, 3, 1, 0, 5, 8, 6, 7, 4]

def check_if_solvable(array):
    inversion_count=0
    check_value=0



    for i in range(0, len(array)):
        for j in range(i+1, len(array)):
            if array[i] != check_value and array[j] != check_value and array[i]>array[j]:
                inversion_count+=1
    return inversion_count

print(check_if_solvable(array))