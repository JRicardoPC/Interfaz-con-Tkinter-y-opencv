import cv2
import PIL.Image, PIL.ImageTk
import time
import os
import multiprocessing

class videoCapture():
   def __init__(self, video_source=0):
      self.vid = cv2.VideoCapture(video_source)
      if not self.vid.isOpened():
         raise ValueError("Unable to open video source", video_source)


   def get_frame(self):
      if self.vid.isOpened():
         ret, frame = self.vid.read()
         if ret:
            # Return a boolean success flag and the current frame converted to BGR
            return (ret, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
         else:
            return (ret, None)
      else:
         return (False, None)

   def isOpened(self):
      return self.vid.isOpened()

   def release(self):
      self.vid.release()

   def startRecordingVideo(self, multiprocess, name):
      #VIDEO
      #fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
      fourcc = cv2.VideoWriter_fourcc(*'XVID')
      out = cv2.VideoWriter(name,fourcc, 30.0, (1296,976))

      while(self.vid.isOpened()):
         if multiprocess.is_set():
            self.vid.release()
            out.release()
            cv2.destroyAllWindows()
            multiprocess.clear()
         
         ret, frame = self.get_frame()
         if ret:
            out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
         else:
            break




   def __del__(self):
      if self.vid.isOpened():
         self.vid.release()