# main
import tkinter as tk
from tkinter.filedialog import askopenfilename
import mainWindows
mainApp = None
filePath = ""

def openFile():
	global filePath
	filePath = askopenfilename()
	print(filePath)
	if(len(filePath) > 2):
		mainWindows.createShowcaseWindow(filePath,openFile,saveFile)

def aboutApp():
	mainWindows.createInfoWindow()

def saveFile():
	if(mainWindows.changedImg != None):
		mainWindows.createSaveWindow()

def closeApp():
	global mainApp
	try:
		mainApp.destroy()
	except Exception as e:
		pass

mainApp = mainWindows.createMainWindow(openFile,aboutApp,closeApp)
mainApp.mainloop()
