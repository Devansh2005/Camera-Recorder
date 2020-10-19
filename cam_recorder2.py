import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import datetime as dt
import argparse  #to pass arguments automatically

class App:

    def __init__(self, window, window_title, video_source=0):
        self.window = window 
        self.window.title(window_title)
        self.video_source = video_source
        self.ok= False

        self.timer = ElapsedTimeClock(self.window)
        self.vid= VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.width, height = self.vid.height)
        self.canvas.pack()

        #Buttons

        self.btn_snapshot= tk.Button(window, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(side =tk.LEFT)

        self.btn_start= tk.Button(window, text="Start", command=self.open_camera)
        self.btn_start.pack(side =tk.LEFT)

        self.btn_stop= tk.Button(window, text="Stop", command=self.close_camera)
        self.btn_stop.pack(side =tk.LEFT)

        self.btn_quit= tk.Button(window, text="Quit", command=quit)
        self.btn_quit.pack(side =tk.LEFT)

        self.delay =10
        self.update()

        self.window.mainloop()

        def snapshot(self):
            ret, frame= self.vid.get_frame()

            if ret:
                cv2.imwrite("frame-"+time.strftime("%d-%m-%Y-%H-%M-%S")+".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        def open_camera(self):
            self.ok= True
            self.timer.start()
            print("Camera Opened => Recording Starts")
        
        def close_camera(self):
            self.ok= False
            self.timer.stop()
            print("Camera Closed => Recording Stops")

            #Upadte GUI with Cv2, pil

        def update(Self):
            ret, frame =self.vid.get_frame()
            if self.ok:
                self.vid.out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

            if ret:
                self.photo = PIL.ImageTk.PhotoImage(inmage= PIL.Image.fromarray(frame))
                self.canvas.create_image(0,0, image=self.photo, anchor= tk.NW)
            self.window.after(self.delay, self.update)


class VideoCapture:
    
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video souce", video_source)
        
        args = CommandLineParse().args

        VIDEO_TYPE={
            "avi":cv2.VideoWriter_fourcc(*"DIVX"),
            "mp4":cv2.VideoWriter_fourcc(*"DIVX"),
            
        }
        self.fourcc=VIDEO_TYPE[args.type[0]]

        STD_DiMENSITIONS ={
            "480p":(640,480),
            "720p":(1280,720),
            "1080p":(1920,1080),
            "4k":(3840,2160)
        }

        res=STD_DiMENSITIONS[args.res[0]]
        print(args.name, self.fourcc, res)


        self.out = cv2.VideoWriter(args.name[0]+"."+args.type[0],self.fourcc,10,res)

        self.vid.set(3,res[0])
        self.vid.set(4,res[1])

        self.width, self.height = res

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame,cv2.COLOR_RGB2BGR))
            else :
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            self.out.release()
            cv2.destroyAllWindows()


class ElapsedTimeClock:
    def __init__(self, window):
        self.T= tk.Label(window, text = "00:00:00", font=("times",20,"bold"),bg="yellow")
        self.T.pack(fill=tk.BOTH, expand=1)

        self.elapsedTime =dt.datetime(1,1,1)
        self.running =0
        self.lastTime= ""
        t= time.localtime()
        self.zeroTime =dt.timedelta(hours=t[3], minutes=t[4], seconds=t[5])



    def tick(self):
        self.now=dt.datetime(1,1,1).now()
        self.elapsedTime = self.now - self.zeroTime
        self.time2 = self.elapsedTime.strftime("%H:%M:%S")

        if self.time2 != self.lastTime:
            self.lastTime= self.time2
            self.T.config(text=self.time2)
        
        self.upwin =self.T.after(100, self.tick)

    def start(self):
        if not sef.running:
            self.zeroTime= dt.datetime(1,1,1).now()- self.elapsedTime
            self.tick()
            self.running= 1
    

    def stop(self):
        if self.running:
            self.T.after_cancel(self.upwin)
            self.elapsedTime= dt.datetime(1,1,1).now()- self.zeroTime
            self.time2 = self.elapsedTime
            self.running= 0



class CommandLineParse:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Video Recorder Application !!")
        parser.add_argument("--type", nargs=1, default=["avi"], type=str, help="To select the type of video")
        parser.add_argument("--res", nargs=1, default=["480p"], type=str, help="Resolution")
        parser.add_argument("--name", nargs=1, default=["output"], type=str, help="Video name")

        self.args =parser.parse_args()
    
def main():
    App(tk.Tk(), "Video Recorder")
main()

