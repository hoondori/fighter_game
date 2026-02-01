"""플레이어 클래스 - GameObject를 상속"""

import pygame
import math
from src.game_object import GameObject
from src.constants import (
    PLAYER_SHAPE, GREEN, PLAYER_SPEED_GRID, 
    PLAYER_MAX_HP, SCREEN_WIDTH, RED, WHITE
)


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
        
        # float 좌표 지원 (부드러운 이동)
        self.grid_x = float(grid_x)
        self.grid_y = float(grid_y)
        
        # HP 시스템
        self.max_hp = PLAYER_MAX_HP
        self.hp = self.max_hp
    
    def move(self, keys, obstacles=None):
        """
        키 입력에 따라 플레이어 이동 (대각선 이동 가능, 속도 정규화)
        화면 밖으로 나가지 못하도록 제한
        
        Args:
            keys: pygame.key.get_pressed()로 얻은 키 상태
            obstacles: 장애물 리스트 (충돌 체크용)
        """
        # 이동 방향 계산
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1
        
        # 이동하지 않으면 return
        if dx == 0 and dy == 0:
            return
        
        # 대각선 이동 시 속도 정규화 (sqrt(2)로 나눔)
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707
        
        # 새 위치 계산
        new_x = self.grid_x + dx * self.speed
        new_y = self.grid_y + dy * self.speed
        
        # 이동 가능한지 체크 (경계 + 장애물)
        old_x, old_y = self.grid_x, self.grid_y
        self.grid_x = new_x
        self.grid_y = new_y
        
        move_valid = self.is_valid_position(new_x, new_y)
        
        # 장애물 충돌 체크
        if move_valid and obstacles:
            for obstacle in obstacles:
                if self.collides_with(obstacle):
                    move_valid = False
                    break
        
        # 이동이 불가능하면 이전 위치로 복원
        if not move_valid:
            self.grid_x = old_x
            self.grid_y = old_y
    
    def take_damage(self, damage):
        """
        데미지를 받음
        
        Args:
            damage: 받을 데미지 양
        
        Returns:
            bool: 아직 살아있으면 True, 죽었으면 False
        """
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return self.hp > 0
    
    def heal(self, amount):
        """
        체력 회복
        
        Args:
            amount: 회복할 체력 양
        """
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
    
    def draw_hp_bar(self, screen):
        """
        체력바 그리기 (화면 상단)
        
        Args:
            screen: pygame screen 객체
        """
        # 체력바 위치 및 크기
        bar_x = 10
        bar_y = 40
        bar_width = 200
        bar_height = 20
        
        # 배경 (빨간색 - 잃은 체력)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # 현재 체력 (녹색)
        hp_ratio = self.hp / self.max_hp
        current_width = int(bar_width * hp_ratio)
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, current_width, bar_height))
        
        # 테두리
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # HP 텍스트
        font = pygame.font.Font(None, 24)
        hp_text = font.render(f"HP: {int(self.hp)}/{self.max_hp}", True, WHITE)
        screen.blit(hp_text, (bar_x + bar_width + 10, bar_y))
    
    def draw_with_hp_bar(self, screen):
        """
        플레이어를 그리고 머리 위에 체력바 그리기
        
        Args:
            screen: pygame screen 객체
        """
        # 기본 그리기
        self.draw(screen)
        # 머리 위 체력바
        self.draw_hp_bar_above(screen, self.hp, self.max_hp)
