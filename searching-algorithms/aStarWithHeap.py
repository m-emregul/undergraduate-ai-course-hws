import cv2
import time
import matplotlib.pyplot as plt
#%matplotlib inline
imageName = input("resim ismi giriniz (uzantısı ile birlikte)")
sx = int(input("baslangıc noktasını giriniz. (ilk sayıyı girince enter'a basınız"))
sy = int(input())
ex = int(input("bitis noktasını giriniz"))
ey = int(input())
print("..........")
startP = [sx,sy]            #baslangıc noktası
endP = [ex,ey]              #bitis noktası

start_time = time.time()
img = cv2.imread(imageName)                     #resim okunuyor
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)      # Opencv BGR, matploblib ise RGB seklindedir. BGR -> RGB dönüşümü
#plt.figure(figsize = (15,15))

def checkThePoints(a, b, height, width):        #girilen noktaların geçerli olup olmadığını kontrol eder. Değilse programı durdurur.
    rules = [a[0] >= 0, b[0] >= 0,
             a[1] >= 0, b[1] >= 0,
             a[0] < height, b[0] < height,
             a[1] < width, b[1] < width ]
    if not all(rules):
        exit("Noktalar bulunmuyor ! Not : [x,y] icin x yukseklik, y genislik ")


class HeapDS:                                        #Heap sınıfı
    def __init__(self):
        self.heapArray = []                             #Heap ağacını gerçekleştirirken kullanılan liste
        self.size = 0                                   #heap ağacı eleman sayısı

    def insertToHeap(self, element):                    #heap e eleman yerleştiren fonksiyon
        i = self.size
        self.heapArray.insert(i,element)
        self.size += 1
        parent = int((i - 1) / 2)

        while i >= 1 and self.heapArray[i].total < self.heapArray[parent].total:            # ağaca yerleştirilen eleman toplam maliyetine göre yukarı taşınır
            self.heapArray[i], self.heapArray[parent] = self.heapArray[parent], self.heapArray[i]
            i = parent
            parent = int((i - 1) / 2)

    def riseInHeap(self, j):                #daha önce heap'te bulunan bir elemana, daha az maliyetli bir yoldan erişilebileceği bulunduğunda elemanın
        parent = int((j - 1) / 2)           # maliyet, önceki düğüm vs bilgileri güncellendikten sonra heapte o elemanın yerini güncelleyen fonksiyonç
        while j >= 1 and self.heapArray[j].total < self.heapArray[parent].total:    #(daha az maliyetli bir yol bulunduğu için elemanın heapte yukarı muhtemeldir.)
            self.heapArray[j], self.heapArray[parent] = self.heapArray[parent], self.heapArray[j]
            j = parent
            parent = int((j - 1) / 2)

    def findSmallestChild(self, i):                                      #heap ağacında verilen bir indisteki düğümün cocuklarına bakar
        if 2 * i + 2 < self.size:
            if self.heapArray[2 * i + 1].total < self.heapArray[2 * i + 2].total:       #iki cocuk varsa maliyeti kücük olanı döndürür
                return 2 * i + 1
            else:
                return 2 * i + 2
        elif 2 * i + 1 < self.size:
            return 2 * i + 1
        else:
            return -1                                #cocuk yoksa -1 döndürür.

    def downHeap(self):                                  #en küçük eleman cıkarıldıktan sonra heap ağacı yeniden düzenlenir.
        i = 0
        tmp = self.findSmallestChild(i)
        while tmp != -1 and self.heapArray[i].total > self.heapArray[tmp].total:
            self.heapArray[i], self.heapArray[tmp] = self.heapArray[tmp], self.heapArray[i]
            i = tmp
            tmp = self.findSmallestChild(i)

    def removeMin(self):                            #heap ağacında en üstteki değeri çıkarıp döndürür.
        if self.size == 0:
            return
        removed = self.heapArray[0]
        self.heapArray[0] = self.heapArray[self.size - 1]
        self.size -= 1
        self.downHeap()
        return removed

class Node:                                          #resimdeki noktalar birer düğüm olarak gerçekleştirilir
    def __init__(self, position, end_p, img):               #noktanın koordinatları, hedef noktası ve resim
        self.position = position                                  #noktanın koordinatları
        self.preNode = None                                      #bu noktaya hangi nokta üzerinden ulaştığımızı tutar
        self.distanceToEnd = calcDistance(self.position, end_p)  # sezgisel fonksiyon hesaplanır.
        self.cost = 0                                        # komşu noktalardan bu noktaya gelmenin maliyeti
        self.cost_before = 0                                 #başlangıctan bu noktaya kadar ki toplam maliyet
        self.total = 0                                       #maliyetler toplamı.
        self.gFunc(img)

    def gFunc(self, img):                        #düğümün maliyetini hesaplama fonksiyonu
        self.cost = 256 - img.item(self.position[0], self.position[1], 0) #R == 0 ise R = 1 alınır
        if self.cost == 256:
            self.cost = 255

    def fReset(self):                           #düğüm oluşturulduğunda init fonksiyonu ile maliyeti de oluşturulur. Başlangıç noktası için bu maliyet tekrar sıfırlanır.
        self.cost = 0
        self.cost_before = 0

    def setTotal(self):
        self.total = self.cost + self.distanceToEnd + self.cost_before      #toplam maliyeti düğüme yazar


def calcDistance(current_p, end_p):                 #h() fonksiyonu. Verilen iki nokta arası sezgisel değeri üretir.
    dx = abs(current_p[0] - end_p[0])
    dy = abs(current_p[1] - end_p[1])
    D = 1
    return D * (dx + dy)

def setAttributes(tNode, currentNode):                      #yeni bir düğüm oluşturulduğunda ya da mevcut düğümün maliyeti güncellendiğinde cagrilir
    tNode.cost_before = currentNode.cost_before + currentNode.cost
    tNode.preNode = currentNode
    tNode.setTotal()

def aStar_Heap(imgP, start_p, end_p):
    height, width, channels = imgP.shape                            #resim yüksekliği, genişliği elde edilir
    checkThePoints(start_p, end_p, height, width)                       #verilen noktalar kontrol edilir.
    visited = [[0 * j for j in range(width)] for i in range(height)]    #resmin boyutlarında bir matris oluşturulur.  Bir nokta kuyruğa eklenirse o nokta 1 yapılır.
    startNode = Node(start_p, end_p,imgP)                                  #baslangıc noktası dugumu olusturulur    #kuyruktan çıkarıldığında ise 2 yapılır
    startNode.fReset()                                                      #baslangıc noktasının maliyeti sıfırlanır
    visited[start_p[0]][start_p[1]] = 1
    myHeap = HeapDS()
    storage = []                                                 #heap den cıkarılan noktaların saklanacağı liste
    myHeap.insertToHeap(startNode)
    heap_max = 0                                            #heap'e eklenen maksimum eleman sayısını tutan degisken
    while myHeap.size > 0:
        if myHeap.size > heap_max:                              #stack'e eklenen maksimum eleman sayısı güncellenir
            heap_max = myHeap.size

        currentNode = myHeap.removeMin()                            # en baştaki eleman alınır.
        storage.append(currentNode)
        visited[currentNode.position[0]][currentNode.position[1]] = 2  #bir kere ziyaret edilmiş düğümü 2 yapıyor

        if currentNode.position == end_p:                             #en son ziyaret edilen nokta hedef noksası mı
            tmpNode = currentNode
            while tmpNode is not None:                               #bulunan yol ve diger bilgiler ekrana basılır
                print(tmpNode.position)
                imgP[tmpNode.position[0],tmpNode.position[1]] = [255,255,255]
                tmpNode = tmpNode.preNode
            print("heap'ten cekilen eleman sayısı : {}".format(len(storage)))
            print("heap'in icerdigi maksimum eleman sayısı {}".format(heap_max))
            print("toplam maliyet : {}".format(currentNode.cost_before + currentNode.cost))
            return

        x = currentNode.position[0]
        y = currentNode.position[1]
        neighbors = [[x+1,y], [x-1,y], [x,y+1], [x,y-1]]                        #komşu noktalar

        for iterN in neighbors:                                                 #komşulara hareket edilir mi kontrolü
            if iterN[0] < 0 or iterN[0] == height or iterN[1] < 0 or iterN[1] == width:
                continue

            if visited[iterN[0]][iterN[1]] == 0:                                      #komşu noktada daha önce düğüm oluşturulmamış ise buradan devam eder
                tmpNode = Node(iterN, end_p, imgP)                                    #yeni düğüm oluşturulur
                visited[iterN[0]][iterN[1]] = 1                                       #visited matrisinde o nokta 1 olarak işaretlenir
                setAttributes(tmpNode, currentNode)                                   #maliyet vs önceki düğüm bilgisi düğüme yazılır
                myHeap.insertToHeap(tmpNode)                                          #heap 'e eklenir

            elif visited[iterN[0]][iterN[1]] == 1:                          #komşu noktada daha önce düğüm oluşturulmuş ise buradan devam eder
                tmp_index = 0
                while tmp_index != myHeap.size:
                    tmpNode_2 = myHeap.heapArray[tmp_index]                                 # heap de o noktanın düğümü aranır.
                    if tmpNode_2.position[0] == iterN[0] and tmpNode_2.position[1] == iterN[1]: #o düğümdeki maliyet ile mevcut maliyet kıyaslanır.
                        if tmpNode_2.cost_before > currentNode.cost_before + currentNode.cost:    #mevcut maliyet daha az ise düğümün bilgileri güncellenir.
                            setAttributes(tmpNode_2, currentNode)
                            myHeap.riseInHeap(tmp_index)                             # maliyeti güncellenen düğüm heapte çıkabiliyorsa yukarı çıkarılır.
                        break
                    tmp_index += 1


aStar_Heap(img, startP, endP )
#plt.imshow(img)
print("elapsed time : {}".format(time.time() - start_time))

