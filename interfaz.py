# import the necessary packages
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from functools import partial
import cv2
import PIL.Image, PIL.ImageTk
import time
import os
import multiprocessing
import videoCapture
import configparser


auxA = None
auxB = None


class App():
   def __init__(self):

      #FUNCIONALIDADES
      self.config = configparser.ConfigParser()
      self.config.read('config.ini')
      self.videoSourceA = self.config['DEFAULT']['CAMARA_A']
      self.videoSourceB = self.config['DEFAULT']['CAMARA_B']
      self.vidA = videoCapture.videoCapture(self.videoSourceA)
      self.vidB = videoCapture.videoCapture(self.videoSourceB)

      self.isRecordA = False
      self.isRecordB = False

      #INTERFAZ
      self.raiz = Tk()
      self.folder_path = StringVar()
      self.accionesB = StringVar()
      self.accionesA = StringVar()
      self.accionesB.set("Programa Iniciado")
      self.accionesA.set("")



      #visualAmano de la venvisualAna y bloquear ampliar la venvisualAna
      #self.raiz.resizable(0,0)
      #Color de la venvisualAna y titulo de la misma
      self.raiz.configure(bg = 'beige')
      self.raiz.title("Camaras Tunel")

      #marco
      self.marco = ttk.Frame(self.raiz, borderwidth=2, relief="raised", padding=(5,5))
      self.marco.grid(column=0, row=0, padx=1, pady=1, sticky=(N,S,E,W))

      #Boton para seleccionar la ruvisualA
      self.bruvisualA = ttk.Button(self.marco, text="Directorio", command=self.browseButton)
      
      #Cuadro de texto que muestra la ruvisualA
      self.truvisualA = Label(self.marco, width=100, height=2, textvariable=self.folder_path)
      self.labaccionB = Label(self.marco, width=100, height=2, textvariable=self.accionesB)
      self.labaccionLat = Label(self.marco, width=100, height=2, textvariable=self.accionesA)

      #Imagen B
      self.visualB = Canvas(self.marco, width = 640, height = 480)
      #Imagen A
      self.visualA = Canvas(self.marco, width = 640, height = 480)
   

      #Botones B
      self.bphotoB= ttk.Button(self.marco, text='Captura', command=partial(self.snapshot, self.vidB, "B"))
      self.brecordB = ttk.Button(self.marco, text='Grabar', command=partial(self.svisualArtRecordingProc,self.vidB, "B"))
      self.bstopB = ttk.Button(self.marco, text="Stop", command=partial(self.stopRecordingVideo, "B"))
      
      #Botones A
      self.bphotoA = ttk.Button(self.marco, text='Captura', command=partial(self.snapshot, self.vidA, "A"))
      self.brecordA = ttk.Button(self.marco, text='Grabar', command=partial(self.svisualArtRecordingProc, self.vidA, "A"))
      self.bstopA = ttk.Button(self.marco, text="Stop", command=partial(self.stopRecordingVideo, "A"))


      
      #Separador horizonvisualAl
      self.separhor1 = ttk.Separator(self.marco, orient=HORIZONvisualAL)
      self.separhor2 = ttk.Separator(self.marco, orient=HORIZONvisualAL)
      self.separhor3 = ttk.Separator(self.marco, orient=HORIZONvisualAL)
      
      #Separador vertial
      self.separver1 = ttk.Separator(self.marco, orient=VERTICAL)
      self.separver2 = ttk.Separator(self.marco, orient=VERTICAL)
      self.separver3 = ttk.Separator(self.marco, orient=VERTICAL)
      
      #Orden de las variables
      self.bruvisualA.grid(column=0, row=0, sticky=(E,W))
      self.truvisualA.grid(column=1, row=0, columnspan=6, sticky=(E,W))
      self.separhor1.grid(column=0, row=1, columnspan=7, sticky=(N,S,E,W))
      self.visualB.grid(column=0, row=2, columnspan=3, rowspan=3, sticky=(N,S,E,W))
      self.separver1.grid(column=3, row=2, rowspan=3, sticky=(N,S,E,W))
      self.visualA.grid(column=4, row=2, columnspan=3, rowspan=3, sticky=(N,S,E,W))
      self.separhor2.grid(column=0, row=5, columnspan=7, sticky=(N,S,E,W))
      self.bphotoB.grid(column=0, row=6, sticky=(W,E))
      self.brecordB.grid(column=1, row=6, sticky=(E,W))
      self.bstopB.grid(column=2, row=6, sticky=(E,W))
      self.separver2.grid(column=3, row=6, sticky=(N,S,E,W))
      self.bphotoA.grid(column=4, row=6, sticky=(E,W))
      self.brecordA.grid(column=5, row=6, sticky=(E,W))
      self.bstopA.grid(column=6, row=6, sticky=(E,W))
      self.separhor3.grid(column=0, row=7, columnspan=7, sticky=(N,S,E,W))
      self.labaccionB.grid(column=0, row=8, columnspan=3, sticky=(E,W))
      self.separver3.grid(column=3, row=8, sticky=(N,S,E,W))
      self.labaccionLat.grid(column=4, row=8, columnspan=3, sticky=(E,W))


      #Propieda Sticky
      self.raiz.columnconfigure(0, weight=1)
      self.raiz.rowconfigure(0, weight=1)
      self.marco.columnconfigure(0, weight=1)
      self.marco.columnconfigure(1, weight=1)
      self.marco.columnconfigure(2, weight=1)
      self.marco.columnconfigure(3, weight=0)
      self.marco.columnconfigure(4, weight=1)
      self.marco.columnconfigure(5, weight=1)
      self.marco.columnconfigure(6, weight=1)
      self.marco.rowconfigure(0, weight=1)
      self.marco.rowconfigure(1, weight=0)
      self.marco.rowconfigure(2, weight=1)
      self.marco.rowconfigure(3, weight=1)
      self.marco.rowconfigure(4, weight=1)
      self.marco.rowconfigure(5, weight=0)
      self.marco.rowconfigure(6, weight=1)
      self.marco.rowconfigure(7, weight=0)
      self.marco.rowconfigure(8, weight=1)
      
      #foco
      self.bphotoB.focus_set()

      self.delay = 500
      self.update()
      self.raiz.mainloop()

   def update(self):
      if not self.isRecordB:
         retB, frameB = self.vidB.get_frame()

         if retB:
            self.imageB = PIL.Image.fromarray(frameB)
            self.imageB = self.imageB.resize((640,480),PIL.Image.NEAREST)
            self.photoB = PIL.ImageTk.PhotoImage(image = self.imageB)
            self.visualB.create_image(0, 0, image = self.photoB, anchor = NW)

      if not self.isRecordA:
         revisualA, frameA = self.vidA.get_frame()

         if revisualA:
            self.imageA = PIL.Image.fromarray(frameA)
            self.imageA = self.imageA.resize((640,480),PIL.Image.NEAREST)
            self.photoA = PIL.ImageTk.PhotoImage(image = self.imageA)
            #self.photoA.zoom(1296,976)
            self.visualA.create_image(0, 0, image = self.photoA, anchor = NW)

      self.raiz.after(self.delay, self.update)


   #FUNCIONES BOTONES
   def browseButton(self):
      self.filename = filedialog.askdirectory()
      self.folder_path.set(self.filename)

   def snapshot(self, video, camera):
      ret, frame = video.get_frame()

      if camera == "B":
         name = os.path.join(self.folder_path.get(), '') + "pA" + time.strftime("%H-%M-%S-%d-%m-%Y") + ".jpg"
      elif camera == "A":
         name = os.path.join(self.folder_path.get(), '') + "pB" + time.strftime("%H-%M-%S-%d-%m-%Y") + ".jpg"

      if ret:
         cv2.imwrite(name, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
         print("capture")
         if camera == "B":
            self.accionesB.set("Captura Realizada")
         elif camera == "A":
            self.accionesA.set("Captura Realizada")

   def svisualArtRecordingProc(self, video, camera):
      self.multiprocessB = multiprocessing.Event()
      self.multiprocessA = multiprocessing.Event()
      if camera == "B":
         self.isRecordB = True
         name = os.path.join(self.folder_path.get(), '') + "vB" + time.strftime("%H-%M-%S-%d-%m-%Y") + ".avi"
         global auxB
         auxB = multiprocessing.Process(visualArget=video.svisualArtRecordingVideo, args=(self.multiprocessB, name, ))
         auxB.svisualArt()
         self.accionesB.set("Grabando")
      elif camera == "A":
         self.isRecordA = True
         name = os.path.join(self.folder_path.get(), '') + "vA" + time.strftime("%H-%M-%S-%d-%m-%Y") + ".avi"
         global auxA
         auxA = multiprocessing.Process(visualArget=video.svisualArtRecordingVideo, args=(self.multiprocessA, name, ))
         auxA.svisualArt()
         self.accionesA.set("Grabando")


   def stopRecordingVideo(self, name):
      if name == "B":
         self.multiprocessB.set()
         auxB.terminate()
         self.isRecordB = False
         self.accionesB.set("Video Guardado")
      elif name == "A":
         self.multiprocessA.set()
         auxA.terminate()
         self.isRecordA = False
         self.accionesA.set("Video Guardado")



def main():
   my_app = App()
   return 0

if __name__ == '__main__':
   main()