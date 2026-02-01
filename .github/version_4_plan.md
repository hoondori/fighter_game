# Version 4 – 난이도와 다양성

## 🎯 목표
지루하지 않은 난이도 곡선 설계 및 적 다양화

---

## 🎮 구현할 게임 기능

### 1. 적 종류 다양화
- **기본 적 (Basic Enemy)**
  - 현재 적을 리네이밍
  - 보통 속도, 보통 체력
- **빠른 적 (Fast Enemy)**
  - 높은 속도, 낮은 체력
  - 작은 크기
- **탱크 적 (Tank Enemy)**
  - 낮은 속도, 높은 체력
  - 큰 크기
  - 여러 번 공격해야 제거
- **엘리트 적 (Elite Enemy)**
  - 보통 속도, 높은 체력
  - 큰 점수 보상

### 2. 적 행동 패턴 차별화
- 기본 적: 직선 추적
- 빠른 적: 지그재그 이동
- 탱크 적: 느리지만 밀어냄
- 엘리트 적: 주기적으로 멈추고 돌진

### 3. 난이도 시스템
- **시간 기반 난이도 증가**
  - 게임 시작 후 30초마다 난이도 증가
  - 적 spawn 주기 감소
  - 적 수 증가
- **레벨 기반 난이도**
  - 레벨업 시 적 강화
  - 엘리트 적 등장 빈도 증가
  - 특수 적 등장

### 4. 스폰 시스템 고도화
- **웨이브 시스템 (선택 사항)**
  - 일정 시간마다 적 집단 spawn
- **적 종류별 스폰 확률**
  - 초반: 기본 적 90%, 빠른 적 10%
  - 중반: 기본 적 60%, 빠른 적 20%, 탱크 20%
  - 후반: 모든 적 균등, 엘리트 추가
- **스폰 위치 다양화**
  - 플레이어로부터 일정 거리 밖
  - 화면 밖 랜덤 위치

### 5. 점수 시스템 확장
- 적 종류별 차등 점수
  - 기본 적: 10점
  - 빠른 적: 15점
  - 탱크 적: 25점
  - 엘리트 적: 50점

### 6. 생존 시간 표시
- 게임 시작 후 경과 시간 표시
- 초 단위로 UI에 표시

---

## 🏗️ 구조 설명

### 주요 클래스 (Version 3 기반 확장)

#### 1. `Enemy` 기본 클래스 확장
```python
class Enemy:
    def __init__(self, x, y, width, height, speed, hp, score_value, enemy_type)
    def move_towards_player(self, player, obstacles)  # 기본 이동
    def update(self, player, obstacles)  # 행동 패턴 포함
    def take_damage(self, damage)
    def is_dead(self)
    def get_score_value(self)
    def draw(self, screen, camera)
```

#### 2. `BasicEnemy` 클래스 (Enemy 상속)
```python
class BasicEnemy(Enemy):
    def __init__(self, x, y)
    # 기본 직선 추적
```

#### 3. `FastEnemy` 클래스 (Enemy 상속)
```python
class FastEnemy(Enemy):
    def __init__(self, x, y)
    def update(self, player, obstacles)
        # 지그재그 패턴 구현
```

#### 4. `TankEnemy` 클래스 (Enemy 상속)
```python
class TankEnemy(Enemy):
    def __init__(self, x, y)
    # 높은 HP, 느린 속도
    # 큰 크기
```

#### 5. `EliteEnemy` 클래스 (Enemy 상속)
```python
class EliteEnemy(Enemy):
    def __init__(self, x, y)
    def update(self, player, obstacles)
        # 돌진 패턴 구현
```

#### 6. `EnemySpawner` 클래스 (신규)
```python
class EnemySpawner:
    def __init__(self, map_width, map_height)
    def update(self, dt, player_pos, difficulty_level)
    def spawn_enemy(self, enemy_type, player_pos)
        # 플레이어로부터 안전 거리 밖에 생성
    def get_spawn_probability(self, difficulty_level)
        # 난이도별 적 종류 확률 반환
    def calculate_spawn_rate(self, difficulty_level)
        # 난이도별 spawn 주기 계산
```

#### 7. `DifficultyManager` 클래스 (신규)
```python
class DifficultyManager:
    def __init__(self)
    def update(self, dt, player_level)
    def get_difficulty_level(self)
    def get_enemy_spawn_rate(self)
    def get_enemy_type_weights(self)
        # 각 적 종류의 spawn 가중치 반환
```

#### 8. `Game` 클래스 확장
```python
class Game:
    def __init__(self)
    def init_difficulty(self)
    def init_spawner(self)
    def update(self)
    def update_difficulty(self)
    def spawn_enemies(self)
    def draw_ui(self)
        # 생존 시간 추가
```

### 게임 루프 흐름 (확장)
```
초기화
├─ DifficultyManager 초기화
├─ EnemySpawner 초기화
└─ 생존 시간 타이머 시작
│
└─> [게임 루프 시작]
    │
    ├─> 업데이트
    │   ├─ 생존 시간 증가
    │   ├─ DifficultyManager 업데이트
    │   │   ├─ 시간 기반 난이도 계산
    │   │   └─ 레벨 기반 난이도 반영
    │   ├─ EnemySpawner 업데이트
    │   │   ├─ 난이도 기반 spawn 주기 결정
    │   │   ├─ 적 종류 확률 계산
    │   │   └─ 적 생성 (다양한 타입)
    │   ├─ 각 적 업데이트
    │   │   └─ 종류별 고유 행동 패턴
    │   ├─ 플레이어 이동
    │   ├─ 카메라 업데이트
    │   ├─ 무기 업데이트
    │   ├─ 충돌 판정
    │   └─ 적 처치 시 종류별 점수 추가
    │
    ├─> 렌더링
    │   ├─ 모든 엔티티 (적 종류별 색상/크기 차이)
    │   └─ UI (HP, Score, Level, 생존 시간)
    │
    └─> FPS 제어
```

---

## 🧪 테스트 항목

### 필수 테스트
- [ ] 4가지 적 타입이 모두 정상 spawn 되는가
- [ ] 각 적의 속도가 의도대로 다른가
- [ ] 탱크 적이 여러 번 공격해야 죽는가
- [ ] 빠른 적의 지그재그 패턴이 작동하는가
- [ ] 엘리트 적의 돌진 패턴이 작동하는가
- [ ] 난이도가 시간에 따라 증가하는가
- [ ] 적 spawn 주기가 점점 빨라지는가
- [ ] 적 종류별 spawn 확률이 난이도에 따라 변하는가
- [ ] 점수가 적 종류별로 다르게 부여되는가
- [ ] 생존 시간이 정확하게 표시되는가

### 추가 확인 사항
- [ ] 적이 플레이어 바로 옆에 spawn 되지 않는가
- [ ] 특정 적 타입이 과도하게 많이 spawn 되지 않는가
- [ ] 탱크 적이 너무 많으면 게임이 어려워지는가
- [ ] 엘리트 적이 너무 자주 등장하지 않는가
- [ ] 후반부에도 플레이가 가능한가

---

## ✅ 다음 버전으로 넘어가기 전 안정화 포인트

### 1. 적 다양성 검증
- [ ] 각 적 타입이 시각적으로 구별되는가
- [ ] 각 적의 행동 패턴이 명확하게 다른가
- [ ] 플레이어가 적 타입을 인식하고 대응할 수 있는가

### 2. 난이도 곡선 검증
- [ ] 초반이 너무 어렵지 않은가
- [ ] 중반부터 점진적으로 어려워지는가
- [ ] 후반부가 극복 불가능하지 않은가
- [ ] 5~10분 생존이 가능한가

### 3. 밸런스 조정
- [ ] 각 적 타입의 HP가 적절한가
- [ ] 각 적 타입의 점수 보상이 적절한가
- [ ] 엘리트 적의 등장 빈도가 적절한가
- [ ] 난이도 증가 속도가 적절한가

### 4. 성능 확인
- [ ] 적 100마리 상태에서도 60 FPS 유지
- [ ] 다양한 적 타입이 동시에 존재해도 문제 없음

### 5. 플레이 테스트
- [ ] 3명 이상의 테스터가 게임을 플레이
- [ ] 난이도에 대한 피드백 수집
- [ ] 재미 요소 확인

---

## 📝 구현 팁

### 1. 적 타입별 속성 정의
```python
ENEMY_TYPES = {
    "basic": {
        "speed": 2,
        "hp": 50,
        "size": 30,
        "score": 10,
        "color": (255, 0, 0)
    },
    "fast": {
        "speed": 4,
        "hp": 30,
        "size": 20,
        "score": 15,
        "color": (255, 255, 0)
    },
    "tank": {
        "speed": 1,
        "hp": 150,
        "size": 50,
        "score": 25,
        "color": (100, 100, 100)
    },
    "elite": {
        "speed": 2.5,
        "hp": 100,
        "size": 40,
        "score": 50,
        "color": (255, 0, 255)
    }
}
```

### 2. 난이도 기반 spawn 확률
```python
def get_enemy_type_weights(self, difficulty_level):
    if difficulty_level < 2:
        return {"basic": 0.9, "fast": 0.1, "tank": 0, "elite": 0}
    elif difficulty_level < 4:
        return {"basic": 0.6, "fast": 0.2, "tank": 0.2, "elite": 0}
    else:
        return {"basic": 0.4, "fast": 0.25, "tank": 0.25, "elite": 0.1}
```

### 3. 지그재그 패턴
```python
class FastEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, ...)
        self.zigzag_timer = 0
        self.zigzag_direction = 1
    
    def update(self, player, obstacles):
        self.zigzag_timer += 1
        if self.zigzag_timer > 30:  # 30프레임마다 방향 전환
            self.zigzag_direction *= -1
            self.zigzag_timer = 0
        
        # 기본 이동 + 수직 방향 추가
        dx, dy = self.calculate_direction_to_player(player)
        perpendicular = (-dy * self.zigzag_direction, dx * self.zigzag_direction)
        self.x += dx * self.speed + perpendicular[0] * 0.5
        self.y += dy * self.speed + perpendicular[1] * 0.5
```

### 4. 돌진 패턴
```python
class EliteEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, ...)
        self.state = "chase"  # chase, charge_up, charge
        self.charge_timer = 0
    
    def update(self, player, obstacles):
        if self.state == "chase":
            self.move_towards_player(player, obstacles)
            self.charge_timer += 1
            if self.charge_timer > 120:  # 2초마다
                self.state = "charge_up"
                self.charge_timer = 0
        elif self.state == "charge_up":
            # 잠시 멈춤
            self.charge_timer += 1
            if self.charge_timer > 30:  # 0.5초 대기
                self.state = "charge"
                self.charge_speed = self.speed * 3
        elif self.state == "charge":
            # 빠르게 돌진
            self.move_towards_player(player, obstacles, self.charge_speed)
            self.charge_timer += 1
            if self.charge_timer > 60:  # 1초 돌진
                self.state = "chase"
                self.charge_timer = 0
```

### 5. 안전 거리 spawn
```python
def spawn_enemy(self, enemy_type, player_pos):
    min_distance = 400  # 최소 거리
    while True:
        x = random.randint(0, self.map_width)
        y = random.randint(0, self.map_height)
        distance = math.sqrt((x - player_pos[0])**2 + (y - player_pos[1])**2)
        if distance > min_distance:
            return self.create_enemy(enemy_type, x, y)
```

---

## 🎯 이 버전의 성공 기준

- 적의 다양성으로 전투가 단조롭지 않음
- 난이도가 자연스럽게 상승
- 5~10분 플레이 시 충분한 도전감
- 각 적 타입에 대한 전략적 대응이 필요
- 생존 시간과 점수를 통한 성취감 제공

**다음 버전(Version 5)에서는 사운드 효과, UI 개선, 애니메이션으로 완성도를 높입니다.**
