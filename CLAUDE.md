# portoptim — Claude 작업 가이드 (인수인계 겸용)

새 세션(계정·기기 변경 포함)에서도 프로젝트를 이어가기 위한 단일 기준. **시작 시 이 파일과 `docs/decisions.md`를 먼저 읽는다.**

## 프로젝트

포트폴리오 최적화·백테스팅 퀀트 엔진 (학습/CV). 최종 목표: 매일 데이터 수집 → 알파 채굴 → 백테스트·검증 → (최후) 자동매매 + 전 과정 웹 대시보드.
파이프라인: **data → returns → metrics → optimizer → backtest → 검증.**
접근: 전체를 한 번에 짜지 않고, **균등가중(EW)으로 파이프라인을 끝까지 한 바퀴 관통해 돌아가는 뼈대**를 먼저 만든 뒤 살을 붙인다. 각 단계는 작게 쪼갠 함수 + 그 함수를 검증하는 테스트로 쌓는다.

## 저장소

- **공개(이 repo `quantproject_open`)**: 엔진·방법론·틀·검증·문서. 파이썬 패키지명은 `portoptim`(레포명과 독립).
- **비공개(`quantproject_closed`, 아직 없음)**: 실제 알파 로직·실거래 API·주문·계좌·운영·자격증명.
- **블로그**: Chirpy/GitHub Pages, repo `tonygjwns-opt.github.io`. `_drafts/`에 초안 → 검토 → `_posts/`로 옮겨 push = 발행. 파일명 `YYYY-MM-DD-제목.md`.

## 작업 방식 (반드시 지킬 것)

- **합의 전 코드·파일생성·commit·push 금지.** 제안·논의까지만; 사용자가 "진행/승인" 해야 실행.
- 한 번에 **아주 작은 한 스텝**. 앞서가지 않는다.
- **매 턴 끝에** 무엇을 했는지(생성/수정 파일·실행 명령·결과) 요약해 보여준다.
- 되돌리기 어려운/외부 공개 동작(commit·push·블로그 발행)은 **매번 승인**받고 진행.
- 사이클: 설계 논의·결정 → 승인 후 구현 → 검증(pytest + 눈) → 블로그 초안 → 검토·수정 → 발행 → 다음.
- 정확도 우선: 전제로 코드 짜지 말고 **실물로 검증**(예: 접속문자열·데이터 소스는 실제로 호출해 확인).

## 블로그 문체 규칙

- 극적 도입·뜸들이기·메타설명("튜토리얼이 아니라~")·훈계조 마무리("그래서 ~가 중요하다")·과장 강조("정답이었다") 금지.
- **"우리가/내가" 등 1인칭 주어 쓰지 않기.** 담백·직접·사실 위주.
- **함수 통짜 구현·검증 로그(pytest 카운트 등)를 글에 넣지 않기** — repo 코드(docstring)·테스트가 원본이고 글↔코드 상호링크로 연결.
- **내부 스텝 라벨(S0/S1/S2)을 독자용 글에 노출하지 않기.**
- 결정은 이 글과 `docs/decisions.md`에 병기. 피드백은 before→after 예시로 받는 게 정확.

## 개발 셋업

pip + venv + requirements, src-layout, setuptools (자세한 근거는 `docs/decisions.md`).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt -e .
pytest
```

## 자격증명 (.env — 커밋 안 됨, 새 환경에서 재작성 필요)

`.env.example`을 복사해 `.env`를 만들고 채운다.
- `DATABASE_URL` — Supabase **Session pooler(포트 5432)** 접속문자열. (Direct=IPv6·Transaction pooler=6543은 피함.)
- `TIINGO_API_KEY` — Tiingo 무료 키(미국 데이터, S2).

## 로드맵 (S# = 한 사이클)

- Phase0: S0 셋업 · S1 DB
- Phase1 데이터: S2 취득 · S3 전처리 · S4 저장(스키마·upsert) · S5 자동화 · S6 재무 · S7 품질·유니버스
- Phase2 분석기반: S8 returns · S9 metrics·risk · S10 inputs
- Phase3 알파: S11 시그널 인터페이스 · S12 평가 · S13 개별시그널(private) · S14 조합
- Phase4 포트폴리오: S15 optimizer(EW→MSR) · S16 regime · S17 allocation · S18 costs
- Phase5 검증: S19 backtest · S20 report·plot · S21 validation
- Phase6(비공개): S22 브로커API · S23 시그널→주문 · S24 킬스위치 · S25 운영
- 웹트랙: W1 데이터현황 · W2 백테스트결과 · W3 시그널탐색 · W4 운영모니터

## 현재 상태 (2026-09-11)

- **완료**: S0(셋업, 커밋 `23f7ebc`), S1(Supabase 연결·SQLAlchemy Core, `8f98b7c`). 블로그 「퀀트 엔진 짓기 #0」 발행됨.
- **진행 중: S2(데이터 취득).** 확정: 소스를 **ABC `PriceSource` 인터페이스** 뒤에 두고 시장별 어댑터 교체. 표준 출력 스키마 `date/ticker/open/high/low/close/adj_close/volume/source`(long). raw→표준형 변환은 순수함수로 분리해 테스트. **미국 소스 = Tiingo** 확정.
- **열린 결정 (재개 시 먼저 정할 것): 한국 소스.** 실측 결과 pykrx는 KRX가 연속 호출에 빈 응답(rate-limit)·ETF 조회 현재 에러; **FDR(finance-datareader)은 한국 주식+ETF+미국을 자격증명·throttle 없이 즉시 취득**(정밀도는 pykrx보다 약간↓). 상세·후보는 `docs/decisions.md` 참고.
- **다음**: 한국 소스 확정 → 인터페이스+어댑터 구현(순수 변환+테스트) → 데이터 소스 비교를 블로그로.
- **미커밋 로컬 상태**: `requirements.txt`에 pandas/pykrx가 잠정 추가돼 있을 수 있음(한국 소스 확정 후 정리). 기기 바뀌면 이 미커밋 변경은 사라지니 재개 시 requirements를 확정 소스에 맞춰 다시 세팅.

## 데이터 소스 요약 (리서치 결론)

전체 비교·근거·출처 URL은 **`docs/research/data-sources.md`** (블로그 원재료). 단일 무료 소스로 한·미·글로벌 + 조정가 + 재무를 다 만족하는 곳은 없음. 시장별 어댑터로 조합.
- 무료 시작: 한국=FDR 또는 pykrx / 미국=Tiingo(키 필요, 조정가 품질 좋음).
- 진지 업그레이드(재무 필요한 S6): **EODHD** — 한국(`.KO/.KQ`)+미국+글로벌 EOD+재무를 한 구독($19.99~$99.99).
- 공통 함정: 한국 수정주가는 배당 미반영(total-return은 배당 별도 보정). EODHD도 OHLC 원본·`adjusted_close`만 완전조정.
