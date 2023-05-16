from tkinter import *
from tkinter import messagebox
import customtkinter
import os
import pygame
import threading
import configparser
import time

try:
	config = configparser.ConfigParser()
	config.read("CTkSoundboard.ini")

	theme = config["CTk"]['theme']
	accentcolor = config["CTk"]['accentcolor']
	lastpath = str(config['CTk']['lastpath'])

	customtkinter.set_appearance_mode(theme)
	customtkinter.set_default_color_theme(accentcolor)
except Exception as e:
	messagebox.showerror('error','couldnt load the config file\ndetails:\n'+str(e))
	lastpath = ""

pygame.mixer.init()

def hideshowcontrolbuttons(hideshow):
	if hideshow == "show":
		stopbutton.pack(padx=9,pady=3,side=LEFT)
		importbutton.pack(pady=3,side=RIGHT,padx=17)
		pathlabel.pack(padx=(5,3),side=LEFT)
		pathentry.pack(side=LEFT,fill=X,expand=TRUE)

		importlabel.pack_forget()
		importprograssbar.pack_forget()
		percentagelabel.pack_forget()
	else:
		stopbutton.pack_forget()
		importbutton.pack_forget()
		pathlabel.pack_forget()
		pathentry.pack_forget()

		importlabel.pack()
		importprograssbar.pack()
		percentagelabel.pack()

def autoimportfromconfigfile(lastpath):
	global path

	if lastpath.endswith("/"):
		path = lastpath
	else:
		path = lastpath + "/"

	loadmusicthread = threading.Thread(target=importmusic)
	loadmusicthread.daemon = True
	loadmusicthread.start()

	del lastpath

def importbuttonpressed():
	global path

	if pathentry.get().endswith("/"):
		path = pathentry.get()
	else:
		path = pathentry.get() + "/"

	if path == "":
		messagebox.showerror("error","path cant be blank")
	else:
		if os.path.isdir(path) == True:
			loadmusicthread = threading.Thread(target=importmusic)
			loadmusicthread.daemon = True
			loadmusicthread.start()
			
			try:
				config.set('CTk','lastpath',str(pathentry.get()))
				with open('CTkSoundboard.ini','w') as file:
					config.write(file)
			except Exception as e:
				messagebox.showerror("error","couldnt write to config file\ndetails:\n"+str(e))
		else:
			messagebox.showerror("error","directory not found")

def stopmusic():
	pygame.mixer.music.stop()

def importmusic():
	global z

	hideshowcontrolbuttons("hide")

	for i in soundframe.winfo_children():
		i.destroy()
	music = []
	for file in os.listdir(path):
		if file.endswith(".mp3") or file.endswith(".wav") or file.endswith(".ogg"):	
			music.append(file)
		else:
			pass

	z = 0
	for file in os.listdir(path):
		def play(file = file):
			try:
				pygame.mixer.music.load(path + file)
				pygame.mixer.music.play(loops=0)
			except Exception as e:
				messagebox.showerror("error","couldnt play the audio\ndetails:\n"+str(e))

		if file.endswith(".mp3") or file.endswith(".wav") or file.endswith(".ogg"):	
			if file.endswith(".mp3"):
				customtkinter.CTkButton(soundframe,text=file.replace(".mp3",""),command=play,height=50).pack(fill=BOTH,padx=3,pady=3)
			elif file.endswith(".wav"):
				customtkinter.CTkButton(soundframe,text=file.replace(".wav",""),command=play,height=50).pack(fill=BOTH,padx=3,pady=3)
			elif file.endswith(".ogg"):
				customtkinter.CTkButton(soundframe,text=file.replace(".ogg",""),command=play,height=50).pack(fill=BOTH,padx=3,pady=3)
			z = z +1
			print(int(z / len(music) * 100))
			percentagelabel.configure(text='%'+str(int(z / len(music) * 100)))
		else:
			pass

	percentagelabel.configure(text='%')
	hideshowcontrolbuttons("show")


root = customtkinter.CTk()
root.title("CTkSoundboard")
root.geometry("500x300")
root.minsize(500, 300)

controlframe = customtkinter.CTkFrame(root)
controlframe.pack(expand=False,fill=X,side=TOP)
controlframe.configure(height=55)

soundframe = customtkinter.CTkScrollableFrame(root)
soundframe.pack(expand=True,fill=BOTH,side=BOTTOM)

stopbutton = customtkinter.CTkButton(controlframe)
stopbutton.configure(text="stop",height=50,width=80,command=stopmusic)

pathlabel = customtkinter.CTkLabel(controlframe)
pathlabel.configure(text="path:")

pathentry = customtkinter.CTkEntry(controlframe)

importbutton = customtkinter.CTkButton(controlframe)
importbutton.configure(text="import",height=50,width=50,command=importbuttonpressed)

importlabel = customtkinter.CTkLabel(controlframe)
importlabel.configure(text='importing')


importprograssbar = customtkinter.CTkProgressBar(controlframe)
importprograssbar.configure(mode="indeterminate")
importprograssbar.start()

percentagelabel = customtkinter.CTkLabel(controlframe)
percentagelabel.configure(text='%')


hideshowcontrolbuttons("show")

if os.path.isdir(lastpath) == True:
	autoimportfromconfigfile(lastpath)


root.mainloop()