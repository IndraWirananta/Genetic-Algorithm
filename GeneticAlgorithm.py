import csv
import math
import random
import copy
import numpy as np

#Variabel /Raka
n_populasi = 60
n_kromosom = 11
p_c = 1
p_m = 0.8
saham = []
saham_50 = []
generasi = 200
min_krom = -0.5
max_krom = 0.5

#Membuka file csv yang berisikan data-data saham perusahaan /Raka
with open('data.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        saham.append(int(row['Terakhir']))
    for i in range(50):
        saham_50.insert(0, saham.pop(0))


#populasi awal /Raka
def generatePop(n_populasi, n_kromosom):
    pop = []
    for i in range(n_populasi):
        krom = []
        for y in range(n_kromosom):
            krom.append(random.randint(0, 9))
        pop.append(krom)
    return pop


#decode kromosom /Indra


def decodeKrom(krom=[]):
    temp_krom = copy.deepcopy(krom)
    krom_alloc = []
    decoded_krom = []

    alloc = math.floor(len(temp_krom) / 11)
    alloc_extra = len(temp_krom) % 11
    for i in range(11):
        krom_alloc.insert(0, alloc)
        if (alloc_extra != 0):
            krom_alloc[0] += 1
            alloc_extra -= 1

    krom_index = 0
    for i in range(11):
        divider = 0
        multi = 0
        for j in range(krom_alloc[i]):
            divider += 10**-(j + 1)
            multi += temp_krom[krom_index] * 10**-(j + 1)
            krom_index += 1
        divider = divider * 9
        decoded_krom.append(min_krom +
                            ((max_krom - min_krom) / divider) * multi)
    return decoded_krom


#Fitness / Indra
def fitness(krom=[], saham=[]):
    backup_krom = copy.deepcopy(krom)
    decoded_krom = decodeKrom(backup_krom)
    fitness = 0
    for i in range(len(saham) - 11, 0, -1):
        prediksi = decoded_krom[0]
        for y in range(10, 0, -1):
            prediksi += decoded_krom[y] * saham[i + y]
        temp = saham[i] - prediksi
        fitness += temp**2
    temp = math.sqrt(fitness)
    fitness = temp / (len(saham) - 12)
    temp = 1 / fitness
    return temp


def fitness_all(pop=[], saham=[]):
    population = copy.deepcopy(pop)
    fitness_all = []
    for i in range(len(population)):
        fitness_all.append(fitness(population[i], saham))
    return fitness_all


#ganti generasi / Raka


def elitism(fitness_all):
    return fitness_all.index(max(fitness_all))


#parent selection / Indra


def rouletteSelection(populasi, fitness_all_pop):
    fitness_all = copy.deepcopy(fitness_all_pop)
    pop_copy = copy.deepcopy(populasi)
    max = np.sum(fitness_all)
    pick = random.uniform(0, max)
    current = 0
    for i in range(len(fitness_all)):
        current += fitness_all[i]
        if current > pick:
            parent1 = pop_copy[i]
            fitness_all.pop(i)
            pop_copy.pop(i)
            break

    max = np.sum(fitness_all)
    pick = random.uniform(0, max)
    current = 0
    for i in range(len(fitness_all)):
        current += fitness_all[i]
        if current > pick:
            parent2 = pop_copy[i]
            break

    return parent1, parent2


#two point crossover / Andang


def crossover(parent1, parent2, p_c, n_kromosom):
    rand = random.random()
    if (rand < p_c):
        j = random.randint(0, n_kromosom - 1)
        i = random.randint(0, n_kromosom - 1)
        if (j > i):
            while (i <= j):
                parent2[i], parent1[i] = parent1[i], parent2[i]
                i += 1
        if (i < j):
            while (j <= i):
                parent2[j], parent1[j] = parent1[j], parent2[j]
                j += 1
    return parent1, parent2


#mutasi / Raka


def mutasi(parent1, parent2, p_m, n_kromosom):
    rand = random.random()
    if (rand < p_m):
        parent1[random.randint(0, n_kromosom - 1)] = random.randint(0, 9)
        parent2[random.randint(0, n_kromosom - 1)] = random.randint(0, 9)

    return parent1, parent2


#prediksi 50 hari kedepan / Andang


def predict(krom=[], saham=[]):
    saham_backup = copy.deepcopy(saham)
    pred_saham = []
    decoded_krom = decodeKrom(krom)
    for i in range(50):
        prediksi = decoded_krom[0]
        for j in range(10):
            prediksi += decoded_krom[j + 1] * saham_backup[j]
        saham_backup.insert(0, round(prediksi))
        pred_saham.append(round(prediksi, 2))
    for i in range(50):
        print(
            f'Prediksi Hari ke-{i+1} : {pred_saham[i]} \t Real : {saham_50[i]} \t Delta(prediksi - real) : {round(pred_saham[i]-saham_50[i],2)}'
        )


#avg finder / Abaikan


def avg_gen_al(percobaan):
    avg_fit = 0
    for i in range(percobaan):
        populasi = generatePop(n_populasi, n_kromosom)
        for i in range(generasi):
            fitness_all_pop = fitness_all(populasi, saham)
            next_pop = []
            best = elitism(fitness_all_pop)
            next_pop.append(populasi[best])
            next_pop.append(populasi[best])
            i = 0
            while (i < n_populasi - 2):
                parent1, parent2 = rouletteSelection(populasi, fitness_all_pop)
                par1, par2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
                child = crossover(par1, par2, p_c, n_kromosom)
                child = mutasi(child[0], child[1], p_m, n_kromosom)
                next_pop += child
                i += 2
            populasi = next_pop

        fitness_all_pop = fitness_all(populasi, saham)
        result = elitism(fitness_all_pop)
        avg_fit += fitness(populasi[result], saham)

    return avg_fit / percobaan


#main program / Andang

populasi = generatePop(n_populasi, n_kromosom)

for i in range(generasi):
    fitness_all_pop = fitness_all(populasi, saham)
    next_pop = []
    best = elitism(fitness_all_pop)
    next_pop.append(populasi[best])
    next_pop.append(populasi[best])
    i = 0
    while (i < n_populasi - 2):
        parent1, parent2 = rouletteSelection(populasi, fitness_all_pop)
        par1, par2 = copy.deepcopy(parent1), copy.deepcopy(parent2)
        child = crossover(par1, par2, p_c, n_kromosom)
        child = mutasi(child[0], child[1], p_m, n_kromosom)
        next_pop += child
        i += 2
    populasi = next_pop

fitness_all_pop = fitness_all(populasi, saham)
result = elitism(fitness_all_pop)

print(
    '================================== Result =================================='
)
print()
print('Best Chromosome            = ', populasi[result])
print('Chromosome Fitness         = ', fitness(populasi[result], saham))
print('Phenotype                  = ')
fenotip = decodeKrom(populasi[result])
for i in range(len(fenotip)):
    print(f'\t a{i}  : {fenotip[i]}')
print(
    '================================= Prediksi ================================='
)
predict(populasi[result], saham)
print(
    '============================================================================'
)
