# Version 3 – 본격적인 게임화

## 🎯 목표
"게임다운 구조" 완성 - 맵 확장, 카메라 시스템, 다양한 무기

---

## 🎮 구현할 게임 기능

### 1. 맵 확장
- 맵 크기를 화면보다 크게 설정 (예: 2400x1800)
- 화면 크기는 그대로 유지 (800x600)

### 2. 카메라 시스템
- 주인공을 중심으로 카메라 이동
- 주인공이 화면 중앙에 위치
- 맵 경계에서 카메라 고정 (검은 영역 방지)

### 3. 무기 종류 확장
- **Sword** (기존)
  - 근접 공격
  - 주인공 주변 원형 범위
- **Gun** (신규)
  - 원거리 공격
  - 가장 가까운 적에게 발사
  - 투사체(Projectile) 사용
- **Magic Spell** (신규)
  - 광역 공격
  - 화면 내 모든 적에게 낮은 데미지

### 4. 점수(Score) 시스템
- 적 처치 시 점수 획득 (예: +10)
- 화면 상단에 점수 표시
- 점수는 누적

### 5. 레벨업 시스템
- 점수 기준 레벨업 (예: 100점마다)
- 레벨업 시 화면에 알림
- 현재 레벨 표시

### 6. 무기 해금 시스템
- 시작: Sword만 보유
- 레벨 2: Gun 해금
- 레벨 3: Magic Spell 해금
- 해금된 무기는 자동으로 추가

### 7. 여러 무기 동시 발동
- 모든 해금된 무기가 동시에 작동
- 각 무기는 독립적인 쿨다운 보유
- 무기마다 다른 발동 주기
  - Sword: 1.0초
  - Gun: 0.5초
  - Magic Spell: 3.0초

---

## 🏗️ 구조 설명

### 주요 클래스 (Version 2 기반 확장)

#### 1. `Camera` 클래스 (신규)
```python
class Camera:
    def __init__(self, screen_width, screen_height, map_width, map_height)
    def update(self, target_pos)  # 타겟(플레이어) 추적
    def apply(self, entity_rect)  # 엔티티 좌표를 화면 좌표로 변환
    def apply_pos(self, pos)  # 위치를 화면 좌표로 변환
```

#### 2. `Projectile` 클래스 (신규)
```python
class Projectile:
    def __init__(self, x, y, target_x, target_y, speed, damage)
    def update(self)  # 이동
    def draw(self, screen, camera)
    def get_rect(self)
    def has_reached_target(self)
```

#### 3. `Gun` 클래스 (신규, Weapon 상속)
```python
class Gun(Weapon):
    def __init__(self)
    def attack(self, player_pos, enemies)
        # 가장 가까운 적 찾기
        # Projectile 생성
    def update_projectiles(self)
    def draw_projectiles(self, screen, camera)
```

#### 4. `MagicSpell` 클래스 (신규, Weapon 상속)
```python
class MagicSpell(Weapon):
    def __init__(self)
    def attack(self, player_pos, enemies)
        # 화면 내 모든 적에게 데미지
    def draw_attack_effect(self, screen, camera, player_pos)
```

#### 5. `WeaponManager` 클래스 (신규)
```python
class WeaponManager:
    def __init__(self)
    def add_weapon(self, weapon)  # 무기 추가
    def update(self, dt, player_pos, enemies)  # 모든 무기 업데이트
    def draw(self, screen, camera, player_pos)  # 무기 이펙트 그리기
    def get_unlocked_weapons(self)
```

#### 6. `ScoreManager` 클래스 (신규)
```python
class ScoreManager:
    def __init__(self)
    def add_score(self, points)
    def get_score(self)
    def get_level(self)
    def check_level_up(self)  # 레벨업 조건 확인
```

#### 7. `Game` 클래스 확장
```python
class Game:
    def __init__(self)
    def init_camera(self)
    def init_weapons(self)
    def init_score(self)
    def handle_level_up(self)  # 레벨업 시 무기 해금
    def update(self)
    def draw(self)
    def draw_ui(self)  # HP, Score, Level 표시
    def run(self)
```

### 게임 루프 흐름 (확장)
```
초기화
├─ 맵 크기 설정 (2400x1800)
├─ 카메라 초기화
├─ WeaponManager 초기화 (Sword 추가)
└─ ScoreManager 초기화
│
└─> [게임 루프 시작]
    │
    ├─> 이벤트 처리
    │
    ├─> 업데이트
    │   ├─ 플레이어 이동
    │   ├─ 카메라 업데이트 (플레이어 추적)
    │   ├─ 적 생성 (맵 전체 영역)
    │   ├─ 적 이동
    │   ├─ 체력 아이템 생성 (맵 전체 영역)
    │   ├─ WeaponManager 업데이트
    │   │   ├─ 각 무기 쿨다운 체크
    │   │   ├─ 자동 공격 실행
    │   │   └─ Projectile 이동
    │   ├─ 충돌 판정
    │   │   ├─ 플레이어 ↔ 적
    │   │   ├─ 플레이어 ↔ 체력 아이템
    │   │   ├─ 무기 ↔ 적
    │   │   └─ Projectile ↔ 적
    │   ├─ 적 처치 시 점수 추가
    │   ├─ 레벨업 체크
    │   └─ 레벨업 시 무기 해금
    │
    ├─> 렌더링 (카메라 기준)
    │   ├─ 배경
    │   ├─ 장애물
    │   ├─ 체력 아이템
    │   ├─ 적들
    │   ├─ 플레이어
    │   ├─ 무기 이펙트
    │   ├─ Projectile들
    │   └─ UI (HP, Score, Level)
    │
    └─> FPS 제어
```

---

## 🧪 테스트 항목

### 필수 테스트
- [ ] 맵이 화면보다 큰가
- [ ] 카메라가 플레이어를 정확히 추적하는가
- [ ] 카메라 이동 시 화면 떨림이 없는가
- [ ] 맵 경계에서 카메라가 적절히 멈추는가
- [ ] Gun이 정상 작동하는가
- [ ] Projectile이 올바르게 이동하는가
- [ ] Magic Spell이 화면 내 모든 적에게 데미지를 주는가
- [ ] 점수가 적 처치 시 올바르게 증가하는가
- [ ] 레벨업이 정확한 점수에서 발생하는가
- [ ] 레벨업 시 무기가 올바르게 해금되는가
- [ ] 여러 무기가 동시에 발동되는가
- [ ] 각 무기의 쿨다운이 독립적으로 작동하는가

### 추가 확인 사항
- [ ] 적이 화면 밖에서도 정상 이동하는가
- [ ] 카메라 밖의 객체가 불필요하게 렌더링되지 않는가 (최적화)
- [ ] Projectile이 맵 밖으로 나가면 제거되는가
- [ ] 무기 3개 동시 발동 시 성능 저하 없는가
- [ ] UI가 카메라 이동에 영향받지 않는가 (고정 위치)

---

## ✅ 다음 버전으로 넘어가기 전 안정화 포인트

### 1. 카메라 시스템 검증
- [ ] 카메라 이동이 부드러운가
- [ ] 경계 처리가 완벽한가
- [ ] 모든 엔티티가 카메라 좌표계를 올바르게 사용하는가

### 2. 무기 시스템 검증
- [ ] 3가지 무기가 모두 안정적으로 작동하는가
- [ ] 무기 간 밸런스가 적절한가
- [ ] Projectile 생성/제거가 메모리 누수 없이 작동하는가

### 3. 레벨업 시스템 검증
- [ ] 레벨업 곡선이 적절한가 (너무 빠르거나 느리지 않은가)
- [ ] 무기 해금 타이밍이 게임 플레이에 적절한가

### 4. 밸런스 조정
- [ ] Sword vs Gun vs Magic Spell 밸런스
- [ ] 적 처치 점수가 적절한가
- [ ] 레벨업 필요 점수가 적절한가

### 5. 성능 최적화
- [ ] 큰 맵에서도 60 FPS 유지
- [ ] 적 50마리 + Projectile 20개 상태에서 원활한가
- [ ] 화면 밖 객체 렌더링 최적화 구현

### 6. 코드 리팩토링
- [ ] Camera 좌표 변환이 일관되게 적용되었는가
- [ ] WeaponManager로 무기 관리가 깔끔한가
- [ ] 클래스 책임이 명확하게 분리되었는가

---

## 📝 구현 팁

### 1. 카메라 좌표 변환
```python
class Camera:
    def update(self, target_pos):
        # 플레이어를 화면 중앙에
        self.x = target_pos[0] - SCREEN_WIDTH // 2
        self.y = target_pos[1] - SCREEN_HEIGHT // 2
        
        # 맵 경계 제한
        self.x = max(0, min(self.x, MAP_WIDTH - SCREEN_WIDTH))
        self.y = max(0, min(self.y, MAP_HEIGHT - SCREEN_HEIGHT))
    
    def apply(self, entity_rect):
        return pygame.Rect(
            entity_rect.x - self.x,
            entity_rect.y - self.y,
            entity_rect.width,
            entity_rect.height
        )
```

### 2. Projectile 이동
```python
class Projectile:
    def __init__(self, x, y, target_x, target_y, speed, damage):
        # 방향 벡터 계산
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        self.vx = (dx / distance) * speed
        self.vy = (dy / distance) * speed
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
```

### 3. WeaponManager
```python
class WeaponManager:
    def update(self, dt, player_pos, enemies):
        for weapon in self.weapons:
            weapon.update(dt)
            if weapon.can_attack():
                weapon.attack(player_pos, enemies)
```

### 4. 레벨업 체크
```python
class ScoreManager:
    def check_level_up(self):
        new_level = self.score // 100 + 1
        if new_level > self.level:
            self.level = new_level
            return True
        return False
```

### 5. 화면 밖 렌더링 최적화
```python
def draw(self, screen, camera):
    screen_rect = pygame.Rect(camera.x, camera.y, SCREEN_WIDTH, SCREEN_HEIGHT)
    if self.get_rect().colliderect(screen_rect):
        # 화면 안에 있을 때만 그리기
        self.do_draw(screen, camera)
```

---

## 🎯 이 버전의 성공 기준

- 넓은 맵을 탐험하는 느낌
- 카메라가 자연스럽고 안정적
- 3가지 무기가 동시에 발동되며 전투가 역동적
- 레벨업 시스템이 진행감과 성장감을 제공
- 3~5분 정도 플레이 가능한 콘텐츠
- 무기 해금으로 인한 흥미 유지

**다음 버전(Version 4)에서는 적 다양화와 난이도 시스템을 추가합니다.**
