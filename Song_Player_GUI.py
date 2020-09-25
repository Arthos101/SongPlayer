from tkinter import *
from Song_Player import *
import threading
from time import sleep
from tkinter import filedialog

class App(): # threading.Thread
    
    def __init__(self):
        self.root = Tk() # create window
        self.song_titles_dir = filedialog.askopenfilename(initialdir = "/",title = "choose file",filetypes = (("txt files","*.txt"),("all files","*.*")))
        self.song_download_dir = filedialog.askdirectory(title='Select Download Location')
        self.txt_song_title = StringVar()
        self.player = Player(self.song_download_dir, self.song_titles_dir, self.txt_song_title)
        self.run()
    
    def song_setup(self):
        if (Player.get_init() == False):
            self.player.play_song_pg() # will not execute anything past this point while the song is still playing or while the while statement is active
            self.setup()
            Player.set_init(True)
        else:
            return
    
    def change_loop_junk(self):
        self.player.toggle_loop()
        self.txt_looping.set(self.player.get_looping())
    
    def callback(self):
        self.player.stop_song_pg()
        self.root.destroy()
    
    def change_song(self):
        self.player.play_next_song()
        self.txt_song_title.set(self.player.get_song_title())
    
    def setup(self):        
        '''
        BUTTONS
        '''
        

        next_song_btn = Button(self.root, text='next song', bd=2, command=self.change_song).grid(row=0)

        pause_song_btn = Button(self.root, text='pause', bd=2, command=self.player.pause_song_pg).grid(row=1)

        unpause_song_btn = Button(self.root, text='unpause', bd=2, command=self.player.unpause_song_pg).grid(row=1, column=1)

        volume_up_btn = Button(self.root, text='Volume Up', bd=2, command=self.player.inc_song_volume).grid(row=3)

        volume_down_btn = Button(self.root, text='Volume Down', bd=2, command=self.player.dec_song_volume).grid(row=3, column = 1)
        
        loop_btn = Button(self.root, text='loop', bd=1, command=self.change_loop_junk).grid(row=4, column=2)

        '''
        BUTTONS
        '''

        '''
        LABELS
        '''
        
        #self.txt_song_title = StringVar()
        self.lbl_song_title = Label(self.root, textvariable=self.txt_song_title, relief=RAISED).grid(row=0, column=1)
        self.txt_song_title.set(self.player.get_song_title())
        
        self.txt_looping = StringVar()
        self.lbl_loop = Label(self.root, textvariable=self.txt_looping, relief=RAISED).grid(row=4, column=1)
        self.txt_looping.set("Not looping")

        '''
        LABELS
        '''
        #self.root.after(0, setup)
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.geometry('300x150') # window size
        
        self.root.after(10, self.song_setup)
        self.root.mainloop()

if __name__ == "__main__":    
    app = App()