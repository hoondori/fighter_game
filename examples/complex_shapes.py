"""복잡한 모양 지원 테스트 및 예제"""

import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from src.player import Player
from src.enemy import Enemy

# 다양한 모양 정의

# L자 모양
L_SHAPE = [
    (0, 0), (0, 1), (0, 2),  # 세로 줄
    (1, 2)                    # 가로 부분
]

# T자 모양
T_SHAPE = [
    (0, 0), (1, 0), (2, 0),  # 위쪽 가로 줄
    (1, 1), (1, 2)           # 세로 줄
]

# + 모양
PLUS_SHAPE = [
    (1, 0),                   # 위
    (0, 1), (1, 1), (2, 1),  # 중간 가로
    (1, 2)                    # 아래
]

# Z자 모양
Z_SHAPE = [
    (0, 0), (1, 0),          # 위쪽 가로
    (1, 1),                   # 중간 대각선
    (1, 2), (2, 2)           # 아래쪽 가로
]

# ㄷ자 모양
U_SHAPE = [
    (0, 0), (0, 1), (0, 2),  # 왼쪽 세로
    (1, 2),                   # 아래 연결
    (2, 0), (2, 1), (2, 2)   # 오른쪽 세로
]


def verify_shape_adjacency(shape):
    """
    모양의 모든 셀이 서로 인접해있는지 검증
    
    Args:
        shape: [(x1, y1), (x2, y2), ...] 상대 좌표 리스트
        
    Returns:
        bool: 모든 셀이 연결되어 있으면 True
    """
    if not shape:
        return False
    
    # BFS로 연결성 확인
    visited = set()
    queue = [shape[0]]
    visited.add(shape[0])
    
    while queue:
        x, y = queue.pop(0)
        
        # 4방향 인접 셀 확인
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (x + dx, y + dy)
            if neighbor in shape and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    # 모든 셀이 방문되었는지 확인
    return len(visited) == len(shape)


def test_shapes():
    """모양 검증 테스트"""
    print("=== 모양 검증 테스트 ===\n")
    
    shapes = {
        "정사각형 (1x1)": [(0, 0)],
        "정사각형 (2x2)": [(0, 0), (0, 1), (1, 0), (1, 1)],
        "L자": L_SHAPE,
        "T자": T_SHAPE,
        "+자": PLUS_SHAPE,
        "Z자": Z_SHAPE,
        "ㄷ자": U_SHAPE,
        "단절된 모양": [(0, 0), (2, 2)]  # 잘못된 예시
    }
    
    for name, shape in shapes.items():
        is_valid = verify_shape_adjacency(shape)
        status = "✅ 유효" if is_valid else "❌ 단절됨"
        print(f"{name}: {status}")
        print(f"  셀 개수: {len(shape)}")
        print(f"  좌표: {shape}\n")


def demo_complex_shapes():
    """복잡한 모양 객체 생성 데모"""
    print("\n=== 복잡한 모양 객체 생성 ===\n")
    
    # L자 플레이어
    player_l = Player(grid_x=10, grid_y=10, shape=L_SHAPE)
    print(f"L자 플레이어:")
    print(f"  기준점: ({player_l.grid_x}, {player_l.grid_y})")
    print(f"  차지하는 그리드: {player_l.get_grid_positions()}")
    print(f"  경계 상자: {player_l.get_bounding_box()}\n")
    
    # T자 적
    enemy_t = Enemy(grid_x=20, grid_y=20, shape=T_SHAPE)
    print(f"T자 적:")
    print(f"  기준점: ({enemy_t.grid_x}, {enemy_t.grid_y})")
    print(f"  차지하는 그리드: {enemy_t.get_grid_positions()}")
    print(f"  경계 상자: {enemy_t.get_bounding_box()}\n")
    
    # 충돌 테스트
    print(f"충돌 여부: {player_l.collides_with(enemy_t)}")
    
    # 같은 위치에 배치
    player_close = Player(grid_x=20, grid_y=20, shape=L_SHAPE)
    print(f"\n같은 위치의 L자 플레이어와 T자 적 충돌: {player_close.collides_with(enemy_t)}")


def visualize_shape(shape, name):
    """
    모양을 ASCII 아트로 시각화
    
    Args:
        shape: [(x, y), ...] 상대 좌표
        name: 모양 이름
    """
    if not shape:
        return
    
    xs = [x for x, y in shape]
    ys = [y for x, y in shape]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    print(f"\n{name}:")
    shape_set = set(shape)
    for y in range(min_y, max_y + 1):
        line = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in shape_set:
                line += "■ "
            else:
                line += "□ "
        print(f"  {line}")


def visualize_all_shapes():
    """모든 모양 시각화"""
    print("\n=== 모양 시각화 ===")
    
    shapes = {
        "1x1 정사각형": [(0, 0)],
        "2x2 정사각형": [(0, 0), (0, 1), (1, 0), (1, 1)],
        "L자": L_SHAPE,
        "T자": T_SHAPE,
        "+자": PLUS_SHAPE,
        "Z자": Z_SHAPE,
        "ㄷ자": U_SHAPE
    }
    
    for name, shape in shapes.items():
        visualize_shape(shape, name)


if __name__ == "__main__":
    test_shapes()
    demo_complex_shapes()
    visualize_all_shapes()
    
    print("\n" + "="*50)
    print("복잡한 모양 지원이 준비되었습니다!")
    print("="*50)
