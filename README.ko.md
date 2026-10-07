<!-- markdownlint-disable MD013 MD024 -->

# Meridian Clock

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | 한국어

[변경 이력](CHANGELOG.md)

세계의 시간을 한 화면에서 확인하세요. Meridian Clock은 여러 도시의 현재 시간을 살펴보고 시간대를 넘나드는 일정을 계획할 수 있는 데스크톱 세계 시계입니다.

시간대 간 날짜와 시간 변환도 지원합니다. 현재 초기 개발 단계이며, 정확하고 편리하면서도 완성도 높은 데스크톱 앱을 목표로 합니다. 앱의 현재 표시 언어는 중국어입니다. 이 한국어 문서가 앱의 한국어 지원을 의미하지는 않습니다.

## 주요 기능

- 시간, 날짜, UTC 오프셋을 표시하는 시계 카드를 매초 갱신합니다.
- 원본 날짜와 시간 또는 시간대를 변경하면 변환 결과를 자동으로 갱신합니다.
- 시계 카드를 추가하거나 삭제하고, 전체 시계를 한 번에 지울 수 있습니다.
- 시계 추가 시 전체 시간대 목록을 검색할 수 있으며 중국어 표시 이름 32개를 제공합니다.
- 시계 목록과 창 위치 및 크기를 저장하고 다음 실행 시 복원합니다.
- 계정이나 인터넷 연결 없이 로컬에서 실행됩니다.

처음 실행하면 베이징, UTC, 런던, 뉴욕, 로스앤젤레스 시계를 표시합니다. 변환 화면에서는 설정 파일에 등록된 자주 쓰는 시간대를 선택할 수 있습니다.

## 시작하기

Python 환경과 의존성은 uv로 관리합니다. `.python-version`에서 Python 3.13을 지정하고 `uv.lock`으로 의존성 버전을 고정합니다.

프로젝트 루트 디렉터리에서 실행하세요.

```bash
uv sync --locked
uv run python main.py
```

실행 의존성은 `pyproject.toml`의 `[project.dependencies]`에, 개발 도구는 `[dependency-groups].dev`에 정의되어 있습니다.

```bash
# 실행 의존성 추가
uv add PACKAGE
# 개발 의존성 추가
uv add --dev PACKAGE
# 잠긴 의존성 버전 업데이트
uv lock --upgrade
```

## 사용 방법

왼쪽 패널에서 도시를 검색하고 시계를 추가합니다. 중국어 표시 이름이나 영어 시간대 식별자로 검색할 수 있습니다. 카드의 × 버튼을 누르면 해당 시계를 삭제하며, 전체 삭제 버튼으로 모든 시계를 지울 수 있습니다.

오른쪽 패널에서 원본 시간대와 날짜 및 시간을 입력하고 대상 시간대를 선택합니다. 결과는 자동으로 갱신됩니다. “使用当前时间” 버튼을 누르면 선택한 원본 시간대의 현재 시간이 입력됩니다.

시계 목록은 변경 시 저장하며, 창 위치와 크기는 종료 시 Qt 설정 기능을 통해 로컬에 저장합니다.

## 프로젝트 구조

```text
.
├── main.py                           # 앱 진입점
├── pyproject.toml                    # 메타데이터와 의존성 그룹
├── uv.lock                           # 의존성 잠금 파일
├── .python-version                   # Python 버전
├── packaging/                        # 앱 및 설치 프로그램 빌드 설정
├── scripts/                          # 운영체제별 빌드 스크립트
├── config/
│   ├── timezones.json                # 자주 쓰는 시간대와 표시 이름
│   └── default_timezones.json        # 최초 시계 목록
├── src/
│   ├── core/
│   │   ├── settings.py               # 사용자 설정
│   │   └── timezone_manager.py       # 설정 로딩과 시간대 계산
│   └── ui/
│       ├── theme.py                  # 공통 테마
│       ├── main_window.py            # 메인 창
│       ├── timezone_display_panel.py # 시계 선택과 그리드
│       ├── timezone_widget.py        # 개별 시계 카드
│       └── converter_widget.py       # 날짜 및 시간 변환 화면
└── tests/
    └── test_clocks.py                # 시간 계산 및 GUI 회귀 테스트
```

## 설정

`config/timezones.json`의 `common_timezones` 배열을 수정하세요.

- `id`: `Asia/Shanghai`와 같은 pytz 시간대 식별자입니다.
- `display_name`: 화면에 표시할 이름입니다.
- `description`: 설명용 정보이며 현재 화면에서는 사용하지 않습니다.
- `utc_offset`: 설명용 정보로, 계산에는 사용하지 않습니다. 실제 오프셋은 pytz에서 가져옵니다.

`config/default_timezones.json`에서 최초 실행 시 표시할 시계를 변경할 수 있습니다. 저장된 사용자 설정이 있으면 해당 설정이 우선합니다. 설정 파일을 수정한 뒤에는 앱을 다시 실행하세요.

## 개발 현황

세계 시계 계산, 시계 추가, 대상 시간 표시, 현재 시간 입력 기능의 문제를 수정했습니다.

서머타임 전환으로 존재하지 않거나 두 번 나타나는 현지 시간을 입력하면 안내 메시지를 표시하고 결과를 비활성화합니다. 중복 시간의 첫 번째 또는 두 번째 시점을 지정하는 기능은 아직 없습니다. 전환 구간 밖의 시간을 선택하세요.

카드 열 수는 사용 가능한 너비에 따라 바뀌며, 좁은 창에서는 메인 패널을 위아래로 배치합니다. 테마와 사용자 설정은 별도 모듈로 관리합니다. 최신 레이아웃과 빌드 설정 변경 사항은 검증 대기 중입니다.

테스트 실행:

```bash
uv run python -m unittest discover -s tests -v
```

현재 시간 정확도, 날짜를 넘기는 변환, 서머타임 경계, 변환 오류 후 복구, 빈 목록을 포함한 시계 목록 저장을 다룹니다.

## 로드맵

- [x] 시간 계산, 변환 표시, 시계 추가 문제 수정.
- [x] 시간대 변환 및 서머타임 회귀 테스트 추가.
- [x] 시계 검색, 시계 목록 및 창 설정 저장.
- [x] 너비에 맞춰 바뀌는 카드 레이아웃과 공통 테마.
- [ ] 키보드 조작, 접근성, 다국어 지원 개선.
- [x] Windows, macOS, Linux 빌드 스크립트 추가.
- [ ] 배포 패키지 검증 및 공개.

## 데스크톱 앱 빌드

```powershell
# Windows: 독립 실행 앱 폴더
powershell -ExecutionPolicy Bypass -File scripts/build-windows.ps1
# Windows: 설치 프로그램(Inno Setup 6 필요)
powershell -ExecutionPolicy Bypass -File scripts/build-windows.ps1 -Installer
```

```bash
# macOS에서 .app 및 .dmg 생성
bash scripts/build-macos.sh
# Linux에서 앱 폴더 및 .tar.gz 생성
bash scripts/build-linux.sh
```

대상 운영체제에서 빌드해야 합니다. 결과물은 `dist/`에 생성됩니다. 스크립트는 패키징 전에 테스트를 실행합니다. 최신 변경 사항에 대해서는 아직 빌드를 실행하지 않았습니다. 자세한 내용은 [빌드 설정 안내(중국어)](packaging/README.md)를 참고하세요. 코드 서명과 macOS 공증은 설정되어 있지 않습니다.

## 기여하기

버그 제보, 제안, 풀 리퀘스트를 환영합니다. 시간 관련 문제를 보고할 때는 시스템 시간대, 원본 및 대상 시간대, 재현 가능한 날짜와 시간을 함께 알려 주세요.

## 라이선스

[MIT 라이선스](LICENSE)로 배포됩니다.

## 스타 기록

[![Star History Chart](https://api.star-history.com/svg?repos=celynnmoonlight/meridian-clock&type=Date)](https://star-history.com/#celynnmoonlight/meridian-clock&Date)

## 작성자 연락처

질문, 의견 또는 협업 제안은 아래 이메일로 연락해 주세요.

- 작성자: [Hachimi Moonlight (@celynnmoonlight)](https://github.com/celynnmoonlight)
- 이메일: [lynnxu2025@gmail.com](mailto:lynnxu2025@gmail.com)
