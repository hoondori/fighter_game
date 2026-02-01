"""장애물 클래스 - GameObject를 상속"""

import pygame
from src.game_object import GameObject
from src.constants import OBSTACLE_COLOR


class Obstacle(GameObject):
    """맵에 고정된 장애물 (플레이어와 적 모두 통과 불가)"""
    
    def __init__(self, grid_x, grid_y, width, height):
        """
        장애물 초기화
        
        Args:
            grid_x: 기준점 그리드 x 좌표
            grid_y: 기준점 그리드 y 좌표
            width: 장애물 너비 (그리드 단위)
            height: 장애물 높이 (그리드 단위)
        """
        # 직사각형 모양 생성
        shape = []
        for dy in range(height):
            for dx in range(width):
                shape.append((dx, dy))
        
        super().__init__(grid_x, grid_y, OBSTACLE_COLOR, grid_size=1, shape=shape)
        self.width = width
        self.height = height
