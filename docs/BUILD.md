# 빌드 방법

## 준비물
- Python 3.10 이상, Pillow
- 원본 `Conker's Bad Fur Day (USA).z64` (README의 해시와 일치)
- 갈무리11 Bold: `tools/galmuri/Galmuri11-Bold.ttf`
- 번역 대본: `tools/tr/ko_0.txt`~`ko_3.txt`, `tools/tr/order.pkl`, `tools/tr/ko_extra.py`, `tools/kextra.py` (원문을 담고 있어 저장소에는 없습니다)

## 순서
1. `tools/` 를 원본 ROM이 있는 폴더의 하위 폴더로 둡니다. (`build.py` 는 `../Conker's Bad Fur Day (USA).z64` 를 읽습니다)
2. `cd tools && python build.py`
   - 세그먼트 6·26(레벨 대사)·28(메뉴·스태프롤) 재압축, 글꼴 블롭 기록, 부트 로더·코드 후크 삽입, CIC-6105 체크섬 재계산
   - 결과: `../Conker's Bad Fur Day (Korean).z64`
3. 차분 생성: `xdelta3 -e -0 -s "Conker's Bad Fur Day (USA).z64" "Conker's Bad Fur Day (Korean).z64" Conker_BFD_KO_v1.0.xdelta`

## 보조 도구
| 파일 | 내용 |
| --- | --- |
| `pack.py` | RareZip(4바이트 길이 + raw deflate) 압축/해제, 오프셋 테이블 |
| `asm.py` | 후크 작성용 소형 MIPS 어셈블러 |
| `kcode.py`, `codepatch.py` | 글자 매핑·폭 계산·텍스처 후크, 게임 코드 4KB 청크 재압축 |
| `mkfont.py` | 갈무리 → I8 글리프(0xE0 바이트) 변환 |
| `crc6105.py` | CIC-6105 체크섬 |
| `export.py`, `lvl.py`, `seg.py` | 대사 추출·세그먼트 분석 |
| `leftover.py` | 패치 ROM에 남은 영어 대사 정적 검사 |
| `mdis.py`, `idis.py`, `xref.py`, `code.py`, `fontdec.py`, `mont.py` | 디스어셈블·참조 검색·글꼴 해독·스크린샷 몽타주 |
