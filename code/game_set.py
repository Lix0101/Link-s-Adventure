# game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../src/src_imgs/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
LEVEL_COLOR = 'yellow'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# weapons 
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic':'../src/src_imgs/weapons/sword/full.png'},
	'lance': {'cooldown': 400, 'damage': 30,'graphic':'../src/src_imgs/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'../src/src_imgs/weapons/axe/full.png'},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic':'../src/src_imgs/weapons/rapier/full.png'},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic':'../src/src_imgs/weapons/sai/full.png'}}

# magic
magic_data = {
	'flame': {'strength': 5,'cost': 10,'graphic':'../src/src_imgs/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'../src/src_imgs/particles/heal/heal.png'}}

# enemy
monster_data = {
	'cat': {'health': 70,'exp':20,'damage':4,'attack_type': 'claw', 'attack_sound':'../src/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 360},
	'levdragon': {'health': 100,'exp':15,'damage':8,'attack_type': 'slash', 'attack_sound':'../src/audio/attack/claw.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'ghost': {'health': 120,'exp':15,'damage':6,'attack_type': 'claw', 'attack_sound':'../src/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 400},
	'TenguBlue':{
		'health' : 1000,
        'exp' :1000,
        'damage':8,
        'speed' : 4,
        'attack_damage' : 50,
        'resistance' :3,
        'attack_radius' : 80,
        'notice_radius' : 2500,
        'attack_type' : 'thunder',
        'attack_sound':'../src/audio/attack/slash.wav'
    },
}

HIT_OFFSET={
    'player': -20,
    'object': -40,
    'grass':-10,
    'invisible':0,
    'boss':-100,
}