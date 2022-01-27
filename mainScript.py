import tkinter as tk
from tkinter import StringVar,Canvas,BooleanVar
from tkinter.filedialog import askopenfile
import tkinter.ttk as ttk
from PIL import Image,ImageDraw,ImageFont,ImageTk
import math
version = "0.1.2"
currentTranslation = 0
translations = [{
	#basic buttons and whatnot
	"basic:language": "EN",
	"basic:result": "Result",
	"basic:done": "Done",
	"basic:save": "Save",
	"basic:start": "Start",
	"basic:openImage": "Open image",
	"basic:ok": "Ok",
	"basic:ready": "Ready",
	"basic:images": "Images",
	"basic:saveInfo": "Image will be saved in app directory",
	"basic:info": "Info",
	"basic:askFilename": "Filename",
	"basic:doneBtn": "Done",
	"basic:noImage": "No image",
	#titles
	"title:metascraper": "Metadata eraser",
	"title:SelectorAppTitle": f"Image Modifier v{version}",
	#info
	"info:normText2": "Image normalizer",
	"info:funcAppInfo1": "Select image and press 'Start'",
	"info:greyscaleText2": "Greyscaler",
	"info:RGBShiftText2": "RGB Shifter",
	"info:BrightnessText2": "Average brightness counter",
	"info:metascraper": "Metadata eraser",
	"info:settingsMainText": "Customise app to your preferences",
	"info:SelectorAppText1.1": "Choose an action",
	#button texts
	"button:startBtn": "Start",
	"button:BtnMetascraper": "MetaScraper",
	"button:SettingsBtn": "Settings",
	"button:RGBShiftText1": "RGB Shifter",
	"button:BrightnessText1": "Average brightness",
	"button:settingsTitle": "App settings",
	"button:normText1": "Normalizer",
	"button:greyscaleText1": "Greyscaler",
	"button:ExitBtn": "Exit",
	#action text (doing something)
	"action:greyscaleAct": "Greyscaling",
	"action:RGBShiftTextAct": "Shifing",
	"action:metascraper": "Cleaning",
	"action:BrightnessAct": "Counting",
	"action:normalisingAct": "Normalizing",
	#rgb's special texts
	"rgbs:RedShiftText": "Red shift",
	"rgbs:GreenShiftText": "Green shift",
	"rgbs:BlueShiftText": "Blue shift",
	"rgbs:noChanges": "No changes made",
	#settings
	"setting:showRes": "Show result",
	"setting:showBefore": "Show before and after images"
},{
	#basic buttons and whatnot
	"basic:language": "RU",
	"basic:result": "Итог",
	"basic:done": "Готово",
	"basic:save": "Сохранить",
	"basic:start": "Начать",
	"basic:openImage": "Открыть картинку",
	"basic:ok": "Ок",
	"basic:ready": "Готов к работе",
	"basic:images": "Изображения",
	"basic:saveInfo": "Изображение будет сохранено в папке программы",
	"basic:info": "Инфо",
	"basic:askFilename": "Имя файла",
	"basic:doneBtn": "Готово",
	"basic:noImage": "Нет картинки",
	#titles
	"title:metascraper": "Очиститель метаданных",
	"title:SelectorAppTitle": f"Преобразователь картинок v{version}",
	#info
	"info:normText2": "Нормализатор картинок",
	"info:funcAppInfo1": "Выберите изображение и нажмите 'Начать'",
	"info:greyscaleText2": "Преобразовать в оттенки серого",
	"info:RGBShiftText2": "Сдвигатель RGB",
	"info:BrightnessText2": "Подсчет средней яркости",
	"info:metascraper": "Очиститель метаданных",
	"info:settingsMainText": "Настройте приложение по вкусу",
	"info:SelectorAppText1.1": "Выберите действие",
	#button texts
	"button:startBtn": "Начать",
	"button:BtnMetascraper": "MetaScraper",
	"button:SettingsBtn": "Настройки",
	"button:RGBShiftText1": "Сдвигатель RGB",
	"button:BrightnessText1": "Средняя яркость",
	"button:settingsTitle": "Настройки приложения",
	"button:normText1": "Нормализатор",
	"button:greyscaleText1": "Ч/Б преобразователь",
	"button:ExitBtn": "Выйти",
	#action text (doing something)
	"action:greyscaleAct": "Ч/Б'шаем",
	"action:RGBShiftTextAct": "Сдвигаем",
	"action:metascraper": "Чистим",
	"action:BrightnessAct": "Считаем",
	"action:normalisingAct": "Нормализируем",
	#rgb's special texts
	"rgbs:RedShiftText": "Сдвиг красного",
	"rgbs:GreenShiftText": "Сдвиг зеленого",
	"rgbs:BlueShiftText": "Сдвиг синего",
	"rgbs:noChanges": "Нет изменений",
	#settings
	"setting:showRes": "Показывать результат",
	"setting:showBefore": "Показывать изображение до и после"
}]
functApp = None;
imagePath = None;
progressBar = None;
statusLabel = None;
filename = None;
LanguageSelector = None;

settings = {
	"showRes": True,
	"showBefore": False
}

def nextLanguage():
	glVars = globals()
	if(glVars["currentTranslation"] < len(glVars["translations"])-1):
		glVars["currentTranslation"] += 1
	else:
		glVars["currentTranslation"] = 0
	glVars["LanguageSelector"]['text'] = translations[currentTranslation]["basic:language"]
	selectorApp.title(translations[currentTranslation]["title:SelectorAppTitle"])
	MainText['text'] = translations[currentTranslation]["title:SelectorAppTitle"]+"\n"+translations[currentTranslation]["info:SelectorAppText1.1"]+":"
	NormaliseBtn['text'] = translations[currentTranslation]["button:normText1"]
	BrightnessBtn['text'] = translations[currentTranslation]["button:greyscaleText1"]
	ShiftRGBBtn['text'] = translations[currentTranslation]["button:RGBShiftText1"]
	GetMedianBrightnessBtn['text'] = translations[currentTranslation]["button:BrightnessText1"]
	SettingsBtn['text'] = translations[currentTranslation]["button:SettingsBtn"]
	exitBtn['text'] = translations[currentTranslation]["button:ExitBtn"]
	selectorApp.update_idletasks()


def exitAll():
	global functApp,selectorApp
	try:
		functApp.destroy();
	except (tk.TclError,AttributeError) as e:
		pass
	if(selectorApp != "." or selectorApp != None):
		selectorApp.destroy();

def showResult(beforeImage,afterImage):
	global settings
	print(beforeImage,afterImage)
	x,y = beforeImage.size
	if(settings['showBefore']):
		baseImage = Image.new("RGB",(math.floor((x+100)*2),y),color=(255,255,255))
		baseImage.paste(beforeImage)
		baseImage.paste(afterImage,(x+100,0))
	else:
		baseImage = Image.new("RGB",(x,y),color=(255,255,255))
		baseImage.paste(afterImage)
	baseImage.show()


def showSettingsMenu():
	global functApp,settings,checkboxes
	functApp = tk.Tk()
	functApp.geometry("256x128")
	functApp.title(translations[currentTranslation]["button:settingsTitle"])
	lb1 = tk.Label(functApp,text=translations[currentTranslation]["info:settingsMainText"])
	lb1.pack()
	def setSetting(setting):
		settings[setting] = not settings[setting]
	for setting in settings:
		cb1 = tk.Checkbutton(functApp,text=translations[currentTranslation][f"setting:{setting}"],command=lambda: setSetting(setting))
		if(settings[setting]):
			cb1.select()
		cb1.pack()
		

def sumArr(arr):
		summ = 0;
		for obj in arr:
			summ += obj
		return summ

def getImage():
	global imagePath,statusLabel,functApp
	ret = askopenfile(filetypes=[(translations[currentTranslation]["basic:images"],("*.png","*.jpeg","*.jpg"))])
	if(ret != None):
		statusLabel['text'] = translations[currentTranslation]["basic:ready"]
		functApp.focus_force()
		functApp.update_idletasks()
		imagePath = ret.name

def normaliseRGB(rgbTuple):
	summ = sumArr(rgbTuple)
	if(summ != 0):
		normR = math.floor((rgbTuple[0] / summ) * 255)
		normG = math.floor((rgbTuple[1] / summ) * 255)
		normB = math.floor((rgbTuple[2] / summ) * 255)
		return (normR,normG,normB)
	else:
		return (0,0,0)


def saveImage(imageObject,skipShow=False,baseline=None):
	global filename,settings
	def sF():
		global filename,settings
		if(len(input1.get()) == 0):
			return
		showInfo(translations[currentTranslation]["basic:info"],translations[currentTranslation]["basic:saveInfo"])
		file = open(input1.get()+".png",'wb')
		imageObject.save(file)
		if(settings["showRes"] and skipShow == False):
			showResult(baseline,imageObject)
		aFA.destroy()
	aFA = tk.Tk()
	aFA.focus_set()
	aFA.title(translations[currentTranslation]["basic:save"])
	text1 = tk.Label(master=aFA,text=translations[currentTranslation]["basic:askFilename"])
	text1.pack()
	input1 = tk.Entry(master=aFA)
	input1.pack()
	doneBtn = tk.Button(master=aFA,text=translations[currentTranslation]["basic:done"],command=sF);
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
		statusLabel['text'] = translations[currentTranslation]["action:normalisingAct"]
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
		statusLabel['text'] = translations[currentTranslation]["basic:done"]
		functApp.update_idletasks()
		saveImage(imageObject=imgBlank,baseline=image)
	else:
		statusLabel['text'] = translations[currentTranslation]["basic:noImage"]
		functApp.update_idletasks()

def createFuncApp(titleTop,titleBox,resoluton,startBtnFunc):
	global functApp,progressBar,statusLabel
	functApp = tk.Tk()
	functApp.focus_set()
	functApp.resizable(0,0)
	functApp.title(titleTop)
	functApp.geometry(resoluton)
	welcomeText = tk.Label(master=functApp,text=titleBox+"\n"+translations[currentTranslation]["info:funcAppInfo1"])
	welcomeText.pack()
	getImageBtn = tk.Button(master=functApp,text=translations[currentTranslation]["basic:openImage"],command=getImage)
	getImageBtn.pack()
	startNormalisingBtn = tk.Button(master=functApp,text=translations[currentTranslation]["basic:start"]+"!",command=startBtnFunc)
	startNormalisingBtn.pack()
	progressBar = ttk.Progressbar(master=functApp,orient="horizontal",mode="determinate",length=100)
	progressBar.pack()
	statusLabel = tk.Label(master=functApp,text=translations[currentTranslation]["basic:noImage"])
	statusLabel.pack()

def normaliseImage():
	createFuncApp(translations[currentTranslation]["button:normText1"],translations[currentTranslation]["info:normText2"],"250x125",startNormalising)

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
		statusLabel['text'] = translations[currentTranslation]["action:greyscaleAct"]
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
		statusLabel['text'] = translations[currentTranslation]["basic:done"]
		functApp.update_idletasks()
		saveImage(imageObject=imgBlank,baseline=image)
	else:
		statusLabel['text'] = translations[currentTranslation]["basic:noImage"]
		functApp.update_idletasks()

def greyscaleImage():
	createFuncApp(translations[currentTranslation]["button:greyscaleText1"],translations[currentTranslation]["info:greyscaleText2"],"250x130",startGreyscaling)

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
		statusLabel['text'] = translations[currentTranslation]["action:RGBShiftTextAct"]
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
		statusLabel['text'] = translations[currentTranslation]["basic:done"]
		functApp.update_idletasks()
		saveImage(imageObject=imgBlank,baseline=image)
	elif(err == True):
		statusLabel['text'] = translations[currentTranslation]["rgbs:noChanges"]
		functApp.update_idletasks()
	else:
		statusLabel['text'] = translations[currentTranslation]["basic:noImage"]
		functApp.update_idletasks()

def shiftRGBImage():
	createFuncApp(translations[currentTranslation]["button:RGBShiftText1"],translations[currentTranslation]["info:RGBShiftText2"],"250x260",startShifing)
	global functApp,redEntry,greenEntry,blueEntry
	redText = tk.Label(master=functApp,text=translations[currentTranslation]["rgbs:RedShiftText"] + " (1-255)")
	redText.pack()
	redEntry = tk.Entry(master=functApp)
	redEntry.pack()
	greenText = tk.Label(master=functApp,text=translations[currentTranslation]["rgbs:GreenShiftText"] + " (1-255)")
	greenText.pack()
	greenEntry = tk.Entry(master=functApp)
	greenEntry.pack()
	blueText = tk.Label(master=functApp,text=translations[currentTranslation]["rgbs:BlueShiftText"] + " (1-255)")
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
	exitBtn = tk.Button(master=infoApp,text=translations[currentTranslation]["basic:ok"],command=closeInfo)
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
		statusLabel['text'] = translations[currentTranslation]["action:BrightnessAct"]
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
		statusLabel['text'] = translations[currentTranslation]["basic:done"]
		functApp.update_idletasks()
		showInfo(translations[currentTranslation]["basic:done"],translations[currentTranslation]["button:BrightnessText1"]+f": {brightness}%")
	else:
		statusLabel['text'] = translations[currentTranslation]["basic:noImage"]
		functApp.update_idletasks()

def metascrapper():
	if(imagePath != None):
		image = Image.open(imagePath)
		saveImage(image,skipShow=True)
	else:
		statusLabel['text'] = translations[currentTranslation]["basic:noImage"]
		functApp.update_idletasks()

def scrapeMetaApp():
	createFuncApp(translations[currentTranslation]["title:metascraper"],translations[currentTranslation]["info:metascraper"],"250x125",metascrapper)

def getMedianBrightness():
	createFuncApp(translations[currentTranslation]["button:BrightnessText1"],translations[currentTranslation]["info:BrightnessText2"],"250x125",findBrightness)

selectorApp = tk.Tk()
selectorApp.title(translations[currentTranslation]["title:SelectorAppTitle"])
selectorApp.geometry("300x190")
selectorApp.resizable(0,0)
MainText = tk.Label(master=selectorApp,text=translations[currentTranslation]["title:SelectorAppTitle"]+"\n"+translations[currentTranslation]["info:SelectorAppText1.1"]+":")
MainText.pack()
NormaliseBtn = tk.Button(master=selectorApp,text=translations[currentTranslation]["button:normText1"],command=normaliseImage)
NormaliseBtn.pack()
BrightnessBtn = tk.Button(master=selectorApp,text=translations[currentTranslation]["button:greyscaleText1"],command=greyscaleImage)
BrightnessBtn.pack()
ShiftRGBBtn = tk.Button(master=selectorApp,text=translations[currentTranslation]["button:RGBShiftText1"],command=shiftRGBImage)
ShiftRGBBtn.pack()
GetMedianBrightnessBtn = tk.Button(master=selectorApp,text=translations[currentTranslation]["button:BrightnessText1"],command=getMedianBrightness)
GetMedianBrightnessBtn.pack()
BtnMetascraper = tk.Button(master=selectorApp,text=translations[currentTranslation]["button:BtnMetascraper"],command=scrapeMetaApp)
BtnMetascraper.pack()
SettingsBtn = tk.Button(master=selectorApp,text=translations[currentTranslation]["button:SettingsBtn"],command=showSettingsMenu)
SettingsBtn.pack_configure(side='right')
exitBtn = tk.Button(master=selectorApp,text=translations[currentTranslation]["button:ExitBtn"],command=exitAll)
exitBtn.pack_configure(side='left')
LanguageSelector = tk.Button(master=selectorApp,text=translations[currentTranslation]["basic:language"],command=nextLanguage)
LanguageSelector.place(anchor="nw")
selectorApp.mainloop()
