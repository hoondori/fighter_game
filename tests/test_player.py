"""Player 클래스 테스트"""

import pytest
import pygame
from src.player import Player
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED


@pytest.fixture(scope="module")
def init_pygame():
    """pygame 초기화 픽스처"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def player(init_pygame):
    """기본 플레이어 인스턴스 픽스처"""
    return Player(x=100, y=100, width=30, height=30, speed=PLAYER_SPEED)


class TestPlayerInitialization:
    """플레이어 초기화 테스트"""
    
    def test_player_creation(self, player):
        """플레이어 생성 테스트"""
        assert player.x == 100
        assert player.y == 100
        assert player.width == 30
        assert player.height == 30
        assert player.speed == PLAYER_SPEED
    
    def test_player_color(self, player):
        """플레이어 색상 설정 테스트"""
        assert player.color is not None
        assert len(player.color) == 3  # RGB


class TestPlayerMovement:
    """플레이어 이동 테스트"""
    
    def test_move_left(self, player):
        """왼쪽 이동 테스트"""
        initial_x = player.x
        
        # 왼쪽 키 누른 상태 시뮬레이션
        keys = {pygame.K_LEFT: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.x < initial_x
    
    def test_move_right(self, player):
        """오른쪽 이동 테스트"""
        initial_x = player.x
        
        keys = {pygame.K_RIGHT: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.x > initial_x
    
    def test_move_up(self, player):
        """위로 이동 테스트"""
        initial_y = player.y
        
        keys = {pygame.K_UP: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.y < initial_y
    
    def test_move_down(self, player):
        """아래로 이동 테스트"""
        initial_y = player.y
        
        keys = {pygame.K_DOWN: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.y > initial_y
    
    def test_wasd_keys(self, init_pygame):
        """WASD 키 이동 테스트"""
        player = Player(x=100, y=100, width=30, height=30, speed=PLAYER_SPEED)
        
        # A 키 (왼쪽)
        keys = {pygame.K_a: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        initial_x = player.x
        player.move(keys_mock)
        assert player.x < initial_x


class TestPlayerBoundaries:
    """플레이어 화면 경계 테스트"""
    
    def test_left_boundary(self, init_pygame):
        """왼쪽 경계 테스트"""
        player = Player(x=0, y=100, width=30, height=30, speed=PLAYER_SPEED)
        
        keys = {pygame.K_LEFT: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.x == 0  # 화면 밖으로 나가지 않음
    
    def test_right_boundary(self, init_pygame):
        """오른쪽 경계 테스트"""
        player = Player(x=SCREEN_WIDTH - 30, y=100, width=30, height=30, speed=PLAYER_SPEED)
        
        keys = {pygame.K_RIGHT: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.x == SCREEN_WIDTH - player.width
    
    def test_top_boundary(self, init_pygame):
        """위쪽 경계 테스트"""
        player = Player(x=100, y=0, width=30, height=30, speed=PLAYER_SPEED)
        
        keys = {pygame.K_UP: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.y == 0
    
    def test_bottom_boundary(self, init_pygame):
        """아래쪽 경계 테스트"""
        player = Player(x=100, y=SCREEN_HEIGHT - 30, width=30, height=30, speed=PLAYER_SPEED)
        
        keys = {pygame.K_DOWN: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        assert player.y == SCREEN_HEIGHT - player.height


class TestPlayerCollision:
    """플레이어 충돌 판정 테스트"""
    
    def test_get_rect(self, player):
        """rect 반환 테스트"""
        rect = player.get_rect()
        assert isinstance(rect, pygame.Rect)
        assert rect.x == player.x
        assert rect.y == player.y
        assert rect.width == player.width
        assert rect.height == player.height
    
    def test_rect_collision(self, init_pygame):
        """rect 충돌 판정 테스트"""
        player1 = Player(x=100, y=100, width=30, height=30)
        player2 = Player(x=100, y=100, width=30, height=30)
        
        # 같은 위치에 있으면 충돌
        assert player1.get_rect().colliderect(player2.get_rect())
        
        # 멀리 떨어져 있으면 충돌 안 함
        player2.x = 200
        player2.y = 200
        assert not player1.get_rect().colliderect(player2.get_rect())
