# RPG Game - Link's Adventure


## 1. 游戏简介

这款游戏是基于经典角色扮演游戏（RPG）风格的改进版本，玩家将通过控制主角林克（Link），在一个被分为三个不同地区的广阔地图上进行探索和冒险。玩家需要击败怪物、积累经验、升级角色，最终挑战强大的BOSS。这个项目是基于https://github.com/clear-code-projects/Zelda 进一步的扩展，重新更新了原有的地图以及添加了一个小的boss

### 1.2 开发环境

- **系统**：MacOS/Windows
- **软件环境**：
  - Vscode
  - Pygame 2.6.1
  - Python 3.10

### 1.3 运行环境以及运行说明

1. 在编译器中配置好Python和Pygame后，即可正常运行。
2. 打开任意一个Python编译器，在终端中切换到`code`目录，并输入以下指令运行程序：
   ```bash
   python main.py

## 2. 游戏玩法

### 2.1 游戏规则
	（1）移动控制：使用键盘上的上下左右箭头键控制主角林克在地图上移动，探索不同区域。

	（2）地图区域：地图分为三个主要区域：沙漠、雪地和草原。每个区域都有独特的环境特点和不同类型的怪物。

	（3）怪物生成：不同区域会生成具有独特属性的怪物，玩家需要根据怪物类型选择合适的武器和魔法进行战斗。
	（4）战斗系统
	•	物理攻击：按下空格键进行物理攻击，伤害取决于当前装备的武器类型。
	•	魔法攻击：按下‘E’键进行魔法攻击，所使用的魔法类型取决于当前选择的魔法。
	（5）武器系统
	•	切换武器：按下‘Q’键在五种不同类型的武器之间切换，每种武器都有不同的攻击方式和效果。
	•	武器特点：每种武器对特定类型的怪物有不同的优势和劣势，玩家需要根据怪物类型选择合适的武器来提高战斗效率。
	（6）魔法系统
	•	切换魔法：按下‘LCTRL’键在火焰魔法和治愈魔法之间切换。
	•	火焰魔法：造成远程伤害，适合攻击群体敌人。
	•	治愈魔法：恢复玩家的生命值，适合在紧急情况下使用。
	（7）经验与升级：击败怪物可获得经验值（XP），累积经验值可提升角色等级，增强角色能力和属性。每次升级后，玩家的血量和蓝量会重置，同时角色的最大生命值、行走速度、攻击力等属性也会提高。
	（8）最终目标：进入雪地区域，与最终BOSS进行决战。成功击败BOSS即为游戏胜利。
	（9）失败条件：玩家血量降至零时，游戏结束，玩家失败。
## 3. 游戏内容介绍
### 3.1地图资源
<img width="640" alt="image" src="https://github.com/user-attachments/assets/0d7b380c-03bc-4f4f-ac41-05a3ea82e637" />
<img width="640" alt="image" src="https://github.com/user-attachments/assets/f19c52c6-80a0-44f9-8c98-4b92f090d7d2" />

### 3.2游戏内容
<img width="640" alt="image" src="https://github.com/user-attachments/assets/a995461f-630c-43f6-8011-9d3f76e27b67" />
<img width="640" alt="image" src="https://github.com/user-attachments/assets/47d2e144-2b3e-4f1e-bb38-56db0f011e5b" />
<img width="401" alt="image" src="https://github.com/user-attachments/assets/8faee760-aecf-4d14-84b5-da5ceef0bed4" />
<img width="395" alt="image" src="https://github.com/user-attachments/assets/ee47cad7-27c6-4415-906a-0b4961ba9150" />

