import numpy as np
import sys
import heapq
import copy
import re
import time 

def tile_misplaced_heuristic(matrice, final_state):
    misplaced_tiles = 0
    if (len(matrice) == len(final_state)):
        i = 0
        while ( i < len(matrice)):
            j = 0
            while ( j < len(matrice)):
                if (matrice[i][j] != final_state[i][j]): 
                    misplaced_tiles += 1
                j += 1
            i += 1
    else:
        return -1
    return misplaced_tiles

def manathan_distance_heuristic(matrice, final_state):
    manathan_distance = 0
    for i in range(len(final_state)):
        for j in range(len(final_state)):
            for ibis in range(len(matrice)):
                for jbis in range(len(matrice)):
                    if (matrice[ibis][jbis] == final_state[i][j] and matrice[ibis][jbis] != 0):
                        manathan_distance += abs(jbis - j) + abs(ibis - i)
                        break
    return manathan_distance

def find_the_final_state(sizeofpuzzle):
    final_state = np.full((sizeofpuzzle, sizeofpuzzle), 0)
    biggest_number = (sizeofpuzzle * sizeofpuzzle)
    start_number = 1
    left = 0
    right = sizeofpuzzle - 1
    top = 0
    bottom = sizeofpuzzle - 1
    while start_number < biggest_number:
        for i in range(left, right + 1):
            final_state[top][i] = start_number
            start_number += 1
            if( start_number == biggest_number):
                break
        top += 1
        for i in range(top, bottom + 1):
            if( start_number == biggest_number):
                break
            final_state[i][right] = start_number
            start_number += 1

        right -= 1
        for i in range(right, left - 1, -1):
            if( start_number == biggest_number):
                break
            final_state[bottom][i] = start_number
            start_number += 1
        bottom -= 1
        for i in range(bottom, top - 1, -1):
            if( start_number == biggest_number):
                break
            final_state[i][left] = start_number
            start_number += 1
        left += 1
    return final_state

def A_star_search(matrice, heuristic):

    matrice_goal = find_the_final_state(len(matrice)).tolist()

    opened_list = []
    if (heuristic == 1):
        heapq.heappush(opened_list, (0, 0 + manathan_distance_heuristic(matrice, matrice_goal), matrice))
    elif (heuristic == 2):
        heapq.heappush(opened_list, (0, 0 + tile_misplaced_heuristic(matrice, matrice_goal), matrice))
    elif (heuristic == 3):
        heapq.heappush(opened_list, (0, 0 + linear_conflit(matrice, matrice_goal), matrice))

    closed_list = {tuple(map(tuple, matrice))}
    already = {tuple(map(tuple, matrice))}
    path = {}
    complexity_in_time = 0
    max_states_in_memory = 0
    start_time = time.time()
    while opened_list:
        smaller = False
        g, _, currentstate = heapq.heappop(opened_list)
        complexity_in_time += 1
        current_memory_states = len(opened_list) + len(closed_list)
        if current_memory_states > max_states_in_memory:
            max_states_in_memory = current_memory_states
        if (currentstate == matrice_goal):
            #ecrire toute les info a donner pour the end 
            path[g] = tuple(map(tuple, currentstate))
            end_time = time.time()
            for i in path:
                print(np.atleast_2d(path[i]))            
            print("Complexité(Time)", complexity_in_time)
            print("Complexité(Size)", max_states_in_memory)
            print("le temps ecoulé,", round(end_time - start_time, 2), "seconds")
            print('le nombre de mouvement requis pour effectuer le puzzle: ', len(path))
            return
        
           
        if (heuristic == 1):
            if (g in path and manathan_distance_heuristic(path[int(g)], matrice_goal) < manathan_distance_heuristic(currentstate, matrice_goal)):
                smaller = True 
        elif (heuristic == 2):
            if (g in path and tile_misplaced_heuristic(path[int(g)], matrice_goal) < tile_misplaced_heuristic(currentstate, matrice_goal)):
                smaller = True
        elif (heuristic == 3):
            if (g in path and linear_conflit(path[int(g)], matrice_goal) < linear_conflit(currentstate, matrice_goal)):
                smaller = True

        closed_list.add(tuple(map(tuple, currentstate)))                
        if (smaller == True):
            continue
        for neighboor in get_neigboor(currentstate):        
            if (tuple(map(tuple, neighboor)) in closed_list):
               continue        
            if smaller == False:
                path[g] = tuple(map(tuple, currentstate)) 
            tentative_g = g + 1
            if (heuristic == 1):
                f = tentative_g + manathan_distance_heuristic(neighboor, matrice_goal) 
            elif (heuristic == 2):
                f = tentative_g + tile_misplaced_heuristic(neighboor, matrice_goal) 
            elif (heuristic == 3):
                f = tentative_g + linear_conflit(neighboor, matrice_goal)
            heapq.heappush(opened_list, (tentative_g, f, neighboor))

    return (print('pas de chemin trouvé'))

def find_element_index(array, element):
    # Parcourir chaque ligne
    for i in range(len(array)):
        # Parcourir chaque colonne de la ligne
        for j in range(len(array[i])):
            # Vérifier si l'élément correspond à l'élément recherché
            if array[i][j] == element:
                return (i, j)  # Retourner l'index (ligne, colonne)
    return None

def get_neigboor(current_state):
    x, y = find_element_index(current_state, 0)
    neighboor = []

    for i in range(0, 4):
        tmp_state = copy.deepcopy(current_state)

        if i == 0: # en haut
            new_x = x - 1
            if (new_x >= 0 and new_x < len(tmp_state)) :
                tmp_change = tmp_state[new_x][y]
                tmp_state[x][y] = tmp_change
                tmp_state[new_x][y] = 0
                neighboor.append(tmp_state)
        elif i == 1: ## en bas
            new_x = x + 1
            if (new_x >= 0 and new_x < len(tmp_state)) :
                tmp_change = tmp_state[new_x][y]
                tmp_state[x][y] = tmp_change
                tmp_state[new_x][y] = 0
                neighboor.append(tmp_state)
        elif i == 2: # a droite
            new_y = y + 1
            if (new_y >= 0 and new_y < len(tmp_state)) :
                tmp_change = tmp_state[x][new_y]
                tmp_state[x][y] = tmp_change
                tmp_state[x][new_y] = 0
                neighboor.append(tmp_state)       
        elif i == 3: #a gauche
            new_y = y - 1
            if (new_y >= 0 and new_y < len(tmp_state)) :
                tmp_change = tmp_state[x][new_y]
                tmp_state[x][y] = tmp_change
                tmp_state[x][new_y] = 0
                neighboor.append(tmp_state)
    return neighboor

def parse_args(fichier):
    try:
        file = open(fichier)
        array = file.readlines()
        for i in range(len(array)):
            array[i] = re.sub(r'\s{2,}', ' ', array[i])
        array = [element for element in array if element[0] != '#']
        for i in range(len(array)):
            array[i] = re.sub(r'#.*', '', array[i])
            array[i] = array[i].replace('\n', '')
            array[i] = array[i].strip()
        taille = int(array[0])
        array.remove(array[0])
        matrice = []
        real_list = [i for i in range(taille * taille)]
        checked_sort = []
        for element in array:
            elements = element.split(' ')
            if (len(elements) == taille):
                tab = []
                for number in elements:
                    tab.append(int(number))
                    checked_sort.append(int(number))
                matrice.append(tab)
            else:
                print(f"Erreur dans le board veuiller verifier")
                return None   
        checked_sort.sort()
        if (checked_sort != real_list):
            print(f"Erreur dans le board veuiller verifier les nombres")
            return None  
        return matrice
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{fichier}' n'existe pas.")
        return None

def linear_conflit(matrice, final_state):
    conflit = 0
    i = 0
    while (i < len(matrice)):
        j = 0
        while ( j < len(matrice)):
            y = j + 1
            if (matrice[i][j] in final_state[i]):
                position = matrice[i].index(matrice[i][j])
                position2 = final_state[i].index(matrice[i][j])
                while(y < len(matrice)):
                    if (matrice[i][y] in final_state[i]):
                        positionbis = final_state[i].index(matrice[i][y])
                        if ( position and position2 and ((position < y ) == (positionbis < position2))):
                            conflit += 1
                    y +=1
            j += 1
        i +=1

    return manathan_distance_heuristic(matrice, final_state) + 2 * conflit

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            print("Choose between 1 : manathan_distance, 2 : Misplaced_tiles and 3 : The linear conflit")
            valeur = input()
            if (int(valeur) > 3 or int(valeur) < 1):
                exit("Incorrect number in the imput value")
            matrice = parse_args(sys.argv[1])
            A_star_search(matrice, int(valeur))
        elif len(sys.argv) == 1:
            print("Choose between 1 : manathan_distance, 2 : Misplaced_tiles and 3 : The linear conflict")
            valeur = input()
            if (int(valeur) > 3 or int(valeur) < 1):
                exit("Incorrect number in the imput value")
            matrice = [[1, 2, 3],
                    [8, 0, 4],
                    [6, 7 ,5]]
            A_star_search(matrice, int(valeur))
        else:
            print("Incorrect number of argument")
    except:
        print('on attend un chiffre')

# ajouter une complecity in size