<p align="center">
  <img src="../../assets/aligns-header.png" alt="黄色と水色の背景に、線でつながった点とALIGNS.mdのタイトル" width="100%">
</p>

<h1 align="center">ALIGNS.md</h1>

<p align="center"><a href="https://aligns.md/ja/">aligns.md</a></p>

<p align="center">
  <a href="../../README.md" lang="en">English</a> · <a href="ko.md" lang="ko">한국어</a> · <strong lang="ja">日本語</strong>
</p>

<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="ライセンス: MIT"></a>
  <a href="https://github.com/hmmhmmhm/aligns.md/stargazers"><img src="../../assets/badges/github-star.svg" alt="GitHubスター"></a>
  <a href="#install-align"><img src="https://img.shields.io/badge/Format-Markdown-222222.svg?logo=markdown" alt="形式: Markdown"></a>
  <a href="https://skills.sh/hmmhmmhm/aligns.md/align"><img src="../../assets/badges/skills-sh.svg" alt="skills.shでインストール"></a>
</p>

## よい結果の基準を決める

ALIGNS.mdには、エージェントに目指してほしい目標と、何かを選ぶときに優先したいことを記録します。**align** スキルを使ってその基準をすり合わせ、作業の変化に応じて見直せます。

<p align="center">
  <img src="../../assets/define-what-good-means.png" alt="複数の経路が共通の基準点に集まる様子" width="100%">
</p>

## 期待することを分けて管理する

個人の判断基準はALIGNS.mdに、繰り返し使えるすり合わせの手順はスキルに置きます。AGENTS.mdやCLAUDE.mdなど、主に使うエージェントの指示ファイルからALIGNS.mdを参照するようにしてください。Gitを使っている場合は、その履歴で変更を追います。スキルを更新しても、合意した基準は書き換わりません。

専門スキルも、この基準に沿って使います。スキルの標準スタイルが自分の好みとして保存されることはなく、ALIGNS.mdですでに決めたことを聞き直されることもありません。 開発・デザイン・レビュー・文章の編集に併用できるスキルは、[おすすめスキル](../recommended-skills.md)（英語）にまとめています。

<p align="center">
  <img src="../../assets/keep-expectations-separate.png" alt="実行環境、指示、期待を表す3つのパネルが、分かれたままつながっている様子" width="100%">
</p>

## 自分の好みを伝える手間が減ります

一度すり合わせた基準は、次の作業にも引き継がれます。エージェントが把握した好みをもとに判断するので、毎回やり方を説明したり、一つひとつ選んだりする手間が減ります。

思っていた結果と違ったら、一緒に基準を見直して、次の作業に反映します。

[実験結果と方法](../../RETENTION_BENCHMARK.md)

<p align="center">
  <a href="../../RETENTION_BENCHMARK.md"><img src="../../assets/benchmarks/retention-comparison.svg" alt="仮想実験: 一般的な指示ではタスク中の回答9回、保存済みの好みとalignを提供した条件では0回。仮定した初期設定の回答4回は別に表示。両条件とも最終結果12件が基準を満たした" width="100%"></a>
</p>

## 必要なときに、またすり合わせる

ここでいうself-alignmentとは、自分の好みや判断基準をエージェントと整理し、その基準に沿って作業できているかを確かめることです。

大事な判断が意図とずれたとき、同じ修正を繰り返して足りない基準に気づいたとき、次に何をすればよいか迷ったときに、すり合わせを見直します。選んだPRのフィードバックや、参照できるプロジェクトの会話を振り返ることもできます。繰り返し現れる判断基準を「好みの不変性（taste invariants）」として捉え、適用範囲や例外とともに確認します。所要時間の目安を見てから、最近の履歴だけを見るか、全体を見るかを選んでください。長い自律作業を任せる前には、いくつかの仮の場面で判断を試します。明らかな誤りはその場で直し、すでに答えた質問は繰り返しません。

依頼は短くても構いません。エージェントは既存の文脈を確認し、結果を大きく左右する情報が足りないときにだけ質問します。いつ質問し、いつ自分で判断して進めるかも相談できます。ALIGNS.mdに残すのは、今後も適用すると確認した方針だけです。

<p align="center">
  <img src="../../assets/continuous-self-alignment.png" alt="基準線から外れた経路が、少しずつ方向を修正する様子" width="100%">
</p>

<a id="install-align"></a>

## alignをインストールする

次の依頼文をエージェントに貼り付けてください。

```text
https://github.com/hmmhmmhm/aligns.md の最新のインストールガイドに従って、alignスキルを設定してください。既存の設定を確認し、主に使うCLIでサポートされている方法でインストールして、このプロジェクトにALIGNS.mdを接続し、対応する更新方法を設定してください。既存の指示と確認済みの私の判断基準は保ち、まだ決まっていない点だけ質問してください。
```

直接インストールすることもできます。

```sh
npx skills add hmmhmmhm/aligns.md --skill align
```

インストール後に、**「このプロジェクトの判断基準をすり合わせたい」**と依頼してください。コマンドや決まった言い方は必要ありません。

[インストール・更新と八つの始め方](../usage.md)（英語）

## チームで使う

コードレビューやエージェントとの会話で確認した判断例を、コーディングエージェントの学習データとして準備できます。学習と結果の評価はチームが行います。

[MLOps・チーム向けの導入検討資料](../translated-briefs/ja.md) · [手動提出ガイド](../team-training-data.md)（英語）

## プロジェクトにバッジを付ける

ALIGNS.mdを使っているプロジェクトのREADMEに、このバッジを付けられます。エージェントに追加を頼むか、選択肢に表示された7番を選んでください。バッジがない場合だけ提案します。下のMarkdownをコピーしても構いません。

[![Uses ALIGNS.md](../../assets/badges/uses-aligns.svg)](https://github.com/hmmhmmhm/aligns.md)

```markdown
[![Uses ALIGNS.md](https://raw.githubusercontent.com/hmmhmmhm/aligns.md/main/assets/badges/uses-aligns.svg)](https://github.com/hmmhmmhm/aligns.md)
```

## ライセンス

[MIT](../../LICENSE). Copyright (c) 2026 hmmhmmhm.

<p align="center">
  <img src="../../assets/aligns-footer.png" alt="緑色の背景に、重なった座標グリッドとALIGNS.mdのタイトル" width="100%">
</p>
