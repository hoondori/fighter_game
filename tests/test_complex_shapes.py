"""복잡한 모양 시스템 테스트"""

import pytest
import pygame
from src.player import Player
from src.enemy import Enemy
from src.constants import PLAYER_SHAPE, RED

# 테스트용 모양 정의
L_SHAPE = [(0, 0), (0, 1), (0, 2), (1, 2)]
T_SHAPE = [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2)]


@pytest.fixture(scope="module")
def init_pygame():
    """pygame 초기화"""
    pygame.init()
    yield
    pygame.quit()


class TestComplexShapes:
    """복잡한 모양 지원 테스트"""
    
    def test_player_default_shape(self, init_pygame):
        """플레이어는 + 모양을 사용"""
        player = Player(grid_x=10, grid_y=10)
        positions = player.get_grid_positions()
        
        # + 모양 = 5개 셀
        assert len(positions) == 5
        # PLAYER_SHAPE 검증
        assert len(PLAYER_SHAPE) == 5
    
    def test_player_custom_shape(self, init_pygame):
        """플레이어는 shape 파라미터를 받지 않음 (항상 + 모양)"""
        player = Player(grid_x=10, grid_y=10)
        positions = player.get_grid_positions()
        
        # + 모양: (1,0), (0,1), (1,1), (2,1), (1,2)
        expected_positions = [(10 + dx, 10 + dy) for dx, dy in PLAYER_SHAPE]
        assert set(positions) == set(expected_positions)
    
    def test_enemy_custom_shape(self, init_pygame):
        """적 커스텀 모양 테스트 (T자)"""
        enemy = Enemy(grid_x=20, grid_y=20, color=RED, shape=T_SHAPE)
        positions = enemy.get_grid_positions()
        
        # 5개 셀
        assert len(positions) == 5
        assert (20, 20) in positions
        assert (21, 20) in positions
        assert (22, 20) in positions
        assert (21, 21) in positions
        assert (21, 22) in positions
    
    def test_bounding_box(self, init_pygame):
        """경계 상자 계산 테스트"""
        enemy = Enemy(grid_x=10, grid_y=10, color=RED, shape=L_SHAPE)
        min_x, min_y, max_x, max_y = enemy.get_bounding_box()
        
        assert min_x == 10
        assert min_y == 10
        assert max_x == 11
        assert max_y == 12
    
    def test_collision_same_position(self, init_pygame):
        """같은 위치에서 충돌 테스트"""
        player = Player(grid_x=10, grid_y=10)
        enemy = Enemy(grid_x=10, grid_y=10, color=RED, shape=T_SHAPE)
        
        # 충돌해야 함
        assert player.collides_with(enemy)
        assert enemy.collides_with(player)
    
    def test_collision_different_position(self, init_pygame):
        """다른 위치에서 충돌 안함 테스트"""
        player = Player(grid_x=10, grid_y=10)
        enemy = Enemy(grid_x=20, grid_y=20, color=RED, shape=T_SHAPE)
        
        # 충돌하지 않아야 함
        assert not player.collides_with(enemy)
        assert not enemy.collides_with(player)
    
    def test_collision_partial_overlap(self, init_pygame):
        """부분 겹침 충돌 테스트"""
        player = Player(grid_x=10, grid_y=10)
        # 플레이어의 + 모양과 겹치도록 배치
        # + 모양: (11,10), (10,11), (11,11), (12,11), (11,12)
        enemy = Enemy(grid_x=11, grid_y=11, color=RED, shape=[(0, 0)])
        
        # 충돌해야 함 (11,11)에서 겹침
        assert player.collides_with(enemy)
    
    def test_valid_position_check(self, init_pygame):
        """유효한 위치 확인 테스트"""
        enemy = Enemy(grid_x=10, grid_y=10, color=RED, shape=L_SHAPE)
        
        # 유효한 위치
        assert enemy.is_valid_position(10, 10)
        assert enemy.is_valid_position(0, 0)
        
        # 화면 밖
        assert not enemy.is_valid_position(-1, 0)
        assert not enemy.is_valid_position(0, -1)
    
    def test_pixel_conversion(self, init_pygame):
        """픽셀 좌표 변환 테스트"""
        enemy = Enemy(grid_x=10, grid_y=10, color=RED, shape=L_SHAPE)
        pixel_x, pixel_y, pixel_width, pixel_height = enemy.get_pixel_pos()
        
        # 경계 상자 기반
        assert pixel_x == 10 * 20  # GRID_WIDTH = 20
        assert pixel_y == 10 * 20
        assert pixel_width == 2 * 20  # 2칸 너비
        assert pixel_height == 3 * 20  # 3칸 높이
    
    def test_backward_compatibility(self, init_pygame):
        """하위 호환성 테스트"""
        # 플레이어는 기본 + 모양
        player = Player(grid_x=10, grid_y=10)
        
        # get_rect(), get_pixel_pos() 호출 가능
        rect = player.get_rect()
        assert rect is not None
        
        pixel_pos = player.get_pixel_pos()
        assert len(pixel_pos) == 4

