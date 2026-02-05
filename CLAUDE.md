# CLAUDE.md - tsuzukit Webサイト要件書

## プロジェクト概要
個人開発者「tsuzukit」のWebサイト構築プロジェクト

## 基本情報
- **活動者名**: tsuzuki817
- **職種**: 個人開発者（エンジニア・デザイナー・クリエイター）
- **実績**: 30個以上のiOSアプリをApp Storeに公開
- **ホスティング**: GitHub Pages
- **技術スタック**: HTML + CSS（シンプル構成）

## サイトの主要機能・コンテンツ

### 1. ポートフォリオ
- 公開済みアプリ30個以上の紹介
- App Storeリンク
- アプリのスクリーンショット・説明
- 技術スタック・開発期間等の詳細

### 2. ブログ機能
- 開発に関する記事投稿
- 技術的な知見の共有
- アプリ開発の過程やTips

### 3. 法的文書ページ
iOSアプリからの参照用として以下のページを設置：
- **プライバシーポリシー**
- **利用規約**
- **特定商取引法に基づく表記**

### 4. iOSアプリとの連携
- 各アプリからの法的文書へのリンク先として機能
- アプリ紹介ページへの誘導

## 技術仕様

### プラットフォーム
- **ホスティング**: GitHub Pages
- **ドメイン**: GitHub標準ドメイン or カスタムドメイン
- **HTTPS**: GitHub Pages標準対応

### 技術スタック
- **フロントエンド**: HTML5 + CSS3（ファイル分割）
- **ファイル構成**: HTMLとCSSは分離してメンテナンス性を向上
- **レスポンシブ対応**: モバイルファーストデザイン
- **ブログ**: 静的サイトジェネレーター使用検討（Jekyll等）
- **バージョン管理**: Git/GitHub

## サイト構成案

```
tsuzuki817.github.io/
├── index.html              # トップページ
├── portfolio/              # ポートフォリオ
│   ├── index.html
│   └── apps/
│       ├── app1.html
│       └── ...
├── blog/                   # ブログ
│   ├── index.html
│   └── posts/
├── legal/                  # 法的文書
│   ├── privacy-policy.html
│   ├── terms-of-service.html
│   └── commercial-law.html
├── about/                  # プロフィール
│   └── index.html
├── contact/                # 連絡先
│   └── index.html
├── assets/                 # リソース
│   ├── css/
│   │   ├── style.css      # メインスタイル
│   │   ├── responsive.css # レスポンシブ対応
│   │   └── components.css # コンポーネント別スタイル
│   ├── js/
│   │   └── main.js        # JavaScript（必要に応じて）
│   └── images/
└── README.md
```

## コーディング規約・構成

### ファイル分割方針
- **HTML**: 各ページ別にファイル分割
- **CSS**: 機能別・用途別にファイル分割
  - `style.css`: 基本スタイル・共通レイアウト
  - `responsive.css`: レスポンシブ対応
  - `components.css`: コンポーネント別スタイル
- **JavaScript**: 必要最小限、外部ライブラリ依存を避ける


## SEO・パフォーマンス要件

### SEO対策
- メタタグの適切な設定
- 構造化データの実装
- sitemap.xmlの生成
- robots.txtの設置

### パフォーマンス
- 軽量なCSS/HTML
- 画像最適化
- GitHub Pagesの配信最適化

## 法的文書要件

### プライバシーポリシー
- 個人情報の取り扱い
- アプリでの情報収集について
- 第三者提供について
- お問い合わせ先

### 利用規約
- サービスの利用条件
- 禁止事項
- 責任の制限
- 規約の変更について

### 特定商取引法
- 事業者の氏名・住所
- 商品・サービスの価格
- 支払い方法・時期
- 返品・交換について

## 開発・運用計画

### Phase 1: 基本サイト構築
1. 基本的なHTML/CSS構造の作成
2. レスポンシブデザインの実装
3. GitHub Pagesでの公開

### Phase 2: コンテンツ充実
1. ポートフォリオページの作成
2. 法的文書ページの作成
3. プロフィール・連絡先ページ

### Phase 3: ブログ機能
1. ブログシステムの実装（Jekyll等）
2. 記事投稿機能
3. カテゴリー・タグ機能

### Phase 4: 最適化・改善
1. SEO対策の実装
2. パフォーマンス最適化
3. アクセス解析の導入

## 運用・保守

### 更新頻度
- **ポートフォリオ**: 新アプリリリース時
- **ブログ**: 月1-2回程度
- **法的文書**: 必要に応じて

### バックアップ・管理
- GitHubでのバージョン管理
- 定期的なコンテンツの見直し
- セキュリティアップデート対応

## 参考・検討事項

### 追加機能候補
- お問い合わせフォーム（外部サービス連携）
- RSS フィード
- ソーシャルメディア連携
- アプリダウンロード数表示（可能であれば）

### 外部サービス連携
- Google Analytics
- Search Console
- Social Media（Twitter, GitHub等）

---

**作成日**: 2025年6月26日  
**更新日**: 2025年6月26日  
**作成者**: Claude (Anthropic)  
**対象**: tsuzuki817 個人開発者サイト


## Google Analytics

以下は、このアカウントの Google タグです。このタグをコピーして、ウェブサイトのすべてのページのコード（<head> 要素の直後）に貼り付けます。各ページに複数の Google タグを実装することはできません。

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QERPQ1EGLH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-QERPQ1EGLH');
</script>

### 重要：新規ページ作成時の必須要件

**すべての新規HTMLページ（ブログ投稿、アプリ詳細ページ等）には、以下のGoogle Analyticsタグを必ず含める必要があります：**

1. **Faviconセクションの直後**に以下のGoogle Analyticsコードを挿入：

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-QERPQ1EGLH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-QERPQ1EGLH');
</script>
```

2. **対象となるページ：**
   - 新規ブログ記事（blog/posts/）
   - 新規アプリ詳細ページ（portfolio/apps/）
   - その他すべての新規HTMLページ

3. **配置場所：**
   - `<head>`セクション内
   - Faviconリンクの直後
   - `</head>`タグの前

**このタグの追加を忘れると、アクセス解析ができなくなるため、新規ページ作成時は必ず確認してください。**

## Google AdSense

以下のGoogle AdSenseコードをすべてのページの`<head>`セクションに含めてください。

```html
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8240751277462688"
    crossorigin="anonymous"></script>
```

### 重要：新規ページ作成時の必須要件

**すべての新規HTMLページには、Google Analyticsタグの直後にGoogle AdSenseコードを追加してください：**

1. **配置場所：**
   - `<head>`セクション内
   - Google Analyticsタグの直後
   - `</head>`タグの前

2. **対象となるページ：**
   - 新規ブログ記事（blog/posts/）
   - 新規アプリ詳細ページ（portfolio/apps/）
   - その他すべての新規HTMLページ

**このタグの追加を忘れると、広告が表示されなくなるため、新規ページ作成時は必ず確認してください。**

## 多言語対応要件

### サポート言語
現在サポートしている言語：
- **日本語** - デフォルト言語（パラメータなし）
- **英語** - `?lang=en` パラメータ
- **韓国語** - `?lang=ko` パラメータ

### 統一された多言語対応方針

**単一HTMLファイル + URLパラメータで多言語対応を実現：**

#### フォルダ構成
- すべてのコンテンツはルートディレクトリに配置
- `/en/` と `/ko/` フォルダは廃止（リダイレクト用のみ保持）
- 言語はURLパラメータ（`?lang=en`）で管理

#### 動的翻訳システム
1. **translations.js** - すべての翻訳テキストを一元管理
2. **language-manager.js** - 言語切り替えと翻訳適用を管理
3. **data-i18n属性** - HTML要素に翻訳キーを指定

#### 実装方法
```html
<!-- HTMLファイル -->
<h1 data-i18n="portfolio.title">Portfolio</h1>
<p data-i18n="portfolio.description">説明文</p>

<!-- スクリプト読み込み -->
<script src="assets/js/translations.js"></script>
<script src="assets/js/language-manager.js"></script>
```

#### メリット
- ファイル数の大幅削減
- メンテナンスの簡素化
- 翻訳の一元管理
- 言語切り替えの即時反映

### 従来の対応要件（移行期間中は併用）

**すべての新規コンテンツ・ページ作成時には、以下の多言語対応を必ず実施してください：**

#### 1. ページ・コンテンツ作成
- 新規ページ作成時は、日本語・英語・韓国語の**3言語すべて**に対応
- 翻訳データファイル (`assets/js/translations.js`) への追加
- 動的翻訳システムへの移行を優先

#### 2. 翻訳システム統合
- `data-i18n` 属性を使用した動的翻訳対応
- 翻訳キーの一貫性保持
- 翻訳ファイルへの新規キー追加

#### 3. 必須ファイル更新対象
新規コンテンツ作成時は以下ファイルの更新が必要：
- `assets/js/translations.js` - 翻訳データ追加
- 日本語版ページ（ルート）
- 英語版ページ（`/en/`）
- 韓国語版ページ（`/ko/`）

#### 4. URL構造
- 日本語：`/` （ルート）
- 英語：`/en/`
- 韓国語：`/ko/`

#### 5. 翻訳データ構造
`translations.js`での言語キー構造例：
```javascript
{
  ja: { /* 日本語翻訳 */ },
  en: { /* 英語翻訳 */ },
  ko: { /* 韓国語翻訳 */ }
}
```

### 注意事項
- **部分的な多言語対応は禁止** - 1言語のみでの公開は行わない
- 機械翻訳に依存せず、自然で適切な翻訳を提供
- 文化的・地域的配慮を含む翻訳対応
- 今後サポート言語を追加する場合は、既存コンテンツすべてに遡って対応

**この多言語対応要件に従わない新規コンテンツの作成・公開は禁止です。**

ダークモード・ライトモードの区別はつけない。
常に統一されたデザインが誰にでも提供される。

## コンポーネント管理要件

### ヘッダーの統一管理

**重要**: ヘッダーは必ず1つのファイル（`components/header.html`）のみで管理すること。

#### 禁止事項
- 言語別のヘッダーファイル作成（header-en.html, header-ko.html等）は**絶対禁止**
- ページ別のヘッダーファイル作成（header-page.html等）は**絶対禁止**
- 複数のヘッダーファイルを条件分岐で使い分けることは**絶対禁止**

#### 必須要件
- すべてのページで`components/header.html`を使用
- 言語切り替えやパス調整が必要な場合は、CSSまたは最小限のJavaScriptで対応
- パスは絶対パス（`/`から始まる）を使用し、相対パスの複雑な計算は避ける

#### 理由
- メンテナンスの簡素化
- 一貫性の保持
- バグの削減
- 開発効率の向上
