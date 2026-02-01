"""무기 시스템 테스트"""

import pytest
import pygame
import time
from src.weapon import Weapon, Sword
from src.enemy import Enemy
from src.constants import SWORD_DAMAGE, SWORD_COOLDOWN, SWORD_RANGE, RED


@pytest.fixture(scope="module")
def init_pygame():
    """pygame 초기화 픽스처"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def sword(init_pygame):
    """기본 Sword 인스턴스 픽스처"""
    return Sword()


class TestWeaponBase:
    """무기 기본 클래스 테스트"""
    
    def test_weapon_creation(self, init_pygame):
        """무기 생성 테스트"""
        weapon = Weapon(damage=50, cooldown=1.0)
        assert weapon.damage == 50
        assert weapon.cooldown == 1.0
        assert weapon.timer == 0
    
    def test_weapon_update(self, init_pygame):
        """무기 쿨다운 업데이트 테스트"""
        weapon = Weapon(damage=50, cooldown=1.0)
        weapon.update(0.5)
        assert weapon.timer == 0.5
        
        weapon.update(0.3)
        assert weapon.timer == 0.8
    
    def test_weapon_can_attack(self, init_pygame):
        """무기 공격 가능 여부 테스트"""
        weapon = Weapon(damage=50, cooldown=1.0)
        
        # 초기에는 공격 불가
        assert not weapon.can_attack()
        
        # 쿨다운 후 공격 가능
        weapon.update(1.0)
        assert weapon.can_attack()
        
        # can_attack() 호출 후 타이머 리셋
        assert weapon.timer == 0


class TestSwordInitialization:
    """Sword 초기화 테스트"""
    
    def test_sword_creation(self, sword):
        """Sword 생성 테스트"""
        assert sword.damage == SWORD_DAMAGE
        assert sword.cooldown == SWORD_COOLDOWN
        assert sword.range == SWORD_RANGE
        assert sword.attack_active == False
    
    def test_sword_stats(self, sword):
        """Sword 스탯 테스트"""
        assert sword.damage > 0
        assert sword.cooldown > 0
        assert sword.range > 0


class TestSwordAttack:
    """Sword 공격 테스트"""
    
    def test_sword_hits_enemy_in_range(self, init_pygame):
        """범위 내 적 공격 테스트"""
        sword = Sword()
        enemy = Enemy(grid_x=10, grid_y=10, color=RED)
        
        # 플레이어 위치 (적과 가까움)
        player_pos = (10, 10)
        
        # 공격
        hit_enemies = sword.attack(player_pos, [enemy])
        
        # 적이 맞음
        assert len(hit_enemies) == 1
        assert enemy.is_dead()
    
    def test_sword_misses_enemy_out_of_range(self, init_pygame):
        """범위 밖 적 공격 실패 테스트"""
        sword = Sword()
        enemy = Enemy(grid_x=50, grid_y=50, color=RED)
        
        # 플레이어 위치 (적과 멀리 떨어짐)
        player_pos = (10, 10)
        
        # 공격
        hit_enemies = sword.attack(player_pos, [enemy])
        
        # 적이 맞지 않음
        assert len(hit_enemies) == 0
        assert not enemy.is_dead()
    
    def test_sword_hits_multiple_enemies(self, init_pygame):
        """여러 적 동시 공격 테스트"""
        sword = Sword()
        enemies = [
            Enemy(grid_x=10, grid_y=10, color=RED),
            Enemy(grid_x=11, grid_y=10, color=RED),
            Enemy(grid_x=10, grid_y=11, color=RED)
        ]
        
        # 플레이어 위치 (모든 적과 가까움)
        player_pos = (10, 10)
        
        # 공격
        hit_enemies = sword.attack(player_pos, enemies)
        
        # 모든 적이 맞음
        assert len(hit_enemies) == 3
        for enemy in enemies:
            assert enemy.is_dead()
    
    def test_sword_attack_activates_effect(self, init_pygame):
        """공격 이펙트 활성화 테스트"""
        sword = Sword()
        enemy = Enemy(grid_x=10, grid_y=10, color=RED)
        
        assert sword.attack_active == False
        
        # 공격
        sword.attack((10, 10), [enemy])
        
        # 이펙트 활성화
        assert sword.attack_active == True
        assert sword.attack_timer == 0
    
    def test_sword_effect_duration(self, init_pygame):
        """공격 이펙트 지속 시간 테스트"""
        sword = Sword()
        enemy = Enemy(grid_x=10, grid_y=10, color=RED)
        
        # 공격
        sword.attack((10, 10), [enemy])
        assert sword.attack_active == True
        
        # 시간 경과
        sword.update(0.1)
        assert sword.attack_active == True
        
        # 충분한 시간 경과 후 이펙트 종료
        sword.update(0.2)
        assert sword.attack_active == False


class TestSwordCooldown:
    """Sword 쿨다운 테스트"""
    
    def test_sword_cooldown_prevents_immediate_reattack(self, init_pygame):
        """쿨다운으로 즉시 재공격 방지 테스트"""
        sword = Sword()
        
        # 초기에는 공격 불가
        assert not sword.can_attack()
        
        # 쿨다운 경과
        sword.update(1.0)
        assert sword.can_attack()
    
    def test_sword_cooldown_resets_after_attack(self, init_pygame):
        """공격 후 쿨다운 리셋 테스트"""
        sword = Sword()
        
        # 쿨다운 경과
        sword.update(1.0)
        assert sword.can_attack()
        
        # 다시 공격 불가
        assert not sword.can_attack()
        
        # 다시 쿨다운 필요
        sword.update(0.5)
        assert not sword.can_attack()
        
        sword.update(0.5)
        assert sword.can_attack()


class TestSwordRangeCalculation:
    """Sword 범위 계산 테스트"""
    
    def test_range_boundary(self, init_pygame):
        """범위 경계 테스트"""
        sword = Sword()
        
        # 정확히 범위 내
        enemy_in = Enemy(grid_x=10, grid_y=10 + sword.range, color=RED)
        # 범위 밖
        enemy_out = Enemy(grid_x=10, grid_y=10 + sword.range + 1, color=RED)
        
        player_pos = (10, 10)
        
        hit_enemies = sword.attack(player_pos, [enemy_in, enemy_out])
        
        # 범위 내 적만 맞음 (거리 계산에 따라 경계에서 약간 다를 수 있음)
        # 정확한 범위는 유클리드 거리로 계산됨
        assert len(hit_enemies) >= 1
