# Version 1 – 게임의 최소 형태 (MVP)

## 🎯 목표
pygame 기본 구조와 게임 루프 이해

---

## 🎮 구현할 게임 기능

### 1. 주인공
- 사각형 Box로 표시
- 키보드로 이동 (상/하/좌/우)
- 화면 밖으로 나가지 못함

### 2. 적
- 사각형 Box로 표시
- 화면 경계에서 spawn
- 직선적으로 주인공을 향해 이동
- 주인공과 충돌 시 게임 종료

### 3. 게임 규칙
- 맵 크기 = 화면 크기 (800x600 추천)
- 장애물 없음
- 무기 없음
- 체력 시스템 없음
- 적과 닿으면 즉시 게임 종료
- 음악/사운드 없음

---

## 🏗️ 구조 설명

### 주요 클래스

#### 1. `Player` 클래스
```python
class Player:
    def __init__(self, x, y, width, height, speed)
    def move(self, keys)  # 키 입력 처리
    def draw(self, screen)  # 화면에 그리기
    def get_rect(self)  # 충돌 판정용 rect
```

#### 2. `Enemy` 클래스
```python
class Enemy:
    def __init__(self, x, y, width, height, speed)
    def move_towards_player(self, player)  # 플레이어 추적
    def draw(self, screen)
    def get_rect()
```

#### 3. `Game` 클래스
```python
class Game:
    def __init__(self)
    def spawn_enemy(self)  # 적 생성
    def check_collision(self)  # 충돌 판정
    def update(self)  # 게임 상태 업데이트
    def draw(self)  # 화면 렌더링
    def run(self)  # 메인 게임 루프
```

### 게임 루프 흐름
```
초기화
│
└─> [게임 루프 시작]
    │
    ├─> 이벤트 처리 (종료, 키 입력)
    │
    ├─> 업데이트
    │   ├─ 플레이어 이동
    │   ├─ 적 생성 (일정 주기)
    │   ├─ 적 이동
    │   └─ 충돌 판정
    │
    ├─> 렌더링
    │   ├─ 화면 클리어
    │   ├─ 플레이어 그리기
    │   ├─ 적들 그리기
    │   └─ 화면 업데이트
    │
    └─> FPS 제어 (60 FPS)
```

---

## 🧪 테스트 항목

### 필수 테스트
- [ ] 주인공이 상하좌우로 정상 이동하는가
- [ ] 주인공이 화면 밖으로 나가지 않는가
- [ ] 적이 화면 경계에서 정상적으로 spawn 되는가
- [ ] 적이 주인공을 향해 이동하는가
- [ ] 주인공과 적이 충돌 시 게임이 즉시 종료되는가
- [ ] 프레임 드랍 없이 60 FPS로 실행되는가

### 추가 확인 사항
- [ ] 여러 적이 동시에 spawn 되어도 문제 없는가
- [ ] 적이 화면 네 방향에서 고르게 spawn 되는가
- [ ] 게임 종료 후 창이 정상적으로 닫히는가

---

## ✅ 다음 버전으로 넘어가기 전 안정화 포인트

### 1. 코드 정리
- [ ] 매직 넘버를 상수로 정의 (화면 크기, 속도 등)
- [ ] 주석 추가
- [ ] 함수/클래스 분리 확인

### 2. 성능 확인
- [ ] 적 10~20마리 상태에서 60 FPS 유지
- [ ] 메모리 누수 없음

### 3. 게임 플레이 확인
- [ ] 최소 30초 이상 생존 가능한 난이도
- [ ] 적 spawn 주기가 적절한가

### 4. 버그 수정
- [ ] 알려진 모든 버그 해결
- [ ] 예외 상황 처리 (창 크기 조정 등)

---

## 📝 구현 팁

1. **pygame 초기화**
   ```python
   pygame.init()
   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
   clock = pygame.time.Clock()
   ```

2. **키 입력 처리**
   ```python
   keys = pygame.key.get_pressed()
   if keys[pygame.K_LEFT]:
       # 왼쪽 이동
   ```

3. **충돌 판정**
   ```python
   if player.get_rect().colliderect(enemy.get_rect()):
       # 게임 종료
   ```

4. **적 spawn 위치**
   - 화면 왼쪽: (0, random_y)
   - 화면 오른쪽: (SCREEN_WIDTH, random_y)
   - 화면 위쪽: (random_x, 0)
   - 화면 아래쪽: (random_x, SCREEN_HEIGHT)

---

## 🎯 이 버전의 성공 기준

- 게임이 실행되고 종료될 때까지 오류 없이 작동
- 플레이어가 적을 피하며 이동 가능
- 충돌 시 명확한 게임 종료
- 코드가 읽기 쉽고 구조가 명확함

**다음 버전(Version 2)에서는 전투 시스템과 체력 개념을 추가합니다.**
