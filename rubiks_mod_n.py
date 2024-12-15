import math
import copy
import random

def file_output(data_output, file_name):
    with open(file_name,'w',encoding='utf-8') as f:
        for l in data_output:
           f.write(','.join([str(x) for x in l])+'\n')

def file_input(file_name):

    with open(file_name,encoding='utf-8',mode = 'r') as f:
        lines = f.readlines()
    data = [x.split(',') for x in lines]
    #data.pop(0)
    for row in data:
        row[-1] = row[-1].replace('\n','')
    return data

def gcd(a,b):

    q = int(a/b)
    r = a % b

    if r == 0:
        return b

    return gcd(b,r)

def random_alg(alg_len):
    moves = ['R','L','U','D','F','B']
    types = [' ',"' ",'2 ']
    alg = ''

    randI = -1
    for move in range(alg_len):
        nextI = randI
        while nextI == randI:
            nextI = int(random.random()*6)
        randI = nextI

        type = int(random.random()*3)
        alg = alg + moves[randI] + types[type]

    return alg

def insert_prime_powers(n,n_index,n_prime_powers,curr_alg,n_algs,curr_unit):

    if n_index == len(n_prime_powers):

        n_algs.append([curr_unit,curr_alg])
        return n_algs


    for curr_multiplier in range(n_prime_powers[n_index][1]):
        if n_index == 0:
            print("Main Cycle ",curr_multiplier," of ", n_prime_powers[n_index][1])
        n_algs = insert_prime_powers(n,n_index+1,n_prime_powers,curr_alg + n_prime_powers[n_index][5][curr_multiplier],n_algs,curr_unit)
        curr_unit = (curr_unit * n_prime_powers[n_index][4]) % n

    return n_algs

def add_multipliers(n,n_prime_powers):

    for power in n_prime_powers:
        #print(power)
        n_over = n // power[0]
        n_over_mult = n_over
        while (n_over_mult + 1) % power[0] != power[3]:
            #print((n_over_mult + 1) % power[0],power[3])
            #print(n_over_mult)
            n_over_mult += n_over

        power.append(n_over_mult+1)
        power.append([])
        curr_alg = ''
        for power_rep in range(power[1]):
            power[-1].append(curr_alg)
            curr_alg += power[2]
            #curr_alg = optimize_alg(curr_alg)

    return n_prime_powers

#def optimize_alg(alg_to_optimize):

   # return random_alg(18)

def compress(n_algs,symbol_index,new_symbols):

    freq_tracker = [0]
    b = len(symbol_index) + len(new_symbols)

    for unit in n_algs:
        unit[1] = [symbol_index.index(unit[1][x]) for x in range(len(unit[1]))]
        for start_symbol in range(len(unit[1])-1):
            freq_tracker = freq_insert(freq_tracker,unit[1][start_symbol],unit[1][start_symbol+1],b)

    compression = []

    for sym in new_symbols:
        print('Compress',sym)
        max_index = freq_tracker.index(max(freq_tracker))
        max_split = [max_index//b,max_index%b]
        compression.append([sym,symbol_index[max_split[0]]+symbol_index[max_split[1]]])
        for unit in n_algs:
            for start_symbol in range(len(unit[1])-2,-1,-1):
                if unit[1][start_symbol] == max_split[0] and unit[1][start_symbol+1] == max_split[1]:

                    unit[1].pop(start_symbol+1)
                    unit[1][start_symbol] = len(symbol_index)

                    if start_symbol > 0:
                        freq_tracker[unit[1][start_symbol-1]*b+max_split[0]] -= 1
                        freq_tracker = freq_insert(freq_tracker,unit[1][start_symbol-1],unit[1][start_symbol],b)

                    if start_symbol + 1 < len(unit[1]):
                        freq_tracker[max_split[1]*b+unit[1][start_symbol+1]] -= 1
                        freq_tracker = freq_insert(freq_tracker,unit[1][start_symbol],unit[1][start_symbol+1],b)

        symbol_index.append(sym)
        freq_tracker[max_split[0]*b+max_split[1]] = 0

    for unit in n_algs:
        unit[1] = ''.join([symbol_index[unit[1][x]] for x in range(len(unit[1]))])
    return n_algs, compression

def freq_insert(freq_tracker,fb1,fb0,b):
    duo_index = fb1*b + fb0
    while len(freq_tracker) <= duo_index:
        freq_tracker.append(0)
    freq_tracker[duo_index] += 1
    return freq_tracker

"""
# simple case for early testing
n = 100
n_prime_powers = [
    [25,11,'F D’ R’ U’ D B D R F2 L2 D’ B2 L2 U’ D R2 D2 ',2],
    [4,2,'U R’ F D’ F2 D F’ R U F2 U’ F2 U F2 U’ F2 U F2 ',3]
]
"""

"""
# medium case
n = 9360
n_prime_powers = [

    [13,7,"L2 U F' R2 F U' L2 U F' R2 F U' L D2 R U F U R' F D' L' F' D' L ",2],
    [5,4,"U2 L F' D R F D R2 D2 L' U' F' U ",2],
    [9,6,"R' U R2 D L' B2 L D' R2 U' R U' ",2],
    [16,4,"U' L2 F2 B L B' U' L' F2 L' F' L' ",3],
    [16,2,"U' F B' R U' B R' U F' B L' U B' L ",7]

]
"""

# maximum case
n = 2424240
n_prime_powers = [
    [37,19,"U2 L F' R B L2 D2 B R' F L B2 R' F D' L' F' D' L2 D2 R U F U ",2], #19
    [13,12,"L2 U F' R2 F U' L2 U F' R2 F U' L D2 R U F U R' F D' L' F' D' L ",2], #12
    [7,6,"R' B2 R U' F2 U R' B2 R U' F2 U2 R U R U' R2 U2 R L F R' F' L' U ",3], #6
    [5,4,"U2 L F' D R F D R2 D2 L' U' F' U ",2],
    [9,6,"R' U R2 D L' B2 L D' R2 U' R U' ",2],#6
    [16,4,"U' L2 F2 B L B' U' L' F2 L' F' L' F ",3],
    [16,2,"U' F B' R U' B R' U F' B L' U B' L ",7]
]


replacer = [[" ",""],["R'",'r'],["L'","l"],["U'","u"],["F'","f"],["D'","d"],["B'","b"],["F2","FF"],["U2","UU"],["R2","RR"],["L2","LL"],["B2","BB"],["D2","DD"]]
symbol_index = ['R','r','L','l','U','u','D','d','F','f','B','b']
new_symbols = ['A','a','C','c','E','e','G','g','H','h','I','i','J','j','K','k','M','m','N','n','O','o','P','p','Q','q'
               ,'S','s','T','t','V','v','W','w','X','x','Y','y','Z','z'
               ,'0','1','2','3','4','5','6','7','8','9'
               ,'!','@','#','$','%','^','&','*','(',')','-','_','=','+']
#new_symbols = ['A','a']

n_index = 0
n_algs = []
curr_unit = 1

#STEP 1: MAKE BASE ALGS
if False:

    n_prime_powers = add_multipliers(n,n_prime_powers)

    step_1_out = []

    for i, n_pow in enumerate(n_prime_powers):
        for j, n_pow_alg in enumerate(n_pow[5]):
            step_1_out.append([i,j,n_pow_alg])

    file_output(step_1_out,'rubiks_mod_n_base_algs.csv')


#STEP 2: OPTIMIZE BASE ALGS

# optimize the algs in rubiks_mod_n_base_algs.csv


#STEP 3: MAKE ALL UNIT ALGS
if False:

    n_prime_powers = add_multipliers(n,n_prime_powers)

    step_3_in = file_input('rubiks_mod_n_base_algs.csv')

    for alg_in in step_3_in:
        n_prime_powers[int(alg_in[0])][5][int(alg_in[1])] = alg_in[2]

    n_algs = insert_prime_powers(n,0,n_prime_powers,'',[],1)

    file_output(n_algs,'rubiks_mod_n_unit_algs.csv')


#STEP 4: OPTIMIZE UNIT ALGS

# optimize the algs in rubiks_mod_n_unit_algs.csv

#STEP 5: OPTIMIZE UNIT ALGS
if True:

    step_5_in = file_input('rubiks_mod_n_unit_algs.csv')
    for unit in n_algs:
        for rep in replacer:
            unit[1] = unit[1].replace(rep[0],rep[1])

    n_algs, compression = compress(n_algs,symbol_index,new_symbols)

    file_output(n_algs,'n_alg.csv')
    file_output(compression,'n_alg_compress.csv')
