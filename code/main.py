import pygame, sys
from game_set import *
from game_manage import Level

class Game:
    def __init__(self):
        # 初始化Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Link Adventure')
        self.clock = pygame.time.Clock()
        
        # 加载背景音乐
        try:
            main_sound = pygame.mixer.Sound('../src/audio/background.wav')
            main_sound.set_volume(0.5)
            main_sound.play(loops=-1)
        except pygame.error as e:
            print(f"无法加载背景音乐: {e}")
        
        # 初始化游戏状态为开始界面
        self.game_state = 'start'  # 'start' 或 'play'
        
        # 加载开始界面背景图像
        try:
            self.start_bg = pygame.image.load('../src/src_imgs/tilemap/image.png').convert_alpha()
            # 缩放背景图像以适应屏幕
            self.start_bg = pygame.transform.scale(self.start_bg, (WIDTH, HEIGTH))
        except pygame.error as e:
            print(f"无法加载开始界面背景图像: {e}")
            self.start_bg = None 
        
        # 设置字体
        try:
            self.font_title = pygame.font.Font(UI_FONT, 64)  # 游戏标题字体
            self.font_info = pygame.font.Font(UI_FONT, 40)   # 提示信息字体
        except IOError:
            print("无法加载指定字体，使用默认字体。")
            self.font_title = pygame.font.SysFont(None, 64)
            self.font_info = pygame.font.SysFont(None, 40)
        
        # 初始化游戏关卡
        self.level = Level()

    def draw_start_screen(self):
        if self.start_bg:
            # 绘制背景图像
            self.screen.blit(self.start_bg, (0, 0))
        else:
            # 如果背景图像未加载，填充背景颜色
            self.screen.fill(WATER_COLOR)  # 从settings.py中获取BG_COLOR
        
        # 绘制游戏标题
        title_surf = self.font_title.render('Link Adventure', True, (0, 0, 0))
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 100))
        self.screen.blit(title_surf, title_rect)
        
        # 绘制提示信息
        info_surf = self.font_info.render('Press SPACE to Start', True, (0, 0, 0))
        info_rect = info_surf.get_rect(center=(WIDTH // 2, HEIGTH // 2 + 50))
        self.screen.blit(info_surf, info_rect)
        

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.game_state == 'start':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_state = 'play'

            if self.game_state == 'start':
                self.draw_start_screen()
            elif self.game_state == 'play':
                self.screen.fill(WATER_COLOR)  # 从settings.py中获取WATER_COLOR
                self.level.run()
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()