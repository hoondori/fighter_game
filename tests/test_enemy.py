"""Enemy 클래스 테스트"""

import pytest
import pygame
import math
from src.enemy import Enemy
from src.player import Player
from src.constants import ENEMY_SPEED


@pytest.fixture(scope="module")
def init_pygame():
    """pygame 초기화 픽스처"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def enemy(init_pygame):
    """기본 적 인스턴스 픽스처"""
    return Enemy(x=0, y=0, width=25, height=25, speed=ENEMY_SPEED)


@pytest.fixture
def player(init_pygame):
    """테스트용 플레이어 인스턴스"""
    return Player(x=400, y=300, width=30, height=30)


class TestEnemyInitialization:
    """적 초기화 테스트"""
    
    def test_enemy_creation(self, enemy):
        """적 생성 테스트"""
        assert enemy.x == 0
        assert enemy.y == 0
        assert enemy.width == 25
        assert enemy.height == 25
        assert enemy.speed == ENEMY_SPEED
    
    def test_enemy_color(self, enemy):
        """적 색상 설정 테스트"""
        assert enemy.color is not None
        assert len(enemy.color) == 3  # RGB


class TestEnemyMovement:
    """적 이동 테스트"""
    
    def test_move_towards_player_basic(self, init_pygame):
        """플레이어를 향한 기본 이동 테스트"""
        enemy = Enemy(x=0, y=0, width=25, height=25, speed=ENEMY_SPEED)
        player = Player(x=100, y=100, width=30, height=30)
        
        initial_x = enemy.x
        initial_y = enemy.y
        
        enemy.move_towards_player(player)
        
        # 적이 플레이어 방향으로 이동했는지 확인
        assert enemy.x > initial_x  # 오른쪽으로 이동
        assert enemy.y > initial_y  # 아래로 이동
    
    def test_move_towards_player_distance(self, init_pygame):
        """적이 이동한 거리가 속도와 일치하는지 테스트"""
        enemy = Enemy(x=0, y=0, width=25, height=25, speed=ENEMY_SPEED)
        player = Player(x=100, y=0, width=30, height=30)  # 같은 y 좌표
        
        initial_x = enemy.x
        enemy.move_towards_player(player)
        
        distance_moved = abs(enemy.x - initial_x)
        # 속도와 근사하게 일치해야 함 (부동소수점 오차 고려)
        assert abs(distance_moved - ENEMY_SPEED) < 0.1
    
    def test_move_towards_player_same_position(self, init_pygame):
        """적과 플레이어 중심이 같은 위치일 때 테스트"""
        # 중심점이 같도록 위치 조정
        enemy = Enemy(x=100, y=100, width=25, height=25, speed=ENEMY_SPEED)
        player = Player(x=100 - 2.5, y=100 - 2.5, width=30, height=30)  # 중심을 맞춤
        
        initial_x = enemy.x
        initial_y = enemy.y
        
        enemy.move_towards_player(player)
        
        # 중심이 같으면 이동하지 않아야 함
        assert abs(enemy.x - initial_x) < 0.01  # 부동소수점 오차 허용
        assert abs(enemy.y - initial_y) < 0.01
    
    def test_move_from_different_directions(self, init_pygame):
        """다양한 방향에서 플레이어로 접근하는 테스트"""
        player = Player(x=400, y=300, width=30, height=30)
        
        # 왼쪽에서 접근
        enemy_left = Enemy(x=100, y=300, width=25, height=25, speed=ENEMY_SPEED)
        enemy_left.move_towards_player(player)
        assert enemy_left.x > 100  # 오른쪽으로 이동
        
        # 오른쪽에서 접근
        enemy_right = Enemy(x=700, y=300, width=25, height=25, speed=ENEMY_SPEED)
        enemy_right.move_towards_player(player)
        assert enemy_right.x < 700  # 왼쪽으로 이동
        
        # 위에서 접근
        enemy_top = Enemy(x=400, y=100, width=25, height=25, speed=ENEMY_SPEED)
        enemy_top.move_towards_player(player)
        assert enemy_top.y > 100  # 아래로 이동
        
        # 아래에서 접근
        enemy_bottom = Enemy(x=400, y=500, width=25, height=25, speed=ENEMY_SPEED)
        enemy_bottom.move_towards_player(player)
        assert enemy_bottom.y < 500  # 위로 이동


class TestEnemyCollision:
    """적 충돌 판정 테스트"""
    
    def test_get_rect(self, enemy):
        """rect 반환 테스트"""
        rect = enemy.get_rect()
        assert isinstance(rect, pygame.Rect)
        # 정수로 변환되어야 함
        assert rect.x == int(enemy.x)
        assert rect.y == int(enemy.y)
        assert rect.width == enemy.width
        assert rect.height == enemy.height
    
    def test_collision_with_player(self, init_pygame):
        """플레이어와의 충돌 테스트"""
        enemy = Enemy(x=100, y=100, width=25, height=25)
        player = Player(x=100, y=100, width=30, height=30)
        
        # 같은 위치에 있으면 충돌
        assert enemy.get_rect().colliderect(player.get_rect())
    
    def test_no_collision_when_far(self, init_pygame):
        """거리가 멀 때 충돌하지 않는지 테스트"""
        enemy = Enemy(x=0, y=0, width=25, height=25)
        player = Player(x=500, y=500, width=30, height=30)
        
        # 멀리 떨어져 있으면 충돌 안 함
        assert not enemy.get_rect().colliderect(player.get_rect())


class TestEnemyBehavior:
    """적의 전체적인 행동 테스트"""
    
    def test_enemy_tracks_moving_player(self, init_pygame):
        """이동하는 플레이어를 추적하는지 테스트"""
        enemy = Enemy(x=0, y=0, width=25, height=25, speed=ENEMY_SPEED)
        player = Player(x=100, y=100, width=30, height=30)
        
        # 여러 프레임 동안 이동
        for _ in range(10):
            prev_distance = math.sqrt(
                (player.x - enemy.x)**2 + (player.y - enemy.y)**2
            )
            enemy.move_towards_player(player)
            new_distance = math.sqrt(
                (player.x - enemy.x)**2 + (player.y - enemy.y)**2
            )
            
            # 거리가 줄어들어야 함 (플레이어가 멈춰있으므로)
            assert new_distance < prev_distance or abs(new_distance - prev_distance) < 0.1
