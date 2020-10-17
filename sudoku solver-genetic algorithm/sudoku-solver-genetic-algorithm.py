import random
from math import factorial,sqrt

board_0 = [9,1,3,7,6,4,8,2,5,
            7,2,4,1,8,5,3,9,6,
           8,6,5,9,2,3,4,1,7,
           1,4,7,5,3,2,9,6,8,
           2,8,6,4,9,7,5,3,1,
           3,5,9,6,1,8,2,7,4,
           5,9,2,8,7,6,1,4,3,
           4,7,1,3,5,9,6,8,2,
           6,3,8,2,4,1,7,5,9]
board_2 = [
    3,6,7,5,1,9,8,4,2,
     8,4,2,3,7,6,9,1,5,
     5,9,1,4,8,2,7,6,3,
    1,8,5,9,2,4,3,7,6,
    9,3,6,7,5,1,2,8,4,
    2,7,4,6,3,8,5,9,1,
    6,2,3,8,4,7,1,5,9,
    4,5,8,1,9,3,6,2,7,
    7,1,9,2,6,5,4,3,8]

board_3 = [1,1,1,2,2,2,3,3,3,
            1,1,1,2,2,2,3,3,3,
            1,1,1,2,2,2,3,3,3,
            1,1,1,2,2,2,3,3,3,
            1,1,1,2,2,2,3,3,3,
            1,1,1,2,2,2,3,3,3,
            1,1,1,2,2,2,3,3,3,
            1,1,1,2,2,2,3,3,3,
            1,1,1,2,2,2,3,3,3]

board_4 = [1,2,3,4,5,6,7,8,9,
            1,2,3,4,5,6,7,8,9,
            1,2,3,4,5,6,7,8,9,
            1,2,3,4,5,6,7,8,9,
            1,2,3,4,5,6,7,8,9,
            1,2,3,4,5,6,7,8,9,
            1,2,3,4,5,6,7,8,9,
            1,2,3,4,5,6,7,8,9,
            1,2,3,4,5,6,7,8,9]

board_22 = [0,0,0,0,6,4,0,0,0,   # 22
        7,0,0,0,0,0,3,9,0,
        8,0,0,0,0,0,0,0,0,
        0,0,0,5,0,2,0,6,0,
        0,8,0,4,0,0,0,0,0,
        3,5,0,6,0,0,0,7,0,
        0,0,2,0,0,0,1,0,3,
        0,0,1,0,5,9,0,0,0,
        0,0,0,0,0,0,7,0,0]

board_50 = [1,6,5,7,9,4,0,3,8,       # 50 given
            4,0,7,0,0,2,0,5,0,
            9,3,0,0,0,6,0,0,4,
           8,1,0,4,0,5,0,0,2,
           5,7,6,2,3,9,4,0,0,
           2,0,0,6,0,1,0,7,5,
           3,0,1,5,0,7,8,4,9,
           6,9,0,0,0,0,5,2,7,
           0,5,0,0,2,8,1,0,3 ]

board_36 = [1,0,0,4,8,9,0,0,6,        #36 given
           7,3,0,0,0,0,0,4,0,
           0,0,0,0,0,1,2,9,5,
           0,0,7,1,2,0,6,0,0,
           5,0,0,7,0,3,0,0,8,
           0,0,6,0,9,5,7,0,0,
           9,1,4,6,0,0,0,0,0,
           0,2,0,0,0,0,0,3,7,
           8,0,0,5,1,2,0,0,4]

board_30 = [5,3,0,0,7,0,0,0,0,  # 30 given
           6,0,0,1,9,5,0,0,0,
           0,9,8,0,0,0,0,6,0,
           8,0,0,0,6,0,0,0,3,
           4,0,0,8,0,3,0,0,1,
           7,0,0,0,2,0,0,0,6,
           0,6,0,0,0,0,2,8,0,
           0,0,0,4,1,9,0,0,5,
           0,0,0,0,8,0,0,7,9]

def print_board(the_board):         # oyun tahtasını ekrana basar
    count = 1
    for i in the_board:
        if count == 10:
            count = 1
            print("")
        print(i, end=" ")
        count += 1


def find_initials(board_p):       # başlangıç durumunda verilen sayıların yerlerini alır, bir diziye yazar ve diziyi döndürür.
    array_initials = []
    for i in range(81):
        if board_p[i] != 0:
            array_initials.append(i)
    return array_initials


def generate_random_populations(array_initials, board_p, pop_size): #başlangıç popülasyonunu üretir
    population_size = pop_size # popülasyon büyüklüğü
    gene_size = 81
    mypopulation = []
    possible_numbers = [1,2,3,4,5,6,7,8,9]
    for i in range(population_size):  # baslangıc popülasyonu rasgele üretilir.
        tmp_list = random.choices(possible_numbers, k=gene_size)
        for j in array_initials:                    #başlangıçta rastgele bireyler üretirken başlangıçta verilen rakamların  değişmemesi için
            tmp_list[j] = board_p[j]
        mypopulation.insert(i, tmp_list)
        #print(tmp_list)
    return mypopulation


def fitness_function(tmp_board):            #uygunluk fonksiyonu
    is_finish = True                     #uygunluk değeri hesaplanırken aynı anda çözüme ulaşılıp ulaşılmadığı kontrolü yapılır.
    row_index = [x for x in range(9)]       # sütun başları indeksleri
    column_index = [x * 9 for x in range(9)]    #satır başları indeksleri
    total = 0
    k = 0
    for i in column_index:                      #satırları kontrolü
        arr = [0 for x in range(10)]             #her rakamdan kaç tane olduğunun bilgisini tutar
        arr[0] = -1
        while k != 9:
            #print(board_p[i + k], end="  ")
            arr[tmp_board[i+k]] += 1
            k = k + 1
        for j in arr:
            if j==-1: continue
            if j==1: total += 1             # eğer bir rakam bir kere geçiyorsa +1
            elif j==0:                      #aksi halde -1
                total -= 1
                is_finish = False               # satırlarda herhangi bir rakam birden fazla ya da az geçiyorsa çözüm değildir.
            #elif j==2 or j==3: total += 2
            elif j > 1:
                total -= 1
                is_finish = False           # satırlarda herhangi bir rakam birden fazla ya da az geçiyorsa çözüm değildir.
        k = 0
    l = 0
    for i in row_index:                     #sütunların kontrülü
        arr = [0 for x in range(10)]        #her rakamdan kaç tane olduğunun bilgisini tutar
        arr[0] = -1
        while k != 9:
            arr[tmp_board[i + l]] += 1
            k = k + 1
            l = l + 9
        for j in arr:
            if j == -1: continue
            if j == 1: total += 1           # eğer bir rakam bir kere geçiyorsa +1, aksi halde -1
            elif j==0:
                is_finish = False           # satırlarda herhangi bir rakam birden fazla ya da az geçiyorsa çözüm değildir.
                total -= 1
            #elif j == 3 or j == 2: total += 2
            elif j > 1:
                is_finish = False               # satırlarda herhangi bir rakam birden fazla ya da az geçiyorsa çözüm değildir.
                total -= 1
        l = 0
        k = 0

    squares = [[0,1,2,9,10,11,18,19,20],[3,4,5,12,13,14,21,22,23],  [6,7,8,15,16,17,24,25,26],
               [27,28,29,36,37,38,45,46,47] , [30,31,32,39,40,41,48,49,50], [33,34,35,42,43,44,51,52,53],
               [54,55,56,63,64,65,72,73,74], [57,58,59,66,67,68,75,76,77], [60,61,62,69,70,71,78,79,80]
               ]
    for i in squares:                       #3x3 lük karelerin kontrolü
        arr = [0 for x in range(10)]        #her rakamdan kaç tane olduğunun bilgisini tutar
        arr[0] = -1
        for j in i:
            arr[tmp_board[j]] += 1
        for z in arr:
            if z == -1: continue
            if z == 1: total += 1                # eğer bir rakam bir kere geçiyorsa +1, aksi halde -1
            elif z ==0: total -= 1
            #elif z == 3 or z == 2: total += 2
            elif z > 1:  total -= 1

    if is_finish == True:                   #uygunluk değeri hesaplanırken aynı anda çözüme ulaşılıp ulaşılmadığı kontrolü yapılır.
        print("soduku has been solved ! \ntotal: ", total)      #çözüme ulaşılmışsa buraya girer.
        print_board(tmp_board)
        return 9999
        #quit()
    return total


def parent_choose_tournament(weights, population_size):                             ## parent seçimi. Turnuva yöntemi kullanılmıştır. Rasgele seçilen k adet bireyden
    index_arr = random.choices( [x for x in range(0, population_size)], k = 3)      # en iyisi seçilir.
    smallest_of_index = index_arr[0]
    for i in index_arr[1:]:
        if weights[i] > weights[smallest_of_index]:  #
            smallest_of_index = i
    return smallest_of_index


def crossover_function(parent1, parent2):               #çaprazlama fonksiyonu. Multi point crossover yöntemi kullanılmıştır.
    k = random.randint(0, 40)                           #rastgele iki nokta seçilir
    k2 = random.randint(41, 80)                         #ikisi arasındaki rakamlar değiştirilir.
    new_1 = []
    new_2 = []
    for i in range(81):
        if i < k or i > k2:
            new_1.insert(i, parent1[i])
            new_2.insert(i, parent2[i])
        else:
            new_1.insert(i, parent2[i])
            new_2.insert(i, parent1[i])
    return [new_1, new_2]


def mutate_function(gene, mutation_rate, initials_array):       #rastgele seçilen bir nokta verilen oranda mutasyona uğratılır.
    if random.uniform(0.0, 1.0) <= mutation_rate:
        while True:
            element = random.randint(0, 80)
            if element not in initials_array:
                break
        others = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        others.remove(gene[element])                            #mutasyonla değiştirilen rakamın aynı rakam ile değiştirilmesi ihtimali ortadan kaldırılır.
        gene[element] = random.choice(others)


def genetic_function(population_begin, population_size, not_touch):     #genetik fonksiyon
    len_inits = 81 - len(not_touch)         # len(not_touch) -> başlangıçta kaç eleman verildiği
    count_generation = 1                    #jenerasyonu sayar
    population = population_begin
    fitness_values = [0 for i in range(population_size)]    #uygunluk değerlerinin tutulduğu dizi

    while True:
        if count_generation == 2000:                        # eğer 2000 jenerasyona kadar çözüme ulaşılamadıysa fonksiyon sonlandırılır.
            print("sudoku could not solved. ")
            return
        for i in range(population_size):
            fitness_values[i] = fitness_function(population[i])     #populasyon içindeki bireylerin uygunluk değerleri hesaplanır.
            if fitness_values[i] == 9999:                   #9999 dönmüşse çözüme ulaşılmış demektir.
                return
        new_population = []
        for i in range(int(population_size/2)):
            p1 = parent_choose_tournament(fitness_values, population_size)
            p2 = parent_choose_tournament(fitness_values, population_size)
            #p1 = parent_choose(fitness_values)
            #p2 = parent_choose(fitness_values)

            if count_generation % 100 == 25:                        #her 100 jenerasyonda, jenerasyon arttıkça çaprazlama olasılığı azaltılır.
                r_rate = 0.80
            elif count_generation % 100 ==50:
                r_rate = 0.75
            elif count_generation % 100 == 75:
                r_rate = 0.70
            else:
                r_rate = 0.65

            if random.uniform(0.0, 1.0) <= r_rate:
                childs = crossover_function(population[p1],population[p2])
            else:
                childs = [population[p1],population[p2]]

            childs = crossover_function(population[p1], population[p2])
            if count_generation %100 == 0:                      # her 100 jenerasyonda bir bireyler yüksek oranda mutasyona tabi tutulur. Amaç popülasyon çeşitliliğini korumaktır.
                for i in range(len_inits):
                    mutate_function(childs[0], 0.99, not_touch)
                    mutate_function(childs[1], 0.99, not_touch)
                    mutate_function(childs[0], 0.99, not_touch)
                    mutate_function(childs[1], 0.99, not_touch)
            else:
                mutate_function(childs[0], 0.99, not_touch)
                mutate_function(childs[1], 0.99, not_touch)
            new_population.append(childs[0])
            new_population.append(childs[1])
        population = new_population
        count_generation += 1
        print("max fitness value :   " , max(fitness_values) , end="  ------ generation:   ")
        print(count_generation)


population_size = 800
the_board = board_50
while True:
    print("\n\nZorluk seviyesi seciniz \nKolay --> 1\nOrta --> 2\nZor --> 3\nCıkmak icin farklı bir tusa basın")
    a = input()
    if a == "1":
        the_board = board_50
    elif a=="2":
        the_board = board_36
    elif a=="3":
        the_board = board_30
    else:
        print("program sonlandırılıyor. !!!")
        for i in range(10000):
            pass
        quit()
    not_touch = find_initials(the_board)
    random_population = generate_random_populations(not_touch, the_board, population_size)
    genetic_function(random_population, population_size, not_touch)

#print(fitness_function(board_0) , fitness_function(board_2),  fitness_function(board_3),  fitness_function(board_4))

