"""무기 클래스"""

import pygame
import math
from src.constants import SWORD_DAMAGE, SWORD_COOLDOWN, SWORD_RANGE, SWORD_EFFECT_COLOR, GRID_WIDTH, GRID_HEIGHT


class Weapon:
    """무기 기본 클래스"""
    
    def __init__(self, damage, cooldown):
        """
        무기 초기화
        
        Args:
            damage: 공격력
            cooldown: 쿨다운 (초)
        """
        self.damage = damage
        self.cooldown = cooldown
        self.timer = 0
    
    def update(self, dt):
        """
        쿨다운 업데이트
        
        Args:
            dt: delta time (초)
        """
        self.timer += dt
    
    def can_attack(self):
        """
        공격 가능 여부 확인
        
        Returns:
            bool: 공격 가능하면 True
        """
        if self.timer >= self.cooldown:
            self.timer = 0
            return True
        return False
    
    def attack(self, player_pos, enemies):
        """
        공격 실행 (오버라이드 필요)
        
        Args:
            player_pos: 플레이어 중심 좌표 (그리드)
            enemies: 적 리스트
        
        Returns:
            list: 공격 당한 적들의 리스트
        """
        return []
    
    def draw_attack_effect(self, screen, player_pos):
        """
        공격 이펙트 그리기 (오버라이드 필요)
        
        Args:
            screen: pygame screen 객체
            player_pos: 플레이어 중심 좌표 (그리드)
        """
        pass


class Sword(Weapon):
    """검 - 원형 범위 공격"""
    
    def __init__(self):
        """검 초기화"""
        super().__init__(SWORD_DAMAGE, SWORD_COOLDOWN)
        self.range = SWORD_RANGE
        self.attack_active = False
        self.attack_timer = 0
        self.attack_duration = 0.2  # 이펙트 표시 시간 (초)
    
    def attack(self, player_pos, enemies):
        """
        원형 범위 내 적들에게 데미지
        
        Args:
            player_pos: 플레이어 중심 좌표 (그리드)
            enemies: 적 리스트
        
        Returns:
            list: 공격 당한 적들의 리스트
        """
        hit_enemies = []
        player_x, player_y = player_pos
        
        for enemy in enemies:
            enemy_center_x, enemy_center_y = enemy.get_center()
            
            # 거리 계산 (그리드 단위)
            distance = math.sqrt(
                (enemy_center_x - player_x)**2 + 
                (enemy_center_y - player_y)**2
            )
            
            # 범위 내면 데미지
            if distance <= self.range:
                enemy.take_damage(self.damage)
                hit_enemies.append(enemy)
        
        # 공격 이펙트 활성화
        self.attack_active = True
        self.attack_timer = 0
        
        return hit_enemies
    
    def update(self, dt):
        """
        쿨다운 및 이펙트 업데이트
        
        Args:
            dt: delta time (초)
        """
        super().update(dt)
        
        if self.attack_active:
            self.attack_timer += dt
            if self.attack_timer >= self.attack_duration:
                self.attack_active = False
    
    def draw_attack_effect(self, screen, player_pos):
        """
        원형 공격 범위 이펙트 그리기
        
        Args:
            screen: pygame screen 객체
            player_pos: 플레이어 중심 좌표 (그리드)
        """
        if self.attack_active:
            player_x, player_y = player_pos
            
            # 그리드 좌표를 픽셀 좌표로 변환
            pixel_x = int(player_x * GRID_WIDTH)
            pixel_y = int(player_y * GRID_HEIGHT)
            pixel_range = int(self.range * GRID_WIDTH)
            
            # 반투명 원 그리기
            alpha = int(255 * (1 - self.attack_timer / self.attack_duration))
            if alpha > 0:
                # 투명도를 위한 서페이스 생성
                s = pygame.Surface((pixel_range * 2, pixel_range * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*SWORD_EFFECT_COLOR, alpha // 2), 
                                 (pixel_range, pixel_range), pixel_range)
                screen.blit(s, (pixel_x - pixel_range, pixel_y - pixel_range))
                
                # 테두리
                pygame.draw.circle(screen, SWORD_EFFECT_COLOR, 
                                 (pixel_x, pixel_y), pixel_range, 2)
