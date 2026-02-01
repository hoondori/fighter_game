# Version 5 – 완성도 향상

## 🎯 목표
플레이 경험(UX) 개선 - 사운드, UI, 애니메이션, 피드백

---

## 🎮 구현할 게임 기능

### 1. 사운드 효과 시스템
- **공격 사운드**
  - Sword 휘두르는 소리
  - Gun 발사 소리
  - Magic Spell 시전 소리
- **피격 사운드**
  - 적이 데미지를 받는 소리
  - 플레이어가 데미지를 받는 소리
- **효과 사운드**
  - 적 제거 시 소리
  - 체력 회복 소리
  - 레벨업 소리
- **사운드 볼륨 조절** (선택 사항)

### 2. UI 개선
- **체력바 개선**
  - 그라데이션 색상 (녹색 → 노란색 → 빨간색)
  - 테두리 추가
- **무기 상태 표시**
  - 현재 보유 무기 아이콘
  - 각 무기의 쿨다운 표시 (원형 게이지)
- **점수 및 레벨 표시 개선**
  - 폰트 크기 및 스타일 개선
  - 레벨업 진행도 바
- **미니맵** (선택 사항)
  - 맵의 축소판
  - 플레이어 위치
  - 적 위치 (근처만)

### 3. 간단한 애니메이션
- **플레이어 애니메이션**
  - 이동 시 스프라이트 변경 (또는 회전)
- **적 애니메이션**
  - 이동 시 애니메이션
  - 피격 시 깜빡임
  - 제거 시 페이드아웃
- **무기 이펙트 애니메이션**
  - Sword 회전 효과
  - Gun 발사 플래시
  - Magic Spell 확산 효과
- **아이템 애니메이션**
  - 체력 회복 아이템 반짝임

### 4. 게임 오버 화면
- **Game Over 표시**
  - 큰 텍스트
  - 최종 점수
  - 생존 시간
  - 도달 레벨
- **재시작 버튼**
  - 'R' 키 또는 버튼 클릭으로 재시작
- **메인 메뉴로 돌아가기** (선택 사항)

### 5. 시작 화면 (선택 사항)
- **타이틀 화면**
  - 게임 제목
  - "Press SPACE to Start"
  - 간단한 조작 설명
- **설정 화면** (선택 사항)
  - 사운드 볼륨 조절
  - 난이도 선택

### 6. 시각적 피드백
- **데미지 표시**
  - 적이 데미지를 받을 때 숫자 표시
- **레벨업 알림**
  - 화면 중앙에 "Level Up!" 표시
  - 해금된 무기 표시
- **경고 표시**
  - 체력이 낮을 때 화면 가장자리 빨간색 테두리

---

## 🏗️ 구조 설명

### 주요 클래스 (Version 4 기반 확장)

#### 1. `SoundManager` 클래스 (신규)
```python
class SoundManager:
    def __init__(self)
    def load_sounds(self)
    def play_sound(self, sound_name)
    def set_volume(self, volume)
    def stop_all(self)
```

#### 2. `UIManager` 클래스 (신규)
```python
class UIManager:
    def __init__(self, screen_width, screen_height)
    def draw_health_bar(self, screen, hp, max_hp)
    def draw_weapon_cooldowns(self, screen, weapons)
    def draw_score_and_level(self, screen, score, level)
    def draw_survival_time(self, screen, time)
    def draw_level_progress(self, screen, score, next_level_score)
    def draw_minimap(self, screen, player, enemies, map_size)  # 선택
```

#### 3. `Animation` 클래스 (신규)
```python
class Animation:
    def __init__(self, frames, frame_duration)
    def update(self, dt)
    def get_current_frame(self)
    def reset(self)
```

#### 4. `Particle` 클래스 (신규)
```python
class Particle:
    def __init__(self, x, y, color, lifetime)
    def update(self, dt)
    def draw(self, screen, camera)
    def is_alive(self)
```

#### 5. `ParticleSystem` 클래스 (신규)
```python
class ParticleSystem:
    def __init__(self)
    def emit(self, x, y, particle_type)
    def update(self, dt)
    def draw(self, screen, camera)
```

#### 6. `DamageNumber` 클래스 (신규)
```python
class DamageNumber:
    def __init__(self, x, y, damage_value)
    def update(self, dt)
    def draw(self, screen, camera)
    def is_finished(self)
```

#### 7. `GameState` 클래스 (신규)
```python
class GameState:
    # MENU, PLAYING, GAME_OVER
    def __init__(self)
    def set_state(self, state)
    def get_state(self)
```

#### 8. `Player` 클래스 확장
```python
class Player:
    def __init__(self, ...)
    def init_animation(self)
    def update(self, ...)
    def draw(self, screen, camera)
        # 애니메이션 적용
    def flash_on_hit(self)  # 피격 시 깜빡임
```

#### 9. `Enemy` 클래스 확장
```python
class Enemy:
    def __init__(self, ...)
    def init_animation(self)
    def take_damage(self, damage)
        # 데미지 숫자 생성
        # 깜빡임 효과
    def die(self)
        # 파티클 효과
        # 사운드 재생
```

#### 10. `Game` 클래스 확장
```python
class Game:
    def __init__(self)
    def init_sound(self)
    def init_ui(self)
    def init_particles(self)
    def show_start_screen(self)  # 선택
    def show_game_over_screen(self)
    def restart_game(self)
    def update(self)
    def draw(self)
    def draw_game_over(self)
    def run(self)
```

### 게임 루프 흐름 (확장)
```
초기화
├─ SoundManager 초기화
├─ UIManager 초기화
├─ ParticleSystem 초기화
└─ GameState 초기화 (MENU)
│
└─> [메인 루프]
    │
    ├─> [MENU 상태]
    │   ├─ 시작 화면 표시
    │   └─ SPACE 입력 대기 → PLAYING으로 전환
    │
    ├─> [PLAYING 상태]
    │   ├─> 이벤트 처리
    │   │
    │   ├─> 업데이트
    │   │   ├─ 모든 게임 로직
    │   │   ├─ 애니메이션 업데이트
    │   │   ├─ 파티클 업데이트
    │   │   ├─ 데미지 숫자 업데이트
    │   │   └─ HP <= 0 → GAME_OVER로 전환
    │   │
    │   ├─> 렌더링
    │   │   ├─ 모든 엔티티 (애니메이션 적용)
    │   │   ├─ 파티클 효과
    │   │   ├─ 데미지 숫자
    │   │   ├─ UI (개선된 디자인)
    │   │   └─ 경고 표시 (체력 낮을 때)
    │   │
    │   └─> 사운드 재생
    │       ├─ 공격 사운드
    │       ├─ 피격 사운드
    │       └─ 효과 사운드
    │
    └─> [GAME_OVER 상태]
        ├─ 게임 오버 화면 표시
        │   ├─ 최종 점수
        │   ├─ 생존 시간
        │   └─ 레벨
        └─ 'R' 키 입력 → 재시작 (PLAYING)
```

---

## 🧪 테스트 항목

### 필수 테스트
- [ ] 모든 사운드가 정상 재생되는가
- [ ] 사운드가 과도하게 겹치지 않는가
- [ ] 체력바 색상이 HP에 따라 변하는가
- [ ] 무기 쿨다운 게이지가 정확한가
- [ ] 레벨 진행도 바가 올바르게 표시되는가
- [ ] 플레이어/적 애니메이션이 부드러운가
- [ ] 피격 시 깜빡임 효과가 보이는가
- [ ] 적 제거 시 파티클 효과가 나타나는가
- [ ] 데미지 숫자가 정확하게 표시되는가
- [ ] 게임 오버 화면이 정상 표시되는가
- [ ] 재시작이 정상 작동하는가
- [ ] 재시작 시 모든 상태가 초기화되는가

### 추가 확인 사항
- [ ] 사운드 볼륨이 적절한가
- [ ] UI가 가독성이 좋은가
- [ ] 애니메이션이 성능에 영향을 주지 않는가
- [ ] 파티클이 너무 많이 생성되지 않는가
- [ ] 시작 화면이 직관적인가 (선택)

---

## ✅ 다음 버전으로 넘어가기 전 안정화 포인트

### 1. 사운드 시스템 검증
- [ ] 모든 사운드 파일이 준비되었는가
- [ ] 사운드가 게임 플레이에 방해되지 않는가
- [ ] 사운드 재생이 성능에 영향을 주지 않는가

### 2. UI/UX 검증
- [ ] UI가 직관적이고 보기 좋은가
- [ ] 모든 정보가 명확하게 전달되는가
- [ ] 색상 대비가 적절한가
- [ ] 폰트 크기가 읽기 좋은가

### 3. 애니메이션 검증
- [ ] 애니메이션이 자연스러운가
- [ ] 프레임 드랍이 없는가
- [ ] 파티클 효과가 과하지 않은가

### 4. 게임 흐름 검증
- [ ] 시작 → 플레이 → 게임오버 → 재시작 흐름이 완벽한가
- [ ] 재시작 시 모든 변수가 초기화되는가
- [ ] 메모리 누수가 없는가

### 5. 플레이 테스트
- [ ] 5명 이상의 테스터 피드백
- [ ] UI 가독성 확인
- [ ] 사운드 볼륨 조정
- [ ] 전반적인 "느낌" 확인

---

## 📝 구현 팁

### 1. 사운드 로드 및 재생
```python
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
    
    def load_sounds(self):
        self.sounds["sword"] = pygame.mixer.Sound("assets/sword.wav")
        self.sounds["gun"] = pygame.mixer.Sound("assets/gun.wav")
        self.sounds["hit"] = pygame.mixer.Sound("assets/hit.wav")
        self.sounds["die"] = pygame.mixer.Sound("assets/die.wav")
        self.sounds["heal"] = pygame.mixer.Sound("assets/heal.wav")
        self.sounds["levelup"] = pygame.mixer.Sound("assets/levelup.wav")
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
```

### 2. 체력바 색상 그라데이션
```python
def draw_health_bar(self, screen, hp, max_hp):
    bar_width = 200
    bar_height = 20
    hp_ratio = hp / max_hp
    
    # 색상 결정
    if hp_ratio > 0.6:
        color = (0, 255, 0)  # 녹색
    elif hp_ratio > 0.3:
        color = (255, 255, 0)  # 노란색
    else:
        color = (255, 0, 0)  # 빨간색
    
    # 배경
    pygame.draw.rect(screen, (50, 50, 50), (10, 10, bar_width, bar_height))
    # 체력
    pygame.draw.rect(screen, color, (10, 10, bar_width * hp_ratio, bar_height))
    # 테두리
    pygame.draw.rect(screen, (255, 255, 255), (10, 10, bar_width, bar_height), 2)
```

### 3. 무기 쿨다운 표시
```python
def draw_weapon_cooldowns(self, screen, weapons):
    x_offset = 10
    for weapon in weapons:
        # 원형 게이지
        center = (x_offset + 20, 50)
        radius = 15
        cooldown_ratio = weapon.timer / weapon.cooldown
        
        # 배경 원
        pygame.draw.circle(screen, (50, 50, 50), center, radius)
        
        # 쿨다운 원호
        if cooldown_ratio < 1:
            end_angle = -90 + (360 * cooldown_ratio)
            # pygame.draw.arc를 사용하여 원호 그리기
        
        # 아이콘 또는 텍스트
        font = pygame.font.Font(None, 20)
        text = font.render(weapon.name[0], True, (255, 255, 255))
        screen.blit(text, (center[0] - 5, center[1] - 8))
        
        x_offset += 50
```

### 4. 간단한 애니메이션
```python
class Animation:
    def __init__(self, frames, frame_duration):
        self.frames = frames  # 프레임 리스트
        self.frame_duration = frame_duration  # 각 프레임 지속 시간
        self.current_frame = 0
        self.timer = 0
    
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def get_current_frame(self):
        return self.frames[self.current_frame]
```

### 5. 피격 깜빡임
```python
class Enemy:
    def take_damage(self, damage):
        self.hp -= damage
        self.flash_timer = 0.2  # 0.2초 동안 깜빡임
    
    def update(self, dt):
        if self.flash_timer > 0:
            self.flash_timer -= dt
    
    def draw(self, screen, camera):
        # 깜빡임 효과
        if self.flash_timer > 0 and int(self.flash_timer * 20) % 2 == 0:
            color = (255, 255, 255)  # 흰색으로 깜빡임
        else:
            color = self.normal_color
        
        rect = camera.apply(self.get_rect())
        pygame.draw.rect(screen, color, rect)
```

### 6. 파티클 효과
```python
class Particle:
    def __init__(self, x, y, color, lifetime):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.color = color
        self.lifetime = lifetime
        self.timer = 0
    
    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.timer += dt
    
    def is_alive(self):
        return self.timer < self.lifetime
    
    def draw(self, screen, camera):
        alpha = 1 - (self.timer / self.lifetime)
        size = int(5 * alpha)
        pos = camera.apply_pos((self.x, self.y))
        pygame.draw.circle(screen, self.color, pos, size)
```

### 7. 데미지 숫자
```python
class DamageNumber:
    def __init__(self, x, y, damage_value):
        self.x = x
        self.y = y
        self.damage = damage_value
        self.timer = 0
        self.duration = 1.0  # 1초 동안 표시
    
    def update(self, dt):
        self.timer += dt
        self.y -= 1  # 위로 올라감
    
    def is_finished(self):
        return self.timer >= self.duration
    
    def draw(self, screen, camera):
        alpha = 1 - (self.timer / self.duration)
        font = pygame.font.Font(None, 24)
        text = font.render(str(self.damage), True, (255, 255, 0))
        pos = camera.apply_pos((self.x, self.y))
        screen.blit(text, pos)
```

### 8. 게임 오버 화면
```python
def draw_game_over(self, screen):
    # 반투명 오버레이
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Game Over 텍스트
    font_large = pygame.font.Font(None, 72)
    text = font_large.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))
    
    # 점수, 시간, 레벨
    font_medium = pygame.font.Font(None, 36)
    score_text = font_medium.render(f"Score: {self.score}", True, (255, 255, 255))
    time_text = font_medium.render(f"Time: {self.survival_time}s", True, (255, 255, 255))
    level_text = font_medium.render(f"Level: {self.level}", True, (255, 255, 255))
    
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))
    screen.blit(time_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 40))
    screen.blit(level_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 80))
    
    # 재시작 안내
    font_small = pygame.font.Font(None, 24)
    restart_text = font_small.render("Press 'R' to Restart", True, (255, 255, 255))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150))
```

---

## 🎯 이 버전의 성공 기준

- 게임이 완성된 느낌
- 사운드와 시각 효과가 게임을 더 재미있게 만듦
- UI가 직관적이고 정보 전달이 명확
- 게임 오버 시 성취감 (점수, 시간, 레벨)
- 재시작이 편리하여 반복 플레이 유도

**다음 버전(Version 6)에서는 자유롭게 게임을 확장합니다.**
