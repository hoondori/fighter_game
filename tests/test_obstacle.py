"""장애물 클래스 테스트"""

import pytest
import pygame
from src.obstacle import Obstacle
from src.player import Player


@pytest.fixture(scope="module")
def init_pygame():
    """pygame 초기화 픽스처"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def obstacle(init_pygame):
    """기본 장애물 인스턴스 픽스처"""
    return Obstacle(grid_x=10, grid_y=10, width=3, height=3)


class TestObstacleInitialization:
    """장애물 초기화 테스트"""
    
    def test_obstacle_creation(self, obstacle):
        """장애물 생성 테스트"""
        assert obstacle.grid_x == 10
        assert obstacle.grid_y == 10
        assert obstacle.width == 3
        assert obstacle.height == 3
    
    def test_obstacle_shape(self, obstacle):
        """장애물 모양 테스트 (3x3 = 9 블록)"""
        assert len(obstacle.shape) == 9
    
    def test_obstacle_color(self, obstacle):
        """장애물 색상 설정 테스트"""
        assert obstacle.color is not None
        assert len(obstacle.color) == 3  # RGB


class TestObstacleCollision:
    """장애물 충돌 테스트"""
    
    def test_collision_with_player(self, init_pygame):
        """플레이어와 장애물 충돌 테스트"""
        obstacle = Obstacle(grid_x=10, grid_y=10, width=3, height=3)
        player = Player(grid_x=10, grid_y=10)
        
        # 충돌 확인
        assert player.collides_with(obstacle)
    
    def test_no_collision_when_far(self, init_pygame):
        """거리가 먼 경우 충돌 없음 테스트"""
        obstacle = Obstacle(grid_x=10, grid_y=10, width=3, height=3)
        player = Player(grid_x=50, grid_y=50)
        
        # 충돌 없음
        assert not player.collides_with(obstacle)
    
    def test_player_blocked_by_obstacle(self, init_pygame):
        """플레이어가 장애물에 막힘 테스트"""
        obstacle = Obstacle(grid_x=15, grid_y=10, width=3, height=3)
        player = Player(grid_x=10, grid_y=10)
        initial_x = player.grid_x
        
        # 오른쪽으로 이동 시도 (장애물이 있는 방향)
        keys = {pygame.K_RIGHT: True}
        keys_mock = type('obj', (object,), {
            '__getitem__': lambda self, key: keys.get(key, False)
        })()
        
        # 여러 번 이동해도 장애물을 통과하지 못함
        for _ in range(100):
            player.move(keys_mock, [obstacle])
        
        # 장애물 앞에서 멈춤
        assert player.grid_x < 15


class TestObstacleDimensions:
    """장애물 크기 테스트"""
    
    def test_small_obstacle(self, init_pygame):
        """작은 장애물 (2x2) 테스트"""
        obstacle = Obstacle(grid_x=10, grid_y=10, width=2, height=2)
        assert len(obstacle.shape) == 4
    
    def test_large_obstacle(self, init_pygame):
        """큰 장애물 (5x5) 테스트"""
        obstacle = Obstacle(grid_x=10, grid_y=10, width=5, height=5)
        assert len(obstacle.shape) == 25
    
    def test_rectangular_obstacle(self, init_pygame):
        """직사각형 장애물 (4x2) 테스트"""
        obstacle = Obstacle(grid_x=10, grid_y=10, width=4, height=2)
        assert len(obstacle.shape) == 8
