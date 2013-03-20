#InputSequence

「Sublime Text 2」にインストールしてつかうプラグイン  
Package Controlには追加していませんので、独自にインストールする必要があります。

## インストール
Package Control から Add Repository を実行。  
ウィンドウ下部にリポジトリパスの入力エリアが出現するので、下記を入力。  

    https://github.com/wakuworks/InputSequence.git

次に Install Package を実行し、InputSequence をインストール。

## アンインストール
Package Control から Remove Package を実行し、InputSequence をアンインストール。  
次にメニューから、`Preferences->Package Settings->Package Control->Settings - User`を開き、  
repositories から `https://github.com/wakuworks/InputSequence.git` の一行を削除。

## 使い方
`command+d`(Mac)などで、複数キャレットを表示させた状態にしておきます。

上記インストール方法では、`ctrl+shift+0`に機能が割り当てられており、入力すると`Sequence Type (alphabet or number):`コマンドバーが出現し、初期コマンドは`00`になっています。
このまま`Enter`を押せば2ケタの連番がカーソル位置に入力されます。

ほかに、

`aa`(小文字アルファベット連番)
`AAA`(大文字アルファベット連番)
`-10`(10からの降順連番)

の機能も備えています。
