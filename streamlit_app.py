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
    st.session_state.all_imgs = len(image_files)

# アノテーションデータのロードまたは初期化
annotations_file = "./data/annotations.json"
if os.path.exists(annotations_file):
    with open(annotations_file, 'r', encoding='utf-8') as f:
        annotations = json.load(f)
else:
    annotations = {}

image_files = [f for f in image_files if f not in annotations.keys()]


# テンプレート辞書
templates = {
    "a": {
        "0": "管内性細胞増生が一部に見られます",
        "1": "管内性細胞増生が全節性に見られます",
    },
    "b": {
        "0": "線維性半月体が見られます",
        "1": "繊維細胞性半月体が見られます",
        "2": "細胞性半月体が見られます",
        "3": "小半月体が見られます",
        "4": "係蹄の癒着が見られます",
        "5": "尿腔内出血",## 浸出が見られます",
        "6": "上皮細胞の増殖が見られます",
        "7": "カプスラードロップが見られます",
    },
    "c": {
        "0": "基底膜の肥厚が見られます",
        "1": "基底膜にスパイクを認めます",
        "2": "基底膜に断裂を認めます",
        "3": "基底膜に沈着様の物質の存在が疑われます",
        "4": "基底膜に二重化を認めます",
        "5": "係蹄壊死を認めます"
    },
    "m": {#メサンギウム
        "0": "メサンギウム細胞の軽度増殖を認めます",
        "1": "メサンギウム細胞の中程度増殖を認めます",
        "2": "メサンギウム細胞の重度増殖を認めます",
        "3": "メサンギウム基質の増加が見られます",
        "4": "メサンギウムの融解が見られます",
        "5": "",
    },
    "d": {
        "0": "全節性硬化が見られます",
        "1": "分節性の硬化が見られます",
        "2": "結節性硬化が疑われます",
    },
    "e": {
        "0": "係蹄腔の虚脱が見られます",
        "1": "係蹄腔の拡張が見られます",
    },
    "f": {#"血管新生","硝子様変化","硝子様血栓"]
        "0": "糸球体周囲の血管新生が見られます",
        "1": "細動脈の硝子様変化が見られます",
        "2": "硝子様血栓が見られます",
    },
}

# 現在の画像ファイル名
current_image_file = image_files[st.session_state.index]

path_ = f"{img_path}"+current_image_file.split("/")[-1]

# 全角を半角に変換する関数
def zenkaku_to_hankaku(text):
    return text.translate(str.maketrans('０１２３４５６７８９', '0123456789'))

# ページ設定で横幅を広げる
st.set_page_config(layout="wide")
form = st.form("checkboxes", clear_on_submit = True)


max_width = 500
max_height = 500
# 画像の表示
def resize_image(image_path, max_width=450, max_height=450):
    image = Image.open(image_path)
    image = image.resize((max_width, max_height))
    return image
resized_image = resize_image(current_image_file, max_width, max_height)
#st.session_state['annotation_text'] = ""
# テキストアノテーションの入力
with form:
    col1, col2 = st.columns([4, 4])
    with col1:
        

        
        checkbox_labels = ["管内細胞増殖:一部","管内細胞増殖:全節"]  # 5個のチェックボックスのラベル
        cols = st.columns(len(checkbox_labels))  # チェックボックスの数だけ列を作成
        checkbox_states_a = []

        for i, label in enumerate(checkbox_labels):
            with cols[i]:  # 各列にチェックボックスを配置
                checkbox_state = st.checkbox(label, key=label,help=templates["a"][str(i)])
                checkbox_states_a.append(checkbox_state)

        st.write("======管外病変======")
        checkbox_labels = ["線維性半月体","繊維細胞性半月体","細胞性半月体","小半月体","癒着","尿腔内出血 浸出","上皮細胞の増殖","カプスラードロップ"]  # 5個のチェックボックスのラベル
        #cols = st.columns(len(checkbox_labels))  # チェックボックスの数だけ列を作成
        checkbox_states_b = []
        rows = [checkbox_labels[:4], checkbox_labels[4:]]
        for cnt,row in enumerate(rows):
            cols = st.columns(4)
            cnt*=4

            for i_, label in enumerate(row):

                with cols[i_]:  # 各列にチェックボックスを配置
                    checkbox_state = st.checkbox(label, key=label,help=templates["b"][str(i_+cnt)])
                    checkbox_states_b.append(checkbox_state)


        st.write("======メサンギウム======")
        checkbox_labels = ["軽度 細胞増殖","中程度 細胞増殖","重度 細胞増殖","基質の増加","融解"]  # 5個のチェックボックスのラベル
        cols = st.columns(len(checkbox_labels))  # チェックボックスの数だけ列を作成
        checkbox_states_m = []

        for i, label in enumerate(checkbox_labels):
            with cols[i]:  # 各列にチェックボックスを配置
                checkbox_state = st.checkbox(label, key=label,help=templates["m"][str(i)])
                checkbox_states_m.append(checkbox_state)

        st.write("======基底膜======")
        checkbox_labels = ["肥厚","スパイク","断裂","沈着","二重化","係蹄壊死"]  # 5個のチェックボックスのラベル
        cols = st.columns(len(checkbox_labels))  # チェックボックスの数だけ列を作成
        checkbox_states_c = []

        for i, label in enumerate(checkbox_labels):
            with cols[i]:  # 各列にチェックボックスを配置
                checkbox_state = st.checkbox(label, key=label,help=templates["c"][str(i)])
                checkbox_states_c.append(checkbox_state)
        st.write("======その他======")
        checkbox_labels = ["全節性硬化","結節性硬化","分節性硬化"]  # 5個のチェックボックスのラベル
        cols = st.columns(len(checkbox_labels))  # チェックボックスの数だけ列を作成
        checkbox_states_d = []

        for i, label in enumerate(checkbox_labels):
            with cols[i]:  # 各列にチェックボックスを配置
                checkbox_state = st.checkbox(label, key=label,help=templates["d"][str(i)])
                checkbox_states_d.append(checkbox_state)
        checkbox_labels_e = ["係蹄腔虚脱","係蹄腔拡張"]  # 5個のチェックボックスのラベル
        cols = st.columns(len(checkbox_labels_e))  # チェックボックスの数だけ列を作成
        checkbox_states_e = []

        for i, label in enumerate(checkbox_labels_e):
            with cols[i]:  # 各列にチェックボックスを配置
                checkbox_state = st.checkbox(label, key=label,help=templates["e"][str(i)])
                checkbox_states_e.append(checkbox_state)

        checkbox_labels_f = ["血管新生","硝子様変化","硝子様血栓"]  # 5個のチェックボックスのラベル
        cols = st.columns(len(checkbox_labels_f))  # チェックボックスの数だけ列を作成
        checkbox_states_f = []

        for i, label in enumerate(checkbox_labels_f):
            with cols[i]:  # 各列にチェックボックスを配置
                checkbox_state = st.checkbox(label, key=label,help=templates["f"][str(i)])
                checkbox_states_f.append(checkbox_state)



    with col2:

        #st.markdown('<div class="image-container">', unsafe_allow_html=True)
        
        target__ = "DMN" #str(tmp["target"].values[0])
        print(target__)
        bp = 90 #tmp["収縮期血圧"].values[0]
        egfr = 60#int(tmp["egfr"].values[0])
        ubp = 3.5#tmp["uprot"].values[0]
        hep = 0.5 #tmp["血尿"].values[0]
        caption_text= f"収縮期血圧:{bp},eGFR:{egfr},尿蛋白:{ubp},血尿:{hep}"
        st.image(resized_image, use_column_width=True)
        st.markdown(f"<div style='text-align: center; font-size: 24px; font-weight: bold;'>{caption_text}</div>", unsafe_allow_html=True)
submit = form.form_submit_button("テンプレートを適用 チェックボックス初期化")

# 自由記述欄の初期値設定
if 'annotation_text' not in st.session_state:
    st.session_state['annotation_text'] = annotations.get(current_image_file, "")
#if st.button("テンプレートを適用"):
if submit:
    print(checkbox_states_a)
    for idx,c in enumerate(checkbox_states_a):
        if c:
            st.session_state["annotation_text"] += templates["a"][str(idx)] + "\n"
    for idx,c in enumerate(checkbox_states_b):
        if c:
            st.session_state["annotation_text"] += templates["b"][str(idx)] + "\n"
    for idx,c in enumerate(checkbox_states_c):
        if c:
            st.session_state["annotation_text"] += templates["c"][str(idx)] + "\n"
    for idx,c in enumerate(checkbox_states_m):
        if c:
            st.session_state["annotation_text"] += templates["m"][str(idx)] + "\n"
    for idx,c in enumerate(checkbox_states_d):
        if c:
            st.session_state["annotation_text"] += templates["d"][str(idx)] + "\n"
    for idx,c in enumerate(checkbox_states_e):
        if c:
            st.session_state["annotation_text"] += templates["e"][str(idx)] + "\n"
    for idx,c in enumerate(checkbox_states_f):
        if c:
            st.session_state["annotation_text"] += templates["f"][str(idx)] + "\n"
    

    print(st.session_state['annotation_text'])


col_1, col_2 = st.columns([1, 1])

with col_1:
    annotation_text = st.text_area("テキスト", value=st.session_state['annotation_text'], height=400)
    # 完了ボタンとクリアボタンを横に並べる
    st.write(f"未アノテーションの画像数: {len(image_files)} / {st.session_state.all_imgs}")

    col_button1, col_button2 = st.columns([1, 1])
    with col_button1:

        
        
        if st.button("完了 次の画像へ"):           
            annotations[current_image_file] = annotation_text
            with open(annotations_file, 'w', encoding='utf-8') as f:
                json.dump(annotations, f, ensure_ascii=False, indent=4)

            # 次の画像に進む
            #st.session_state.index += 1
            # テンプレート番号を空白に初期化
            #if st.session_state.index >= len(image_files):
            #    st.session_state.index = 0
            with open(annotations_file, 'r', encoding='utf-8') as f:
                annotations_data = f.read()
            st.download_button(
                label="アノテーションファイルをダウンロード",
                data=annotations_data,
                file_name="annotations.json",
                mime="application/json"
            )
            if len(image_files) == 1:
                print("last")
                #download annotation json
                st.session_state.index = 0
                # アノテーションJSONファイルをダウンロード


                
                st.success("すべての画像にアノテーションが完了しました")
            st.session_state['annotation_text'] = ""
            
            print(st.session_state)
            
            if len(image_files) != 1:

                st.rerun()
            
            
            

            
    with col_button2:
        
        if st.button("テキストをクリア"):
            st.session_state['annotation_text'] = ""
            st.rerun()

with col_2:
    target__ = "DMN" #str(tmp["target"].values[0])
    bp = 90 #tmp["収縮期血圧"].values[0]
    egfr = 60#int(tmp["egfr"].values[0])
    ubp = 3.5#tmp["uprot"].values[0]
    hep = 0.5 #tmp["血尿"].values[0]
    caption_text= f"収縮期血圧:{bp},eGFR:{egfr},尿蛋白:{ubp},血尿:{hep}"
    st.image(resized_image, use_column_width=True)
    st.markdown(f"<div style='text-align: center; font-size: 24px; font-weight: bold;'>{caption_text}</div>", unsafe_allow_html=True)



