import tkinter as tk
from tkinter import StringVar,Canvas,BooleanVar
from tkinter.filedialog import askopenfile
import tkinter.ttk as ttk
from PIL import Image,ImageDraw,ImageFont,ImageTk
import math
version = "0.1.1"
currentTranslation = 0
translations = ({
	"Language": "EN",
	"done": "Done",
	"save": "Save",
	"openImage": "Open image",
	"start": "Start",
	"ok": "Ok",
	"ready": "Ready",
	"images": "Images",
	"saveInfo": "Image will be saved in app directory",
	"info": "Info",
	"askFilename": "Filename",
	"doneBtn": "Done",
	"normalisingAct": "Normalising",
	"noImage": "No image",
	"funcAppInfo1": "Select image and press 'Start'",
	"startBtn": "Start",
	"normText1": "Normaliser",
	"normText2": "Image normaliser",
	"greyscaleAct": "Greyscaling",
	"greyscaleText1": "Greyscaler",
	"greyscaleText2": "Greyscale an image",
	"RGBShiftTextAct": "Shifting",
	"RGBShiftText1": "RGB shift",
	"RGBShiftText2": "RGB shifter",
	"RedShiftText": "Red shift",
	"GreenShiftText": "Green shift",
	"BlueShiftText": "Blue shift",
	"BrightnessAct": "Calculating",
	"BrightnessText1": "Median brightness",
	"BrightnessText2": "Finding median brightness",
	"SelectorAppTitle": f"Image Modifier v{version}",
	"SelectorAppText1.1": "Choose an action",
	"ExitBtn": "Exit",
	"noChanges": "No changes made",
	"result": "Result",
	"settingsTitle": "App settings",
	"setting:showRes": "Show results",
	"SettingsBtn": "Settings",
	"settingsMainText": "Change app to your preferences"
},{
	"Language": "RU",
	"result": "Итог",
	"done": "Готово",
	"save": "Сохранить",
	"start": "Начать",
	"openImage": "Открыть картинку",
	"ok": "Ок",
	"ready": "Готов к работе",
	"images": "Изображения",
	"saveInfo": "Изображение будет сохранено в папке программы",
	"info": "Инфо",
	"askFilename": "Имя файла",
	"doneBtn": "Готово",
	"normalisingAct": "Нормализируем",
	"noImage": "Нет картинки",
	"funcAppInfo1": "Выберите изображение и нажмите 'Начать'",
	"startBtn": "Начать",
	"normText1": "Нормализатор",
	"normText2": "Нормализатор картинок",
	"greyscaleAct": "Ч/Б'шаем",
	"greyscaleText1": "Ч/Б преобразователь",
	"greyscaleText2": "Преобразовать в оттенки серого",
	"RGBShiftTextAct": "Сдвигаем",
	"RGBShiftText1": "Сдвигатель RGB",
	"RGBShiftText2": "Сдвигатель RGB",
	"RedShiftText": "Сдвиг красного",
	"GreenShiftText": "Сдвиг зеленого",
	"BlueShiftText": "Сдвиг синего",
	"BrightnessAct": "Считаем",
	"BrightnessText1": "Средняя яркость",
	"BrightnessText2": "Подсчет средней яркости",
	"SelectorAppTitle": f"Преобразователь картинок v{version}",
	"SelectorAppText1.1": "Выберите действие",
	"ExitBtn": "Выйти",
	"noChanges": "Нет изменений",
	"settingsTitle": "Настройки приложения",
	"setting:showRes": "Показывать результат",
	"SettingsBtn": "Настройки",
	"settingsMainText": "Настройте приложение по вкусу"
})
functApp = None;
imagePath = None;
progressBar = None;
statusLabel = None;
filename = None;
functAppActive = False;
LanguageSelector = None;

checkboxes = []

settings = {
	"showRes": True
}

def nextLanguage():
	glVars = globals()
	if(glVars["currentTranslation"] < len(glVars["translations"])-1):
		glVars["currentTranslation"] += 1
	else:
		glVars["currentTranslation"] = 0
	glVars["LanguageSelector"]['text'] = translations[currentTranslation]["Language"]
	selectorApp.title(translations[currentTranslation]["SelectorAppTitle"])
	MainText['text'] = translations[currentTranslation]["SelectorAppTitle"]+"\n"+translations[currentTranslation]["SelectorAppText1.1"]+":"
	NormaliseBtn['text'] = translations[currentTranslation]["normText1"]
	BrightnessBtn['text'] = translations[currentTranslation]["greyscaleText1"]
	ShiftRGBBtn['text'] = translations[currentTranslation]["RGBShiftText1"]
	GetMedianBrightnessBtn['text'] = translations[currentTranslation]["BrightnessText1"]
	SettingsBtn['text'] = translations[currentTranslation]["SettingsBtn"]
	exitBtn['text'] = translations[currentTranslation]["ExitBtn"]
	selectorApp.update_idletasks()


def exitAll():
	global functApp,selectorApp,functAppActive
	try:
		functApp.destroy();
	except (tk.TclError,AttributeError) as e:
		pass
	if(selectorApp != "." or selectorApp != None):
		selectorApp.destroy();

def showResult(fileName):
	global functApp
	functApp = tk.Tk()
	functApp.title(translations[currentTranslation]["result"])
	canvas = Canvas(functApp)
	fileName = f"./{fileName}"
	imageObject = Image.open(fileName);
	img1 = ImageTk.PhotoImage(imageObject)
	print(fileName)
	image = canvas.create_image(0, 0, anchor='nw',image=img1);
	exitBtn = tk.Button(master=functApp,text=translations[currentTranslation]["ok"],command=functApp.destroy)
	exitBtn.pack()
	image.pack()


def showSettingsMenu():
	global functApp,settings,checkboxes
	functApp = tk.Tk()
	functApp.geometry("256x64")
	functApp.title(translations[currentTranslation]["settingsTitle"])
	lb1 = tk.Label(functApp,text=translations[currentTranslation]["settingsMainText"])
	lb1.pack()
	def setSetting(setting):
		settings[setting] = not settings[setting]
	for setting in settings:
		cb1 = tk.Checkbutton(functApp,text=translations[currentTranslation][f"setting:{setting}"],command=lambda: setSetting(setting))
		if(settings[setting]):
			cb1.select()
		cb1.pack_configure(side="left")
		

def sumArr(arr):
		summ = 0;
		for obj in arr:
			summ += obj
		return summ

def getImage():
	global imagePath,statusLabel,functApp
	ret = askopenfile(filetypes=[(translations[currentTranslation]["images"],("*.png","*.jpeg","*.jpg"))])
	if(ret != None):
		statusLabel['text'] = translations[currentTranslation]["ready"]
		functApp.focus_force()
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
	global filename,settings
	def sF():
		showInfo(translations[currentTranslation]["info"],translations[currentTranslation]["saveInfo"])
		global filename
		file = open(input1.get()+".png",'wb')
		imageObject.save(file)
		if(settings["showRes"]):
			imageObject.show(title=translations[currentTranslation]["result"])
		aFA.destroy()
	aFA = tk.Tk()
	aFA.focus_set()
	aFA.title(translations[currentTranslation]["save"])
	text1 = tk.Label(master=aFA,text=translations[currentTranslation]["askFilename"])
	text1.pack()
	input1 = tk.Entry(master=aFA)
	input1.pack()
	doneBtn = tk.Button(master=aFA,text=translations[currentTranslation]["done"],command=sF);
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
		statusLabel['text'] = translations[currentTranslation]["normalisingAct"]
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
		statusLabel['text'] = translations[currentTranslation]["done"]
		functApp.update_idletasks()
		saveImage(imgBlank)
	else:
		statusLabel['text'] = translations[currentTranslation]["noImage"]
		functApp.update_idletasks()

def createFuncApp(titleTop,titleBox,resoluton,startBtnFunc):
	global functApp,progressBar,statusLabel
	functAppActive = True;
	functApp = tk.Tk()
	functApp.focus_set()
	functApp.resizable(0,0)
	functApp.title(titleTop)
	functApp.geometry(resoluton)
	welcomeText = tk.Label(master=functApp,text=titleBox+"\n"+translations[currentTranslation]["funcAppInfo1"])
	welcomeText.pack()
	getImageBtn = tk.Button(master=functApp,text=translations[currentTranslation]["openImage"],command=getImage)
	getImageBtn.pack()
	startNormalisingBtn = tk.Button(master=functApp,text=translations[currentTranslation]["start"]+"!",command=startBtnFunc)
	startNormalisingBtn.pack()
	progressBar = ttk.Progressbar(master=functApp,orient="horizontal",mode="determinate",length=100)
	progressBar.pack()
	statusLabel = tk.Label(master=functApp,text=translations[currentTranslation]["noImage"])
	statusLabel.pack()

def normaliseImage():
	createFuncApp(translations[currentTranslation]["normText1"],translations[currentTranslation]["normText2"],"250x125",startNormalising)

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
		statusLabel['text'] = translations[currentTranslation]["greyscaleAct"]
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
		statusLabel['text'] = translations[currentTranslation]["done"]
		functApp.update_idletasks()
		saveImage(imgBlank)
	else:
		statusLabel['text'] = translations[currentTranslation]["noImage"]
		functApp.update_idletasks()

def greyscaleImage():
	createFuncApp(translations[currentTranslation]["greyscaleText1"],translations[currentTranslation]["greyscaleText2"],"250x130",startGreyscaling)

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
	shiftRGBTuple = ()
	err = False
	try:
		shiftRGBTuple = (int(redEntry.get()),int(greenEntry.get()),int(blueEntry.get()))
	except ValueError as e:
		err = True

	if(imagePath != None and err == False):
		shiftRGBTuple = (int(redEntry.get()),int(greenEntry.get()),int(blueEntry.get()))
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
		statusLabel['text'] = translations[currentTranslation]["RGBShiftTextAct"]
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
				imgBlank.putpixel([x,y],shiftRGB(pixels[x,y],shiftRGBTuple))
				pixelDraw += 1
		statusLabel['text'] = translations[currentTranslation]["done"]
		functApp.update_idletasks()
		saveImage(imgBlank)
	elif(err == True):
		statusLabel['text'] = translations[currentTranslation]["noChanges"]
		functApp.update_idletasks()
	else:
		statusLabel['text'] = translations[currentTranslation]["noImage"]
		functApp.update_idletasks()

def shiftRGBImage():
	createFuncApp(translations[currentTranslation]["RGBShiftText1"],translations[currentTranslation]["RGBShiftText2"],"250x260",startShifing)
	global functApp,redEntry,greenEntry,blueEntry
	redText = tk.Label(master=functApp,text=translations[currentTranslation]["RedShiftText"] + " (1-255)")
	redText.pack()
	redEntry = tk.Entry(master=functApp)
	redEntry.pack()
	greenText = tk.Label(master=functApp,text=translations[currentTranslation]["GreenShiftText"] + " (1-255)")
	greenText.pack()
	greenEntry = tk.Entry(master=functApp)
	greenEntry.pack()
	blueText = tk.Label(master=functApp,text=translations[currentTranslation]["BlueShiftText"] + " (1-255)")
	blueText.pack()
	blueEntry = tk.Entry(master=functApp)
	blueEntry.pack()

def showInfo(topTitle,info):
	def closeInfo():
		infoApp.destroy()
	infoApp = tk.Tk()
	infoApp.geometry("300x50")
	infoApp.title(topTitle)
	info = tk.Label(master=infoApp,text=info)
	info.pack()
	exitBtn = tk.Button(master=infoApp,text=translations[currentTranslation]["ok"],command=closeInfo)
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
		statusLabel['text'] = translations[currentTranslation]["BrightnessAct"]
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
		statusLabel['text'] = translations[currentTranslation]["done"]
		functApp.update_idletasks()
		showInfo(translations[currentTranslation]["done"],translations[currentTranslation]["BrightnessText1"]+f": {brightness}%")
	else:
		statusLabel['text'] = translations[currentTranslation]["noImage"]
		functApp.update_idletasks()

def getMedianBrightness():
	createFuncApp(translations[currentTranslation]["BrightnessText1"],translations[currentTranslation]["BrightnessText2"],"250x125",findBrightness)

selectorApp = tk.Tk()
selectorApp.title(translations[currentTranslation]["SelectorAppTitle"])
selectorApp.geometry("300x170")
selectorApp.resizable(0,0)
MainText = tk.Label(master=selectorApp,text=translations[currentTranslation]["SelectorAppTitle"]+"\n"+translations[currentTranslation]["SelectorAppText1.1"]+":")
MainText.pack()
NormaliseBtn = tk.Button(master=selectorApp,text=translations[currentTranslation]["normText1"],command=normaliseImage)
NormaliseBtn.pack()
BrightnessBtn = tk.Button(master=selectorApp,text=translations[currentTranslation]["greyscaleText1"],command=greyscaleImage)
BrightnessBtn.pack()
ShiftRGBBtn = tk.Button(master=selectorApp,text=translations[currentTranslation]["RGBShiftText1"],command=shiftRGBImage)
ShiftRGBBtn.pack()
GetMedianBrightnessBtn = tk.Button(master=selectorApp,text=translations[currentTranslation]["BrightnessText1"],command=getMedianBrightness)
GetMedianBrightnessBtn.pack()
SettingsBtn = tk.Button(master=selectorApp,text=translations[currentTranslation]["SettingsBtn"],command=showSettingsMenu)
SettingsBtn.pack_configure(side='right')
exitBtn = tk.Button(master=selectorApp,text=translations[currentTranslation]["ExitBtn"],command=exitAll)
exitBtn.pack_configure(side='left')
LanguageSelector = tk.Button(master=selectorApp,text=translations[currentTranslation]["Language"],command=nextLanguage)
LanguageSelector.place(anchor="nw")
selectorApp.mainloop()
