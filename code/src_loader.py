from csv import reader
from os import walk
import pygame
import os
def import_csv_layout(path):
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map,delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
    surface_list = []
    for _, _, img_files in walk(path):
        img_files = sorted(img_files)  # 按文件名排序
        for image in img_files:
            if image.endswith('.png'):  # 只加载 PNG 文件
                full_path = os.path.join(path, image)
                try:
                    image_surf = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(image_surf)
                except pygame.error as e:
                    print(f"无法加载图像 {full_path}: {e}")
    return surface_list
