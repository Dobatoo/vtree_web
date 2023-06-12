# Vtrees(仮)ドキュメント(仮)

最終編集:2021/08/25

## 仕様

### これは何

ある動画に対する「その動画のURLを概要欄に含む動画」や、あるチャンネルに対する「そのチャンネルのURLを概要欄に含む動画」をYouTube Data APIにより収集することで、ある動画やあるチャンネル自身の統計情報としては現れない関係や再生回数等を算出・閲覧できる。(ハズ…)

### 外部スクリプトを実行する

django-extensions([https://django-extensions.readthedocs.io/en/latest/])を使用する。  
具体的には`python manage.py runscript [スクリプト名]`で実行ができる。  
(例:scriptsでチャンネルを追加する `python manage.py runscript scripts --script-args [チャンネルID]`)  
django-extensionsにより、Djangoプロジェクト直下でDjangoが使用するアプリ―ケーションを使用したスクリプトを実行することができる。  
実行するスクリプトには`run()`メソッドが必要。引数を取る場合は`run(*args)`の形で定義し、`--script-args [引数1] [引数2] ...`の形で値を渡す。

様々な関数を実装して遊べる

## TODO,今後の課題

- YouTube Data APIの仕様により、あるクエリに対して500件以上の検索結果(次ページ)が返されない
  - 投稿動画について : order=date,dateBeforeを活用し、まだ収集できていない投稿動画を検索する。
  - 引用動画について : どうしろって言うんだ。order=dateだと次ページトークンが送られてこない怪現象が発生した。" | "でOR検索を止めるとできるのかもしれない？
- 新着動画の追加
  - dateAfterでいい感じに…　恐らくこれは投稿動画/引用動画どちらでも上手くいくハズ。
- 更新が自動じゃない
  - webサービスのアクセスに応じて…等の方法がある。トークン上限がネック。
  - RSSとか使う手もあるかもしれない。
- フロントエンドがしょぼい(を超えて無)
  - それはまた別ですることとする！
- 全動画を表示する所
  - 無限スクロールやページネーションが必要
- 集計チャンネルの登録がユーザーからできない
  - トークン上限が…という気持ち。集計待ちキューを実装するとできるかも？

## 反省,学習

- 難しい
  - DjangoのモデルとYouTubeのAPIに苦しめられた
  - YouTubeのAPIのメソッドに関するドキュメントが無いので型やメソッドの存在をサンプルから推測するしかない。
- Python
  - 静的型検証欲しい…と思うようになった
  - 型アノテーションはそこそこ仕事をしてくれたように見える。
  - *args,**kwargsの使い方に注意
- Django
  - View,Template
    - とっつきやすい　特に文句はない
  - Model
    - 外部キー制約を持つフィールドが持つ値は外部キーのインスタンス(エントリ?)。間違えてfilter,get等で`fieldAsForeignKey = someValue(pk等)`のような指定をしてはいけない。
    - 代わりに外部キーへのアクセスが簡単
      - forwardは`model.fieldAsForeignKey.valueOfAnotherModel`のイメージ
      - reverseはOneToOneはforwardと同じか、一要素としての扱いと同じ。その他は`fieldName_set`?あまりよくわかっていない(使っていないはず)
    - クエリの最適化よくわからない
- YouTube Data API
  - これが一番悪い　親切なようで不親切な公式
  - 公式サイトでクエリのテストができる(とても良かった)
  - quotaは特定の情報を取るときは1,検索するときは100のイメージ
  - 合計が500件以上を越えるとNextPageTokenを送ってこなくなる。
  - なぜかsearchでorder=date,qでOR(|)検索を行うと、maxResultsの指定に関わらず完全一致以外に返さない＆NextPageTokenを返さないという状況になる。
- その他
  - 平均引用回数は約100回/本を見積もっている
    - ある動画一本で500近い引用回数(検索結果)が表示されたこともある。困る