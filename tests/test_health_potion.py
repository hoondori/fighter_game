"""체력 회복 아이템 테스트"""

import pytest
import pygame
from src.health_potion import HealthPotion
from src.player import Player
from src.constants import HEALTH_POTION_HEAL


@pytest.fixture(scope="module")
def init_pygame():
    """pygame 초기화 픽스처"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def potion(init_pygame):
    """기본 체력 회복 아이템 인스턴스 픽스처"""
    return HealthPotion(grid_x=10, grid_y=10)


class TestHealthPotionInitialization:
    """체력 회복 아이템 초기화 테스트"""
    
    def test_potion_creation(self, potion):
        """체력 회복 아이템 생성 테스트"""
        assert potion.grid_x == 10
        assert potion.grid_y == 10
        assert potion.heal_amount == HEALTH_POTION_HEAL
    
    def test_potion_shape(self, potion):
        """체력 회복 아이템 모양 테스트 (H 모양)"""
        assert len(potion.shape) == 7  # H 모양 = 7 블록
    
    def test_potion_color(self, potion):
        """체력 회복 아이템 색상 테스트 (녹색)"""
        assert potion.color is not None
        assert len(potion.color) == 3  # RGB


class TestHealthPotionPickup:
    """체력 회복 아이템 획득 테스트"""
    
    def test_player_heals_on_pickup(self, init_pygame):
        """플레이어가 아이템 획득 시 체력 회복 테스트"""
        player = Player(grid_x=10, grid_y=10)
        potion = HealthPotion(grid_x=10, grid_y=10)
        
        # 플레이어 데미지
        player.take_damage(30)
        assert player.hp == 70
        
        # 아이템으로 회복
        player.heal(potion.heal_amount)
        assert player.hp == 90
    
    def test_collision_detection(self, init_pygame):
        """플레이어와 아이템 충돌 감지 테스트"""
        player = Player(grid_x=10, grid_y=10)
        potion = HealthPotion(grid_x=10, grid_y=10)
        
        # 충돌 확인
        assert player.collides_with(potion)
    
    def test_no_collision_when_far(self, init_pygame):
        """거리가 먼 경우 충돌 없음 테스트"""
        player = Player(grid_x=10, grid_y=10)
        potion = HealthPotion(grid_x=50, grid_y=50)
        
        # 충돌 없음
        assert not player.collides_with(potion)
    
    def test_heal_amount_value(self, potion):
        """회복량 값 테스트"""
        assert potion.heal_amount > 0
        assert potion.heal_amount == 20  # 기본 회복량
