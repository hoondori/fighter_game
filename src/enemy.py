"""적 캐릭터 클래스"""

import pygame
import math
from src.constants import ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED, ENEMY_COLOR


class Enemy:
    """플레이어를 추적하는 적 캐릭터"""
    
    def __init__(self, x, y, width=ENEMY_WIDTH, height=ENEMY_HEIGHT, speed=ENEMY_SPEED):
        """
        적 초기화
        
        Args:
            x: 초기 x 좌표
            y: 초기 y 좌표
            width: 적 너비
            height: 적 높이
            speed: 이동 속도
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = ENEMY_COLOR
    
    def move_towards_player(self, player):
        """
        플레이어를 향해 직선으로 이동
        
        Args:
            player: Player 객체
        """
        # 플레이어의 중심점 계산
        player_center_x = player.x + player.width / 2
        player_center_y = player.y + player.height / 2
        
        # 적의 중심점 계산
        enemy_center_x = self.x + self.width / 2
        enemy_center_y = self.y + self.height / 2
        
        # 플레이어까지의 거리 계산
        dx = player_center_x - enemy_center_x
        dy = player_center_y - enemy_center_y
        distance = math.sqrt(dx**2 + dy**2)
        
        # 거리가 0이면 이동하지 않음 (0으로 나누기 방지)
        if distance > 0:
            # 정규화된 방향 벡터
            direction_x = dx / distance
            direction_y = dy / distance
            
            # 속도를 곱해 이동
            self.x += direction_x * self.speed
            self.y += direction_y * self.speed
    
    def draw(self, screen):
        """
        화면에 적을 그림
        
        Args:
            screen: pygame display surface
        """
        pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), self.width, self.height))
    
    def get_rect(self):
        """
        충돌 판정용 rect 반환
        
        Returns:
            pygame.Rect: 적의 충돌 영역
        """
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
