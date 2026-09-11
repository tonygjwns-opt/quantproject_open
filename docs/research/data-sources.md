# 데이터 소스 비교 리서치 (2026-09, 내부 근거 자료)

S2(데이터 취득)의 소스 선택 근거. 블로그용 원재료이자 결정 로그(`../decisions.md`)의 상세 뒷받침. 가격·무료한도·커버리지는 자주 바뀌므로 채택 전 대상 티커로 재검증할 것.

## 맥락 / 우리 요구

- 유니버스: 전종목 아님 — 각국·섹터 ETF + 대형주 + 섹터 주도주(한·미·기타). 소수(수십~수백).
- 필요: 일봉 EOD OHLCV + 조정가(배당·분할) + 배당/분할 이벤트, 그리고 (S6) 재무제표.
- 제약: "PC 꺼도 매일 수집" → 클라우드(GitHub Actions)가 쓰고 공유 저장소(Supabase)에 적재. 무료 선호, 파이썬.

## 비교 기준

커버리지(US/KR/기타·ETF) · 가격데이터(OHLCV·조정·이벤트) · 재무 · 품질/조정정확도 · 이력길이 · 파이썬 접근성 · 무료한도/가격 · 공식성·안정성 · 레이트리밋 · 우리 규모 실용성.

## 종합 비교표

| Provider | 한국주식 | 미국 | 기타글로벌 | 조정가 | 재무제표 | 파이썬 | 비용 |
|---|---|---|---|---|---|---|---|
| yfinance | ○ `.KS/.KQ` | ◎ | ○ | ○(조정+배당/분할) | △ 짧고 결측 | ◎ 표준 | 무료(비공식·429 리스크) |
| Stooq | ? 불확실 | ○ | ○(EU중심) | △ 조정종가만 | ✗ | △ datareader | 무료 |
| Tiingo | ? 약함 | ◎ 고품질 | △ | ◎ | ○(US) | ○ | 무료 50/h·유료 $30/mo |
| Alpha Vantage | ✗ | ○ | △ | 유료전용 | ○(US) | ○ | 무료 25/일(빡셈) |
| Polygon(Massive) | ✗ | ◎ 최상 | ✗ | ○(분할) | ○(US) | ◎ 공식 | 무료 5/분·$29+/mo |
| FMP | △ 상위티어·미검증 | ◎ | ○ 상위티어 | ◎ | ◎ 강점(US·EU) | ○ | 무료 250/일·$15~149/mo |
| EODHD | ◎ `.KO/.KQ`+ETF | ◎ | ◎ 70+거래소 | △ `adjusted_close`만 | ◎ US완전·KR미검증 | ○ 공식 | $19.99(EOD)~$99.99(EOD+재무) |
| pykrx | ◎ KRX 원천 | ✗ | ✗ | ○(자본변동, 배당X) | △ PER/PBR/배당(재무제표X) | ◎ | 무료 |
| FDR | ○(정밀도 pykrx↓) | ○(야후) | ○ | 한국△/미국○ | ○(네이버·미검증) | ◎ 단순 | 무료 |

## provider별 요점

### yfinance (Yahoo, 비공식)
- 커버: 미국·글로벌 광범위, 한국 `.KS`(KOSPI)/`.KQ`(KOSDAQ), 지수 `^KS11`. 지역 ETF는 대부분 미국상장(EWY 등).
- 가격: `.history(auto_adjust=True)` 기본 조정. 배당/분할 `.dividends/.splits/.actions`. (2024~25 `download()`의 Adj Close 동작 변경 — 코드 확인 필요.)
- 재무: `.income_stmt/.balance_sheet/.cashflow` 있으나 이력 짧고 결측 잦음 → 보조/불신.
- 약점: 비공식 스크래핑, 2025년부터 `429 Too Many Requests` 빈발 → 캐싱·백오프 필수. 필드가 조용히 바뀜.

### Stooq
- 커버: 미국·EU·일부 글로벌. 한국 커버리지 불확실. 조정종가만(비조정 없음). 배당/분할 이벤트 불명확. 재무 사실상 없음.
- 위치: 미국·EU EOD의 2차 검증/백업용. 단독 주소스 부적합. 공식 API 없음(CSV/datareader).

### Tiingo
- 커버: US·중국·ADR 중심 108k+ 증권, ETF·뮤추얼펀드 강함. 한국 개별주 불확실(미국상장 한국 ETF는 커버).
- 가격: EOD 조정/비조정, 배당·분할 API 별도. CRSP 준수, 품질 평판 좋음.
- 재무: US 중심(무료 5년/유료 15년+). 한국 재무 사실상 미지원 추정.
- 무료: 시간당 50 req, 일 1,000, 월 500 심볼(재무·뉴스 제외). 유료 Power $30/mo(개인).
- 위치: **미국 축 기본 소스로 유력.** 한국·글로벌 재무는 약함.

### Alpha Vantage
- 커버: 글로벌 100k+, 단 한국 KRX 미지원(불확실). 조정 일봉은 프리미엄 전용. 재무(손익/재무상태/현금흐름) US 중심.
- 무료: **일 25 req / 분 5**(매우 빡빡) → 소수라도 매일 돌리기엔 사실상 유료 전제. 프리미엄 $50~250/mo.
- 위치: 우리 유니버스(한국 포함)엔 취약. 보조/특정목적.

### Polygon.io (현 Massive.com 리브랜딩)
- 커버: **주식은 미국 전용**(한국·글로벌 주식 없음). 미국 정확도·인프라 최상급(SIP 직결). ETF·미국지수 포함.
- 가격: aggregates OHLCV, `adjusted`(분할). 배당/분할 reference 별도. Flat Files(S3 bulk).
- 재무: 미국만(SEC EDGAR 10-K/10-Q). 무료 5/분.
- 위치: 미국 전용 보조. 다지역 유니버스 단독 불가.

### FMP (Financial Modeling Prep)
- 커버: 글로벌 70k+, 40~70 거래소. 한국은 상위티어(Ultimate)·명시 미확인(불확실).
- 가격: EOD, 분할조정/배당+분할조정/비조정 각각 엔드포인트. 배당/분할 이벤트.
- 재무: **강점**(손익/재무상태/현금흐름·비율·밸류에이션). As-Reported는 미국만, 국제 표준화 재무는 신흥국·소형주 갭 가능.
- 무료: 250 req/일. 유료 Starter~Ultimate $15~149/mo(변동, 재확인). Premium+ Bulk Download.
- 위치: **US+KR+글로벌 EOD+재무를 단일 API**로 → 다지역에 현실적. 단 한국 커버·정확도는 무료로 실측 검증 권장.

### EODHD (유료 고품질, 진지 업그레이드 후보)
- 커버: 70+ 거래소 150k+ 티커. **한국 확정 지원** — `.KO`(KOSPI, ~2,093) `.KQ`(KOSDAQ, ~1,846), 한국 ETF 포함(예 `005930.KO`, `035900.KQ`). 미국 `US` 통합.
- 가격: EOD. **OHLC는 원본, `adjusted_close`만 분할+배당 완전조정**(볼륨은 분할만). CRSP 방식. 상폐/생존편향 데이터 제공.
- 재무: 3표+밸류에이션+추정치. US 완전(~1985), 비US·한국 대체로 ~2000. **한국 재무 이력 깊이·필드 충실도는 독립검증 없음 → 대상 티커로 확인 권장.** ETF 펀더멘털도.
- 가격 플랜(2026, 개인): Free 20/일·EOD 1년만. **EOD All World $19.99/mo(재무 없음)**. Fundamentals $59.99. **ALL-IN-ONE $99.99/mo(연 ~$83, EOD+실시간+재무)**. 콜 가중치: EOD 1, 펀더멘털 10, Bulk 100. 분당 1,000/일 100k.
- 파이썬: 공식 `eodhd`(pip, pandas) 또는 REST+requests. 평판 Trustpilot ~4점, 가성비·bulk 강점.
- 위치: **한국까지 커버하며 EOD+재무를 월 $20~100대에** → 진지 업그레이드 경로로 적합. 유의: adjusted_close만 조정, 한국 재무 깊이 사전검증, 개인=비상업용.

### pykrx (한국, KRX 원천, 무료)
- 커버: 한국 전용(KOSPI/KOSDAQ/KONEX 주식·ETF·지수). 미국 없음.
- 가격: `get_market_ohlcv(adjusted=True)` 수정주가(자본변동만, 배당X). 펀더멘털 `get_market_fundamental`(PER/PBR/EPS/BPS/DIV/DPS) — **전체 재무제표는 없음**.
- 출처: KRX 공식 + 수정주가는 네이버. 정확도 평판 좋음(커뮤니티 표준). 비공식 스크래핑.
- 레이트리밋: KRX가 연속 호출에 강하게 제한 → `time.sleep` 권장. **최근 일부 데이터에 KRX 로그인(KRX_ID/KRX_PW) 요구 정황.**

### FinanceDataReader / FDR (무료 wrapper)
- 커버: **글로벌** — 한국(KRX)·미국(NASDAQ/NYSE)·중국·홍콩·일본·베트남, ETF·지수·환율·크립토. `fdr.DataReader('005930', ...)` 한 줄.
- 가격: 미국은 야후 Adj Close. **한국은 네이버 — 수정주가지만 거래량 미조정 이슈(#85), 별도 Adj Close 없음, 배당 미반영.**
- 재무: `SnapDataReader`로 네이버 재무제표 가능(커버·안정성 불확실).
- 위치: 다국가를 한 API로. 한국 정밀도는 pykrx보다 한 수 아래.

## 실측 메모 (2026-09-11, 이 기기에서 직접 호출)

- **pykrx**: `get_market_ohlcv(adjusted=True)` 005930 → 정상(시가/고가/저가/종가/거래량/등락률, index 날짜). 그러나 여러 호출 뒤 `adjusted=False`·펀더멘털·시가총액·종목리스트·ETF가 **빈 응답("Expecting value")** — KRX rate-limit 정황. **ETF는 별도 에러**(`'isin'`, `KeyError('시장')`). "KRX 로그인 실패: KRX_ID/KRX_PW 미설정" 경고 반복.
- **FDR**: `DataReader`로 **KR 주식(005930)·KR ETF(069500)·US(AAPL)·US ETF(SPY) 모두 한 번에 정상** 취득, throttle·키 없음. KR 컬럼 Open/High/Low/Close/Volume/Change, US는 +Adj Close.

## 핵심 결론

1. 단일 무료 소스로 한·미·글로벌 + 조정가 + 재무를 다 만족하는 곳은 없다.
2. 한국 정밀도: pykrx(KRX 직접) > FDR/yfinance. 미국 순수 EOD 품질: Tiingo·Polygon 최상.
3. 재무는 무료권이 부실(특히 한국) → 제대로면 EODHD/FMP 유료.
4. **EODHD가 유일하게 한국(개별주+ETF)+미국+글로벌 EOD+재무를 한 구독($20~$100/mo)** → 진지 업그레이드 경로.
5. 공통 함정: 한국 수정주가는 배당 미반영(total-return은 배당 별도 보정). EODHD도 OHLC 원본·adjusted_close만 완전조정.

## 결정(요약) — 상세는 ../decisions.md

- 소스는 인터페이스(ABC `PriceSource`) 뒤에 두고 시장별 교체.
- 미국 = Tiingo(무료·품질). 한국 = **미결**(pykrx 실측 문제 vs FDR 즉시 동작). 재무 필요 시(S6) EODHD 업그레이드.

## 참고 URL

**yfinance**: https://pypi.org/project/yfinance/ · Adj Close 변경 https://medium.com/@josue.monte/why-adj-close-disappeared-in-yfinance-and-how-to-adapt-6baebf1939f6 · 429 이슈 https://github.com/ranaroussi/yfinance/issues/2125 · 가이드 https://scrapfly.io/blog/posts/guide-to-yahoo-finance-api
**Stooq**: https://www.quantstart.com/articles/an-introduction-to-stooq-pricing-data/ · https://stooq.com/db/h/ · https://pydata.github.io/pandas-datareader/readers/stooq.html · 이슈 https://github.com/pydata/pandas-datareader/issues/594
**Tiingo**: 가격 https://www.tiingo.com/about/pricing · 배당 https://www.tiingo.com/documentation/corporate-actions/dividends · 분할 https://www.tiingo.com/documentation/corporate-actions/splits · lib https://github.com/hydrosquall/tiingo-python · 리뷰 https://www.quantstart.com/articles/evaluating-data-coverage-with-tiingo/
**Alpha Vantage**: 문서 https://www.alphavantage.co/documentation/ · 프리미엄 https://www.alphavantage.co/premium/ · lib https://github.com/RomelTorres/alpha_vantage · 비교 https://dev.to/pickuma/alpha-vantage-vs-yahoo-finance-api-free-market-data-for-side-projects-an-honest-comparison-411o
**Polygon/Massive**: 심볼범위 https://polygon.io/knowledge-base/article/what-symbols-exchanges-are-included-in-polygons-data · 이력 https://polygon.io/knowledge-base/article/how-much-historical-stock-data-does-polygon-have · 재무 https://polygon.io/knowledge-base/article/how-much-historical-data-does-polygon-have-for-financial-10k-and-10q-reports · lib https://polygon.readthedocs.io/
**FMP**: 가격 https://site.financialmodelingprep.com/pricing-plans · 조정 EOD https://site.financialmodelingprep.com/developer/docs/stable/historical-price-eod-dividend-adjusted · 거래소 https://site.financialmodelingprep.com/developer/docs/stable/available-exchanges · 적합성 https://site.financialmodelingprep.com/education/data/when-financial-modeling-prep-is-the-right-tool--and-when-it-isnt · lib https://github.com/daxm/fmpsdk
**EODHD**: 가격 https://eodhd.com/pricing · 한도/콜가중치 https://eodhd.com/financial-apis/api-limits · 거래소 https://eodhd.com/list-of-stock-markets · KOSPI https://eodhd.com/exchange/KO · KOSDAQ https://eodhd.com/exchange/KQ · 조정가 설명 https://eodhd.com/financial-academy/financial-faq/adjusted-close-and-close-whats-the-difference · 상폐 https://eodhd.com/financial-apis/delisted-stock-companies-data · 펀더멘털 https://eodhd.com/financial-apis/stock-etfs-fundamental-data-feeds · 한국 재무 실사례 https://eodhd.com/financial-summary/035900.KQ · lib https://pypi.org/project/eodhd/ · Trustpilot https://www.trustpilot.com/review/eodhd.com
**pykrx**: https://github.com/sharebook-kr/pykrx · https://pypi.org/project/pykrx/
**FDR**: https://github.com/FinanceData/FinanceDataReader · 가이드 https://financedata.github.io/posts/finance-data-reader-users-guide.html · 수정주가/거래량 이슈 #85 https://github.com/FinanceData/FinanceDataReader/issues/85
**비교 리뷰**: https://waylandz.com/quant-book-en/Data-Provider-Comparison/ · https://odemeridian.com/blog/data-apis-quant-finance

## 불확실 (채택 전 실측 필요)

- Tiingo·Alpha Vantage·FMP의 한국(KRX) 개별주·재무 실제 커버리지.
- EODHD 한국 재무 이력 깊이·필드 충실도, KOSPI/KOSDAQ 지수 시계열 편입.
- Stooq 한국 커버리지·배당/분할·비조정가 제공.
- 각 provider의 명시적 SLA, FMP/EODHD 최신 가격(재확인).
- pykrx 빈 응답이 순수 rate-limit인지 KRX 로그인 요구인지(쿨다운 후 재확인).
