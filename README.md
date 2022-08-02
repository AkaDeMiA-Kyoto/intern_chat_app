# 門田雅樹　インターン課題

時間が少しかかりましたが、なんとかカリキュラムを終えることができましたので、反省も兼ねてREADMEを書いてみます。<br>
お手柔らかにコードレビューお願い致します。

# 所感

全体的にとても楽しめる内容でした。<br>
インプットとしてDef Initや本が2,3冊ありましたが、アウトプットが適切に合間に挟まれていて楽しく学習ができました。<br>
内容の重複ももちろんありましたが、それ以上に学びを得ることができたという実感を得ることができました。

# アピールポイント

全体的にきれいなものを作ることを意識しました。<br>
たとえば、CSSはかなり原作に忠実に作ることを意識しました。<br>
僕なりにできるだけ指定されたプロトタイプに類似したものを作ろうと努力したので、比較しながら見ていただければ嬉しいです。<br>
※自環境に合わせたので他環境だと一部乱れがあるかもしれません、環境の違いを吸収できるように、これを書いたら少し詰めてみようと思います。<br>
また、コードも全体的にすっきりとしたものを作ることを意識しました。<br>
課題にはありませんでしたがクラスベースビューに`views.py`を書き変えたのは上記の目標を達成するのにかなり貢献したのではないかと思います。<br>
副次的効果として自分がクラスに慣れることができたのもよかったです。<br>
これはクラスベースビューのおかげというよりはDjangoのおかげかもしれませんが、今までクラスを知ってはいてもほとんど使用していなかったのが、クラスへの理解が深まったのをきっかけに個人のプロジェクトでも用いることができたのはよかったです。かなり整然としたものを製作することができました。

ただ、後述のN+1問題の強引な解決によってフレンド一覧周りはすこし煩雑になってしまいました。

# 反省点

やはり、N+1問題をうまく解決できなかった点です。<br>
うまくクエリの発行回数が落とせず、無理やり辞書に落とし込んで解決したのですが、結局オーダーとしてはあまり芳しくないものになってしまいました。<br>
ORMを使っていないので多少は高速だと思うのですが、それでも少しもたつきを感じます。<br>
解答例のようなものが思いつけるように勉強を深めていこうと思います。


# Author


* 作成者：門田雅樹
* 所属：AkaDeMiA
