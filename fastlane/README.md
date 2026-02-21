fastlane documentation
----

# Installation

Make sure you have the latest version of the Xcode command line tools installed:

```sh
xcode-select --install
```

For _fastlane_ installation instructions, see [Installing _fastlane_](https://docs.fastlane.tools/#installing-fastlane)

# Available Actions

## iOS

### ios fetch_portfolio_data

```sh
[bundle exec] fastlane ios fetch_portfolio_data
```

ポートフォリオ用の全アプリメタデータを取得（カテゴリ、リリース日、更新日を含む）

### ios fetch_public_info

```sh
[bundle exec] fastlane ios fetch_public_info
```

App Store Lookup APIを使ってパブリック情報を取得

### ios generate_portfolio

```sh
[bundle exec] fastlane ios generate_portfolio
```

ポートフォリオ用の完全なデータセットを生成

----

This README.md is auto-generated and will be re-generated every time [_fastlane_](https://fastlane.tools) is run.

More information about _fastlane_ can be found on [fastlane.tools](https://fastlane.tools).

The documentation of _fastlane_ can be found on [docs.fastlane.tools](https://docs.fastlane.tools).
