# Fighter Game - Version 1 (MVP)

격투 게임의 최소 버전 구현 프로젝트입니다.

## 🎮 게임 설명

- **주인공**: 파란색 사각형으로 표시되며 키보드로 이동 가능
- **적**: 빨간색 사각형으로 표시되며 주인공을 추적
- **목표**: 적과 충돌하지 않고 최대한 오래 생존

## 🚀 설치 및 실행

### 1. 필수 패키지 설치

```bash
conda run -n pygame pip install -r requirements.txt
```

### 2. 게임 실행

```bash
conda run -n pygame python main.py
```

### 3. 테스트 실행

```bash
conda run -n pygame pytest tests/ -v
```

## 🎯 조작 방법

- **이동**: 화살표 키 또는 WASD
  - ↑ / W: 위로 이동
  - ↓ / S: 아래로 이동
  - ← / A: 왼쪽으로 이동
  - → / D: 오른쪽으로 이동
- **게임 종료**: ESC 키
- **게임 오버 후**:
  - R: 재시작
  - ESC: 종료

## 📁 프로젝트 구조

```
fighter_game/
├── src/
│   ├── __init__.py       # 패키지 초기화
│   ├── constants.py      # 게임 상수 정의
│   ├── player.py         # Player 클래스
│   ├── enemy.py          # Enemy 클래스
│   └── game.py           # Game 클래스 (메인 로직)
├── tests/
│   ├── __init__.py
│   ├── test_player.py    # Player 테스트
│   ├── test_enemy.py     # Enemy 테스트
│   └── test_game.py      # Game 테스트
├── main.py               # 게임 실행 진입점
├── requirements.txt      # 의존성 패키지
└── README.md            # 프로젝트 문서
```

## 🎨 게임 기능

### 구현된 기능
- ✅ 플레이어 이동 (상하좌우)
- ✅ 화면 경계 제한
- ✅ 적 자동 spawn (2초마다)
- ✅ 적 자동 추적 (플레이어를 향해 이동)
- ✅ 충돌 판정
- ✅ 게임 오버 및 재시작
- ✅ 적 개수 표시

### Version 1 특징
- 단순한 박스 형태의 캐릭터
- 무기 시스템 없음
- 체력 시스템 없음
- 장애물 없음
- 음악/사운드 없음

## 🧪 테스트

프로젝트는 pytest를 사용한 종합적인 테스트 스위트를 포함합니다:

### 테스트 커버리지
- **Player 테스트** (`test_player.py`)
  - 플레이어 생성 및 초기화
  - 이동 기능 (상하좌우, WASD)
  - 화면 경계 제한
  - 충돌 판정

- **Enemy 테스트** (`test_enemy.py`)
  - 적 생성 및 초기화
  - 플레이어 추적 이동
  - 다양한 방향에서 접근
  - 충돌 판정

- **Game 테스트** (`test_game.py`)
  - 게임 초기화
  - 적 spawn 시스템
  - 충돌 감지
  - 게임 상태 관리
  - 성능 테스트 (다수의 적)

### 테스트 실행 방법

```bash
# 전체 테스트 실행
conda run -n pygame pytest tests/ -v

# 특정 테스트 파일 실행
conda run -n pygame pytest tests/test_player.py -v

# 커버리지 리포트와 함께 실행
conda run -n pygame pytest tests/ -v --cov=src --cov-report=html
```

## 📊 기술 스택

- **Python 3.x**
- **Pygame 2.5.0+**: 게임 엔진
- **Pytest 7.4.0+**: 테스트 프레임워크

## 🔧 개발 환경

- Conda 환경 이름: `pygame`
- 화면 크기: 800x600
- 프레임레이트: 60 FPS

## 📝 다음 버전 계획

Version 2에서는 다음 기능들이 추가될 예정입니다:
- 전투 시스템
- 체력 시스템
- 공격 메커니즘
- 점수 시스템

## 🐛 알려진 이슈

현재 알려진 이슈 없음

## 📄 라이선스

이 프로젝트는 학습 목적으로 제작되었습니다.

## 👥 기여

이슈 제보 및 개선 제안은 언제나 환영합니다!
