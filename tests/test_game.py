"""Game 클래스 테스트"""

import pytest
import pygame
from src.game import Game
from src.constants import GRID_COLS, GRID_ROWS


@pytest.fixture(scope="module")
def init_pygame():
    """pygame 초기화 픽스처"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def game(init_pygame):
    """기본 게임 인스턴스 픽스처"""
    return Game()


class TestGameInitialization:
    """게임 초기화 테스트"""
    
    def test_game_creation(self, game):
        """게임 생성 테스트"""
        assert game.screen is not None
        assert game.clock is not None
        assert game.player is not None
        assert game.enemies == []
        assert game.running is True
        assert game.game_over is False
    
    def test_player_start_position(self, game):
        """플레이어 시작 위치 테스트 (그리드 중앙)"""
        assert game.player.grid_x == GRID_COLS // 2
        assert game.player.grid_y == GRID_ROWS // 2
    
    def test_font_initialization(self, game):
        """폰트 초기화 테스트"""
        assert game.font is not None
        assert game.small_font is not None


class TestEnemySpawning:
    """적 spawn 테스트"""
    
    def test_spawn_enemy(self, game):
        """적 spawn 테스트"""
        initial_enemy_count = len(game.enemies)
        game.spawn_enemy()
        assert len(game.enemies) == initial_enemy_count + 1
    
    def test_spawn_multiple_enemies(self, game):
        """여러 적 spawn 테스트"""
        game.enemies = []  # 초기화
        
        for i in range(5):
            game.spawn_enemy()
        
        assert len(game.enemies) == 5
    
    def test_spawned_enemy_at_screen_edge(self, game):
        """spawn된 적이 화면 경계 근처에 있는지 테스트 (모양 크기 고려)"""
        game.enemies = []
        game.spawn_enemy()
        
        enemy = game.enemies[0]
        
        # 적의 모든 그리드 위치가 화면 안에 있어야 함
        positions = enemy.get_grid_positions()
        for x, y in positions:
            assert 0 <= x < GRID_COLS
            assert 0 <= y < GRID_ROWS
        
        # 적의 일부가 가장자리에 닿아 있어야 함
        xs = [x for x, y in positions]
        ys = [y for x, y in positions]
        at_edge = (
            min(xs) == 0 or 
            max(xs) == GRID_COLS - 1 or 
            min(ys) == 0 or 
            max(ys) == GRID_ROWS - 1
        )
        assert at_edge


class TestCollisionDetection:
    """충돌 판정 테스트"""
    
    def test_no_collision_initially(self, game):
        """초기에는 충돌이 없어야 함"""
        game.enemies = []
        assert game.check_collision() is False
        assert game.game_over is False
    
    def test_collision_detection(self, init_pygame):
        """충돌 감지 테스트 (Version 2: HP 시스템)"""
        game = Game()
        game.enemies = []
        
        # 플레이어의 + 모양 중 한 위치에 적 spawn
        # PLAYER_SHAPE = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
        # (1, 1) 위치에 적을 배치하면 확실히 충돌
        from src.enemy import Enemy
        from src.constants import RED
        enemy = Enemy(
            grid_x=game.player.grid_x + 1,
            grid_y=game.player.grid_y + 1,
            color=RED
        )
        game.enemies.append(enemy)
        
        # 충돌 확인 (데미지를 받지만 즉시 게임 오버는 아님)
        initial_hp = game.player.hp
        assert game.check_collision() is True
        assert game.player.hp < initial_hp  # HP 감소
        
        # 여러 번 충돌하면 게임 오버
        for _ in range(20):
            game.collision_cooldown = 0  # 쿨다운 무시
            game.check_collision()
        assert game.game_over is True  # HP가 0이 되어 게임 오버
    
    def test_no_collision_when_far(self, init_pygame):
        """거리가 멀 때 충돌하지 않는지 테스트"""
        game = Game()
        game.enemies = []
        
        from src.enemy import Enemy
        from src.constants import RED
        enemy = Enemy(grid_x=0, grid_y=0, color=RED)
        game.enemies.append(enemy)
        
        # 충돌하지 않음
        assert game.check_collision() is False
        assert game.game_over is False


class TestGameState:
    """게임 상태 테스트"""
    
    def test_game_over_state(self, init_pygame):
        """게임 오버 상태 테스트"""
        game = Game()
        
        assert game.game_over is False
        
        # 게임 오버 트리거
        game.game_over = True
        
        assert game.game_over is True
    
    def test_update_when_game_over(self, init_pygame):
        """게임 오버 시 업데이트가 멈추는지 테스트"""
        game = Game()
        game.game_over = True
        
        initial_enemy_count = len(game.enemies)
        
        # update 호출해도 적이 spawn되지 않아야 함
        game.update()
        
        # 적 개수가 변하지 않음
        assert len(game.enemies) == initial_enemy_count


class TestGameIntegration:
    """게임 통합 테스트"""
    
    def test_game_loop_components(self, game):
        """게임 루프 구성 요소 테스트"""
        # 게임 루프의 주요 메서드들이 존재하는지 확인
        assert hasattr(game, 'handle_events')
        assert hasattr(game, 'update')
        assert hasattr(game, 'draw')
        assert hasattr(game, 'run')
    
    def test_enemy_spawn_timer(self, init_pygame):
        """적 spawn 타이머 테스트"""
        game = Game()
        
        # 타이머 변수 존재 확인
        assert hasattr(game, 'last_spawn_time')
        assert game.last_spawn_time >= 0
    
    def test_multiple_update_cycles(self, init_pygame):
        """여러 업데이트 사이클 테스트"""
        game = Game()
        game.enemies = []
        
        # 여러 번 업데이트 실행
        for _ in range(10):
            game.update()
        
        # 게임이 정상적으로 작동해야 함
        assert game.running is True


class TestGamePerformance:
    """게임 성능 테스트"""
    
    def test_many_enemies(self, init_pygame):
        """많은 적이 있을 때 테스트"""
        game = Game()
        
        # 20개의 적 spawn
        for _ in range(20):
            game.spawn_enemy()
        
        assert len(game.enemies) == 20
        
        # 업데이트 실행
        game.update()
        
        # 게임이 정상적으로 작동해야 함
        assert game.running is True
