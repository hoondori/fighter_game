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
        # H 모양 (Health를 나타냄, 플레이어/적과 확실히 구별)
        shape = [
            (0, 0), (0, 1), (0, 2),  # 왼쪽 세로 줄
                    (1, 1),           # 중간 가로
            (2, 0), (2, 1), (2, 2)   # 오른쪽 세로 줄
        ]
        super().__init__(grid_x, grid_y, HEALTH_POTION_COLOR, grid_size=1, shape=shape)
        self.heal_amount = HEALTH_POTION_HEAL
