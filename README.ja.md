# Meridian Clock

[English](README.md) | [简体中文](README.zh-CN.md) | 日本語 | [한국어](README.ko.md)

[変更履歴](CHANGELOG.md)

世界の時間を、ひとつの画面に。Meridian Clock は、各都市の時刻を確認し、タイムゾーンをまたぐ予定を立てるためのデスクトップ世界時計です。

日付と時刻の変換にも対応しています。現在は開発初期段階で、正確で使いやすく、洗練されたデスクトップアプリを目指しています。アプリの表示言語は現在中国語です。この文書の日本語化は、アプリの日本語対応を意味するものではありません。

## 主な機能

- 時刻、日付、UTC オフセットを表示する時計カードを毎秒更新。
- 元の日時やタイムゾーンを変更すると、変換結果を自動更新。
- 時計カードの追加、削除、一括削除。
- 時計追加時に全タイムゾーンを検索可能。中国語の表示名を 32 件収録。
- 時計一覧とウィンドウの位置・サイズを保存し、次回起動時に復元。
- アカウントやネット接続なしでローカル動作。

初回起動時は北京、UTC、ロンドン、ニューヨーク、ロサンゼルスの時計を表示します。変換画面では、設定ファイルに登録されたよく使うタイムゾーンを選択できます。

## 起動方法

Python 環境と依存関係は uv で管理します。`.python-version` で Python 3.13 を指定し、`uv.lock` で依存関係のバージョンを固定しています。

プロジェクトのルートディレクトリで実行してください。

```bash
uv sync --locked
uv run python main.py
```

実行時の依存関係は `pyproject.toml` の `[project.dependencies]`、開発ツールは `[dependency-groups].dev` に定義されています。

```bash
# 実行時の依存関係を追加
uv add PACKAGE
# 開発用の依存関係を追加
uv add --dev PACKAGE
# ロックされた依存関係を更新
uv lock --upgrade
```

## 使い方

左側のパネルで都市を検索して時計を追加します。中国語の表示名、または英語のタイムゾーン識別子で検索できます。カードの × を押すと削除でき、一括削除ボタンですべての時計を削除できます。

右側のパネルでは、変換元のタイムゾーンと日時、変換先のタイムゾーンを選択します。結果は自動で更新されます。「使用当前时间」ボタンは、変換元として選んだタイムゾーンの現在時刻を入力します。

時計一覧は変更時に、ウィンドウの位置とサイズは終了時に、Qt の設定機構を通じてローカルに保存します。

## プロジェクト構成

```text
.
├── main.py                           # 起動処理
├── pyproject.toml                    # メタデータと依存関係
├── uv.lock                           # 依存関係のロックファイル
├── .python-version                   # Python バージョン
├── packaging/                        # アプリとインストーラーの構築設定
├── scripts/                          # 各 OS のビルドスクリプト
├── config/
│   ├── timezones.json                # よく使うタイムゾーンと表示名
│   └── default_timezones.json        # 初回表示する時計
├── src/
│   ├── core/
│   │   ├── settings.py               # ユーザー設定
│   │   └── timezone_manager.py       # 設定読み込みと時刻計算
│   └── ui/
│       ├── theme.py                  # 共通テーマ
│       ├── main_window.py            # メインウィンドウ
│       ├── timezone_display_panel.py # 時計選択とグリッド
│       ├── timezone_widget.py        # 時計カード
│       └── converter_widget.py       # 日時変換画面
└── tests/
    └── test_clocks.py                # 時刻計算と GUI の回帰テスト
```

## 設定

`config/timezones.json` の `common_timezones` 配列を編集します。

- `id`：`Asia/Shanghai` などの pytz タイムゾーン識別子。
- `display_name`：画面に表示する名前。
- `description`：説明用の情報。現在は画面で使用していません。
- `utc_offset`：説明用の情報で、計算には使用しません。実際のオフセットは pytz から取得します。

`config/default_timezones.json` で初回起動時の時計を変更できます。保存済みのユーザー設定がある場合は、そちらを優先します。設定ファイルを編集した後はアプリを再起動してください。

## 開発状況

世界時計の計算、時計の追加、変換先の時刻表示、現在時刻の入力処理は修正済みです。

夏時間の切り替えにより存在しない時刻や、二度現れる時刻を入力すると、説明を表示して変換結果を無効にします。二度現れる時刻のどちらを使うかは、まだ指定できません。切り替え区間外の時刻を選んでください。

カードの列数は表示領域に応じて変わります。幅の狭いウィンドウではメインパネルを縦に並べます。テーマとユーザー設定は独立したモジュールで管理しています。最新のレイアウトとビルド設定は検証待ちです。

テストの実行：

```bash
uv run python -m unittest discover -s tests -v
```

現在時刻の精度、日付をまたぐ変換、夏時間の境界、変換エラーからの復帰、空の一覧を含む時計一覧の保存を対象にしています。

## ロードマップ

- [x] 時刻計算、変換表示、時計追加の修正。
- [x] タイムゾーン変換と夏時間の回帰テスト。
- [x] 時計検索、時計一覧とウィンドウ設定の保存。
- [x] 可変列数のカードレイアウトと共通テーマ。
- [ ] キーボード操作、アクセシビリティ、多言語対応の改善。
- [x] Windows、macOS、Linux のビルドスクリプト。
- [ ] 配布パッケージの検証と公開。

## デスクトップアプリのビルド

```powershell
# Windows：単独で動作するアプリのフォルダー
powershell -ExecutionPolicy Bypass -File scripts/build-windows.ps1
# Windows：インストーラー（Inno Setup 6 が必要）
powershell -ExecutionPolicy Bypass -File scripts/build-windows.ps1 -Installer
```

```bash
# macOS 上で .app と .dmg を生成
bash scripts/build-macos.sh
# Linux 上でアプリのフォルダーと .tar.gz を生成
bash scripts/build-linux.sh
```

対象の OS 上でビルドしてください。生成物は `dist/` に出力します。スクリプトはパッケージ化の前にテストを実行します。最新の変更については、まだビルドを実行していません。詳細は[ビルド設定の説明（中国語）](packaging/README.md)を参照してください。コード署名と macOS の公証は未設定です。

## コントリビュート

不具合報告、提案、プルリクエストを歓迎します。時刻に関する不具合では、システムのタイムゾーン、変換元と変換先のタイムゾーン、再現できる日時を記載してください。

## ライセンス

[MIT ライセンス](LICENSE)で公開しています。

## スター履歴

[![Star History Chart](https://api.star-history.com/svg?repos=celynnmoonlight/meridian-clock&type=Date)](https://star-history.com/#celynnmoonlight/meridian-clock&Date)

## 作者へのお問い合わせ

ご質問、ご意見、共同開発のご相談は、以下のメールアドレスまでご連絡ください。

- 作者: [Hachimi Moonlight (@celynnmoonlight)](https://github.com/celynnmoonlight)
- メール： [lynnxu2025@gmail.com](mailto:lynnxu2025@gmail.com)
