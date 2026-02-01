"""적 캐릭터 클래스 - GameObject를 상속"""

import pygame
import math
from src.game_object import GameObject
from src.constants import ENEMY_SPEED_GRID


class Enemy(GameObject):
    """플레이어를 추적하는 적 캐릭터 (그리드 기반, 부드러운 이동, 다양한 모양)"""
    
    def __init__(self, grid_x, grid_y, color, shape=None):
        """
        적 초기화
        
        Args:
            grid_x: 기준점 그리드 x 좌표 (float 가능)
            grid_y: 기준점 그리드 y 좌표 (float 가능)
            color: 적의 색상
            shape: 상대 좌표 리스트 [(0,0), (1,0), ...] 또는 None (1x1 정사각형)
        """
        if shape is None:
            shape = [(0, 0)]  # 기본: 1x1 정사각형
        
        super().__init__(grid_x, grid_y, color, grid_size=1, shape=shape)
        self.speed = ENEMY_SPEED_GRID
        
        # float 좌표 지원 (부드러운 이동)
        self.grid_x = float(grid_x)
        self.grid_y = float(grid_y)
    
    def get_grid_positions(self):
        """
        현재 차지하고 있는 모든 그리드 좌표 반환 (정수로 변환)
        
        Returns:
            list: [(x1, y1), (x2, y2), ...] 절대 좌표 리스트
        """
        return [(int(self.grid_x + dx), int(self.grid_y + dy)) for dx, dy in self.shape]
    
    def move_towards_player(self, player, other_enemies=None):
        """
        플레이어를 향해 직선으로 이동 (다른 적들과 겹치지 않게)
        
        Args:
            player: Player 객체
            other_enemies: 다른 적들의 리스트 (충돌 체크용)
        """
        # 플레이어의 중심점 계산
        player_center_x, player_center_y = player.get_center()
        
        # 적의 중심점
        enemy_center_x, enemy_center_y = self.get_center()
        
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
            new_x = self.grid_x + direction_x * self.speed
            new_y = self.grid_y + direction_y * self.speed
            
            # 이동 가능한지 체크 (경계 + 다른 적들과 충돌)
            old_x, old_y = self.grid_x, self.grid_y
            self.grid_x = new_x
            self.grid_y = new_y
            
            # 경계를 벗어나는지 체크
            positions = self.get_grid_positions()
            move_valid = True
            
            if positions:
                xs = [x for x, y in positions]
                ys = [y for x, y in positions]
                
                # 경계 체크
                from src.constants import GRID_COLS, GRID_ROWS
                if min(xs) < 0 or max(xs) >= GRID_COLS or min(ys) < 0 or max(ys) >= GRID_ROWS:
                    move_valid = False
            
            # 다른 적들과 충돌하는지 체크
            if move_valid and other_enemies:
                for other in other_enemies:
                    if other is not self and self.collides_with(other):
                        move_valid = False
                        break
            
            # 이동이 불가능하면 이전 위치로 복원
            if not move_valid:
                self.grid_x = old_x
                self.grid_y = old_y
