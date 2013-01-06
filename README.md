#InputSequence

「Sublime Text 2」にインストールしてつかうプラグイン
Package Controlには追加していませんので、独自にインストールする必要があります。

## インストール
まず、`InputSequence`フォルダーをSublime Text 2の`Package`フォルダーに保存します。
（メニューの`Prefarences->Browse Packages`からアクセス) 

次に、ショートカットキーを設定しておきます。
はじめて設定する場合、空のテキストかもしれませんが、以下のように設定します。

```json
[
	// Input Sequence
	{ "keys": ["ctrl+shift+0"], "command": "input_sequence"}
]
```

JSON記述の配列記述なので、ほかに設定がある場合、
```json
[
	// Input Sequence
	{ "keys": ["ctrl+shift+0"], "command": "input_sequence"},

	// その他の設定
	{ "keys": ["ctrl+shift+="], "command": "calculate", "args": {"replace": false} },
	{ "keys": ["ctrl+shift+alt+1"], "command": "calculate_count" },
	{ "keys": ["ctrl+shift+c"], "command": "calculate", "args": {"replace": true} }
]

セミコロン`,`の使い方に気をつけてください。

## 使い方
`command+d`(Mac)などで、複数キャレットを表示させた状態にしておきます。

上記インストール方法では、`ctrl+shift+0`に機能が割り当てられており、入力すると`Sequence Type (alphabet or number):`コマンドバーが出現し、初期コマンドは`00`になっています。
このまま`Enter`を押せば2ケタの連番がカーソル位置に入力されます。

ほかに、

`aa`(小文字アルファベット連番)
`AAA`(大文字アルファベット連番)
`-10`(10からの降順連番)

の機能も備えています。

