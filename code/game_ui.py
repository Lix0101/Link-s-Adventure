import pygame
from game_set import *

class UI:
    def __init__(self):
        # General setup
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.large_font = pygame.font.Font(UI_FONT, 40)  # 更大的字体用于升级提示

        # Bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        self.level_bar_rect = pygame.Rect(10, 58, ENERGY_BAR_WIDTH, BAR_HEIGHT)  # 确保在 settings.py 中定义 LEVEL_BAR_WIDTH

        # Load weapon graphics
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon_surf = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon_surf)

        # Load magic graphics
        self.magic_graphics = []
        for magic in magic_data.values():
            magic_surf = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic_surf)

        # Load boss faceset image 
        self.boss_faceset = pygame.image.load('../src/src_imgs/monsters/TenguBlue/Faceset.png').convert_alpha()

        # Level-up notification setup
        self.level_up_font = self.large_font
        self.level_up_message = ""
        self.level_up_timer = 0
        self.level_up_duration = 2000  # 显示2秒
        self.level_up_alpha = 0  # 透明度用于渐显渐隐
        self.level_up_fade_in = True  # 是否在渐显
        self.level_up_position = (self.display_surface.get_width() // 2, 100)  # 中央顶部

        

    def show_bar(self, current, max_amount, bg_rect, color):
        # Draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_level(self, exp, level, level_bar_rect):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, level_bar_rect)

        ratio = exp / 100  # 假设每级需要100点经验
        ratio = min(max(ratio, 0), 1)  # 确保 ratio 在 0 到 1 之间
        current_width = level_bar_rect.width * ratio
        current_rect = level_bar_rect.copy()
        current_rect.width = current_width

        #  experience bar
        pygame.draw.rect(self.display_surface, LEVEL_COLOR, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, level_bar_rect, 3)

        # Display the current level
        level_text = self.font.render(f"Level: {level}", False, TEXT_COLOR)
        level_text_rect = level_text.get_rect(midleft=(level_bar_rect.right + 10, level_bar_rect.centery))
        self.display_surface.blit(level_text, level_text_rect)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(100, 630, has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)

    def display_boss(self, boss):
        # 获取屏幕尺寸
        screen_width, screen_height = self.display_surface.get_size()
        # 设置边距
        margin_x = 10
        margin_y = 10

        # 计算Boss头像的位置（右上角）
        face_rect = self.boss_faceset.get_rect(topright=(screen_width - margin_x, margin_y))
        self.display_surface.blit(self.boss_faceset, face_rect)

        # 计算Boss血条的位置
        boss_health_bar_width = 250  # 根据需要调整血条宽度
        boss_health_bar_rect = pygame.Rect(screen_width - margin_x - boss_health_bar_width, margin_y + face_rect.height + 10, boss_health_bar_width, BAR_HEIGHT)
        self.show_bar(boss.current_health, boss.max_health, boss_health_bar_rect, HEALTH_COLOR)

        # 显示Boss名称
        boss_name_text = self.font.render("BOSS", False, TEXT_COLOR)
        boss_name_rect = boss_name_text.get_rect(midright=(face_rect.left - 10, face_rect.centery))
        self.display_surface.blit(boss_name_text, boss_name_rect)

    def show_level_up(self, level):
        """显示等级提升的提示"""
        self.level_up_message = f"Leveled Up! Now Level {level}"
        self.level_up_timer = pygame.time.get_ticks()
        self.level_up_alpha = 0  # 重置透明度
        self.level_up_fade_in = True  # 开始渐显

    def display_level_up(self):
        """在屏幕上显示等级提升的消息"""
        if self.level_up_message:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.level_up_timer

            # 控制动画阶段
            if elapsed < self.level_up_duration:
                if self.level_up_fade_in:
                    # 渐显阶段
                    self.level_up_alpha += 5  # 每帧增加透明度
                    if self.level_up_alpha >= 255:
                        self.level_up_alpha = 255
                        self.level_up_fade_in = False
                else:
                    # 渐隐阶段
                    self.level_up_alpha -= 5
                    if self.level_up_alpha <= 0:
                        self.level_up_alpha = 0
                        self.level_up_message = ""
            else:
                self.level_up_message = ""

            if self.level_up_alpha > 0:
                # 创建一个带透明度的表面
                level_up_surface = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
                
                # 渲染文字
                text_surf = self.level_up_font.render(self.level_up_message, True, TEXT_COLOR)
                text_rect = text_surf.get_rect(center=self.level_up_position)

                outline_color = (0, 0, 0)  # 黑色描边
                outline_thickness = 2
                # 渲染描边
                for dx in range(-outline_thickness, outline_thickness + 1):
                    for dy in range(-outline_thickness, outline_thickness + 1):
                        if dx != 0 or dy != 0:
                            outline_surf = self.level_up_font.render(self.level_up_message, True, outline_color)
                            outline_rect = outline_surf.get_rect(center=(self.level_up_position[0] + dx, self.level_up_position[1] + dy))
                            level_up_surface.blit(outline_surf, outline_rect)
                
                # 渲染主文字
                level_up_surface.blit(text_surf, text_rect)

                icon_rect = self.icon_rect.copy()
                icon_rect.midright = (text_rect.left - 10, text_rect.centery)
                level_up_surface.blit(self.level_up_icon, icon_rect)

                # 设置整体透明度
                level_up_surface.set_alpha(self.level_up_alpha)

                # 绘制到主显示表面
                self.display_surface.blit(level_up_surface, (0, 0))

    def display(self, player, boss=None, boss_in_range=False):
        # Player UI
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)
        self.show_level(player.exp, player.level, self.level_bar_rect)

        # 显示玩家等级提升提示
        self.display_level_up()

        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)

        # 若boss在注意范围内，显示boss的血量和头像
        if boss_in_range and boss is not None:
            self.display_boss(boss)