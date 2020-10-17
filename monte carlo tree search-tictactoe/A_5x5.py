from math import sqrt,log
from copy import deepcopy
from random import choice


class Board:
    def __init__(self):                                          #oyun tahtası
        self.b = {1: ' ' , 2: ' ' , 3: ' ' , 4: ' ', 5: ' ',
            6: ' ' , 7: ' ' , 8: ' ' ,9: ' ', 10: ' ',
            11: ' ' , 12: ' ' , 13: ' ', 14: ' ', 15: ' ',
            16: ' ', 17: ' ', 18: ' ', 19: ' ', 20: ' ',
            21: ' ', 22: ' ', 23: ' ', 24: ' ', 25: ' '}
        self.moves = [x for x in range(1, 26)]

    def printBoard(self):                                 #oyun tahtasını ekrana basar
        print("01" + ' | ' + "02" + ' | ' + "03" +  ' | ' + "04" +  ' | ' + "05" + "            " + self.b[1] + ' | ' + self.b[2] + ' | ' + self.b[3] + ' | ' + self.b[4]+ ' | ' + self.b[5])
        print('---------------------           ---------------------')
        print("06" + ' | ' + "07" + ' | ' + "08" +  ' | ' + "09"+  ' | ' + "10"+ "            " + self.b[6] + ' | ' + self.b[7] + ' | ' + self.b[8]+ ' | ' + self.b[9] + ' | ' + self.b[10])
        print('---------------------           ---------------------')
        print("11" + ' | ' + "12" + ' | ' + "13" +  ' | ' + "14"+  ' | ' + "15"+ "            " + self.b[11] + ' | ' + self.b[12] + ' | ' + self.b[13]+ ' | ' + self.b[14] + ' | ' + self.b[15])
        print('---------------------           ---------------------')
        print("16" + ' | ' + "17" + ' | ' + "18" + ' | ' + "19" + ' | ' + "20" + "            " + self.b[16] + ' | ' + self.b[17] + ' | ' + self.b[18] + ' | ' + self.b[19] + ' | ' + self.b[20])
        print('---------------------           ---------------------')
        print("21" + ' | ' + "22" + ' | ' + "23" + ' | ' + "24" + ' | ' + "25" + "            " + self.b[21] + ' | ' +self.b[22] + ' | ' + self.b[23] + ' | ' + self.b[24] + ' | ' + self.b[25])

    def check_winner_diagonal(self, player_sign):                         #oyunu bir tarafın kazanıp kazanılmadığının kontrolü
        x = 1
        while x < 8:
            if self.b[x] == player_sign and self.b[x+6] == player_sign and self.b[x+12] == player_sign and self.b[x+18] == player_sign:
                return True
            x += 6
        x = 5
        while x < 10:
            if self.b[x] == player_sign and self.b[x+4] == player_sign and self.b[x+8] == player_sign and self.b[x+12] == player_sign:
                return True
            x += 4
        if self.b[2] == player_sign and self.b[8] == player_sign and self.b[14] == player_sign and self.b[20] == player_sign:
            return True
        if self.b[6] == player_sign and self.b[12] == player_sign and self.b[18] == player_sign and self.b[24] == player_sign:
            return True
        if self.b[4] == player_sign and self.b[8] == player_sign and self.b[12] == player_sign and self.b[16] == player_sign:
            return True
        if self.b[10] == player_sign and self.b[14] == player_sign and self.b[18] == player_sign and self.b[22] == player_sign:
            return True
        return False

    def check_winner_horitonzal(self, player_sign):                       #oyunu bir tarafın kazanıp kazanılmadığının kontrolü
        for i in range(0,5):
            for j in range(1,3):
                if self.b[j+i*5] == player_sign and self.b[j + i*5 + 1] == player_sign and self.b[j + i*5 + 2] == player_sign and self.b[j + i*5 + 3] == player_sign:
                    return True
        return False

    def check_winner_vertical(self, player_sign):                         #oyunu bir tarafın kazanıp kazanılmadığının kontrolü
        for i in range(0,5):
            for j in range(1,7,5):
                if self.b[j + i] == player_sign and self.b[j + i + 5] == player_sign and self.b[j + i + 10] == player_sign and self.b[j + i + 15] == player_sign:
                    return True
        return False

    def check_winner(self, player_sing):                                      #oyunu bir tarafın kazanıp kazanılmadığının kontrolü
        if self.check_winner_vertical(player_sing) or self.check_winner_horitonzal(player_sing) or self.check_winner_diagonal(player_sing):
            if player_sing == "X":
                return -1
            elif player_sing == "O":
                return 1
        return 0

    def my_move(self):                                  # kullanıcının hamlesinin alınması
        while True:
            mymove = int(input("hamlenizi giriniz\n"))
            if mymove not in self.moves:
                print("gecersiz ! ")
            else:
                break
        self.b[mymove] = "O"
        self.moves.remove(mymove)

    def computer_move(self):                           #bilgisayarın hamlesi, monte carlo algoritması burada çağırılır.
        com_move = monte_carlo_tree(self, 10000)
        self.b[com_move] = "X"
        self.moves.remove(com_move)

    def copy_board(self):                   #oyun tahtası nesnesinin kopyalanması
        c = Board()
        c = deepcopy(self)
        return c

    def make_move(self, r):              #simulasyon bölümünde hamleleri yapan fonksiyon
        if len(self.moves) > 0:
            if len(self.moves) % 2 == 0:
                self.b[r] = "X"
            elif len(self.moves) % 2 == 1:
                self.b[r] = "O"


class Node:         #düğüm sınıfı

    def __init__(self, parent=None, board=None, node_move=None):
        self.parent = parent
        self.node_board = board
        self.children = []
        self.visits = 0         #düğümün kaç kere ziyaret edildiği bilgisi burada tutulur.
        self.point = 0              #oyunun sonucuna göre düğüme yeni bir puan eklenir.
        self.node_move = node_move                  #bu düğüme gelirken yapılan hamle burada tutulur
        self.unvisited = deepcopy(self.node_board.moves)

    def select(self):       #mante carlo algoritmasında selection kısmında çağrılır. En umut verici düğüm seçilir.
        s = sorted(self.children, key=lambda c: c.point / c.visits + sqrt(2 * log(self.visits) / c.visits))
        return s[-1]

    def expand(self, tmp_board, rand):              #expansion kısmında çağırılır. Yeni düğüm üretilir.
        child = Node(parent=self, board=tmp_board, node_move=rand)
        self.children.append(child)
        return child

    def update(self, result):           #backpropagation kısmında çağırılır. Oyun sonuçlarına düğümlere ilgili bilgileri ekler.
        self.visits += 1
        self.point += result

    def print_node(self):                #oyun ağacının tamamını ekrana basar.
        print("visit and point , number of children : ", self.visits, self.point, len(self.children))
        for i in self.children:
            i.print_node()


def monte_carlo_tree(current_board, number):
    root = Node(board=current_board)                #mevcut oyun tahtası ile root düğümü oluşturuluyor.

    for i in range(number):
        tmp_board = current_board.copy_board()       #oyun tahtası kopyalanıyor.Monte carlo algoritması içinde hamleler bu kopya üzerinde yapılıyor.
        node = root
                                                      #selection
        while len(node.unvisited) == 0 and len(node.children) != 0:
            node = node.select()                       #düğümlerin içinde yapılan hamle tutulur. Yeni bir düğüme gelindiğinde o hamle tahta üzerinde oynanır.
            tmp_board.make_move(node.node_move)
            tmp_board.moves.remove(node.node_move)  #her tablo nesnesinde yapılabilecek hamleleri tutan moves listesi vardır. Yeni bir hamle yapıldığında, hamle bu listeden çıkarılır.

        flag = 0        #selection kısmının sonunda oyun sonlanmış mı kontrolü yapılır.
        if len(tmp_board.moves) == 0:
            flag = 1

                                                      #expansion
        if len(node.unvisited) != 0 and flag == 0:
            rand = choice(node.unvisited)   #henüz yapılmamış hamlelerden birisi rastgele seçilir. henüz yapılmamış hamleler listesinden çıkarılır. Yeni düğüm oluşturulur.
            node.unvisited.remove(rand)
            tmp_board.make_move(rand)
            tmp_board.moves.remove(rand)
            node = node.expand(tmp_board, rand)

                                                        #simulation
        result = 1
        while True:                  #oyun bitene kadar rastgele hamlelerle simüle edilir. Bilgisayar kazanırsa 2, berabere biterse 1, kullanıcı kazanırsa 0 sonucu çıkarılır.
            if len(tmp_board.moves) == 0:
                break
            if tmp_board.check_winner("O") == 1:
                result = 0
                break
            if tmp_board.check_winner("X") == -1:
                result = 2
                break

            rand = choice(tmp_board.moves)
            tmp_board.make_move(rand)
            tmp_board.moves.remove(rand)

                                                    #backpropagation
        while node != None:         #puan ve ziyaret bilgisi düğümlere eklenir.
            node.update(result)
            node = node.parent

    s = sorted(root.children, key=lambda c: c.point / c.visits)         #monte carlo algoritması en umut verici hamleyi döndürür.
    return s[-1].node_move


def play_game():         #oyunun oynandığı ana fonksiyon

    while True:
        result = 0
        main_board = Board()        #yeni bir oyun tahtası nesnesi üretilir.
        main_board.printBoard()
        while True:
            print(" \n--------------------------------------")
            main_board.my_move()        #kullanıcıdan hamlesi input olarak alınır ve tabloya işlenir.
            result = main_board.check_winner("O")

            if result == 1:
                print("siz kazandınız ! ")
                main_board.printBoard()
                break
            if len(main_board.moves) == 0:
                print("berabere ! ")
                break
            print("\nBilgisayarın hamlesi  ")
            main_board.computer_move()      #bilgisayar monte carlo algoritması ile en umut verici hamleyi bulup onu oynar.
            result = main_board.check_winner("X")
            main_board.printBoard()
            if result == -1:
                print("bilgisayar kazandı ! ")
                break
            if len(main_board.moves) == 0:
                print("berabere ! ")
                break

        inpt = input("Yeniden oynamak için bir tusa basin. ")


play_game()
