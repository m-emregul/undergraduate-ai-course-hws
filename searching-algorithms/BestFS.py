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
endP = [ex,ey]                #bitis noktası

start_time = time.time()
img = cv2.imread(imageName)                      #resim okunuyor
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)      # Opencv BGR, matploblib ise RGB seklindedir.  BGR -> RGB dönüşümü
#plt.figure(figsize = (15,15))

def checkThePoints(a, b, height, width):            #girilen noktaların geçerli olup olmadığını kontrol eder. Değilse programı durdurur.
    rules = [a[0] >= 0, b[0] >= 0,
             a[1] >= 0, b[1] >= 0,
             a[0] < height, b[0] < height,
             a[1] < width, b[1] < width ]
    if not all(rules):
        exit("Noktalar bulunmuyor ! Not : [x,y] icin x yukseklik, y genislik ")


def findMin(nodeList):                              ##verilen listedeki en küçük elemanın indisini döndürür.
    k = 0
    count = 0
    for aNode in nodeList:
        if aNode.distanceToEnd < nodeList[k].distanceToEnd:
            k = count
        count += 1
    return k

class Node:                                             #resimdeki noktalar birer düğüm olarak gerçekleştirilir
    def __init__(self,position,end_p,img):               #noktanın koordinatları, hedef noktası ve resim
        self.position = position                         #noktanın koordinatları
        self.preNode = None                                 #bu noktaya hangi nokta üzerinden ulaştığımızı tutar
        self.distanceToEnd = calcDistance(self.position, end_p)    # sezgisel fonksiyon hesaplanır.
        self.cost = 0                                        # komşu noktalardan bu noktaya gelmenin maliyeti
        self.gFunc(img)

    def gFunc(self, img):                                #düğümün maliyetini hesaplama fonksiyonu
        self.cost = 256 - img.item(self.position[0], self.position[1], 0)       #R == 0 ise R = 1 alınır
        if self.cost == 256:
            self.cost = 255

    def fReset(self):                                       #baslangıc dugumu icin maliyeti sıfırlar
        self.cost = 0

def calcDistance(current_p, end_p):                         ##h() fonksiyonu. Verilen iki nokta arası sezgisel değeri üretir.
    dx = abs(current_p[0] - end_p[0])
    dy = abs(current_p[1] - end_p[1])
    D = 1
    return D * (dx + dy)


def BestFS(imgP, start_p, end_p):
    height, width, channels = imgP.shape                         #resim yüksekliği, genişliği elde edilir
    checkThePoints(start_p, end_p, height, width)                   #verilen noktalar kontrol edilir.
    visited = [  [0 * j for j in range(width)] for i in range(height)]   #resmin boyutlarında bir matris oluşturulur. Bir nokta kuyruğa eklenirse o nokta 1 yapılır.
    startNode = Node(start_p,end_p,imgP)                                   #baslangıc noktası dugumu olusturulur
    startNode.fReset()                                      #baslangıc noktasının maliyeti sıfırlanır
    visited[start_p[0]][start_p[1]] = 1
    myQueue = []                                         #komsuların eklendiği liste (stack)
    storage = []                                         #stack den cıkarılan elemanların tutulduğu liste
    stack_max = 0                                           #stack e eklenen maksimum eleman sayısını tutan degisken
    myQueue.append(startNode)
    total_cost = 0                                          #Algoritmanın bulduğu yolun maliyetini tutan degisken
    while len(myQueue) > 0:
        if len(myQueue) > stack_max:                        #stack'e eklenen maksimum eleman sayısı güncellenir
            stack_max = len(myQueue)

        indexNode = findMin(myQueue)                                 #en kücük elemanın indisi bulunur.
        currentNode = myQueue.pop(indexNode)                        #o indisten eleman çıkarılır
        #myQueue.sort(key=lambda z: z.distanceToEnd, reverse=False)     #önceki 2 satırın alternatifi
        #currentNode = myQueue.pop(0)

        storage.append(currentNode)
        if currentNode.position == end_p:                       #en son ziyaret edilen nokta hedef noksası mı
            tmpNode = currentNode
            while tmpNode is not None:                           #bulunan yol ve diger bilgiler ekrana basılır
                print(tmpNode.position)
                #imgP[tmpNode.position[0],tmpNode.position[1]] = [255,255,255]
                total_cost += tmpNode.cost
                tmpNode = tmpNode.preNode
            print("stack'ten cekilen eleman sayısı : {}".format(len(storage)))
            print("stack'in icerdigi maksimum eleman sayısı {}".format(stack_max))
            print("toplam maliyet : {}".format(total_cost))
            return

        x = currentNode.position[0]
        y = currentNode.position[1]

        neighbors = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]                        #komsular
        for iterN in neighbors:                                                 #komsulara hareket edilir mi kontrolü
            if iterN[0] < 0 or iterN[0] == height or iterN[1] < 0 or iterN[1] == width :
                continue
            if visited[iterN[0]][iterN[1]] == 1:                             #komşu nokta için daha önce bir düğüm üretilmiş mi kontrolü
                continue
            tmpNode = Node(iterN,end_p,imgP)                            #komsular için düğümler üretilir
            visited[iterN[0]][iterN[1]] = 1                             #visited matrisinde o noktalar işaretlenir
            tmpNode.preNode = currentNode                                # önceki düğüm bilgisi yeni düğümlere yazılır
            myQueue.append(tmpNode)                                     #yeni dügüm stack 'e eklenir.



BestFS(img,startP,endP )
#plt.imshow(img)
print("elapsed time : {}".format(time.time() - start_time))

