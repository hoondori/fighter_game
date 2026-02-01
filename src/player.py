"""플레이어 클래스"""

import pygame
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_COLOR
)


class Player:
    """게임의 주인공 캐릭터"""
    
    def __init__(self, x, y, width=PLAYER_WIDTH, height=PLAYER_HEIGHT, speed=PLAYER_SPEED):
        """
        플레이어 초기화
        
        Args:
            x: 초기 x 좌표
            y: 초기 y 좌표
            width: 플레이어 너비
            height: 플레이어 높이
            speed: 이동 속도
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = PLAYER_COLOR
    
    def move(self, keys):
        """
        키 입력에 따라 플레이어 이동
        화면 밖으로 나가지 못하도록 제한
        
        Args:
            keys: pygame.key.get_pressed()로 얻은 키 상태
        """
        # 왼쪽 이동
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
        
        # 오른쪽 이동
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            if self.x + self.width > SCREEN_WIDTH:
                self.x = SCREEN_WIDTH - self.width
        
        # 위로 이동
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
            if self.y < 0:
                self.y = 0
        
        # 아래로 이동
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            if self.y + self.height > SCREEN_HEIGHT:
                self.y = SCREEN_HEIGHT - self.height
    
    def draw(self, screen):
        """
        화면에 플레이어를 그림
        
        Args:
            screen: pygame display surface
        """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        """
        충돌 판정용 rect 반환
        
        Returns:
            pygame.Rect: 플레이어의 충돌 영역
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)
