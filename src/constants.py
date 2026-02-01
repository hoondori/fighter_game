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

# 플레이어 설정 (그리드 단위)
PLAYER_GRID_SIZE = 1  # 그리드 셀 단위
PLAYER_SPEED_GRID = 1  # 한 번 이동 시 그리드 셀 개수
PLAYER_COLOR = BLUE

# 적 설정 (그리드 단위)
ENEMY_GRID_SIZE = 1  # 그리드 셀 단위
ENEMY_SPEED_GRID = 0.15  # 한 프레임당 이동 그리드 (느리게 조정)
ENEMY_COLOR = RED
ENEMY_SPAWN_INTERVAL = 2000  # 밀리초 (2초)

# 게임 타이틀
GAME_TITLE = "Fighter Game - Version 1"
