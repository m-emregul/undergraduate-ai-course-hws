import random
import time
import pygame
pygame.init()
beginning_time = time.time()

X = 22          #labirentin boyutları
Y = 22
K = 10          #engel sayısı = K*4

moves = [1, 2, 3, 4]
Maze = [[0 for x in range(Y)] for y in range(X)]        #Labirent oluşturulur
for i in range(X):
    for j in range(Y):
        if i == 0 or j == 0 or i == X - 1 or j == Y - 1:
            Maze[i][j] = 5
        else:
            Maze[i][j] = 0


def isWalkable(Maze, point):
    if Maze[point[0]][point[1]] == 5:       #Labirentte girilen  noktada engel varsa False, yoksa True döner
        return False
    return True


def generate_obstacle(Maze, l, w, K):       #K adet L şeklinde engel rastgele yerlere yerleştirilir
    num = int(K / 2)
    count = 0
    while count < num:
        rx = random.randint(2, l - 3)                       #labirent üzerinde rastgele bir nokta seçilir. O noktanın olduğu bölgeye, eğer uygunsa L şeklinde engel çizilir.
        ry = random.randint(2, w - 3)
        if isWalkable(Maze, [rx, ry]) and isWalkable(Maze, [rx, ry + 1]) and isWalkable(Maze,
                                                                                        [rx + 1, ry]) and isWalkable(
                Maze, [rx + 2, ry]) and isWalkable(Maze, [rx + 3, ry]):
            Maze[rx][ry] = 5
            Maze[rx][ry + 1] = 5
            Maze[rx + 1][ry] = 5
            Maze[rx + 2][ry] = 5
            Maze[rx + 3][ry] = 5
            count += 1
    count = 0                                   # engellerin yarısı dikey L, yarısı yatay L.
    while count < num:
        rx = random.randint(2, l - 3)
        ry = random.randint(2, w - 3)
        if isWalkable(Maze, [rx, ry]) and isWalkable(Maze, [rx - 1, ry]) and isWalkable(Maze,
                                                                                        [rx, ry + 1]) and isWalkable(
                Maze, [rx, ry + 2]) and isWalkable(Maze, [rx, ry + 3]):
            Maze[rx][ry] = 5
            Maze[rx - 1][ry] = 5
            Maze[rx][ry + 1] = 5
            Maze[rx][ry + 2] = 5
            Maze[rx][ry + 3] = 5
            count += 1
    return


generate_obstacle(Maze, X, Y, K)

#for i in range(X):
#    print(Maze[i])


def fitness(Maze, l, w, arr, generation):   #degerlendirme fonksiyonu.  l ve w labirentin boyuntları.    arr popülasyondaki bir eleman.  generation, jenerasyon sayısı
    fvalue = 0                              #duvara çarpmadan gidilen nokta sayısını tutar
    point = [1, 1]                          #baslangıc
    for n in arr:
        if n == 1:                          #sıradaki noktaya yürünebiliyorsa yürünür. Yürünemiyorsa değerlerndirme fonksiyonunun ürettiği değer döndürülür.
            if isWalkable(Maze, [point[0], point[1] - 1]):
                point = [point[0], point[1] - 1]
                fvalue += 1

            else:
                return f_distance(point, l, w)
        elif n == 2:
            if isWalkable(Maze, [point[0] - 1, point[1]]):
                point = [point[0] - 1, point[1]]
                fvalue += 1

            else:
                return f_distance(point, l, w)

        elif n == 3:
            if isWalkable(Maze, [point[0], point[1] + 1]):
                point = [point[0], point[1] + 1]
                fvalue += 1
            else:
                return f_distance(point, l, w)
        elif n == 4:
            if isWalkable(Maze, [point[0] + 1, point[1]]):
                point = [point[0] + 1, point[1]]
                fvalue += 1
            else:
                return f_distance(point, l, w)

        if point[0] == l - 2 and point[1] == w - 2:         #sonuç bulunduysa yol labirent üzerinde çizilir.
            draw(Maze, l, w, arr)
            display_maze(Maze, l, w)                         #labirent ekrana bastırılır
            print("Target is found ! ")                     #ilgili bilgiler ekrana basılır ve program durdurulur.
            print("the path : {}".format(arr[:fvalue]))
            print("length of the path : {}".format(fvalue))
            print("generation : {}".format(generation))
            print("elapsed time :", time.time() - beginning_time)
            closing = input("--- > press something to exit ---> ")
            pygame.quit()
            exit(0)
            #return
    return f_distance(point, l, w)


def display_maze(Maze, l, w):               #Labirenti i pygame kütüphanesini kullanarak ekrana bastırır
    ekran = pygame.display.set_mode((600, 480))
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)

    for y in range(X):
        for x in range(Y):
            rect = pygame.Rect(x * 20 + 1, y * 20 + 1, 20, 20)
            if Maze[x][y] == 5:
                pygame.draw.rect(ekran, WHITE, rect)
            elif Maze[x][y] == 8:
                pygame.draw.rect(ekran, RED, rect)
            elif Maze[x][y] == 0:
                pygame.draw.rect(ekran, BLACK, rect)
    pygame.display.flip()



def draw(M, l, w, arr):         #bulunan sonucu labirent üzerine çizer
    point = [1,1]
    M[1][1] = 8
    for n in arr:
        if n == 1:
            point = [point[0], point[1]-1]
        elif n == 2:
            point = [point[0]-1, point[1]]
        elif n == 3:
            point = [point[0], point[1]+1]
        elif n == 4:
            point = [point[0]+1, point[1]]

        M[point[0]][point[1]] = 8
        if point[0] == l - 2 and point[1] == w - 2:
            return


def f_distance(po, le, we):                             # değerlendirme fonksiyonu
    return ((po[0] + po[1] - 2) / (le - po[0] + we - po[1] - 2)) * 100


def crossover(parent1, parent2):        #iki parent ile yeni bir child üretir.
    parent = []
    length = len(parent1)
    k = random.randint(0, length)       #rasgele bir nokta seçilir. Başlangıçtan o noktaya kadar ilk parent'tan, o noktadan sona kadar ikinci parent' alınır.
    for i in range(0, length):
        if i <= k:
            parent.insert(i, parent1[i])
        else:
            parent.insert(i, parent2[i])
    return parent


def random_parent(weights):     #rulet tekeri
    totals = []                 #değerlendirme fonksiyonundan yüksek değer almış parentlerın seçilme ihtimalini artırır.
    running_total = 0
    for w in weights:
        running_total += w
        totals.append(running_total)
    rnd = random.random() * running_total
    for indeks, total in enumerate(totals):
        if rnd <= total:
            return indeks
    return 0


def mutate(gene, mutation_rate):                 #girilen mutasyon oranında olasıkla rastgele bir yerde mutasyona sebep bolur
    if random.uniform(0.0, 1.0) <= mutation_rate:
        element = random.randint(0, len(gene) - 1)
        others = [1, 2, 3, 4]
        others.remove(gene[element])
        gene[element] = random.choice(others)


def genetic_func(Maze, l, w, population_begin):         #genetik fonksiyon, population_begin = baslangıç popülasyonu
    count = 1                                       #jenerasyon sayar
    population = population_begin
    while True:
        fitness_values = [0 for i in range(len(population))]
        for i in range(len(population)):                            #popülasyondaki her bir eleman için, fitness değeri üretilir
            fitness_values[i] = fitness(Maze, l, w, population[i], count)

        new_population = []
        for ij in population:                            #popülasyondaki eleman kadar yeni eleman üretilir.
            par1 = random_parent(fitness_values)          #fitness değeri yüksek elemanlardan yeni çocuklar üretilir
            par2 = random_parent(fitness_values)
            child = crossover(population[par1], population[par2])
            mutate(child, 0.5)
            new_population.append(child)
        population = new_population
        count += 1


population_size = 50                       #popülasyon büyüklüğü
gene_size = 150
mypopulation = []
for i in range(population_size):        #baslangıc popülasyonu rasgele üretilir.
    mypopulation.insert(i, random.choices(moves, k=gene_size))

display_maze(Maze, X, Y)
genetic_func(Maze, X, Y, mypopulation)                  # X, Y labirentin boyutları



