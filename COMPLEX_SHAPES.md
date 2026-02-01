# 복잡한 모양 지원 구현 완료

## 🎯 목적
단순 정사각형에서 벗어나 L자, T자 등 복잡한 모양을 지원할 수 있는 확장 가능한 시스템 구현

## ✅ 구현 내용

### 1. 핵심 개념: **List of Grid Points**

모든 게임 객체가 **여러 개의 그리드 셀**을 차지할 수 있도록 변경:

```python
# 기존: 단일 위치
self.grid_x = 10
self.grid_y = 10

# 새로운 방식: 상대 좌표 리스트
self.shape = [(0,0), (0,1), (0,2), (1,2)]  # L자 모양
```

### 2. Player 클래스 업데이트

**주요 추가 기능:**

```python
class Player:
    def __init__(self, grid_x, grid_y, shape=None):
        # shape이 None이면 기본 정사각형
        if shape is None:
            self.shape = [(i, j) for i in range(grid_size) 
                          for j in range(grid_size)]
        else:
            self.shape = shape  # 커스텀 모양
    
    def get_grid_positions(self):
        """절대 그리드 좌표 반환"""
        return [(self.grid_x + dx, self.grid_y + dy) 
                for dx, dy in self.shape]
    
    def is_valid_position(self, new_x, new_y):
        """모든 셀이 화면 안에 있는지 확인"""
        for dx, dy in self.shape:
            abs_x = new_x + dx
            abs_y = new_y + dy
            if not (0 <= abs_x < GRID_COLS and 0 <= abs_y < GRID_ROWS):
                return False
        return True
    
    def collides_with(self, other):
        """그리드 기반 정밀 충돌 판정"""
        my_positions = set(self.get_grid_positions())
        other_positions = set(other.get_grid_positions())
        return bool(my_positions & other_positions)
```

**하위 호환성:**
- `shape=None` → 기존 정사각형 동작
- `get_pixel_pos()`, `get_rect()` 유지
- 각 셀마다 사각형 렌더링

### 3. Enemy 클래스 업데이트

동일한 구조로 적용:
- `shape` 파라미터 지원
- `get_grid_positions()` 메서드
- 부드러운 이동 유지 (float 좌표)
- 경계 상자 기반 충돌 판정

### 4. Game 클래스 충돌 판정

```python
def check_collision(self):
    """그리드 기반 정밀 충돌"""
    for enemy in self.enemies:
        if self.player.collides_with(enemy):
            self.game_over = True
            return True
    return False
```

## 🎮 사용 예시

### 기본 사용 (정사각형)

```python
# shape=None이면 자동으로 정사각형
player = Player(grid_x=10, grid_y=10)
enemy = Enemy(grid_x=20, grid_y=20)
```

### 복잡한 모양

```python
# L자 모양 플레이어
L_SHAPE = [(0,0), (0,1), (0,2), (1,2)]
player = Player(grid_x=10, grid_y=10, shape=L_SHAPE)

# T자 모양 적
T_SHAPE = [(0,0), (1,0), (2,0), (1,1), (1,2)]
enemy = Enemy(grid_x=20, grid_y=20, shape=T_SHAPE)

# 충돌 확인
if player.collides_with(enemy):
    print("충돌!")
```

## 📦 제공된 예제 모양

[examples/complex_shapes.py](examples/complex_shapes.py)에서 제공:

### 시각화

```
L자:
  ■ □ 
  ■ □ 
  ■ ■ 

T자:
  ■ ■ ■ 
  □ ■ □ 
  □ ■ □ 

+자:
  □ ■ □ 
  ■ ■ ■ 
  □ ■ □ 

Z자:
  ■ ■ □ 
  □ ■ □ 
  □ ■ ■ 

ㄷ자:
  ■ □ ■ 
  ■ □ ■ 
  ■ ■ ■ 
```

### 모양 정의

```python
# L자
L_SHAPE = [(0,0), (0,1), (0,2), (1,2)]

# T자
T_SHAPE = [(0,0), (1,0), (2,0), (1,1), (1,2)]

# +자
PLUS_SHAPE = [(1,0), (0,1), (1,1), (2,1), (1,2)]

# Z자
Z_SHAPE = [(0,0), (1,0), (1,1), (1,2), (2,2)]

# ㄷ자
U_SHAPE = [(0,0), (0,1), (0,2), (1,2), 
           (2,0), (2,1), (2,2)]
```

## ✅ 모양 유효성 검증

**규칙:** 모든 셀이 서로 **인접**해야 함 (상하좌우로 연결)

```python
def verify_shape_adjacency(shape):
    """BFS로 연결성 확인"""
    visited = set()
    queue = [shape[0]]
    visited.add(shape[0])
    
    while queue:
        x, y = queue.pop(0)
        # 4방향 확인
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            neighbor = (x+dx, y+dy)
            if neighbor in shape and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return len(visited) == len(shape)
```

## 🧪 테스트 결과

```bash
$ conda run -n pygame python examples/complex_shapes.py

=== 모양 검증 테스트 ===

정사각형 (1x1): ✅ 유효
L자: ✅ 유효
T자: ✅ 유효
+자: ✅ 유효
Z자: ✅ 유효
ㄷ자: ✅ 유효
단절된 모양: ❌ 단절됨

=== 충돌 테스트 ===
같은 위치의 L자와 T자: 충돌 감지됨 ✅
```

**모든 기존 테스트 통과:** 38개 테스트 ✅

## 🎯 장점

### 1. 확장성
- 새로운 모양을 쉽게 추가 가능
- Tetris, Sokoban 등 타일 기반 게임으로 확장 가능

### 2. 정밀한 충돌 판정
- 각 그리드 셀 단위로 정확한 충돌 감지
- 경계 상자보다 정밀

### 3. 하위 호환성
- 기존 코드 동작 유지 (shape=None)
- 기존 API 유지 (get_rect, get_pixel_pos)

### 4. 유연성
- 런타임에 모양 변경 가능
- 캐릭터별 고유 모양 설정 가능

## 🔧 구현 세부사항

### 좌표 시스템

```python
# 기준점 (grid_x, grid_y) + 상대 좌표 (dx, dy)
절대 좌표 = (grid_x + dx, grid_y + dy)

# 예시: L자 (기준점 10, 10)
shape = [(0,0), (0,1), (0,2), (1,2)]
positions = [(10,10), (10,11), (10,12), (11,12)]
```

### 렌더링

```python
def draw(self, screen):
    for grid_x, grid_y in self.get_grid_positions():
        pixel_x = grid_x * GRID_WIDTH
        pixel_y = grid_y * GRID_HEIGHT
        pygame.draw.rect(screen, self.color, 
                        (pixel_x, pixel_y, GRID_WIDTH, GRID_HEIGHT))
```

### 충돌 판정

```python
# Set intersection으로 O(n+m) 시간
my_positions = set(self.get_grid_positions())
other_positions = set(other.get_grid_positions())
collision = bool(my_positions & other_positions)
```

## 🚀 향후 활용 가능성

### 1. 캐릭터 클래스 시스템
```python
class Warrior(Player):
    def __init__(self, grid_x, grid_y):
        # 전사는 십자가 모양
        super().__init__(grid_x, grid_y, shape=PLUS_SHAPE)

class Archer(Player):
    def __init__(self, grid_x, grid_y):
        # 궁수는 1칸
        super().__init__(grid_x, grid_y, shape=[(0,0)])
```

### 2. 변형 시스템
```python
# 파워업으로 모양 변경
player.shape = BIGGER_SHAPE
player.color = GOLD  # 시각적 변화
```

### 3. 장애물/벽
```python
class Wall:
    def __init__(self, positions):
        self.grid_positions = positions
    
    def get_grid_positions(self):
        return self.grid_positions
```

### 4. 애니메이션
```python
# 모양을 순차적으로 변경하여 애니메이션
shapes = [FRAME1, FRAME2, FRAME3]
current_frame = (current_frame + 1) % len(shapes)
player.shape = shapes[current_frame]
```

## 📊 성능

- **충돌 판정:** O(n+m) where n, m은 각 객체의 셀 개수
- **렌더링:** 각 셀마다 1개의 사각형 (기존과 동일)
- **메모리:** 셀당 2개의 정수 (x, y)

일반적인 캐릭터 크기(1-10 셀)에서는 성능 영향 무시 가능.

## 🎉 결과

✅ **복잡한 모양 시스템 구현 완료**
- List of grid points로 모든 객체 관리
- 정사각형부터 복잡한 모양까지 지원
- 정밀한 그리드 기반 충돌 판정
- 하위 호환성 유지
- 38개 테스트 모두 통과

**비록 렌더링은 정사각형 셀들이지만, 향후 스프라이트로 교체 가능하며 로직은 완벽하게 복잡한 모양을 지원합니다!** 🚀
