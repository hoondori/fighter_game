"""플레이어 클래스"""

import pygame
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    GRID_WIDTH, GRID_HEIGHT, GRID_COLS, GRID_ROWS,
    PLAYER_GRID_SIZE, PLAYER_SPEED_GRID, PLAYER_COLOR
)


class Player:
    """게임의 주인공 캐릭터 (그리드 기반)"""
    
    def __init__(self, grid_x, grid_y, grid_size=PLAYER_GRID_SIZE, speed=PLAYER_SPEED_GRID):
        """
        플레이어 초기화
        
        Args:
            grid_x: 초기 그리드 x 좌표
            grid_y: 초기 그리드 y 좌표
            grid_size: 플레이어 그리드 크기 (셀 개수)
            speed: 이동 속도 (그리드 셀 단위)
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.grid_size = grid_size
        self.speed = speed
        self.color = PLAYER_COLOR
        
        # 키 입력 쿨다운 (너무 빠른 이동 방지)
        self.move_cooldown = 0
        self.move_delay = 3  # 프레임 수 (더 빠른 반응)
    
    def move(self, keys):
        """
        키 입력에 따라 플레이어 이동 (그리드 단위)
        화면 밖으로 나가지 못하도록 제한
        
        Args:
            keys: pygame.key.get_pressed()로 얻은 키 상태
        """
        # 쿨다운 감소
        if self.move_cooldown > 0:
            self.move_cooldown -= 1
            return
        
        moved = False
        
        # 왼쪽 이동
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.grid_x > 0:
                self.grid_x -= self.speed
                moved = True
        
        # 오른쪽 이동
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.grid_x + self.grid_size < GRID_COLS:
                self.grid_x += self.speed
                moved = True
        
        # 위로 이동
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.grid_y > 0:
                self.grid_y -= self.speed
                moved = True
        
        # 아래로 이동
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.grid_y + self.grid_size < GRID_ROWS:
                self.grid_y += self.speed
                moved = True
        
        # 이동했으면 쿨다운 설정
        if moved:
            self.move_cooldown = self.move_delay
    
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
        화면에 플레이어를 그림
        
        Args:
            screen: pygame display surface
        """
        pixel_x, pixel_y, pixel_width, pixel_height = self.get_pixel_pos()
        pygame.draw.rect(screen, self.color, (pixel_x, pixel_y, pixel_width, pixel_height))
    
    def get_rect(self):
        """
        충돌 판정용 rect 반환
        
        Returns:
            pygame.Rect: 플레이어의 충돌 영역
        """
        pixel_x, pixel_y, pixel_width, pixel_height = self.get_pixel_pos()
        return pygame.Rect(pixel_x, pixel_y, pixel_width, pixel_height)
