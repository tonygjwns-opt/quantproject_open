# portoptim

포트폴리오 최적화·백테스팅을 위한 퀀트 엔진. 매일 데이터 수집 → 분석·알파 → 백테스트·검증까지의
전 과정을 작고 검증 가능한 단위로 쌓아 올리고, 각 단계를 블로그 글과 상호 링크한다.

## 공개 ↔ 비공개 경계

이 저장소(공개)는 **엔진과 방법론**만 담는다 — 데이터 골격, returns, metrics, optimizer,
backtest, 검증, 웹 틀, 예제, 테스트, 문서. 실제 알파 시그널 로직·실거래 API·주문·계좌·운영과
자격증명(`.env`)은 이 엔진을 import 하는 **별도의 비공개 저장소**에 둔다.

## 개발 환경

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt -e .
pytest
```

- `pyproject.toml` — 패키지 메타 · 빌드(setuptools) · src-layout 선언
- `requirements.txt` — 런타임 의존성
- `requirements-dev.txt` — 개발·검증 의존성(pytest 등)

## 상태

S0(프로젝트 셋업) 진행 중. 로드맵은 EW(균등가중)로 데이터→returns→metrics→optimizer→backtest를
한 바퀴 관통해 에쿼티 커브 한 장을 만드는 것부터 시작한다.

## 라이선스

[MIT](LICENSE)
