#InputSequence

テキストエディター'Sublime Text'で連番を簡単に入力できるプラグインです。

Sublimeテキストに、連番英数を入力する機能を追加します。
Sublimeの複数キャレット機能を使って、数カ所にキャレット表示した状態で、`ctrl+shift+0`コマンドを実行、
下部に出てくるフォームに入力フォーマットを指定すればキャレット位置に前から順番に数字が入力されます。

## 基本的な使い方

### インストール
Package Controlには追加されていませんので、github リポジトリパスを入力していただいてから、インストールします。  
Package Control から Add Repository を実行。  
ウィンドウ下部にリポジトリパスの入力エリアが出現するので、下記を入力。  

[https://github.com/kazu1107/InputSequence.git](https://github.com/kazu1107/InputSequence.git)

次に Install Package を実行し、InputSequence をインストール。

### アンインストール
Package Control から Remove Package を実行し、InputSequence をアンインストール。  
次にメニューから、`Preferences > Package Settings > Package Control > Settings - User`を開き、  
repositories から [https://github.com/kazu1107/InputSequence.git](https://github.com/kazu1107/InputSequence.git) の一行を削除。

### 操作手順

1. `command+d`(Mac)などの操作で、複数キャレットを表示させた状態にしておきます。
2. `ctrl+shift+0`を入力すると`Sequence Format:`コマンドバーが出現します（初期コマンドは空白）
3. キャレットの位置に、0,1,2...と連番が表示されます。
4. `Enter`キーで確定します。

### 基本的なフォーマット指定

`aa`     小文字アルファベット連番
`AAA` 大文字アルファベット連番
~~`-10`(10からの降順連番)~~ **仕様変更しました** 詳しくは演算の項参照
`05` 5からの2ケタの連番。99の次は00になります
`$1` 1からの連番。9の次は10(2ケタ)になります
`$a0` **a0, a1, ... a9, b0, b1, ... z9, aa0 **とケタ上がりします


## 演算指定で特殊な入力
v2.0.0から、降順連番以外に様々な演算が可能になりました。


###演算の指定方法
例：Sequence Format:`020+5,2`  
以下の条件で連番入力します  

* 初期値 20
* ゼロ埋め 3ケタ
* 一度の加算で+5にする
* 同じ数字を2回ずつ

入力結果 : **020, 020 ,025 ,025 ,030 ,030 ...**

###四則演算
* `+` 初期値から指定値を足していきます。(例:`+10`)
* `-` 初期値から指定値を引いていきます。(例:`-2`)
* `*` 初期値に指定値をかけていきます(例:`*2`) ※数が大きくなると不具合あり
* `/` 初期値から指定値を割っていきます(例:`/2`)

###フォーマット指定
C言語のprintf()関数に似た指定方法です。

* `%d` 10進数  
* `%x` 16進数(アルファベット表記：小文字)
* `%X` 16進数(アルファベット表記：大文字)
* `%o` 8進数
* `%b` 2進数
* `%a` アルファベット(a-z)
* `%A` アルファベット(A-Z)

その他オプション

* `%5d` 5ケタ0埋め  
    基本のフォーマット指定で桁数指定している場合、がケタ追加されます（例：`00A%5d`)
    => ** 00001, 00002


###制御演算
* `,` 指定値分、演算をスキップ(同じ数字を表示)します  (例:`,2` => **0,0,1,1,2,2 ...**)
* `.` 指定値で、連番をストップします(例:`.20` => **... 18,19,20** (以降入力されない))
* `~` 値が指定値以上になったとき、初期値に戻します。(例:`~15` => **... 13,14,15,0,1 ...**)
* `@` `~`で戻るときの初期値を指定します。(例:`~15@5`=> **... 13,14,15,5,6,7 ...**)

###組み合わせ例

* 初期値1に2を足します  
  `$1+2` => 1,3,5,7,9,11 ...
* 初期値1000から2を引きます(自動ケタ合わせ機能と併用はできません）  
  `1000-2`=> 1000,0998,0996, ...
* 初期値2に2を足していきます。ただし、2回ずつ同じ値を入力します  
  `$2+2,2` => 2,2,4,4,6,6,...
* 1〜5の連番を繰り返します  
  `1~5` => 1,2,3,4,5,1,2,3,4,5,1 ...
* 1〜5の連番を表示後、3〜5を繰り返します  
  `1~5@3` => 1,2,3,4,5,3,4,5,3,4,5 ...
* 初期値2に10をかけていきます。（初期値0だと連番にはなりません）  
  `$2*10` => 2,20,40,80,...
* 100を2で割っていきます。（小数点以下は切り捨て 自動調整桁数調整は無効になります）  
  `$100/2` => 100,050,025,... 
* 16進数で2の累乗  
  `$2%x*2` => 2,4,8,10,20,40,80,100,200...

## 更新情報
###2014.9.4 :ver 2.0.0b
* ベータリリース
* 入力エラー時の不具合解消

###2014.5.5 :ver 2.0.0a
* Sublime Text3に対応するため全面的に書き直し。
* コマンド追加

###2013.4.15 :ver 1.1
* ケタ追加機能を追加
* 英文字の連番がA-Zであるべきところ、A-Xになっていたので修正


###2012.09.20 :ver 1.0
* 初期バージョン作成

## トラブルシューティング
### Windowsでデフォルトのショートカット（Ctrl+Shift+0）が効かない
IMEのキーボードレイアウト変更機能が、ショートカットとしてCtrl+Shift+0にデフォルトでアサインされているのが原因です。別のキーをアサインするか、下記の方法でIMEのアサインを解除してください。

1. **コントロールパネル**を開く。
2. **地域と言語**を開く。
3. **キーボードと言語**タブを選択した後、**キーボードの変更**をクリックする。
4. **詳細なキー設定**タブを選択した後、**入力言語を切り替える**を選択する。
5. **キーシーケンスの変更**をクリックする。
6. **キーボードレイアウトの切り替え**を、**割り当てなし**に変更する。
7. OKボタンを押してすべてのダイアログを閉じる。