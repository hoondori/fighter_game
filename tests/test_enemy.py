"""Enemy 클래스 테스트"""

import pytest
import pygame
import math
from src.enemy import Enemy
from src.player import Player
from src.constants import ENEMY_SPEED_GRID, RED


@pytest.fixture(scope="module")
def init_pygame():
    """pygame 초기화 픽스처"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def enemy(init_pygame):
    """기본 적 인스턴스 픽스처"""
    return Enemy(grid_x=0, grid_y=0, color=RED)


@pytest.fixture
def player(init_pygame):
    """테스트용 플레이어 인스턴스"""
    return Player(grid_x=10, grid_y=10)


class TestEnemyInitialization:
    """적 초기화 테스트"""
    
    def test_enemy_creation(self, enemy):
        """적 생성 테스트"""
        assert enemy.grid_x == 0
        assert enemy.grid_y == 0
        assert enemy.speed == ENEMY_SPEED_GRID
    
    def test_enemy_color(self, enemy):
        """적 색상 설정 테스트"""
        assert enemy.color is not None
        assert len(enemy.color) == 3  # RGB


class TestEnemyMovement:
    """적 이동 테스트"""
    
    def test_move_towards_player_basic(self, init_pygame):
        """플레이어를 향한 기본 이동 테스트"""
        enemy = Enemy(grid_x=0, grid_y=0, color=RED)
        player = Player(grid_x=10, grid_y=10)
        
        initial_x = enemy.grid_x
        initial_y = enemy.grid_y
        
        enemy.move_towards_player(player)
        
        # 적이 플레이어 방향으로 이동했는지 확인
        assert enemy.grid_x > initial_x  # 오른쪽으로 이동
        assert enemy.grid_y > initial_y  # 아래로 이동
    
    def test_move_towards_player_distance(self, init_pygame):
        """적이 이동한 거리가 속도와 일치하는지 테스트"""
        enemy = Enemy(grid_x=0, grid_y=0, color=RED)
        player = Player(grid_x=10, grid_y=0)  # 같은 y 좌표
        
        initial_x = enemy.grid_x
        enemy.move_towards_player(player)
        
        distance_moved = abs(enemy.grid_x - initial_x)
        # 속도와 근사하게 일치해야 함 (부동소수점 오차 고려)
        assert abs(distance_moved - ENEMY_SPEED_GRID) < 0.1
    
    def test_move_towards_player_same_position(self, init_pygame):
        """적과 플레이어 중심이 비슷한 위치일 때 테스트"""
        # 플레이어 중심과 적의 위치가 가까워서 거의 이동하지 않음
        player = Player(grid_x=10, grid_y=10)
        player_center = player.get_center()
        
        # 적을 플레이어 중심에 배치
        enemy = Enemy(grid_x=player_center[0], grid_y=player_center[1], color=RED)
        
        initial_x = enemy.grid_x
        initial_y = enemy.grid_y
        
        enemy.move_towards_player(player)
        
        # 중심이 가까우면 거의 이동하지 않아야 함
        distance_moved = math.sqrt((enemy.grid_x - initial_x)**2 + (enemy.grid_y - initial_y)**2)
        assert distance_moved < ENEMY_SPEED_GRID * 2  # 속도의 2배 이하로 이동
    
    def test_move_from_different_directions(self, init_pygame):
        """다양한 방향에서 플레이어로 접근하는 테스트"""
        player = Player(grid_x=14, grid_y=14)
        
        # 왼쪽에서 접근
        enemy_left = Enemy(grid_x=5, grid_y=14, color=RED)
        enemy_left.move_towards_player(player)
        assert enemy_left.grid_x > 5  # 오른쪽으로 이동
        
        # 오른쪽에서 접근
        enemy_right = Enemy(grid_x=20, grid_y=14, color=RED)
        enemy_right.move_towards_player(player)
        assert enemy_right.grid_x < 20  # 왼쪽으로 이동
        
        # 위에서 접근
        enemy_top = Enemy(grid_x=14, grid_y=5, color=RED)
        enemy_top.move_towards_player(player)
        assert enemy_top.grid_y > 5  # 아래로 이동
        
        # 아래에서 접근
        enemy_bottom = Enemy(grid_x=14, grid_y=20, color=RED)
        enemy_bottom.move_towards_player(player)
        assert enemy_bottom.grid_y < 20  # 위로 이동


class TestEnemyCollision:
    """적 충돌 판정 테스트"""
    
    def test_get_rect(self, enemy):
        """rect 반환 테스트"""
        rect = enemy.get_rect()
        assert isinstance(rect, pygame.Rect)
        pixel_x, pixel_y, pixel_width, pixel_height = enemy.get_pixel_pos()
        assert rect.x == int(pixel_x)
        assert rect.y == int(pixel_y)
        assert rect.width == int(pixel_width)
        assert rect.height == int(pixel_height)
    
    def test_collision_with_player(self, init_pygame):
        """플레이어와의 충돌 테스트"""
        enemy = Enemy(grid_x=10, grid_y=10, color=RED)
        player = Player(grid_x=10, grid_y=10)
        
        # 같은 위치에 있으면 충돌
        assert enemy.get_rect().colliderect(player.get_rect())
    
    def test_no_collision_when_far(self, init_pygame):
        """거리가 멀 때 충돌하지 않는지 테스트"""
        enemy = Enemy(grid_x=0, grid_y=0, color=RED)
        player = Player(grid_x=20, grid_y=20)
        
        # 멀리 떨어져 있으면 충돌 안 함
        assert not enemy.get_rect().colliderect(player.get_rect())


class TestEnemyBehavior:
    """적의 전체적인 행동 테스트"""
    
    def test_enemy_tracks_moving_player(self, init_pygame):
        """이동하는 플레이어를 추적하는지 테스트"""
        enemy = Enemy(grid_x=0, grid_y=0, color=RED)
        player = Player(grid_x=10, grid_y=10)
        
        # 여러 프레임 동안 이동
        for _ in range(10):
            prev_distance = math.sqrt(
                (player.grid_x - enemy.grid_x)**2 + (player.grid_y - enemy.grid_y)**2
            )
            enemy.move_towards_player(player)
            new_distance = math.sqrt(
                (player.grid_x - enemy.grid_x)**2 + (player.grid_y - enemy.grid_y)**2
            )
            
            # 거리가 줄어들어야 함 (플레이어가 멈춰있으므로)
            assert new_distance < prev_distance or abs(new_distance - prev_distance) < 0.1


class TestEnemyHP:
    """적 HP 시스템 테스트 (Version 2)"""
    
    def test_initial_hp(self, init_pygame):
        """초기 HP 테스트"""
        enemy = Enemy(grid_x=0, grid_y=0, color=RED, hp=50)
        assert enemy.hp == 50
        assert enemy.max_hp == 50
    
    def test_default_hp(self, enemy):
        """기본 HP 테스트"""
        assert enemy.hp == 1
        assert enemy.max_hp == 1
    
    def test_take_damage(self, init_pygame):
        """데미지 받기 테스트"""
        enemy = Enemy(grid_x=0, grid_y=0, color=RED, hp=100)
        alive = enemy.take_damage(30)
        assert enemy.hp == 70
        assert alive
    
    def test_death(self, init_pygame):
        """죽음 테스트"""
        enemy = Enemy(grid_x=0, grid_y=0, color=RED, hp=50)
        alive = enemy.take_damage(50)
        assert enemy.hp == 0
        assert not alive
        assert enemy.is_dead()
    
    def test_overkill(self, init_pygame):
        """오버킬 테스트 (HP보다 큰 데미지)"""
        enemy = Enemy(grid_x=0, grid_y=0, color=RED, hp=50)
        enemy.take_damage(100)
        assert enemy.hp == 0
        assert enemy.is_dead()


class TestEnemyObstacleAvoidance:
    """적 장애물 회피 테스트 (Version 2)"""
    
    def test_obstacle_blocks_enemy(self, init_pygame):
        """장애물이 적 이동을 막음 테스트 (우회 가능)"""
        from src.obstacle import Obstacle
        
        enemy = Enemy(grid_x=10, grid_y=10, color=RED)
        player = Player(grid_x=20, grid_y=10)
        obstacle = Obstacle(grid_x=15, grid_y=10, width=3, height=3)
        
        initial_x = enemy.grid_x
        
        # 여러 번 이동 시도
        for _ in range(100):
            enemy.move_towards_player(player, obstacles=[obstacle])
        
        # 적이 움직였고 (우회함), 장애물을 통과하지 않음
        assert enemy.grid_x > initial_x  # 이동했음
        
        # 적이 장애물 내부에 있지 않음
        assert not enemy.collides_with(obstacle)
    
    def test_enemy_avoids_multiple_obstacles(self, init_pygame):
        """여러 장애물 회피 테스트"""
        from src.obstacle import Obstacle
        
        enemy = Enemy(grid_x=10, grid_y=10, color=RED)
        player = Player(grid_x=30, grid_y=10)
        obstacles = [
            Obstacle(grid_x=15, grid_y=10, width=2, height=2),
            Obstacle(grid_x=20, grid_y=10, width=2, height=2)
        ]
        
        # 여러 번 이동
        for _ in range(50):
            enemy.move_towards_player(player, obstacles=obstacles)
        
        # 적이 움직였지만 장애물 안에 있지 않음
        for obstacle in obstacles:
            assert not enemy.collides_with(obstacle)
    
    def test_enemy_with_obstacles_and_other_enemies(self, init_pygame):
        """장애물과 다른 적들 모두 고려한 이동 테스트"""
        from src.obstacle import Obstacle
        
        enemy1 = Enemy(grid_x=10, grid_y=10, color=RED)
        enemy2 = Enemy(grid_x=12, grid_y=10, color=RED)
        player = Player(grid_x=20, grid_y=10)
        obstacle = Obstacle(grid_x=15, grid_y=10, width=2, height=2)
        
        # 두 적 모두 이동
        for _ in range(10):
            enemy1.move_towards_player(player, [enemy1, enemy2], [obstacle])
            enemy2.move_towards_player(player, [enemy1, enemy2], [obstacle])
        
        # 적들이 장애물을 통과하지 않음
        assert not enemy1.collides_with(obstacle)
        assert not enemy2.collides_with(obstacle)
