"""게임 메인 로직"""

import pygame
import random
import sys
import math
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    GRID_WIDTH, GRID_HEIGHT, GRID_COLS, GRID_ROWS,
    BLACK, WHITE, GAME_TITLE, ENEMY_SPAWN_INTERVAL,
    ENEMY_SHAPES, ENEMY_COLORS, MAX_ENEMIES,
    HEALTH_POTION_SPAWN_INTERVAL, NUM_OBSTACLES,
    PLAYER_COLLISION_DAMAGE, ENEMY_HP
)
from src.player import Player
from src.enemy import Enemy
from src.obstacle import Obstacle
from src.health_potion import HealthPotion
from src.weapon import Sword


class Game:
    """게임 메인 클래스 (그리드 기반)"""
    
    def __init__(self):
        """게임 초기화"""
        # Pygame 초기화
        pygame.init()
        
        # 화면 설정
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        
        # 시계 설정 (FPS 제어)
        self.clock = pygame.time.Clock()
        
        # 플레이어 생성 (그리드 중앙)
        self.player = Player(
            grid_x=GRID_COLS // 2,
            grid_y=GRID_ROWS // 2
        )
        
        # 적 리스트
        self.enemies = []
        
        # 장애물 리스트
        self.obstacles = []
        self.spawn_obstacles()
        
        # 체력 회복 아이템 리스트
        self.health_potions = []
        
        # 무기 (Sword)
        self.sword = Sword()
        
        # 게임 상태
        self.running = True
        self.game_over = False
        
        # 적 spawn 타이머
        self.last_spawn_time = pygame.time.get_ticks()
        
        # 체력 회복 아이템 spawn 타이머
        self.last_potion_spawn_time = pygame.time.get_ticks()
        
        # 충돌 데미지 쿨다운 (너무 빠른 연속 데미지 방지)
        self.collision_cooldown = 0
        self.collision_cooldown_max = 30  # 프레임 수 (0.5초)
        
        # 폰트 설정 (게임 오버 메시지용)
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        
        # delta time 추적
        self.last_time = pygame.time.get_ticks() / 1000.0
        
        # 체력바 표시 옵션 (H 키로 토글)
        self.show_hp_bars = True
        
        # 배경 음악 로드 및 재생
        self.load_music()
    
    def load_music(self):
        """배경 음악 로드 및 재생"""
        try:
            # 음악 파일이 있으면 로드
            music_path = "assets/bgm.mp3"
            import os
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)  # 무한 반복
                pygame.mixer.music.set_volume(0.5)  # 볼륨 50%
        except Exception as e:
            # 음악 파일이 없어도 게임은 계속 진행
            print(f"배경 음악 로드 실패 (선택 사항): {e}")
    
    def spawn_obstacles(self):
        """맵에 장애물 생성 (플레이어 주변은 피함)"""
        MIN_OBSTACLE_DISTANCE = 5  # 장애물 간 최소 거리
        MAX_ATTEMPTS = 100  # 배치 시도 횟수 제한
        
        for _ in range(NUM_OBSTACLES):
            # 장애물을 벽처럼 만들기 (width 또는 height 중 하나를 길게)
            if random.random() < 0.5:
                # 가로로 긴 벽
                width = random.randint(5, 15)
                height = random.randint(1, 3)
            else:
                # 세로로 긴 벽
                width = random.randint(1, 3)
                height = random.randint(5, 15)
            
            # 랜덤 위치 (플레이어와 다른 장애물들과 일정 거리 유지)
            for attempt in range(MAX_ATTEMPTS):
                grid_x = random.randint(5, GRID_COLS - width - 5)
                grid_y = random.randint(5, GRID_ROWS - height - 5)
                
                # 플레이어 중심에서 일정 거리 이상 떨어져 있는지 확인
                player_center_x = GRID_COLS // 2
                player_center_y = GRID_ROWS // 2
                distance_to_player = math.sqrt((grid_x - player_center_x)**2 + (grid_y - player_center_y)**2)
                
                if distance_to_player <= 10:  # 플레이어와 너무 가까움
                    continue
                
                # 다른 장애물들과의 거리 확인
                too_close = False
                for existing_obstacle in self.obstacles:
                    # 각 장애물의 중심 계산
                    existing_center_x = existing_obstacle.grid_x + existing_obstacle.width / 2
                    existing_center_y = existing_obstacle.grid_y + existing_obstacle.height / 2
                    new_center_x = grid_x + width / 2
                    new_center_y = grid_y + height / 2
                    
                    # 중심 간 거리 계산
                    distance = math.sqrt((new_center_x - existing_center_x)**2 + 
                                       (new_center_y - existing_center_y)**2)
                    
                    if distance < MIN_OBSTACLE_DISTANCE:
                        too_close = True
                        break
                
                if not too_close:
                    # 적절한 위치 찾음
                    obstacle = Obstacle(grid_x, grid_y, width, height)
                    self.obstacles.append(obstacle)
                    break
    
    def spawn_enemy(self):
        """화면 경계에서 적을 spawn (그리드 좌표, 다양한 모양)"""
        # 최대 개수 제한
        if len(self.enemies) >= MAX_ENEMIES:
            return
        
        # 랜덤으로 모양 선택 (위치 조정을 위해 먼저 선택)
        shape_index = random.randint(0, len(ENEMY_SHAPES) - 1)
        shape = ENEMY_SHAPES[shape_index]
        color = ENEMY_COLORS[shape_index]
        
        # 모양의 경계 상자 계산
        if shape:
            xs = [dx for dx, dy in shape]
            ys = [dy for dx, dy in shape]
            shape_min_x, shape_max_x = min(xs), max(xs)
            shape_min_y, shape_max_y = min(ys), max(ys)
        else:
            shape_min_x = shape_max_x = shape_min_y = shape_max_y = 0
        
        # 랜덤으로 spawn 위치 선택 (0: 왼쪽, 1: 오른쪽, 2: 위, 3: 아래)
        side = random.randint(0, 3)
        
        if side == 0:  # 왼쪽
            grid_x = -shape_min_x  # 모양의 왼쪽 끝이 화면 왼쪽에 오도록
            grid_y = random.randint(-shape_min_y, GRID_ROWS - 1 - shape_max_y)
        elif side == 1:  # 오른쪽
            grid_x = GRID_COLS - 1 - shape_max_x  # 모양의 오른쪽 끝이 화면 오른쪽에 오도록
            grid_y = random.randint(-shape_min_y, GRID_ROWS - 1 - shape_max_y)
        elif side == 2:  # 위
            grid_x = random.randint(-shape_min_x, GRID_COLS - 1 - shape_max_x)
            grid_y = -shape_min_y  # 모양의 위쪽 끝이 화면 위에 오도록
        else:  # 아래
            grid_x = random.randint(-shape_min_x, GRID_COLS - 1 - shape_max_x)
            grid_y = GRID_ROWS - 1 - shape_max_y  # 모양의 아래쪽 끝이 화면 아래에 오도록
        
        enemy = Enemy(grid_x, grid_y, color, shape, hp=ENEMY_HP)
        self.enemies.append(enemy)
    
    def spawn_health_potion(self):
        """체력 회복 아이템 생성 (장애물과 겹치지 않게)"""
        max_attempts = 10
        for _ in range(max_attempts):
            grid_x = random.randint(5, GRID_COLS - 8)
            grid_y = random.randint(5, GRID_ROWS - 8)
            
            # 임시 포션 생성
            temp_potion = HealthPotion(grid_x, grid_y)
            
            # 장애물과 겹치는지 확인
            collides = False
            for obstacle in self.obstacles:
                if temp_potion.collides_with(obstacle):
                    collides = True
                    break
            
            if not collides:
                self.health_potions.append(temp_potion)
                break
    
    def check_collision(self):
        """플레이어와 적의 충돌 판정 (그리드 기반 정밀 충돌)"""
        # 쿨다운 감소
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1
            return False
        
        # 그리드 기반 정밀 충돌 판정 사용
        for enemy in self.enemies:
            if self.player.collides_with(enemy):
                # 데미지 받음
                if not self.player.take_damage(PLAYER_COLLISION_DAMAGE):
                    self.game_over = True
                
                # 쿨다운 설정
                self.collision_cooldown = self.collision_cooldown_max
                return True
        
        return False
    
    def check_health_potion_pickup(self):
        """체력 회복 아이템 획득 체크"""
        for potion in self.health_potions[:]:
            if self.player.collides_with(potion):
                self.player.heal(potion.heal_amount)
                self.health_potions.remove(potion)
    
    def check_weapon_hit(self):
        """무기 공격 판정 및 죽은 적 제거"""
        # 죽은 적 제거
        self.enemies = [enemy for enemy in self.enemies if not enemy.is_dead()]
    
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # 키 입력 처리
            if event.type == pygame.KEYDOWN:
                # H 키로 체력바 표시 토글
                if event.key == pygame.K_h:
                    self.show_hp_bars = not self.show_hp_bars
            
            # 게임 오버 상태에서 재시작 또는 종료
            if self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()  # 게임 재시작
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.running = False
    
    def update(self):
        """게임 상태 업데이트"""
        if self.game_over:
            return
        
        # Delta time 계산
        current_time = pygame.time.get_ticks() / 1000.0
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # 키 입력 처리
        keys = pygame.key.get_pressed()
        
        # ESC 키로 게임 종료
        if keys[pygame.K_ESCAPE]:
            self.running = False
        
        # 플레이어 이동 (장애물 포함)
        self.player.move(keys, self.obstacles)
        
        # 적 spawn (일정 시간마다)
        current_time_ms = pygame.time.get_ticks()
        if current_time_ms - self.last_spawn_time > ENEMY_SPAWN_INTERVAL:
            self.spawn_enemy()
            self.last_spawn_time = current_time_ms
        
        # 체력 회복 아이템 spawn (일정 시간마다)
        if current_time_ms - self.last_potion_spawn_time > HEALTH_POTION_SPAWN_INTERVAL:
            self.spawn_health_potion()
            self.last_potion_spawn_time = current_time_ms
        
        # 무기 업데이트
        self.sword.update(dt)
        
        # 무기 자동 발동
        if self.sword.can_attack():
            player_center = self.player.get_center()
            self.sword.attack(player_center, self.enemies)
        
        # 적 이동: 모든 적들과 충돌 체크 (거리 기반 최적화는 유지)
        # 먼 적부터 이동하여 앞쪽 적들이 먼저 자리 잡도록 함
        if self.enemies:
            # 플레이어 중심 계산
            player_center_x, player_center_y = self.player.get_center()
            
            # 플레이어로부터의 거리 기준으로 정렬 (먼 적부터)
            sorted_enemies = sorted(
                self.enemies,
                key=lambda e: (e.grid_x - player_center_x)**2 + (e.grid_y - player_center_y)**2,
                reverse=True
            )
            
            # 각 적은 모든 다른 적들 및 장애물과 충돌 체크
            for enemy in sorted_enemies:
                enemy.move_towards_player(self.player, self.enemies, self.obstacles)
        
        # 충돌 판정
        self.check_collision()
        
        # 체력 회복 아이템 획득
        self.check_health_potion_pickup()
        
        # 무기 공격으로 죽은 적 제거
        self.check_weapon_hit()
    
    def draw(self):
        """화면 렌더링"""
        # 화면 클리어 (검은색 배경)
        self.screen.fill(BLACK)
        
        # 장애물 그리기
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # 체력 회복 아이템 그리기
        for potion in self.health_potions:
            potion.draw(self.screen)
        
        # 적들 그리기
        for enemy in self.enemies:
            if self.show_hp_bars:
                enemy.draw_with_hp_bar(self.screen)
            else:
                enemy.draw(self.screen)
        
        # 플레이어 그리기
        if self.show_hp_bars:
            self.player.draw_with_hp_bar(self.screen)
        else:
            self.player.draw(self.screen)
        
        # 무기 공격 이펙트 그리기
        player_center = self.player.get_center()
        self.sword.draw_attack_effect(self.screen, player_center)
        
        # 체력바 그리기 (화면 상단)
        self.player.draw_hp_bar(self.screen)
        
        # 체력바 토글 힌트 표시
        hp_hint_text = self.small_font.render("Press H to toggle HP bars", True, WHITE)
        self.screen.blit(hp_hint_text, (SCREEN_WIDTH - 300, 10))
        
        # 적 개수 표시
        enemy_count_text = self.small_font.render(f"Enemies: {len(self.enemies)}", True, WHITE)
        self.screen.blit(enemy_count_text, (10, 10))
        
        # 게임 오버 메시지
        if self.game_over:
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            restart_text = self.small_font.render("Press R to Restart or ESC to Quit", True, WHITE)
            
            # 화면 중앙에 텍스트 배치
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
        
        # 화면 업데이트
        pygame.display.flip()
    
    def run(self):
        """메인 게임 루프"""
        while self.running:
            # 이벤트 처리
            self.handle_events()
            
            # 게임 상태 업데이트
            self.update()
            
            # 화면 렌더링
            self.draw()
            
            # FPS 제어 (60 FPS)
            self.clock.tick(FPS)
        
        # 게임 종료
        pygame.quit()
        sys.exit()
