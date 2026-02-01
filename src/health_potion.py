"""체력 회복 아이템 클래스 - GameObject를 상속"""

import pygame
from src.game_object import GameObject
from src.constants import HEALTH_POTION_COLOR, HEALTH_POTION_HEAL


class HealthPotion(GameObject):
    """체력 회복 아이템"""
    
    def __init__(self, grid_x, grid_y):
        """
        체력 회복 아이템 초기화
        
        Args:
            grid_x: 기준점 그리드 x 좌표
            grid_y: 기준점 그리드 y 좌표
        """
        # 십자 모양
        shape = [
            (0, 1),           # 위
            (1, 0), (1, 1), (1, 2),  # 중간 가로
            (2, 1)            # 아래
        ]
        super().__init__(grid_x, grid_y, HEALTH_POTION_COLOR, grid_size=1, shape=shape)
        self.heal_amount = HEALTH_POTION_HEAL
