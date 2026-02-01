"""게임 메인 로직"""

import pygame
import random
import sys
from src.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    BLACK, WHITE, GAME_TITLE, ENEMY_SPAWN_INTERVAL
)
from src.player import Player
from src.enemy import Enemy


class Game:
    """게임 메인 클래스"""
    
    def __init__(self):
        """게임 초기화"""
        # Pygame 초기화
        pygame.init()
        
        # 화면 설정
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        
        # 시계 설정 (FPS 제어)
        self.clock = pygame.time.Clock()
        
        # 플레이어 생성 (화면 중앙)
        self.player = Player(
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2
        )
        
        # 적 리스트
        self.enemies = []
        
        # 게임 상태
        self.running = True
        self.game_over = False
        
        # 적 spawn 타이머
        self.last_spawn_time = pygame.time.get_ticks()
        
        # 폰트 설정 (게임 오버 메시지용)
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
    
    def spawn_enemy(self):
        """화면 경계에서 적을 spawn"""
        # 랜덤으로 spawn 위치 선택 (0: 왼쪽, 1: 오른쪽, 2: 위, 3: 아래)
        side = random.randint(0, 3)
        
        if side == 0:  # 왼쪽
            x = 0
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 1:  # 오른쪽
            x = SCREEN_WIDTH
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # 위
            x = random.randint(0, SCREEN_WIDTH)
            y = 0
        else:  # 아래
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT
        
        enemy = Enemy(x, y)
        self.enemies.append(enemy)
    
    def check_collision(self):
        """플레이어와 적의 충돌 판정"""
        player_rect = self.player.get_rect()
        
        for enemy in self.enemies:
            if player_rect.colliderect(enemy.get_rect()):
                self.game_over = True
                return True
        
        return False
    
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
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
        
        # 키 입력 처리
        keys = pygame.key.get_pressed()
        
        # ESC 키로 게임 종료
        if keys[pygame.K_ESCAPE]:
            self.running = False
        
        # 플레이어 이동
        self.player.move(keys)
        
        # 적 spawn (일정 시간마다)
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > ENEMY_SPAWN_INTERVAL:
            self.spawn_enemy()
            self.last_spawn_time = current_time
        
        # 적 이동
        for enemy in self.enemies:
            enemy.move_towards_player(self.player)
        
        # 충돌 판정
        self.check_collision()
    
    def draw(self):
        """화면 렌더링"""
        # 화면 클리어 (검은색 배경)
        self.screen.fill(BLACK)
        
        # 플레이어 그리기
        self.player.draw(self.screen)
        
        # 적들 그리기
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
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
