# importing the libraries
import urllib.request
import re
import youtube_dl
import os
import pygame as pg
import random as r
from mutagen.mp3 import MP3
import threading
from tkinter import *

class Player: # class for playing the music, i.e. the name "Player"
    
    initiated = False
    
    def __init__(self, directory, directory_for_song_titles, txt, songs=[]): # constructor, songs can be filled out as a predetermined list of strings   txt
        self.directory = directory + "/"
        self.songs = songs
        self.song_titles_dir = directory_for_song_titles
        if (len(songs)==0): # if songs is empty
            self.get_list_of_songs()
        self.download_songs()
        self.thread = 0
        self.end_thread = False
        self.current_song = 0
        self.current_song_file = 0
        self.playing_song = False
        self.looping = False
        self.txt = txt
        self.song_name = ""
        
    @classmethod
    def get_init(self):
        return Player.initiated
    
    @classmethod
    def set_init(self, val):
        Player.initiated = val
    
    def toggle_loop(self):
        self.looping = not self.looping
    
    def get_looping(self):
        return self.looping
    
    def get_song_title(self):
        return self.current_song
    
    def get_playing_song(self):
        return self.playing_song
    
    def convert_to_time(seconds):
        milliseconds = seconds * 1000
        return milliseconds
        '''
        hours = seconds // 3600
        seconds %= 3600
        mins = seconds // 60
        seconds %= 60
        '''
    
    def get_list_of_songs(self):
        try:
            with open(self.song_titles_dir, "r") as file: # change to path of songs list
                for line in file:
                    stripped_line = line.strip()
                    self.songs.append(stripped_line)
        except:
            print("NO DIRECTORY GIVEN")
    
    def get_random_song(self):
        self.current_song = self.songs[r.randint(0, len(self.songs) - 1)]
        return self.current_song
    
    def download_songs(self): # download the songs from the internet and save them as an mp3 on the directory specified
      if len(self.songs) > 0:
          for song in self.songs:
              installed = False
              for filename in os.listdir(self.directory):
                if (filename.endswith('.mp3')):
                  if (filename[:-4] == song):
                      print(song + ": ALREADY INSTALLED")
                      installed = True
                      break
              if (installed == False):
                  print(song + ": INSTALLING...")
                  ydl_opts = {
                      'format': 'best',
                      'outtmpl': self.directory + song + '.mp4',
                      'postprocessors': [{
                          'key': 'FFmpegExtractAudio',
                          'preferredcodec': 'mp3',
                          'preferredquality': '192',
                  }],
                  }
                  song = song.replace(" ", "+")
                  html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + song)
                  video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                  url = "https://www.youtube.com/watch?v=" + video_ids[0]
                  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                      ydl.download([url])
                      
    def init_music_windows(self, file): # useless right now just for later use i guess, should probably get rid of it
        os.startfile(file)
        
    def play_song_os(self, song_name): # pracitcally useless right now
        for filename in os.listdir(self.directory):
            if (filename.endswith('.mp3')):
              if (filename[:-4] == song_name):
                  self.init_music_os(self.directory + self.get_random_song())    
    
    def play_song_pg(self):
        if (self.looping == False or self.song_name == ""): # if no songs has played yet or if looping is enabled
            self.song_name = self.get_random_song() # pick random song
        else: #otherwise
            pass # do nothing
        for filename in os.listdir(self.directory):
            if (filename.endswith('.mp3')):
              if (filename[:-4] == self.song_name):
                  self.init_music_pg(self.directory + self.song_name + ".mp3", 0.03) # best volume for me :)
    
    def init_music_pg(self, file, volume=0.1):
        '''
        stream music with mixer.music module in a blocking manner
        this will stream the sound from disk while playing
        '''
        # set up the mixer
        freq = 44100     # audio CD quality
        bitsize = -16    # unsigned 16 bit
        channels = 2     # 1 is mono, 2 is stereo
        buffer = 2048    # number of samples (experiment to get best sound)
        pg.mixer.init(freq, bitsize, channels, buffer)
        # volume value 0.0 to 1.0
        pg.mixer.music.set_volume(volume)
        #clock = pg.time.Clock()
        try:
            pg.mixer.music.load(file)
            self.current_song_file = file
            print("Music file {} loaded!".format(file))
        except pg.error:
            print("File {} not found! ({})".format(file, pg.get_error()))
            return
        pg.mixer.music.play()
        self.end_thread = False
        self.thread = threading.Thread(target=self.check_song_over)
        self.thread.start()
        self.thread.deamon = True
        self.playing_song = True
        self.txt.set(self.song_name)
        print(self.txt.get())
        
    def stop_song_pg(self):
        self.end_thread = True
        pg.mixer.music.stop()
        self.current_song_file = 0
        self.playing_song = False
    
    def play_next_song(self):
        self.stop_song_pg()
        self.play_song_pg()
    
    def inc_song_volume(self):
        pg.mixer.music.set_volume(pg.mixer.music.get_volume() + 0.01)
    
    def check_song_over(self):
        while True:
            if (pg.mixer.music.get_busy() == 0):
                self.play_next_song()
                break
            if (self.end_thread == True):
                break
    
    def dec_song_volume(self):
        pg.mixer.music.set_volume(pg.mixer.music.get_volume() - 0.01)
    
    def pause_song_pg(self):
        pg.mixer.music.pause()
        self.playing_song = False
    
    def unpause_song_pg(self):
        pg.mixer.music.unpause()
        self.playing_song = True
              
if __name__ == "__main__":
    downloaded_songs_directory = 'C:\\Users\\Arthos\\Documents\\Discord Bot\\Songs\\'
    player = Player(downloaded_songs_directory)
    player.play_song_pg() # will not execute anything past this point while the song is still playing or while the while statement is active