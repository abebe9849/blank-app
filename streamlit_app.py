import streamlit as st
import os,cv2
import json,glob
import pandas as pd

#df = pd.read_csv("/home/user/ABE/kidneyDINO/final_pas.csv")
from PIL import Image


img_path = "./data/images"
image_files = glob.glob(f"{img_path}/*")  # 画像ファイルのリスト

# 現在の画像インデックス
if 'index' not in st.session_state:
    st.session_state.index = 0

# アノテーションデータのロードまたは初期化
annotations_file = "./data/annotations.json"
if os.path.exists(annotations_file):
    with open(annotations_file, 'r', encoding='utf-8') as f:
        annotations = json.load(f)
else:
    annotations = {}

image_files = [f for f in image_files if f not in annotations.keys()]
print(image_files)


if 'sidebar_closed' not in st.session_state:
    st.session_state.sidebar_closed = False
# テンプレート辞書
templates = {
    "a": {
        "0": "",
        "1": "管内増殖が一部に見られます",
        "2": "管内増殖が全節性に見られます",
        "3": "所見a3のテンプレート文章",
        "4": "所見a4のテンプレート文章",
        "5": "所見a5のテンプレート文章",
        
    },
    "b": {
        "0": "",
        "1": "所見b1のテンプレート文章",
        "2": "メサンギウム細胞増多が見られます",
        "5": "核崩壊が見られます",
        "6": "硝子様の血栓が見られます",
        "7": "係蹄腔の狭小化が見られます",
        "8": "係蹄に壊死が見られます",
    },
    "c": {
        "0": "",
        "1": "基底膜の二重化が分節性に見られます",
        "2": "基底膜の二重化が全節性に見られます",
        "3": "基底膜にスパイクを認めます",
        "4": "糸球体は分葉状を呈しています",
        "5": "半月体が全周性に見られます",
        "6": "半月体が全周性に見られます",
        "7": "基底膜の肥厚を認めます"
    },
    "d": {
        "0": "",
        "1": "全節性硬化が見られます",
        "2": "結節性硬化が疑われます",
        "3": "分節性の硬化が見られます",
        "4": "結節性硬化が疑われます",
    }
    "e": {
        "0": "光学顕微鏡では特記すべき所見はありません",
        "1": "糸球体周囲の血管新生が見られます",
        "2": "細動脈の硝子様変化が見られます",
    }
}

# 現在の画像ファイル名
current_image_file = image_files[st.session_state.index]

path_ = f"{img_path}"+current_image_file.split("/")[-1]

#tmp = df[df["path"]==path_]

#target,label,BMI,DBP,DM,age,alb,egfr,uprot,収縮期血圧,血尿

# 全角を半角に変換する関数
def zenkaku_to_hankaku(text):
    return text.translate(str.maketrans('０１２３４５６７８９', '0123456789'))

# ページ設定で横幅を広げる
st.set_page_config(layout="wide")


#st.write(f"未アノテーションの画像数: {len(image_files)}")


k = ["管内/管外増殖","メサンギウム領域","基底膜","硬化","周囲血管"]
# サイドバーのテンプレートの表示
st.sidebar.write("テンプレートの対応表")
for i,key in enumerate(templates):
    st.sidebar.write(f" {k[i]}:")
    for num, text in templates[key].items():
        st.sidebar.write(f"{num}: {text}")


def change_value():
    st.session_state["template_a"] = ""
    st.session_state["template_b"] = ""
    st.session_state["template_c"] = ""
    st.session_state["template_d"] = "" 
    st.session_state["template_e"] = "" 
    # https://zenn.dev/alivelimb/books/python-web-frontend/viewer/about-streamlit

# レイアウト設定
col1, col2 = st.columns([1, 2])
#st.session_state['annotation_text'] = ""
# テキストアノテーションの入力
with col1:
    st.write(f"未アノテーションの画像数: {len(image_files)}")
    target__ = "DMN" #str(tmp["target"].values[0])
    print(target__)
    bp = 90 #tmp["収縮期血圧"].values[0]
    egfr = 60#int(tmp["egfr"].values[0])
    ubp = 3.5#tmp["uprot"].values[0]
    hep = 0.5 #tmp["血尿"].values[0]
    st.write(f"{target__}")



    st.write(f"収縮期血圧:{bp},egfr:{egfr},尿蛋白:{ubp},血尿:{hep}")

    # テンプレート番号の入力
    template_a = zenkaku_to_hankaku(st.text_input("管内/管外増殖", key="template_a"))
    template_b = zenkaku_to_hankaku(st.text_input("メサンギウム領域", key="template_b"))
    template_c = zenkaku_to_hankaku(st.text_input("基底膜", key="template_c"))
    template_d = zenkaku_to_hankaku(st.text_input("硬化", key="template_d"))
    template_e = zenkaku_to_hankaku(st.text_input("周囲血管", key="template_e"))

    # 自由記述欄の初期値設定
    if 'annotation_text' not in st.session_state:
        st.session_state['annotation_text'] = annotations.get(current_image_file, "")

    # テンプレート文章の取得
    if st.button("テンプレートを適用"):
        for t in template_a:
            if t in templates["a"]:
                st.session_state['annotation_text'] += templates["a"][t] + "\n"
        for t in template_b:
            if t in templates["b"]:
                st.session_state['annotation_text'] += templates["b"][t] + "\n"
        for t in template_c:
            if t in templates["c"]:
                st.session_state['annotation_text'] += templates["c"][t] + "\n"
        for t in template_d:
            if t in templates["d"]:
                st.session_state['annotation_text'] += templates["d"][t] + "\n"
        for t in template_e:
            if t in templates["e"]:
                st.session_state['annotation_text'] += templates["e"][t] + "\n"
        print(st.session_state['annotation_text'])
    

    annotation_text = st.text_area("テキスト", value=st.session_state['annotation_text'], height=200)
    # 完了ボタンとクリアボタンを横に並べる
    col_button1, col_button2 = st.columns([1, 1])
    with col_button1:
        
        if st.button("完了", on_click=change_value):            
            annotations[current_image_file] = annotation_text
            with open(annotations_file, 'w', encoding='utf-8') as f:
                json.dump(annotations, f, ensure_ascii=False, indent=4)

            # 次の画像に進む
            #st.session_state.index += 1
            # テンプレート番号を空白に初期化
            #if st.session_state.index >= len(image_files):
            #    st.session_state.index = 0
            if len(image_files) == 1:
                st.success("すべての画像にアノテーションが完了しました")
                with open(annotations_file, "rb") as file:
                    file_data = file.read()
                b64 = base64.b64encode(file_data).decode()
                href = f'<a href="data:application/json;base64,{b64}" download="aaa.json">Click here to download aaa.json</a>'
                st.markdown(href, unsafe_allow_html=True)
                
                
            st.session_state['annotation_text'] = ""
            
            print(st.session_state)
            


            st.rerun()
            
            
            

            

    with col_button2:
        if st.button("クリア"):
            st.session_state['annotation_text'] = ""
            st.rerun()
if st.session_state.sidebar_closed:
    max_width = 400  # 800 * 0.9
    max_height = 400  # 600 * 0.9
else:
    max_width = 500
    max_height = 500
# 画像の表示
def resize_image(image_path, max_width=450, max_height=450):
    image = Image.open(image_path)
    image = image.resize((max_width, max_height))
    return image

with col2:
    #st.markdown('<div class="image-container">', unsafe_allow_html=True)
    resized_image = resize_image(current_image_file, max_width, max_height)
    st.image(resized_image, caption=current_image_file, use_column_width=True)

    #st.markdown('</div>', unsafe_allow_html=True)

