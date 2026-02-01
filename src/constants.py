"""게임 상수 정의"""

# 그리드 설정
GRID_WIDTH = 20  # 각 그리드 셀의 픽셀 너비 (작은 타일로 부드러운 이동)
GRID_HEIGHT = 20  # 각 그리드 셀의 픽셀 높이

# 화면 설정
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1400
FPS = 60

# 그리드 개수 (자동 계산)
GRID_COLS = SCREEN_WIDTH // GRID_WIDTH  # 70
GRID_ROWS = SCREEN_HEIGHT // GRID_HEIGHT  # 70

# 색상 정의 (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# 게임 객체 모양 정의 (상대 좌표)
# 플레이어: + 모양
PLAYER_SHAPE = [
    (1, 0),                    # 위
    (0, 1), (1, 1), (2, 1),   # 중간 가로
    (1, 2)                     # 아래
]

# 적 모양들
ENEMY_SHAPE_SQUARE = [(0, 0)]  # 정사각형 (1x1)

ENEMY_SHAPE_L = [
    (0, 0), (0, 1), (0, 2),   # 세로 줄
    (1, 2)                     # 가로 부분
]

ENEMY_SHAPE_T = [
    (0, 0), (1, 0), (2, 0),   # 위쪽 가로 줄
    (1, 1), (1, 2)            # 세로 줄
]

ENEMY_SHAPE_Z = [
    (0, 0), (1, 0),           # 위쪽 가로
    (1, 1),                    # 중간 대각선
    (1, 2), (2, 2)            # 아래쪽 가로
]

ENEMY_SHAPE_BLOCK = [
    (0, 0), (0, 1),
    (1, 0), (1, 1)            # 2x2 블록
]

# 적 모양 리스트 (spawn 시 랜덤 선택용)
ENEMY_SHAPES = [
    ENEMY_SHAPE_SQUARE,
    ENEMY_SHAPE_L,
    ENEMY_SHAPE_T,
    ENEMY_SHAPE_Z,
    ENEMY_SHAPE_BLOCK
]

# 적 색상 리스트 (모양별 색상)
ENEMY_COLORS = [
    RED,      # 정사각형
    ORANGE,   # L자
    YELLOW,   # T자
    MAGENTA,  # Z자
    PURPLE    # 블록
]

# 플레이어 설정 (그리드 단위)
PLAYER_GRID_SIZE = 1  # 그리드 셀 단위
PLAYER_SPEED_GRID = 0.3  # 한 프레임당 이동 그리드 (부드러운 이동)
PLAYER_COLOR = BLUE
PLAYER_MAX_HP = 100  # 최대 체력
PLAYER_COLLISION_DAMAGE = 10  # 적과 충돌 시 받는 데미지

# 적 설정 (그리드 단위)
ENEMY_GRID_SIZE = 1  # 그리드 셀 단위
ENEMY_SPEED_GRID = 0.1  # 한 프레임당 이동 그리드 (더 느리게 조정)
ENEMY_COLOR = RED
ENEMY_SPAWN_INTERVAL = 2000  # 밀리초 (2초)
MAX_ENEMIES = 30  # 최대 적 개수 제한
COLLISION_CHECK_DISTANCE = 5  # 충돌 체크 거리 (그리드 단위, 이 거리 이상은 충돌 불가능)

# 게임 타이틀
GAME_TITLE = "Fighter Game - Version 2"

# 체력 회복 아이템 설정
HEALTH_POTION_SIZE = 1  # 그리드 셀 단위
HEALTH_POTION_COLOR = GREEN
HEALTH_POTION_HEAL = 20  # 회복량
HEALTH_POTION_SPAWN_INTERVAL = 15000  # 밀리초 (15초)

# 장애물 설정
OBSTACLE_COLOR = (100, 100, 100)  # 회색
NUM_OBSTACLES = 10  # 맵에 생성할 장애물 개수

# 적 HP 설정
ENEMY_HP = 100  # 적의 기본 체력

# 무기 설정 - Sword
SWORD_DAMAGE = 50  # 공격력
SWORD_COOLDOWN = 1.0  # 초 (자동 발동 간격)
SWORD_RANGE = 5.0  # 공격 범위 (그리드 단위)
SWORD_EFFECT_COLOR = (255, 255, 100)  # 노란색 계열

# 녹백 설정
KNOCKBACK_DISTANCE = 5.0  # 데미지 받을 때 밀려나는 거리 (그리드 단위)
