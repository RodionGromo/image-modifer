import tkinter as tk
from tkinter import StringVar
from tkinter.filedialog import askopenfile
import tkinter.ttk as ttk
from PIL import Image,ImageDraw,ImageFont
import math

functApp = None;
imagePath = None;
progressBar = None;
statusLabel = None;
filename = None;
def exitAll():
	global functApp,selectorApp
	if(functApp != None):
		functApp.destroy();
	if(selectorApp != None):
		selectorApp.destroy();

def showFeedbackMenu():
	global functApp
	functApp = tk.Tk()
	functApp.title("Нет")
	functApp.geometry("120x50")
	noText = tk.Label(master=functApp,text="Нет")
	exitBtn = tk.Button(master=functApp,text="Понял, ухожу",command=exitAll)
	noText.pack()
	exitBtn.pack()

def sumArr(arr):
		summ = 0;
		for obj in arr:
			summ += obj
		return summ

def getImage():
	global imagePath,statusLabel,functApp
	ret = askopenfile(filetypes=[("Картинки",("*.png","*.jpeg","*.jpg"))])
	if(ret != None):
		statusLabel['text'] = "Готов к работе!"
		functApp.update_idletasks()
		imagePath = ret.name

def normaliseRGB(rgbTuple):
	#print(f"got {rgbTuple}")
	summ = sumArr(rgbTuple)
	if(summ != 0):
		normR = math.floor((rgbTuple[0] / summ) * 255)
		normG = math.floor((rgbTuple[1] / summ) * 255)
		normB = math.floor((rgbTuple[2] / summ) * 255)
		return (normR,normG,normB)
	else:
		return (0,0,0)


def saveImage(imageObject):
	global filename
	def sF():
		global filename
		file = open(input1.get()+".png",'wb')
		imageObject.save(file)
		aFA.destroy()
	aFA = tk.Tk()
	aFA.title("Сохранить")
	text1 = tk.Label(master=aFA,text="Имя файла?")
	text1.pack()
	input1 = tk.Entry(master=aFA)
	input1.pack()
	doneBtn = tk.Button(master=aFA,text="Готово",command=sF);
	doneBtn.pack()
	aFA.mainloop()


def startNormalising():
	global progressBar,functApp,imagePath,statusLabel
	if(imagePath != None):
		rgbTuples = []
		lastPerc = 0;
		readPixels = 0;
		imgBlank = None;
		font = None;
		fontSize = 0;
		image = Image.open(imagePath)
		pixels = image.load()
		imageW,imageH = image.size
		totalPixels = imageH * imageW
		statusLabel['text'] = "Нормализуем..."
		functApp.update_idletasks()
		fontSize = math.ceil((imageW / 2)/28)
		imgBlank = Image.new("RGB",image.size,(0,0,0))
		pixelDraw = 0;
		for x in range(imageW):
			for y in range(imageH):
				perc = math.floor((pixelDraw / totalPixels) * 100)
				if(perc != lastPerc):
					progressBar['value'] = perc
					functApp.update_idletasks()
					lastPerc = perc
				imgBlank.putpixel((x,y),normaliseRGB(pixels[x,y]))	
				pixelDraw += 1
		statusLabel['text'] = "Готово!"
		functApp.update_idletasks()
		saveImage(imgBlank)
	else:
		statusLabel['text'] = "Нет картинки"
		functApp.update_idletasks()

def createFuncApp(titleTop,titleBox,resoluton,startBtnFunc):
	global functApp,progressBar,statusLabel
	functApp = tk.Tk()
	functApp.title(titleTop)
	functApp.geometry(resoluton)
	welcomeText = tk.Label(master=functApp,text=f"{titleBox}\nВыберите картинку и жмите 'Начать!'")
	welcomeText.pack()
	getImageBtn = tk.Button(master=functApp,text="Открыть картинку",command=getImage)
	getImageBtn.pack()
	startNormalisingBtn = tk.Button(master=functApp,text="Начать!",command=startBtnFunc)
	startNormalisingBtn.pack()
	progressBar = ttk.Progressbar(master=functApp,orient="horizontal",mode="determinate",length=100)
	progressBar.pack()
	statusLabel = tk.Label(master=functApp,text="Нет картинки")
	statusLabel.pack()

def normaliseImage():
	createFuncApp("Нормализатор","Нормализатор картинок","250x125",startNormalising)

def calcBrightness(rgbTuple):
	return math.floor((rgbTuple[0] + rgbTuple[1] +  rgbTuple[2]) / 3)

def startGreyscaling():
	global progressBar,functApp,imagePath,statusLabel
	if(imagePath != None):
		rgbTuples = []
		lastPerc = 0;
		readPixels = 0;
		imgBlank = None;
		font = None;
		fontSize = 0;
		image = Image.open(imagePath)
		pixels = image.load()
		imageW,imageH = image.size
		totalPixels = imageH * imageW
		statusLabel['text'] = "Ч/Б'шаем..."
		functApp.update_idletasks()
		fontSize = math.ceil((imageW / 2)/28)
		imgBlank = Image.new("L",image.size,0)
		pixelDraw = 0;
		for x in range(imageW):
			for y in range(imageH):
				perc = math.floor((pixelDraw / totalPixels) * 100)
				if(perc != lastPerc):
					progressBar['value'] = perc
					functApp.update_idletasks()
					lastPerc = perc
				imgBlank.putpixel([x,y],calcBrightness(pixels[x,y]))
				pixelDraw += 1
		statusLabel['text'] = "Готово!"
		functApp.update_idletasks()
		saveImage(imgBlank)
	else:
		statusLabel['text'] = "Нет картинки"
		functApp.update_idletasks()

def greyscaleImage():
	createFuncApp("Ч/Б преобразователь","Ч/Б преобразователь картинок","250x120",startGreyscaling)

def overflowAdd(number,maximum,additive):
	left = 0
	decAdditive = 0
	if(number + additive > maximum):
		left = maximum - number
		decAdditive = additive - decAdditive;
		return decAdditive
	else:
		return number + additive

def shiftRGB(rgbTuple,shiftRGBTuple):
	return (overflowAdd(rgbTuple[0],255,shiftRGBTuple[0]),overflowAdd(rgbTuple[1],255,shiftRGBTuple[1]),overflowAdd(rgbTuple[2],255,shiftRGBTuple[2]))

def startShifing():
	global progressBar,functApp,imagePath,statusLabel,redEntry,greenEntry,blueEntry
	if(imagePath != None):
		rgbTuples = []
		lastPerc = 0;
		readPixels = 0;
		imgBlank = None;
		font = None;
		fontSize = 0;
		image = Image.open(imagePath)
		pixels = image.load()
		imageW,imageH = image.size
		totalPixels = imageH * imageW
		statusLabel['text'] = "Сдвигаем..."
		functApp.update_idletasks()
		fontSize = math.ceil((imageW / 2)/28)
		imgBlank = Image.new("RGB",image.size,(255,255,255))
		pixelDraw = 0;
		for x in range(imageW):
			for y in range(imageH):
				perc = math.floor((pixelDraw / totalPixels) * 100)
				if(perc != lastPerc):
					progressBar['value'] = perc
					functApp.update_idletasks()
					lastPerc = perc
				imgBlank.putpixel([x,y],shiftRGB(pixels[x,y],(int(redEntry.get()),int(greenEntry.get()),int(blueEntry.get()))))
				pixelDraw += 1
		statusLabel['text'] = "Готово!"
		functApp.update_idletasks()
		saveImage(imgBlank)
	else:
		statusLabel['text'] = "Нет картинки"
		functApp.update_idletasks()

def shiftRGBImage():
	createFuncApp("Сдвигатель RGB значений","Сдвигатель RGB значений","250x260",startShifing)
	global functApp,redEntry,greenEntry,blueEntry
	redText = tk.Label(master=functApp,text="Сдвиг красного цвета (1-255)")
	redText.pack()
	redEntry = tk.Entry(master=functApp)
	redEntry.pack()
	greenText = tk.Label(master=functApp,text="Сдвиг зеленого цвета (1-255)")
	greenText.pack()
	greenEntry = tk.Entry(master=functApp)
	greenEntry.pack()
	blueText = tk.Label(master=functApp,text="Сдвиг синего цвета (1-255)")
	blueText.pack()
	blueEntry = tk.Entry(master=functApp)
	blueEntry.pack()

def showInfo(topTitle,info):
	def closeInfo():
		infoApp.destroy()
	infoApp = tk.Tk()
	infoApp.geometry("150x50")
	infoApp.title("topTitle")
	info = tk.Label(master=infoApp,text=info)
	info.pack()
	exitBtn = tk.Button(master=infoApp,text="Ок",command=closeInfo)
	exitBtn.pack()

def findBrightness():
	global progressBar,functApp,imagePath,statusLabel,redEntry,greenEntry,blueEntry
	if(imagePath != None):
		rgbTuples = []
		lastPerc = 0;
		readPixels = 0;
		imgBlank = None;
		font = None;
		fontSize = 0;
		image = Image.open(imagePath)
		pixels = image.load()
		imageW,imageH = image.size
		totalPixels = imageH * imageW
		statusLabel['text'] = "Считаем..."
		functApp.update_idletasks()
		fontSize = math.ceil((imageW / 2)/28)
		imgBlank = Image.new("RGB",image.size,(255,255,255))
		pixelDraw = 0;
		pixelBrightness = []
		for x in range(imageW):
			for y in range(imageH):
				perc = math.floor((pixelDraw / totalPixels) * 100)
				if(perc != lastPerc):
					progressBar['value'] = perc
					functApp.update_idletasks()
					lastPerc = perc
				pixelBrightness.append(calcBrightness(pixels[x,y]))
				imgBlank.putpixel([x,y],calcBrightness(pixels[x,y]))
				pixelDraw += 1
		brightness = math.floor((((sumArr(pixelBrightness) / len(pixelBrightness)-1) / 255) * 100) *10)/10
		statusLabel['text'] = "Готово!"
		functApp.update_idletasks()
		showInfo("Готов!",f"Средняя яркость: {brightness}%")
	else:
		statusLabel['text'] = "Нет картинки"
		functApp.update_idletasks()

def getMedianBrightness():
	createFuncApp("Средняя яркость","Нахождение средней яркости изображения","250x125",findBrightness)

selectorApp = tk.Tk()
selectorApp.title("Модификатор картинок v0.1")
selectorApp.geometry("300x170")
selectorApp.resizable(0,0)
MainText = tk.Label(master=selectorApp,text="Преобразователь картинок v0.1\nВыберите действие:")
MainText.pack()
NormaliseBtn = tk.Button(master=selectorApp,text="Нормализовать",command=normaliseImage)
NormaliseBtn.pack()
BrightnessBtn = tk.Button(master=selectorApp,text="Преобразовать в оттенки серого",command=greyscaleImage)
BrightnessBtn.pack()
ShiftRGBBtn = tk.Button(master=selectorApp,text="Сдвиг цвета",command=shiftRGBImage)
ShiftRGBBtn.pack()
GetMedianBrightnessBtn = tk.Button(master=selectorApp,text="Найти среднюю яркость изображения",command=getMedianBrightness)
GetMedianBrightnessBtn.pack()
SendFeedbackBtn = tk.Button(master=selectorApp,text="Оставить отзыв",command=showFeedbackMenu)
SendFeedbackBtn.pack_configure(side='right')
exitBtn = tk.Button(master=selectorApp,text="Выход",command=exitAll)
exitBtn.pack_configure(side='left')
selectorApp.mainloop()