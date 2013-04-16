#InputSequenceとは

「Sublime Text 2」にインストールして使用するプラグインです。

Sublimeテキストに、連番数字を入力機能を追加するプラグインです。
Sublimeの複数キャレット機能を使って、数カ所にキャレット表示した状態で、`ctrl+shift+0`コマンドを実行、
下部に出てくるフォームに入力フォーマットを指定すればキャレット位置に前から順番に数字が入力されます。


## インストール
Package Controlには追加されていませんので、github リポジトリパスを入力していただいてから、インストールする必要があります。
Package Control から Add Repository を実行。  
ウィンドウ下部にリポジトリパスの入力エリアが出現するので、下記を入力。  

    https://github.com/kope88/InputSequence.git

次に Install Package を実行し、InputSequence をインストール。

## アンインストール
Package Control から Remove Package を実行し、InputSequence をアンインストール。  
次にメニューから、`Preferences->Package Settings->Package Control->Settings - User`を開き、  
repositories から `https://github.com/kope88/InputSequence.git` の一行を削除。

## 使い方
`command+d`(Mac)などで、複数キャレットを表示させた状態にしておきます。

ショートカットキーは`ctrl+shift+0`が割り当てられており、入力すると`Sequence Type (alphabet or number):`コマンドバーが出現します（初期コマンドは`$0`です）
このまま`Enter`を押せば0からの連番がカーソル位置に入力されます。

その他、コマンド指定方法

* `aa`(小文字アルファベット連番)
* `AAA`(大文字アルファベット連番)
* `-10`(10からの降順連番)
* `05`(5からの2ケタの連番。99の次は00になります)
* `$1`(1からの連番。9の次は10(2ケタ)になります)
* `$a0`(a0, a1, ... a9, b0, b1, ... z9, aa0とケタ上がりします)


## 更新情報
2013.4.15 :ver 1.1
・ケタ追加機能を追加
・英文字の連番がA-Zであるべきところ、A-Xとなっていたので修正


2012.09.20 :ver 1.0
初期バージョン作成