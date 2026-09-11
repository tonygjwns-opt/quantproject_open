# 결정 기록 (Decision Log)

프로젝트의 엔지니어링 결정과 그 이유를 짧게 남긴다. 독자용 서술은 블로그에, 여기엔 **무엇을 · 왜 · 대안**만. 구현 상세는 코드·테스트가 원본이므로 중복하지 않는다.

---

## 2026-07-19 · S0 프로젝트 셋업 구성

- **결정**: `pip + venv + requirements` / `src-layout` / `setuptools` / MIT / 패키지명 `portoptim`(레포명 `quantproject_open`과 독립).
- **이유**: 학습·기록용이라 설명거리가 적고 투명한 도구가 낫다. src-layout는 테스트가 *설치된* 패키지를 import하게 강제해 "로컬에선 되는데 배포하면 깨지는" 사고를 막는다.
- **대안**: poetry/uv(자동 락이지만 설명거리 많음), flat-layout.
- **관련**: 커밋 `23f7ebc`, 블로그 「퀀트 엔진 짓기 #0」.

## 2026-07-19 · S1 DB = Supabase (호스팅 Postgres)

- **결정**: 호스팅 Postgres(Supabase), **Session pooler(포트 5432)** 접속, 접근은 **SQLAlchemy Core**. 저장 계층은 나중에 교체 가능하도록 여지를 둠.
- **이유**: "PC 꺼도 매일 수집"은 *항상 켜진 컴퓨트(GitHub Actions) + 공유 저장소*를 뜻한다 → 클라우드가 쓰는 저장소는 로컬 DuckDB가 될 수 없다. 유니버스가 작아 네트워크·용량 부담이 적고, 웹 트랙에 Auth·API 내장이 유리.
- **대안**: DuckDB/parquet(로컬·빠르나 공유 저장소로 부적합 → 로컬 분석용 옵션으로 남김), Neon(순수 PG), 로컬 Docker PG(서버 관리 부담).
- **함정**: Direct(IPv6 전용)·Transaction pooler(6543, `pgbouncer` psycopg3 비호환)는 피함 → Session pooler 5432. `normalize_url`이 `pgbouncer` 파라미터를 걸러냄.
- **관련**: 커밋 `8f98b7c`, 블로그 「퀀트 엔진 짓기 #0」.

## 2026-07-19 · S2 데이터 소스 = 인터페이스 뒤 pluggable, 시작 pykrx + Tiingo

- **결정**: 소스를 인터페이스(**ABC `PriceSource`**) 뒤에 두고 시장별 어댑터를 교체한다. 시작 어댑터 = **pykrx**(한국, KRX 원천·무료) + **Tiingo**(미국·지역 ETF, 무료 티어·조정가 품질). 표준 출력 스키마 = `date/ticker/open/high/low/close/adj_close/volume/source`(long). raw→표준형 변환은 순수함수로 분리해 테스트.
- **이유**: 한·미·글로벌 + 조정가 + 재무를 *단일 무료 소스*로 다 만족하는 곳이 없다(리서치 결론). 인터페이스로 두면 소스 교체가 어댑터 내부로 국소화된다. ABC는 타입체커 없이도 계약을 런타임에 강제한다.
- **대안**: yfinance 단일(비공식·`429` 레이트리밋·재무 부실로 배제), 함수+레지스트리(가볍지만 상태 많은 소스 확장에 불리), Protocol(정적 검사에 타입체커 필요).
- **업그레이드 경로**: 재무가 필요해지는 S6에서 **EODHD**(`.KO/.KQ` 한국 + 미국 + 글로벌 EOD + 재무, $19.99~$99.99/월)로 어댑터 추가.
- **공통 함정**: 한국 수정주가는 배당 미반영(total-return은 배당으로 별도 보정 필요). EODHD도 OHLC는 원본·`adjusted_close`만 완전조정.
- **관련**: 데이터 소스 비교 리서치(본 세션), 블로그(예정).

## 2026-09-11 · S2 한국 소스 재검토 (미결)

- **상황**: 시작 소스로 pykrx(한국)+Tiingo(미국)를 정했으나, pykrx **실측**에서 KRX가 연속 호출에 빈 응답(rate-limit)을 주고 ETF 조회가 현재 에러(`'isin'`/`KeyError('시장')`). 반면 **FDR(finance-datareader)은 한국 주식+ETF, 미국 주식+ETF를 한 번에 정상 취득**(자격증명·throttle 없음). 미국은 야후, 한국은 네이버 소스.
- **후보**: (A) **FDR로 한국 소스 변경** — 실용·ETF 됨, 정밀도 pykrx보다 약간↓(거래량 미조정 이슈, 별도 adj_close 없음). (B) **pykrx 유지 + throttle/retry + KRX 로그인**(KRX_ID/PW 자격증명). (C) 하이브리드 pykrx(주식)+FDR(ETF).
- **미결** — 재개 시 먼저 결정. 미국=Tiingo, 인터페이스=ABC `PriceSource`, 표준 스키마는 유지. 진지한 정밀도는 나중 EODHD 업그레이드로 보완 가능.
