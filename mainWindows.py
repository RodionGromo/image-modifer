import tkinter as tk
from PIL import Image,ImageDraw,ImageFont,ImageTk
from tkinter.filedialog import askdirectory
import tkinter.ttk as ttk
import math
import os

filepath = ""
saveFiletype = "png"
localShowcase = None
changedImg = None
changerApp = None
openFunct = None
saveFunct = None

def createMainWindow(openFunct,infoFunct,closeFunct):
	appVar = tk.Tk()
	appVar.title("ImageModifier")
	l1 = tk.Label(master=appVar,text="Добро пожаловать в...",font="Arial 14")
	l1.pack()
	l2 = tk.Label(text="ImageModifier!",font="Arial 26")
	l2.pack()
	openBtn = tk.Button(text="Открыть картинку",command=openFunct)
	openBtn.pack()
	infoBtn = tk.Button(text="О приложении",command=infoFunct)
	infoBtn.pack()
	closeBtn = tk.Button(text="Закрыть приложение",command=closeFunct)
	closeBtn.pack()
	return appVar

def createInfoWindow():
	infoApp = tk.Tk()
	infoApp.title("О ImageModifier")
	l1 = tk.Label(master=infoApp,text="ImageModifier v0.2.0",font="Arial 14")
	l1.pack()
	l2 = tk.Label(master=infoApp,text="Создано RodionGromo",font="Arial 7")
	l2.pack_configure(anchor="sw")
	return infoApp

def normaliseRGB(rgbTuple):
	summ = sumArr(rgbTuple)
	if(summ != 0):
		normR = math.floor((rgbTuple[0] / summ) * 255)
		normG = math.floor((rgbTuple[1] / summ) * 255)
		normB = math.floor((rgbTuple[2] / summ) * 255)
		return (normR,normG,normB)
	else:
		return (0,0,0)

def greyscale(rgbTuple):
	summ = sumArr(rgbTuple)
	cnt1 = int(summ / 3)
	return (cnt1,cnt1,cnt1)

def destroyCA():
	try:
		changerApp.destroy()
	except (tk.TclError,AttributeError) as e:
		pass

def modifierApp(action,newRGBTuple=None):
	global changerApp,changedImg,filepath,openFunctG,saveFunctG
	destroyCA()
	imgBase = Image.open(filepath)
	imgBlank = Image.new(mode="RGB",size=imgBase.size,color=(255,255,255))
	imgx,imgy = imgBlank.size
	imgBasePixels = imgBase.load()
	changedPix = 0
	for x in range(imgx):
		for y in range(imgy):
			if(action == 'norm'):
				imgBlank.putpixel([x,y],normaliseRGB(imgBasePixels[x,y]))
			elif(action == 'grscl'):
				imgBlank.putpixel([x,y],greyscale(imgBasePixels[x,y]))
			elif(action == 'rgbSwap'):
				imgBlank.putpixel([x,y],modifyRGB(imgBasePixels[x,y],newRGBTuple))
			changedPix += 1
	changedImg = imgBlank
	createShowcaseWindow(filepath,openFunctG,saveFunctG,imgBlank)

def modifyRGB(rgbTuple,newRGB):
	a = 0
	def addAdv(num,addV,maxV):
		if(num > maxV):
			num = maxV
		if(num + addV > maxV):
			return addV - (maxV - num)
		else:
			return num + addV
	if(len(rgbTuple) == 4):
		r,g,b,a = rgbTuple
	else:
		r,g,b = rgbTuple
		a = 0
	rAdd,gAdd,bAdd = newRGB
	return (addAdv(r,rAdd,255),addAdv(g,gAdd,255),addAdv(b,bAdd,255),a)

def advModifierApp(action):
	destroyCA()
	basicApp = tk.Tk()
	basicApp.title("Преобразователь 2.0")
	if(action == "rgbSwap"):
		tk.Label(master=basicApp,text="Значение R (от 1 до 254)").pack()
		entrR = tk.Entry(master=basicApp)
		entrR.pack()
		tk.Label(master=basicApp,text="Значение G (от 1 до 254)").pack()
		entrG = tk.Entry(master=basicApp)
		entrG.pack()
		tk.Label(master=basicApp,text="Значение B (от 1 до 254)").pack()
		entrB = tk.Entry(master=basicApp)
		entrB.pack()
		def modifyImg():
			rgbT = (int(entrR.get()),int(entrG.get()),int(entrB.get()))
			modifierApp("rgbSwap",rgbT)
			basicApp.destroy()
		startBtn = tk.Button(master=basicApp,text="Подсчитать",command=modifyImg).pack()

def sumArr(arr):
		summ = 0;
		for obj in arr:
			summ += obj
		return summ

def openChanges():
	global localShowcase,filepath,changerApp
	destroySC()
	changerApp = tk.Tk()
	changerApp.title("Доступные изменения")
	l1 = tk.Label(master=changerApp,text="Доступные преобразования")
	l1.pack()
	b1 = tk.Button(master=changerApp,text="Нормализатор",command=lambda: modifierApp('norm'))
	b2 = tk.Button(master=changerApp,text="Ч/Б преобразователь",command=lambda: modifierApp('grscl'))
	b3 = tk.Button(master=changerApp,text="RGB настройщик",command=lambda: advModifierApp('rgbSwap'))
	b1.pack()
	b2.pack()
	b3.pack()

def destroySC():
	global localShowcase
	try:
		localShowcase.destroy()
	except (tk.TclError,AttributeError) as e:
		pass


def createSaveWindow():
	def saveImg():
		global changedImg
		if(len(entr1.get()) > 1):
			path = askdirectory()
			print(path)
			changedImg.save(fp=f"{path}/{entr1.get()}.{saveFiletype}")
			#os.system(f"start {path}")
			saveWindow.destroy()
	saveWindow = tk.Tk()
	saveWindow.title("Сохранить...")
	lb1 = tk.Label(master=saveWindow,text="Введите имя файла:")
	entr1 = tk.Entry(master=saveWindow)
	btn1 = tk.Button(master=saveWindow,text="Выбрать папку и сохранить",command=saveImg)
	lb1.pack()
	entr1.pack()
	btn1.pack()
	saveWindow.mainloop()


def createShowcaseWindow(fileToShow,openFunct,saveFunct,changedImg=None):
	global filepath,localShowcase,openFunctG,saveFunctG
	destroySC()
	openFunctG = openFunct
	saveFunctG = saveFunct
	filepath = fileToShow
	localShowcase = tk.Toplevel()
	localShowcase.title("Преобразования")
	img1 = Image.open(filepath)
	img1_1 = Image.new(mode="RGB",size=(1005,500),color=(255,255,255))
	img1_1.paste(im=img1.resize(size=(500,500)))
	if(changedImg != None):
		img1_1.paste(im=changedImg.resize(size=(500,500)),box=(505,0))
	img2 = ImageTk.PhotoImage(img1_1)
	limg = tk.Label(master=localShowcase,image=img2)
	limg.image = img2
	limg.pack()
	openBtn = tk.Button(master=localShowcase,text="Открыть картинку",command=openFunct)
	openBtn.pack()
	saveBtn = tk.Button(master=localShowcase,text="Сохранить получившуюся картинку",command=saveFunct)
	saveBtn.pack()
	openChangesBtn = tk.Button(master=localShowcase,text="Открыть доступные изменения",command=openChanges)
	openChangesBtn.pack()