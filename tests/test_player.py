"""Player 클래스 테스트"""

import pytest
import pygame
from src.player import Player
from src.constants import GRID_COLS, GRID_ROWS, PLAYER_SPEED_GRID


@pytest.fixture(scope="module")
def init_pygame():
    """pygame 초기화 픽스처"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def player(init_pygame):
    """기본 플레이어 인스턴스 픽스처"""
    return Player(grid_x=10, grid_y=10)


class TestPlayerInitialization:
    """플레이어 초기화 테스트"""
    
    def test_player_creation(self, player):
        """플레이어 생성 테스트"""
        assert player.grid_x == 10
        assert player.grid_y == 10
        assert player.grid_size == 1
        assert player.speed == PLAYER_SPEED_GRID
    
    def test_player_color(self, player):
        """플레이어 색상 설정 테스트"""
        assert player.color is not None
        assert len(player.color) == 3  # RGB


class TestPlayerMovement:
    """플레이어 이동 테스트"""
    
    def test_move_left(self, init_pygame):
        """왼쪽 이동 테스트"""
        player = Player(grid_x=10, grid_y=10)
        initial_x = player.grid_x
        
        # 왼쪽 키 누른 상태 시뮬레이션
        keys = {pygame.K_LEFT: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.grid_x < initial_x
    
    def test_move_right(self, init_pygame):
        """오른쪽 이동 테스트"""
        player = Player(grid_x=10, grid_y=10)
        initial_x = player.grid_x
        
        keys = {pygame.K_RIGHT: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.grid_x > initial_x
    
    def test_move_up(self, init_pygame):
        """위로 이동 테스트"""
        player = Player(grid_x=10, grid_y=10)
        initial_y = player.grid_y
        
        keys = {pygame.K_UP: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.grid_y < initial_y
    
    def test_move_down(self, init_pygame):
        """아래로 이동 테스트"""
        player = Player(grid_x=10, grid_y=10)
        initial_y = player.grid_y
        
        keys = {pygame.K_DOWN: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.grid_y > initial_y
    
    def test_wasd_keys(self, init_pygame):
        """WASD 키 이동 테스트"""
        player = Player(grid_x=10, grid_y=10)
        
        # A 키 (왼쪽)
        keys = {pygame.K_a: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        initial_x = player.grid_x
        player.move(keys_mock)
        assert player.grid_x < initial_x


class TestPlayerBoundaries:
    """플레이어 화면 경계 테스트"""
    
    def test_left_boundary(self, init_pygame):
        """왼쪽 경계 테스트"""
        player = Player(grid_x=0, grid_y=10)
        
        keys = {pygame.K_LEFT: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.grid_x == 0  # 화면 밖으로 나가지 않음
    
    def test_right_boundary(self, init_pygame):
        """오른쪽 경계 테스트"""
        player = Player(grid_x=GRID_COLS - 1, grid_y=10)
        
        keys = {pygame.K_RIGHT: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.grid_x == GRID_COLS - 1
    
    def test_top_boundary(self, init_pygame):
        """위쪽 경계 테스트"""
        player = Player(grid_x=10, grid_y=0)
        
        keys = {pygame.K_UP: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.grid_y == 0
    
    def test_bottom_boundary(self, init_pygame):
        """아래쪽 경계 테스트"""
        player = Player(grid_x=10, grid_y=GRID_ROWS - 1)
        
        keys = {pygame.K_DOWN: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.grid_y == GRID_ROWS - 1


class TestPlayerCollision:
    """플레이어 충돌 판정 테스트"""
    
    def test_get_rect(self, player):
        """rect 반환 테스트"""
        rect = player.get_rect()
        assert isinstance(rect, pygame.Rect)
        pixel_x, pixel_y, pixel_width, pixel_height = player.get_pixel_pos()
        assert rect.x == int(pixel_x)
        assert rect.y == int(pixel_y)
        assert rect.width == int(pixel_width)
        assert rect.height == int(pixel_height)
    
    def test_rect_collision(self, init_pygame):
        """rect 충돌 판정 테스트"""
        player1 = Player(grid_x=10, grid_y=10)
        player2 = Player(grid_x=10, grid_y=10)
        
        # 같은 위치에 있으면 충돌
        assert player1.get_rect().colliderect(player2.get_rect())
        
        # 멀리 떨어져 있으면 충돌 안 함
        player2.grid_x = 20
        player2.grid_y = 20
        assert not player1.get_rect().colliderect(player2.get_rect())
