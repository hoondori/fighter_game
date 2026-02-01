"""적 캐릭터 클래스"""

import pygame
import math
from src.constants import (
    GRID_WIDTH, GRID_HEIGHT, GRID_COLS, GRID_ROWS,
    ENEMY_GRID_SIZE, ENEMY_SPEED_GRID, ENEMY_COLOR
)


class Enemy:
    """플레이어를 추적하는 적 캐릭터 (그리드 기반, 부드러운 이동)"""
    
    def __init__(self, grid_x, grid_y, grid_size=ENEMY_GRID_SIZE, speed=ENEMY_SPEED_GRID):
        """
        적 초기화
        
        Args:
            grid_x: 초기 그리드 x 좌표 (float 가능)
            grid_y: 초기 그리드 y 좌표 (float 가능)
            grid_size: 적 그리드 크기
            speed: 이동 속도 (그리드 셀 단위, float 가능)
        """
        self.grid_x = float(grid_x)
        self.grid_y = float(grid_y)
        self.grid_size = grid_size
        self.speed = speed
        self.color = ENEMY_COLOR
    
    def move_towards_player(self, player):
        """
        플레이어를 향해 직선으로 이동 (그리드 좌표에서)
        
        Args:
            player: Player 객체
        """
        # 플레이어의 그리드 중심점 계산
        player_center_x = player.grid_x + player.grid_size / 2
        player_center_y = player.grid_y + player.grid_size / 2
        
        # 적의 그리드 중심점 계산
        enemy_center_x = self.grid_x + self.grid_size / 2
        enemy_center_y = self.grid_y + self.grid_size / 2
        
        # 플레이어까지의 거리 계산 (그리드 단위)
        dx = player_center_x - enemy_center_x
        dy = player_center_y - enemy_center_y
        distance = math.sqrt(dx**2 + dy**2)
        
        # 거리가 0이면 이동하지 않음 (0으로 나누기 방지)
        if distance > 0:
            # 정규화된 방향 벡터
            direction_x = dx / distance
            direction_y = dy / distance
            
            # 속도를 곱해 이동 (그리드 단위)
            self.grid_x += direction_x * self.speed
            self.grid_y += direction_y * self.speed
            
            # 화면 경계 제한
            self.grid_x = max(0, min(self.grid_x, GRID_COLS - self.grid_size))
            self.grid_y = max(0, min(self.grid_y, GRID_ROWS - self.grid_size))
    
    def get_pixel_pos(self):
        """
        그리드 좌표를 픽셀 좌표로 변환
        
        Returns:
            tuple: (pixel_x, pixel_y, pixel_width, pixel_height)
        """
        pixel_x = self.grid_x * GRID_WIDTH
        pixel_y = self.grid_y * GRID_HEIGHT
        pixel_width = self.grid_size * GRID_WIDTH
        pixel_height = self.grid_size * GRID_HEIGHT
        return (pixel_x, pixel_y, pixel_width, pixel_height)
    
    def draw(self, screen):
        """
        화면에 적을 그림
        
        Args:
            screen: pygame display surface
        """
        pixel_x, pixel_y, pixel_width, pixel_height = self.get_pixel_pos()
        pygame.draw.rect(screen, self.color, (int(pixel_x), int(pixel_y), int(pixel_width), int(pixel_height)))
    
    def get_rect(self):
        """
        충돌 판정용 rect 반환
        
        Returns:
            pygame.Rect: 적의 충돌 영역
        """
        pixel_x, pixel_y, pixel_width, pixel_height = self.get_pixel_pos()
        return pygame.Rect(int(pixel_x), int(pixel_y), int(pixel_width), int(pixel_height))
