# weather-news

openweatherAPI を用いて作成したお天気サイト。札幌、新潟、東京、大阪、福岡の 6 日先までの天気を取得しそれらの気温や湿度などの天気の情報を比較し憑依させています。

## 使用技術

node.js: 16
Django==3.2.12
vue "^2.6.14

使用した API
openweatherAPI
https://openweathermap.org/

### 実装できなかったこと

- 会員登録したユーザーのコメントといいね機能
  （フロントを Vue、バックエンドを Django で開発を行うと立てるサーバーが 2 つになり、2 つのサーバー間でやり取りをする際に CSRF エラーが発生する。会員登録機能をつけるなら Django のみで開発するべきだった）

- 特定の天気条件が発生した場合に登録されたメールアドレスに通知を送信する機能
  （会員登録機能自体が作れなかったためユーザーのメールアドレスが取得できなかった。メールアドレスを使う際のセキュリティの知識不足、無料の API では取得できる天気の情報が足りなかった。）

- フロントエンドで表示する天気情報の都市を変更できるようにする
  （Vue のライフサイクルダイアグラムの考えから Vue では実装できない。API はページが読み込まれた時点で呼ばれるもの。ボタンを押すたびに API を呼び出すことは Vue では不可能だった。）

## デモ動画

[https://youtu.be/RHp5wv9onJE](https://youtu.be/RHp5wv9onJE)

## スクリーンショット

![スクリーンショット](/screenshots/screenshot1.png.png)
![スクリーンショット](/screenshots/screenshot2.png.png)
