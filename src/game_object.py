"""게임 객체 기본 클래스"""

import pygame
from src.constants import GRID_WIDTH, GRID_HEIGHT, GRID_COLS, GRID_ROWS


class GameObject:
    """모든 게임 객체의 기본 클래스 (그리드 기반, 복잡한 모양 지원)"""
    
    def __init__(self, grid_x, grid_y, color, grid_size=1, shape=None):
        """
        게임 객체 초기화
        
        Args:
            grid_x: 기준점 그리드 x 좌표
            grid_y: 기준점 그리드 y 좌표
            color: RGB 색상 튜플
            grid_size: 그리드 크기 (shape이 None일 때)
            shape: 상대 좌표 리스트 [(0,0), (1,0), ...] 또는 None (정사각형)
        """
        self.grid_x = float(grid_x)
        self.grid_y = float(grid_y)
        self.grid_size = grid_size
        self.color = color
        
        # 모양 정의: shape이 None이면 정사각형
        if shape is None:
            self.shape = [(i, j) for i in range(grid_size) for j in range(grid_size)]
        else:
            self.shape = shape
    
    def get_grid_positions(self):
        """
        현재 차지하고 있는 모든 그리드 좌표 반환
        
        Returns:
            list: [(x1, y1), (x2, y2), ...] 절대 좌표 리스트
        """
        return [(int(self.grid_x + dx), int(self.grid_y + dy)) for dx, dy in self.shape]
    
    def get_bounding_box(self):
        """
        모든 그리드 포인트를 포함하는 최소 경계 상자 계산
        
        Returns:
            tuple: (min_x, min_y, max_x, max_y) 그리드 좌표
        """
        positions = self.get_grid_positions()
        if not positions:
            return (int(self.grid_x), int(self.grid_y), int(self.grid_x), int(self.grid_y))
        xs = [x for x, y in positions]
        ys = [y for x, y in positions]
        return (min(xs), min(ys), max(xs), max(ys))
    
    def get_center(self):
        """
        객체의 중심점 계산
        
        Returns:
            tuple: (center_x, center_y) float 좌표
        """
        if not self.shape:
            return (self.grid_x, self.grid_y)
        
        avg_x = sum(dx for dx, dy in self.shape) / len(self.shape)
        avg_y = sum(dy for dx, dy in self.shape) / len(self.shape)
        return (self.grid_x + avg_x, self.grid_y + avg_y)
    
    def get_pixel_pos(self):
        """
        경계 상자의 픽셀 좌표로 변환
        
        Returns:
            tuple: (pixel_x, pixel_y, pixel_width, pixel_height)
        """
        min_x, min_y, max_x, max_y = self.get_bounding_box()
        pixel_x = min_x * GRID_WIDTH
        pixel_y = min_y * GRID_HEIGHT
        pixel_width = (max_x - min_x + 1) * GRID_WIDTH
        pixel_height = (max_y - min_y + 1) * GRID_HEIGHT
        return (pixel_x, pixel_y, pixel_width, pixel_height)
    
    def draw(self, screen):
        """
        화면에 객체를 그림 (각 그리드 셀마다 사각형)
        
        Args:
            screen: pygame display surface
        """
        for grid_x, grid_y in self.get_grid_positions():
            pixel_x = grid_x * GRID_WIDTH
            pixel_y = grid_y * GRID_HEIGHT
            pygame.draw.rect(screen, self.color, (pixel_x, pixel_y, GRID_WIDTH, GRID_HEIGHT))
    
    def get_rect(self):
        """
        충돌 판정용 rect 반환 (경계 상자 기반)
        
        Returns:
            pygame.Rect: 객체의 충돌 영역
        """
        pixel_x, pixel_y, pixel_width, pixel_height = self.get_pixel_pos()
        return pygame.Rect(int(pixel_x), int(pixel_y), int(pixel_width), int(pixel_height))
    
    def collides_with(self, other):
        """
        다른 객체와의 그리드 기반 정밀 충돌 판정
        
        Args:
            other: 다른 게임 객체 (get_grid_positions 메서드 필요)
            
        Returns:
            bool: 충돌하면 True
        """
        my_positions = set(self.get_grid_positions())
        other_positions = set(other.get_grid_positions())
        return bool(my_positions & other_positions)
    
    def is_valid_position(self, new_x, new_y):
        """
        새로운 위치가 유효한지 확인 (화면 밖으로 나가지 않는지)
        
        Args:
            new_x: 새로운 기준점 x 좌표
            new_y: 새로운 기준점 y 좌표
            
        Returns:
            bool: 유효하면 True
        """
        for dx, dy in self.shape:
            abs_x = int(new_x + dx)
            abs_y = int(new_y + dy)
            if abs_x < 0 or abs_x >= GRID_COLS or abs_y < 0 or abs_y >= GRID_ROWS:
                return False
        return True
