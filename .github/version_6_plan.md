# Version 6 – 자유 확장 단계

## 🎯 목표
게임 완성 및 자유로운 확장 - 추가 기능, 최적화, 리팩토링

---

## 🎮 확장 아이디어 목록

이 버전은 **자유 확장 단계**로, 아래 아이디어 중 원하는 것을 선택하거나 새로운 아이디어를 구현할 수 있습니다.

### 1. 보스 몬스터 시스템
- **보스 등장 조건**
  - 일정 시간 생존 시 (예: 5분)
  - 특정 레벨 도달 시
- **보스 특징**
  - 매우 높은 HP
  - 고유한 공격 패턴
  - 페이즈 시스템 (HP 감소에 따라 패턴 변화)
  - 보스 체력바 (화면 상단)
- **보스 처치 보상**
  - 대량 점수
  - 특수 아이템
  - 무기 업그레이드

### 2. 무기 강화/진화 시스템
- **무기 레벨업**
  - 적 처치 시 무기 경험치 획득
  - 레벨업 시 공격력/범위/속도 증가
- **무기 진화**
  - 특정 레벨 도달 시 무기 진화
  - Sword → Great Sword (더 넓은 범위)
  - Gun → Dual Gun (2발 동시 발사)
  - Magic Spell → Meteor (강력한 광역 공격)
- **무기 조합**
  - 2개의 무기를 조합하여 새로운 무기 생성

### 3. 패시브 스킬 시스템
- **레벨업 시 스킬 선택**
  - 3가지 스킬 중 1개 선택
  - 게임 일시정지
- **스킬 종류**
  - 이동 속도 증가
  - 최대 HP 증가
  - HP 자동 회복
  - 추가 무기 슬롯
  - 공격력/범위/속도 증가
  - 경험치 획득 증가
  - 적 처치 시 폭발
  - 무적 시간 증가

### 4. 아이템 드랍 시스템
- **적 처치 시 아이템 드랍**
  - 경험치 보석
  - 체력 회복 아이템
  - 임시 버프 아이템
  - 코인 (화폐)
- **아이템 자석**
  - 일정 범위 내 아이템 자동 획득
  - 패시브 스킬로 범위 확장

### 5. 다양한 맵
- **맵 선택 시스템**
  - 시작 시 맵 선택
- **맵 종류**
  - 평원 (기본)
  - 숲 (시야 제한, 장애물 많음)
  - 던전 (좁은 통로)
  - 화산 (용암 지대, 주기적 데미지)
- **맵 특수 효과**
  - 환경 위험 요소
  - 특수 적 등장

### 6. 캐릭터 선택 시스템
- **다양한 캐릭터**
  - 전사: 높은 HP, 느린 속도
  - 도적: 낮은 HP, 빠른 속도
  - 마법사: 보통 HP, 마법 위력 증가
- **캐릭터별 시작 무기 다름**
- **고유 패시브 능력**

### 7. 저장/불러오기 시스템
- **진행 상황 저장**
  - 최고 점수
  - 생존 시간 기록
  - 해금한 캐릭터/무기
- **업적 시스템**
  - 특정 조건 달성 시 업적
  - 업적 달성 시 보상

### 8. 설정 메뉴
- **옵션 화면**
  - 배경 음악 볼륨
  - 효과음 볼륨
  - 화면 해상도
  - 풀스크린 모드
  - 키 바인딩 변경
- **일시정지 메뉴**
  - 'ESC'로 일시정지
  - 재개, 재시작, 메인 메뉴

### 9. 멀티플레이어 (로컬)
- **2인 협동 플레이**
  - 화면 분할 또는 공유 화면
  - 각자 다른 캐릭터 선택
  - 협동 공격

### 10. 코드 리팩토링 및 최적화
- **코드 정리**
  - 클래스 구조 재설계
  - 디자인 패턴 적용 (Factory, Observer 등)
  - 코드 중복 제거
- **성능 최적화**
  - 쿼드트리로 충돌 검사 최적화
  - 오브젝트 풀링
  - 화면 밖 객체 업데이트 최소화
- **테스트 코드**
  - 단위 테스트 작성
  - 통합 테스트

### 11. 고급 AI
- **적 AI 개선**
  - A* 알고리즘으로 장애물 우회
  - 협동 공격 패턴
  - 플레이어 공격 회피
- **보스 AI**
  - 상태 머신
  - 복잡한 공격 패턴

### 12. 추가 무기
- **새로운 무기 아이디어**
  - Boomerang: 던지고 돌아옴
  - Lightning: 체인 공격
  - Shield: 주변 회전하며 방어
  - Laser: 관통 공격
  - Bomb: 시간차 폭발
  - Whip: 긴 범위 공격

### 13. 스토리 모드
- **단계별 미션**
  - 특정 목표 달성 (적 처치 수, 생존 시간)
  - 미션 클리어 시 다음 스테이지
- **엔딩**
  - 모든 스테이지 클리어 시 엔딩

---

## 🏗️ 구현 추천 순서

개인적으로 추천하는 구현 순서:

### Phase 1: 즉시 재미를 더하는 요소
1. **무기 강화/진화 시스템** - 진행감 향상
2. **패시브 스킬 시스템** - 다양성 추가
3. **아이템 드랍 시스템** - 수집 재미

### Phase 2: 장기적 재미
4. **보스 몬스터 시스템** - 목표 제공
5. **저장/불러오기 + 업적** - 리플레이 가치
6. **설정 메뉴** - 사용자 편의성

### Phase 3: 확장성
7. **캐릭터 선택 시스템** - 다양한 플레이 스타일
8. **다양한 맵** - 새로운 경험
9. **추가 무기** - 전략성 증가

### Phase 4: 완성도
10. **코드 리팩토링** - 유지보수성
11. **성능 최적화** - 쾌적한 플레이
12. **고급 AI** - 도전적인 게임플레이

---

## 🧪 각 기능별 테스트 항목

### 보스 시스템
- [ ] 보스가 정해진 조건에서 등장하는가
- [ ] 보스 체력바가 정확하게 표시되는가
- [ ] 보스 패턴이 예측 가능하면서도 도전적인가
- [ ] 보스 처치 시 보상이 제공되는가

### 무기 강화/진화
- [ ] 무기 경험치가 정확하게 누적되는가
- [ ] 레벨업 시 효과가 명확하게 체감되는가
- [ ] 진화 시 시각적 변화가 있는가
- [ ] 밸런스가 무너지지 않는가

### 패시브 스킬
- [ ] 스킬 선택 화면이 직관적인가
- [ ] 모든 스킬이 정상 작동하는가
- [ ] 스킬 조합이 게임을 파괴하지 않는가
- [ ] 스킬 설명이 명확한가

### 저장/불러오기
- [ ] 저장이 올바르게 작동하는가
- [ ] 불러오기 시 데이터가 정확한가
- [ ] 저장 파일이 손상되어도 크래시하지 않는가

### 설정 메뉴
- [ ] 모든 설정이 즉시 적용되는가
- [ ] 설정이 저장되어 다음 실행 시 유지되는가
- [ ] 일시정지 시 게임이 완전히 멈추는가

---

## ✅ 최종 완성 체크리스트

### 게임플레이
- [ ] 10분 이상 플레이해도 지루하지 않은가
- [ ] 난이도 곡선이 적절한가
- [ ] 전투가 만족스러운가
- [ ] 성장 시스템이 동기부여를 주는가

### 기술적 완성도
- [ ] 버그가 없는가
- [ ] 60 FPS 유지되는가
- [ ] 메모리 누수가 없는가
- [ ] 예외 상황이 처리되는가

### 사용자 경험
- [ ] UI가 직관적인가
- [ ] 사운드가 적절한가
- [ ] 조작이 편안한가
- [ ] 튜토리얼/설명이 충분한가

### 코드 품질
- [ ] 코드가 읽기 쉬운가
- [ ] 클래스 구조가 명확한가
- [ ] 주석이 적절한가
- [ ] 확장 가능한 구조인가

---

## 📝 구현 팁

### 1. 보스 몬스터 예시
```python
class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 80, 1.5, 1000, 500, "boss")
        self.phase = 1
        self.pattern_timer = 0
    
    def update(self, player, obstacles):
        # HP에 따른 페이즈 변경
        if self.hp < self.max_hp * 0.5 and self.phase == 1:
            self.phase = 2
            self.speed *= 1.5
        
        # 페이즈별 패턴
        if self.phase == 1:
            self.pattern_chase(player)
        elif self.phase == 2:
            self.pattern_charge(player)
    
    def pattern_chase(self, player):
        # 기본 추적
        pass
    
    def pattern_charge(self, player):
        # 돌진 공격
        pass
```

### 2. 패시브 스킬 선택 화면
```python
class SkillSelection:
    def __init__(self, available_skills):
        self.skills = random.sample(available_skills, 3)
        self.selected = None
    
    def draw(self, screen):
        # 반투명 오버레이
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # 스킬 카드 3개 표시
        for i, skill in enumerate(self.skills):
            x = SCREEN_WIDTH // 4 * (i + 1) - 100
            y = SCREEN_HEIGHT // 2 - 100
            self.draw_skill_card(screen, skill, x, y)
    
    def handle_click(self, pos):
        # 클릭 위치에 따라 스킬 선택
        pass
```

### 3. 무기 진화
```python
class Weapon:
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.max_level = 5
    
    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.get_exp_for_next_level():
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.exp = 0
        self.apply_upgrade()
        
        if self.level == self.max_level:
            self.evolve()
    
    def evolve(self):
        # 무기 진화 로직
        pass
```

### 4. 아이템 드랍
```python
class Enemy:
    def die(self):
        # 일정 확률로 아이템 드랍
        if random.random() < 0.3:  # 30% 확률
            item_type = random.choice(["exp", "health", "coin"])
            return Item(self.x, self.y, item_type)
        return None
```

### 5. 저장/불러오기
```python
import json

class SaveManager:
    def save_game(self, data):
        with open("savegame.json", "w") as f:
            json.dump(data, f)
    
    def load_game(self):
        try:
            with open("savegame.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def save_high_score(self, score):
        data = self.load_game() or {}
        if "high_score" not in data or score > data["high_score"]:
            data["high_score"] = score
            self.save_game(data)
```

---

## 🎯 최종 목표

- **완성된 게임** - 처음부터 끝까지 플레이 가능
- **재미있는 게임** - 반복해서 플레이하고 싶음
- **깔끔한 코드** - 나중에 다시 봐도 이해 가능
- **포트폴리오 가능** - 다른 사람에게 보여줄 수 있는 수준

---

## 🚀 더 나아가기

이 게임을 완성한 후:

1. **배포**
   - itch.io에 업로드
   - GitHub에 오픈소스로 공개
   - 친구들과 공유

2. **다음 프로젝트**
   - 다른 장르 게임 (플랫포머, 퍼즐 등)
   - 3D 게임 (Pygame → Unity/Unreal)
   - 멀티플레이어 게임 (네트워킹)

3. **학습 심화**
   - 게임 디자인 이론
   - 고급 알고리즘 (A*, NavMesh)
   - 게임 최적화 기법

---

## 🎉 축하합니다!

Version 6까지 완료하면 **완전한 2D 서바이벌 게임**을 만든 것입니다!

이 경험은:
- pygame 마스터
- 게임 개발 전반적 이해
- 프로젝트 관리 능력
- 문제 해결 능력

을 모두 향상시켰을 것입니다.

**Happy Coding! 🎮**
