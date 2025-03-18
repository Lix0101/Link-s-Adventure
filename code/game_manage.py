import pygame 
from game_set import *
from game_tile import Tile
from player_entity import Player
from src_loader import *
from random import choice, randint
from player_weapon import Weapon
from game_ui import UI
from enemy_entity import Enemy
from boss_entity import Boss
from game_particles import AnimationPlayer
from player_magic import MagicPlayer

class Level:
    def __init__(self):

        # 整个屏幕信息
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.player = None
        self.boss = None  # 用来保存Boss的引用
        self.create_map()

        # user interface 
        self.ui = UI()

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        # 游戏状态变量
        self.game_over = False
        self.game_victory = False
        

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../src/map/mapset_FloorBlocks.csv'),
            'grass': import_csv_layout('../src/map/mapset_Grass.csv'),
            'object': import_csv_layout('../src/map/mapset_Objects.csv'),
            'entities': import_csv_layout('../src/map/mapset_Entities.csv'),
            'boss': import_csv_layout('../src/map/mapset_Boss.csv')
        }
        graphics = {
            'grass': import_folder('../src/src_imgs/Grass'),
            'objects': import_folder('../src/src_imgs/objects')
        }
        self.player = Player((3000, 2500),
                             [self.visible_sprites],
                             self.obstacle_sprites,
                             self.create_attack,
                             self.destroy_attack,
                             self.create_magic)
        
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        elif style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x,y),
                                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                'grass',
                                random_grass_image)

                        elif style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                        elif style == 'entities':
                            if col == '0':
                                monster_name = 'ghost'
                            elif col == '1':
                                monster_name = 'levdragon'
                            elif col == '2':
                                monster_name = 'cat'
                            Enemy(  
                                    monster_name,
                                    (x,y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    player=self.player)
                            
                        elif style == 'boss':
                            if col == '0':
                                self.boss = Boss(
                                    (x,y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    player=self.player,
                                    spawn_enemy_callback=self.spawn_enemy
                                )

    def spawn_enemy(self, monster_name, pos):
        """
        动态创建敌人，如ghost。
        monster_name: 字符串，怪物名称
        pos: (x,y) 元组，生成怪物的位置坐标
        """
        Enemy(
            monster_name,
            pos,
            [self.visible_sprites, self.attackable_sprites],
            self.obstacle_sprites,
            self.damage_player,
            self.trigger_death_particles,
            player=self.player
        )

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def check_game_over(self):
        if self.player.health <= 0 and not self.game_over:
            self.game_over = True
            self.display_game_over()

    def check_game_victory(self):
        if self.boss:
            if self.boss.current_health <= 0 and not self.game_victory:
                self.game_victory = True
                self.display_game_victory()
        else:
            if not self.game_victory:
                self.game_victory = True
                self.display_game_victory()

    def display_game_over(self):
        # 显示游戏失败的界面
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over!', True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.display_surface.get_width()//2, self.display_surface.get_height()//2))
        self.display_surface.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(3000)  # 暂停3秒后退出游戏
        pygame.quit()
        exit()

    def display_game_victory(self):
        # 显示游戏胜利的界面
        font = pygame.font.Font(None, 74)
        text = font.render('Game Win!', True, (0, 255, 0))
        text_rect = text.get_rect(center=(self.display_surface.get_width()//2, self.display_surface.get_height()//2))
        self.display_surface.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(3000)  # 暂停3秒后退出游戏
        pygame.quit()
        exit()

    def run(self):
        # 更新和绘制游戏
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()

        # 检测boss_in_range
        boss_in_range = False
        if self.boss is not None:
            boss_in_range = self.boss.player_in_range

        self.ui.display(self.player, boss=self.boss, boss_in_range=boss_in_range)

        # 检测游戏胜利和失败
        self.check_game_victory()
        self.check_game_over()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
         
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # floor
        self.floor_surf = pygame.image.load('../src/src_imgs/tilemap/mapset.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player):
        
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)