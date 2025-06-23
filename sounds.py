import pygame as pg
import random

class Sound:
	def __init__(self):
		pg.mixer.init()
		self.menu_music_path = "Sound/music.mp3"
		self.hit_sound = pg.mixer.Sound("Sound/hit.wav")
		self.explosion_sound = pg.mixer.Sound("Sound/Explosion.wav")
		self.shoot_sounds = [
            pg.mixer.Sound("Sound/shoot1.wav"),
            pg.mixer.Sound("Sound/shoot2.wav")
        ]
		self.select_sound = pg.mixer.Sound("Sound/select.wav") 

		for x in self.shoot_sounds:
			x.set_volume(0.1)
		
	def play_menu_music(self):
		if not pg.mixer.music.get_busy():
			pg.mixer.music.load(self.menu_music_path)
			pg.mixer.music.play(-1)

	def stop_music(self):
		pg.mixer.music.stop()

	def play_shoot(self):
		random.choice(self.shoot_sounds).play()

	def play_explosion(self):
		self.explosion_sound.play()

	def play_hit(self):
		self.hit_sound.play()
	
	def play_select(self):
		self.select_sound.play()