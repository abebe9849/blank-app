# 🎈 Blank app template

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-gsicntv03eq.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   git clone https://github.com/abebe9849/blank-app.git
   
   pip install -r requirements.txt
   ```

2. Run the app

   ```
   streamlit run streamlit_app.py
   ```

### 使い方

糸球体画像に所見文をつける。所見文はPAS染色の１つの糸球体に対してつけるものであり、他の染色は考慮しないものとする.(他の染色でないとわからないものは所見に反映させなくてよい)

所見文はチェックボックスを用いてつける。？にカーソルを乗せるとチェックボックスに対応した所見文章が表示される

チェックボックスをつけて"適用"をクリックすると下の”テキスト”欄に対応する所見文章が生成される。

所見文とその横の糸球体画像をみて誤りがないことを確認したあと、"完了"をクリックすると次の画像に遷移する。

所見文のテキスト欄を初期化してすべて消したい場合には"テキストをクリア"　をクリックする。

作業中に所見文の作業結果をダウンロードしたい場合、"完了"の下の"ダウンロード"をクリックする。


不明点や不具合があれば [こちらまで](https://mail.google.com/mail/?view=cm&fs=1&to=masamasa20001002@gmail.com&su=【糸球体画像に対するキャプションつけ】)



