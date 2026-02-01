"""플레이어 클래스 - GameObject를 상속"""

import pygame
from src.game_object import GameObject
from src.constants import PLAYER_SHAPE, GREEN, PLAYER_SPEED_GRID


class Player(GameObject):
    """게임의 주인공 캐릭터 (그리드 기반, + 모양)"""
    
    def __init__(self, grid_x, grid_y):
        """
        플레이어 초기화
        
        Args:
            grid_x: 기준점 그리드 x 좌표
            grid_y: 기준점 그리드 y 좌표
        """
        super().__init__(grid_x, grid_y, GREEN, grid_size=1, shape=PLAYER_SHAPE)
        self.speed = PLAYER_SPEED_GRID
        
        # 키 입력 쿨다운 (너무 빠른 이동 방지)
        self.move_cooldown = 0
        self.move_delay = 3  # 프레임 수
    
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
        new_x, new_y = self.grid_x, self.grid_y
        
        # 왼쪽 이동
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x = self.grid_x - self.speed
            if self.is_valid_position(new_x, new_y):
                self.grid_x = new_x
                moved = True
        
        # 오른쪽 이동
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x = self.grid_x + self.speed
            if self.is_valid_position(new_x, new_y):
                self.grid_x = new_x
                moved = True
        
        # 위로 이동
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y = self.grid_y - self.speed
            if self.is_valid_position(new_x, new_y):
                self.grid_y = new_y
                moved = True
        
        # 아래로 이동
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y = self.grid_y + self.speed
            if self.is_valid_position(new_x, new_y):
                self.grid_y = new_y
                moved = True
        
        # 이동했으면 쿨다운 설정
        if moved:
            self.move_cooldown = self.move_delay
