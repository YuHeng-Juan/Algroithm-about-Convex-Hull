import numpy as np
import time
from tkinter import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
def compare(a,b): #比較哪個點比較小 先比y,y一樣在比x
    return a[1]<b[1] or (a[1]==b[1] and a[0]<b[0])

def cross(origin,a,b): #二階行列式 可以看成平行四邊形的面積 如果值>0則夾角小於180度 AO向量到BO向量的夾角 
    return (a[0]-origin[0])*(b[1]-origin[1]) - (a[1]-origin[1])*(b[0]-origin[0])

def Q_distance(a,b): #距離平方和
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def far(origin,a,b): #origin到a的距離 有沒有比 origin到b的距離長
    return Q_distance(origin,a) > Q_distance(origin,b)

def drawPic():
    try:num=int(inputEntry.get())
    except:
        num=10
        print ('請輸入整數')
        inputEntry.delete(0,END)
        inputEntry.insert(0,'10')
       
    #清空影象，以使得前後兩次繪製的影象不會重疊
    drawPic.f.clf()
    drawPic.a=drawPic.f.add_subplot(111)
       
    P = np.random.randint(1,num,(num,2))
    drawPic.a.scatter(*zip(*P),color = 'black')
    drawPic.canvas.draw()
    global Choose
    Choose = np.array([[0,0]])
    print(P)

    start = 0
    for i in range(0,num): # sort all point
        if compare(P[i],P[start]): # find the smallest point
            start = i
    v = 0 # 被選擇的頂點個數
    Choose[v] = P[start] #紀錄起點
    current = start #當前點
    #尋找下一個被包的點
    v = 1
    while True:
        nextone = current
        for i in range(0,num):
            theta = cross(Choose[v-1],P[i],P[nextone])
            if theta>0 or (theta==0 and far(Choose[v-1],P[i],P[nextone])):
                nextone = i
        if nextone == start: #代表回到原點
            Choose = np.append(Choose, [P[start]], axis=0)
            break
        Choose = np.append(Choose, [P[nextone]], axis=0) #Choose[v] = P[nextone]
        current = nextone
        v += 1

def SBS():
    global time
    temp = list(zip(*Choose))
    if time > len(temp[0]):
        root.destroy()
    else:
        drawPic.a.plot(temp[0][0:time],temp[1][0:time],color = 'red')
        drawPic.canvas.draw()
        text1.delete(1.0,END)
        text1.insert("end","{}\n".format(Choose[0:time]))
        time += 1

matplotlib.use('TkAgg')
root = Tk()
root.title('Convex Hull')
    
drawPic.f = Figure(figsize=(5,4), dpi=100) #在Tk的GUI上放置一個畫布，並用.grid()來調整佈局

drawPic.canvas = FigureCanvasTkAgg(drawPic.f, master=root) 
drawPic.canvas.draw() 
drawPic.canvas.get_tk_widget().grid(row=0,column=0,rowspan=50) 
    
#放置標籤、文字框和按鈕等部件，並設定文字框的預設值和按鈕的事件函式
Label(root,text='請輸入樣本數量：').grid(row=0,column=1,sticky=N+W)
inputEntry=Entry(root)
inputEntry.grid(row=1,column=1,sticky=N)
inputEntry.insert(0,'10')
Button(root,text='creat',command=drawPic).grid(row=2,column=1,sticky=N+W)
time = 2
text1 = Text(root,width=20,height=15)
text1.grid(row=3,column=1,sticky=N+W)
Button(root,text='next',command=SBS).grid(row=4,column=1,sticky=N+W)

#啟動事件迴圈
root.mainloop()