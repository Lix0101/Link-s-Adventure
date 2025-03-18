#to do 
# 1. bossUI修改、2.音效添加 3.视频录制
import pygame
from game_set import *
from game_entity import Entity
from src_loader import import_folder
from enemy_entity import Enemy

class Boss(Enemy):
    def __init__(self, pos, groups, obstacle_sprites, damage_player, trigger_death_particles, player, spawn_enemy_callback=None,):
        super().__init__('TenguBlue', pos, groups, obstacle_sprites, damage_player, trigger_death_particles, player,)

        # Boss属性
        self.max_health = 1000
        self.current_health = self.max_health
        self.exp = 1000
        self.speed = 4
        self.attack_damage = 20
        self.resistance = 3
        self.attack_radius = 150
        self.notice_radius = 400


        self.attack_type = 'thunder'

        self.transformed = False
        self.trans_ready = False
        self.pause_animation = True
        self.attack_animation_done = False
        self.player_in_range = False

        # 魔法相关
        self.magic_done = False
        self.magic_invulnerable = False  # 魔法释放中无敌但不闪烁

        self.spawn_enemy_callback = spawn_enemy_callback

        # 载入资源
        self.import_boss_graphics()

        self.status = 'trans'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]

        self.state_animation_speeds = {
            'idle': 0.07,
            'walk': 0.07,
            'attack': 0.07,
            'hit': 0.1,
            'trans': 0.1,
            'magic': 0.1
        }

    def import_boss_graphics(self):
        self.animations = {
            'idle': [],
            'walk': [],
            'attack': [],
            'hit': [],
            'trans': [],
            'magic': []
        }
        main_path = '../src/src_imgs/monsters/TenguBlue/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        self.player_in_range = (distance <= self.notice_radius)

        if not self.transformed:
            if self.player_in_range and not self.trans_ready:
                self.trans_ready = True
                self.pause_animation = False
            if self.status != 'trans':
                self.status = 'trans'
            return

        # 当血量低于30%且尚未释放魔法时进入magic状态
        if self.status != 'magic' and self.current_health < 0.3 * self.max_health and not self.magic_done:
            self.status = 'magic'
            self.magic_invulnerable = True
            self.frame_index = 0
            return

        # 如果正在释放魔法，不会进入hit状态，即使vulnerable为False
        if not self.vulnerable and not self.magic_invulnerable:
            if self.status != 'hit':
                self.frame_index = 0
            self.status = 'hit'
            return

        # 未处于magic时才执行普通状态逻辑
        if self.status != 'magic':
            if distance <= self.attack_radius and self.can_attack:
                if self.status != 'attack':
                    self.frame_index = 0
                    self.attack_animation_done = False
                self.status = 'attack'
            elif self.player_in_range:
                self.status = 'walk'
            else:
                self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            if not self.attack_animation_done:
                if self.frame_index == 0 and self.can_attack:
                    self.attack_time = pygame.time.get_ticks()
                    self.damage_player(self.attack_damage, self.attack_type)
            else:
                self.status = 'idle'
                self.can_attack = False

        elif self.status == 'walk':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

        if self.status == 'trans' and not self.transformed:
            self.direction = pygame.math.Vector2()

        if self.status == 'magic':
            # 魔法释放时不移动
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        if self.pause_animation and self.status == 'trans':
            self.image = animation[int(self.frame_index)]
            self.rect = self.image.get_rect(center=self.hitbox.center)
            return

        current_speed = self.state_animation_speeds.get(self.status, 0.1)
        self.frame_index += current_speed
        if self.frame_index >= len(animation):
            if self.status in ['walk', 'idle']:
                self.frame_index = 0
            else:
                self.frame_index = len(animation) - 1

                if self.status == 'trans' and not self.transformed:
                    self.transformed = True
                    self.status = 'idle'

                if self.status == 'attack':
                    self.attack_animation_done = True

                if self.status == 'hit' and self.vulnerable:
                    self.status = 'idle'

                if self.status == 'magic':
                    # Magic动画结束
                    if not self.magic_done:
                        self.summon_minions()
                        self.magic_done = True
                    self.status = 'idle'
                    self.magic_invulnerable = False
                    self.vulnerable = True

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # 如果在magic_invulnerable状态下，不闪烁，直接set_alpha(255)
        if self.magic_invulnerable:
            self.image.set_alpha(255)
        else:
            # 如果不是magic_invulnerable但无敌则闪烁
            if not self.vulnerable:
                alpha = self.wave_value()
                self.image.set_alpha(alpha)
            else:
                self.image.set_alpha(255)

    def get_damage(self, player, attack_type):
        # 魔法释放中无敌，不可受伤
        if self.vulnerable and not self.magic_invulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            damage = player.get_full_weapon_damage() if attack_type == 'weapon' else player.get_full_magic_damage()
            self.current_health -= damage
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
            if self.status != 'hit':
                self.frame_index = 0
            self.status = 'hit'
        

    def check_death(self):
        if self.current_health <= 0:
            self.kill()

    def summon_minions(self):
        if self.spawn_enemy_callback:
            offsets = [(100,0),(-100,0),(0,100),(0,-100)]
            for ox, oy in offsets:
                summon_pos = (self.rect.centerx + ox, self.rect.centery + oy)
                self.spawn_enemy_callback(
                    monster_name='ghost',
                    pos=summon_pos
                )

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)