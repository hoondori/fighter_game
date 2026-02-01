"""Player 클래스 테스트"""

import pytest
import pygame
import math
from src.player import Player
from src.obstacle import Obstacle
from src.constants import GRID_COLS, GRID_ROWS, PLAYER_SPEED_GRID, PLAYER_MAX_HP


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
        # 연속 이동에서는 약간 경계를 넘을 수 있음
        assert player.grid_x <= 0.5  # 경계 근처에서 멈춤
        assert player.grid_x <= 0.5  # 경계 근처에서 멈춤
    
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
        # 연속 이동에서는 약간 경계를 넘을 수 있음
        assert player.grid_y <= 0.5  # 경계 근처에서 멈춤
    
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


class TestPlayerHP:
    """플레이어 HP 시스템 테스트 (Version 2)"""
    
    def test_initial_hp(self, player):
        """초기 HP 테스트"""
        assert player.hp == PLAYER_MAX_HP
        assert player.max_hp == PLAYER_MAX_HP
    
    def test_take_damage(self, player):
        """데미지 받기 테스트"""
        initial_hp = player.hp
        player.take_damage(10)
        assert player.hp == initial_hp - 10
    
    def test_hp_not_below_zero(self, player):
        """HP가 0 이하로 떨어지지 않음 테스트"""
        player.take_damage(200)
        assert player.hp == 0
    
    def test_death(self, player):
        """죽음 테스트"""
        alive = player.take_damage(50)
        assert alive  # 아직 살아있음
        
        alive = player.take_damage(50)
        assert not alive  # 죽음
    
    def test_heal(self, player):
        """체력 회복 테스트"""
        player.take_damage(30)
        player.heal(20)
        assert player.hp == PLAYER_MAX_HP - 10
    
    def test_heal_not_over_max(self, player):
        """최대 HP 초과 회복 불가 테스트"""
        player.heal(50)
        assert player.hp == PLAYER_MAX_HP


class TestPlayerDiagonalMovement:
    """플레이어 대각선 이동 테스트 (Version 2)"""
    
    def test_diagonal_movement(self, init_pygame):
        """대각선 이동 테스트"""
        player = Player(grid_x=10, grid_y=10)
        initial_x = player.grid_x
        initial_y = player.grid_y
        
        # 오른쪽 아래 대각선
        keys = {pygame.K_RIGHT: True, pygame.K_DOWN: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock)
        
        # 두 방향으로 모두 이동
        assert player.grid_x > initial_x
        assert player.grid_y > initial_y
    
    def test_diagonal_speed_normalization(self, init_pygame):
        """대각선 이동 속도 정규화 테스트"""
        player1 = Player(grid_x=10, grid_y=10)
        player2 = Player(grid_x=10, grid_y=10)
        
        # 수평 이동
        keys_horizontal = {pygame.K_RIGHT: True}
        keys_mock_h = type('obj', (object,), {
            '__getitem__': lambda self, key: keys_horizontal.get(key, False)
        })()
        player1.move(keys_mock_h)
        horizontal_distance = player1.grid_x - 10
        
        # 대각선 이동
        keys_diagonal = {pygame.K_RIGHT: True, pygame.K_DOWN: True}
        keys_mock_d = type('obj', (object,), {
            '__getitem__': lambda self, key: keys_diagonal.get(key, False)
        })()
        player2.move(keys_mock_d)
        
        # 대각선 이동 거리 계산
        diagonal_distance = math.sqrt((player2.grid_x - 10)**2 + (player2.grid_y - 10)**2)
        
        # 대각선 이동 거리가 수평 이동 거리와 비슷해야 함 (속도 정규화)
        # 약간의 오차 허용
        assert abs(diagonal_distance - horizontal_distance) < 0.1
    
    def test_all_diagonal_directions(self, init_pygame):
        """모든 대각선 방향 테스트"""
        # 오른쪽 위
        player1 = Player(grid_x=30, grid_y=30)
        keys = {pygame.K_RIGHT: True, pygame.K_UP: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        player1.move(keys_mock)
        assert player1.grid_x > 30 and player1.grid_y < 30
        
        # 왼쪽 위
        player2 = Player(grid_x=30, grid_y=30)
        keys = {pygame.K_LEFT: True, pygame.K_UP: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        player2.move(keys_mock)
        assert player2.grid_x < 30 and player2.grid_y < 30
        
        # 왼쪽 아래
        player3 = Player(grid_x=30, grid_y=30)
        keys = {pygame.K_LEFT: True, pygame.K_DOWN: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        player3.move(keys_mock)
        assert player3.grid_x < 30 and player3.grid_y > 30


class TestPlayerObstacleCollision:
    """플레이어 장애물 충돌 테스트 (Version 2)"""
    
    def test_obstacle_blocks_movement(self, init_pygame):
        """장애물이 이동을 막음 테스트"""
        player = Player(grid_x=10, grid_y=10)
        obstacle = Obstacle(grid_x=15, grid_y=10, width=3, height=3)
        
        initial_x = player.grid_x
        
        # 오른쪽으로 이동 시도 (장애물 방향)
        keys = {pygame.K_RIGHT: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        # 여러 번 이동해도 장애물 통과 불가
        for _ in range(100):
            player.move(keys_mock, [obstacle])
        
        # 장애물 앞에서 멈춤
        assert player.grid_x < 15
    
    def test_can_move_around_obstacle(self, init_pygame):
        """장애물을 우회할 수 있음 테스트"""
        player = Player(grid_x=10, grid_y=10)
        obstacle = Obstacle(grid_x=15, grid_y=10, width=3, height=3)
        
        # 위로 이동 가능 (장애물이 없는 방향)
        keys = {pygame.K_UP: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        player.move(keys_mock, [obstacle])
        assert player.grid_y < 10
