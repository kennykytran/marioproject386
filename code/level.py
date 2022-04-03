import pygame, sys
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Coin, Palm, Mushroom, Flower
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from score import Score, Coin_count, Live_count
from settings import *
from sound import Sound

class Level:
	def __init__(self,level_data,surface):
		# general setup
		self.display_surface = surface
		self.world_shift = 0
		self.current_x = None
		self.sound = Sound()

		# player 
		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout)

		# score text
		self.score_text = pygame.font.SysFont(None, 48).render('SCORE', True, (60,60,60))
		self.score_text_rect = surface.get_rect()
		self.score_text.set_alpha(127)

		# score
		self.score = Score(self.display_surface)

		# coin count text
		self.coin_count_text = pygame.font.SysFont(None, 48).render('COIN COUNT', True, (60, 60, 60))
		self.coin_count_text_rect = surface.get_rect()
		self.coin_count_text.set_alpha(127)

		# coin count
		self.coin_count = Coin_count(self.display_surface)

		# live count
		self.live_count_text = pygame.font.SysFont(None, 48).render('LIVES', True, (60, 60, 60))
		self.live_count_text_rect = surface.get_rect()
		self.live_count_text.set_alpha(127)

		# live
		self.live_count = Live_count(self.display_surface)

		# dust
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False

		# fireball
		self.fireball_sprite = pygame.sprite.GroupSingle()

		# terrain setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

		#  goal
		goal_layout = import_csv_layout(level_data['goal'])
		self.goal_sprites = self.create_tile_group(goal_layout, 'goal')

		# death barrier
		death_barrier_layout = import_csv_layout(level_data['death_barrier'])
		self.death_barrier_sprites = self.create_tile_group(death_barrier_layout, 'death_barrier')

		# grass setup
		grass_layout = import_csv_layout(level_data['grass'])
		self.grass_sprites = self.create_tile_group(grass_layout,'grass')

		# crates 
		crate_layout = import_csv_layout(level_data['crates'])
		self.crate_sprites = self.create_tile_group(crate_layout,'crates')

		# coins 
		coin_layout = import_csv_layout(level_data['coins'])
		self.coin_sprites = self.create_tile_group(coin_layout,'coins')

		# foreground palms 
		# fg_palm_layout = import_csv_layout(level_data['fg palms'])
		# self.fg_palm_sprites = self.create_tile_group(fg_palm_layout,'fg palms')

		# mushroom
		mushroom_layout = import_csv_layout(level_data['mushroom'])
		self.mushroom_sprites = self.create_tile_group(mushroom_layout, 'mushroom')

		# flower
		flower_layout = import_csv_layout(level_data['flower'])
		self.flower_sprites = self.create_tile_group(flower_layout, 'flower')

		# background palms 
		bg_palm_layout = import_csv_layout(level_data['bg palms'])
		self.bg_palm_sprites = self.create_tile_group(bg_palm_layout,'bg palms')

		# enemy 
		enemy_layout = import_csv_layout(level_data['enemies'])
		self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

		# constraint 
		constraint_layout = import_csv_layout(level_data['constraints'])
		self.constraint_sprites = self.create_tile_group(constraint_layout,'constraint')

		# decoration 
		self.sky = Sky(8)
		level_width = len(terrain_layout[0]) * tile_size
		self.water = Water(screen_height - 20,level_width)
		self.clouds = Clouds(400,level_width,30)

	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)
						
					if type == 'grass':
						grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png')
						tile_surface = grass_tile_list[int(val)]
						sprite = StaticTile(tile_size,x,y,tile_surface)
					
					if type == 'crates':
						sprite = Crate(tile_size,x,y)

					if type == 'coins':
						if val == '0': sprite = Coin(tile_size,x,y,'../graphics/coins/gold')
						if val == '1': sprite = Coin(tile_size,x,y,'../graphics/coins/silver')

					if type == 'fg palms':
						if val == '0': sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_small',38)
						if val == '1': sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_large',64)

					if type == 'bg palms':
						sprite = Palm(tile_size,x,y,'../graphics/terrain/palm_bg',64)

					if type == 'enemies':
						sprite = Enemy(tile_size,x,y)

					if type == 'constraint':
						sprite = Tile(tile_size,x,y)

					if type == 'death_barrier':
						sprite = Tile(tile_size,x,y)

					if type == 'goal':
						sprite = Tile(tile_size,x,y)

					if type == 'mushroom':
						sprite = Mushroom(tile_size,x,y)

					if type == 'flower':
						sprite = Flower(tile_size,x,y)


					sprite_group.add(sprite)
		
		return sprite_group

	def player_setup(self,layout):
		for row_index, row in enumerate(layout):
			for col_index,val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '0':
					sprite = Player((x,y),self.display_surface,self.create_jump_particles)
					self.player.add(sprite)
				if val == '1':
					hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
					sprite = StaticTile(tile_size,x,y,hat_surface)
					self.goal.add(sprite)

	def enemy_collision_reverse(self):
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
				enemy.reverse()

	def create_jump_particles(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_particle_sprite)

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		# collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
		collidable_sprites = self.terrain_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()
		# collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
		collidable_sprites = self.terrain_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.dust_sprite.add(fall_dust_particle)

	def check_mushroom_collision(self):
		player = self.player.sprite
		mushroom_collisions = pygame.sprite.spritecollide(self.player.sprite, self.mushroom_sprites, False)

		if mushroom_collisions:
			player.change_to_super()
			for mushroom in mushroom_collisions:
				mushroom.kill()

	def check_flower_collision(self):
		player = self.player.sprite
		flower_collisions = pygame.sprite.spritecollide(self.player.sprite, self.flower_sprites, False)

		if flower_collisions:
			player.change_to_fire()
			for flower in flower_collisions:
				flower.kill()

	def check_goal_collision(self):
		player = self.player.sprite
		goal_collisions = pygame.sprite.spritecollide(self.player.sprite, self.goal_sprites, False)
		if goal_collisions:
			print("YOU WON!")
			pygame.quit()
			sys.exit()

	def check_death_barrier(self):
		player = self.player.sprite
		death_barrier_collision = pygame.sprite.spritecollide(player, self.death_barrier_sprites, False)
		now = pygame.time.get_ticks()
		if death_barrier_collision:
			player.direction.y = -30
			if now - player.invulnerable_timer > 1000:
				self.live_count.add_score(-1)
				player.change_invul_timer(now)
				if not player.states == 'normal':
					if player.states == 'fire':
						player.change_to_super()
					elif player.states == 'super':
						player.change_to_normal()
				else:
					player.hit()

	def check_goomba_collision(self):
		player = self.player.sprite
		goomba_collisions = pygame.sprite.spritecollide(player, self.enemy_sprites, False)
		now = pygame.time.get_ticks()

		if goomba_collisions:
			for goomba in goomba_collisions:
				goomba_center = goomba.rect.centery
				goomba_top = goomba.rect.top
				player_bottom = self.player.sprite.rect.bottom
				if goomba_top < player_bottom < goomba_center and self.player.sprite.direction.y >= 0:
					self.score.add_score(100)
					self.sound.play_stomp()
					goomba.kill()
					player.direction.y = -16
				elif now - player.invulnerable_timer > 1000:
					self.live_count.add_score(-1)
					player.change_invul_timer(now)
					if not player.states == 'normal':
						if player.states == 'fire':
							player.change_to_super()
						elif player.states == 'super':
							player.change_to_normal()
					else:
						player.hit()

		if not player.lives:
			self.sound.play_game_over()
			pygame.quit()
			sys.exit()

	# def check_goal_collisions(self):
	# 	goal_collisions = pygame.sprite.spritecollide(self.player.sprite, self.goal.sprite, False)
	#
	# 	if goal_collisions:
	# 		print("YOU WON!")
	# 		pygame.quit()
	# 		sys.exit()

	def check_coin_collision(self):
		player = self.player.sprite
		coin_collisions = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites, False)

		if coin_collisions:
			for coin in coin_collisions:
				self.score.add_score(10)
				self.coin_count.add_score(1)
				self.sound.play_coin()
				coin.kill()

	def run(self):
		# run the entire game / level 
		
		# sky 
		self.sky.draw(self.display_surface)
		self.clouds.draw(self.display_surface,self.world_shift)

		# score
		self.score.draw()

		# score text
		self.display_surface.blit(self.score_text, (self.score_text_rect.centerx - 50, 32))

		# coin count
		self.coin_count.draw()

		# coin count text
		self.display_surface.blit(self.coin_count_text, (screen_width - 300, 32))

		# live count
		self.live_count.draw()

		# live count text
		self.display_surface.blit(self.live_count_text, (160, 32))

		# background palms
		self.bg_palm_sprites.update(self.world_shift)
		self.bg_palm_sprites.draw(self.display_surface)

		# terrain 
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.display_surface)
		
		# enemy 
		self.enemy_sprites.update(self.world_shift)
		self.constraint_sprites.update(self.world_shift)
		self.enemy_collision_reverse()
		self.enemy_sprites.draw(self.display_surface)

		# crate 
		self.crate_sprites.update(self.world_shift)
		self.crate_sprites.draw(self.display_surface)

		# grass
		self.grass_sprites.update(self.world_shift)
		self.grass_sprites.draw(self.display_surface)

		# coins 
		self.coin_sprites.update(self.world_shift)
		self.coin_sprites.draw(self.display_surface)

		# mushroom
		self.mushroom_sprites.update(self.world_shift)
		self.mushroom_sprites.draw(self.display_surface)

		# flower
		self.flower_sprites.update(self.world_shift)
		self.flower_sprites.draw(self.display_surface)

		# goal
		self.goal_sprites.update(self.world_shift)

		# death_barrier
		self.death_barrier_sprites.update(self.world_shift)

		# foreground palms
		# self.fg_palm_sprites.update(self.world_shift)
		# self.fg_palm_sprites.draw(self.display_surface)

		# dust particles 
		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.display_surface)

		# player sprites
		self.player.update()
		self.horizontal_movement_collision()
		
		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.create_landing_dust()

		self.check_mushroom_collision()
		self.check_flower_collision()
		self.check_coin_collision()
		self.check_goal_collision()
		self.check_death_barrier()

		self.scroll_x()
		self.player.draw(self.display_surface)
		self.goal.update(self.world_shift)
		self.goal.draw(self.display_surface)

		self.check_goomba_collision()
		# water 
		# self.water.draw(self.display_surface,self.world_shift)
