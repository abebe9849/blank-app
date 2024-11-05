import streamlit as st
import os,cv2
import json,glob
import pandas as pd
## ref: https://jsn.or.jp/journal/document/46_8/sigematu.pdf 
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
        "0": "管内性細胞増殖が見られます",
        "10":"糸球体毛細血管係蹄の管腔内の細胞数が増加し，管腔の狭小化を引き起こしている細胞増殖",
        "1": "糸球体が虚脱しています",
        "11": "糸球体毛細血管は虚脱し，ボーマン嚢の肥厚やボウマン腔の線維化を伴う場合がある",
        
    },
    "b": {
        "0": "線維性半月体が見られます",##説明文をクリック音で表示に全部かえる
        "10":"3層以上の管外性細胞増殖があり,その成分として細胞が50%以上ある病巣",
        "1": "繊維細胞性半月体が見られます",
        "2": "細胞性半月体が見られます",
        "3": "小半月体が見られます",#定義を細かく記載
        "4": "係蹄の癒着が時方向に見られます",##N時方向に
        "5": "偽尿細管形成が見られます",
        "6": "カプスラードロップが見られます",
    },
    "c": {
        "0": "基底膜の肥厚が見られます",##説明文に見えにくい場合にはなしでよい　と補足
        "1": "基底膜にスパイクが疑われます",##説明文に見えにくい場合にはなしでよい　と補足
        "2": "基底膜に断裂を認めます",
        "3": "基底膜に沈着様の物質の存在が疑われます",
        "4": "基底膜に二重化を認めます",##説明文に見えにくい場合にはなしでよい　と補足
        "5": "係蹄壊死を認めます"
    },
    "m": {#メサンギウム
        "0": "メサンギウム細胞の軽度増殖を認めます",
        "1": "メサンギウム細胞の中程度増殖を認めます",
        "2": "メサンギウム細胞の高度増殖を認めます",
        "3": "メサンギウム基質の増加が見られます",
        "4": "メサンギウムの融解が見られます",
        "5": "",
        "10": "メサンギウム基質に4~5個のメサンギウム細胞が見られる",
        "11": "メサンギウム基質に6~7個のメサンギウム細胞が見られる",
        "12": "メサンギウム基質に8個以上のメサンギウム細胞が見られる",
    },
    "d": {
        "0": "全節性硬化が見られます",
        "2": "分節性の硬化が時方向に見られます",##N時方向に... txt
        "1": "結節性硬化が疑われます",
        "11": "PAS染色ではっきりしない場合未記載で可",
        "12": "硬化が見られる場所を'N時方向'で記載　糸球体毛細血管係蹄の一部（すべての係蹄を侵さない）に硬化が認められる。",
        
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

hep_dict = {0:"-",0.5:"±",1.0:"+",2.0:"++",3.0:"+++"}

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
        

        
        checkbox_labels = ["管内細胞増殖","虚脱／虚血糸球体"]  # 5個のチェックボックスのラベル
        cols = st.columns(len(checkbox_labels))  # チェックボックスの数だけ列を作成
        checkbox_states_a = []

        for i, label in enumerate(checkbox_labels):
            with cols[i]:  # 各列にチェックボックスを配置
                if i in [0,1,2]:
                    i+=10
                checkbox_state = st.checkbox(label, key=label,help=templates["a"][str(i)])
                checkbox_states_a.append(checkbox_state)

        st.write("======メサンギウム======")
        checkbox_labels = ["軽度 細胞増殖","中程度 細胞増殖","高度 細胞増殖","基質の増加","融解"]  # 5個のチェックボックスのラベル
        cols = st.columns(len(checkbox_labels))  # チェックボックスの数だけ列を作成
        checkbox_states_m = []

        for i, label in enumerate(checkbox_labels):
            with cols[i]:  # 各列にチェックボックスを配置
                if i in [0,1,2]:
                    i+=10
                checkbox_state = st.checkbox(label, key=label,help=templates["m"][str(i)])
                checkbox_states_m.append(checkbox_state)

        st.write("======基底膜======")
        checkbox_labels = ["肥厚","スパイク","断裂","沈着","二重化","壊死"]  # 5個のチェックボックスのラベル
        cols = st.columns(len(checkbox_labels))  # チェックボックスの数だけ列を作成
        checkbox_states_c = []

        for i, label in enumerate(checkbox_labels):
            with cols[i]:  # 各列にチェックボックスを配置
                checkbox_state = st.checkbox(label, key=label,help=templates["c"][str(i)])
                checkbox_states_c.append(checkbox_state)
        st.write("======硬化======")
        checkbox_labels = ["全節性硬化","結節性硬化","分節性硬化"]  # 5個のチェックボックスのラベル
        cols = st.columns(len(checkbox_labels))  # チェックボックスの数だけ列を作成
        checkbox_states_d = []

        for i, label in enumerate(checkbox_labels):
            with cols[i]:  # 各列にチェックボックスを配置
                if i in [1,2]:
                    i+=10
                checkbox_state = st.checkbox(label, key=label,help=templates["d"][str(i)])
                checkbox_states_d.append(checkbox_state)

        st.write("======管外病変======")
        checkbox_labels = ["線維性半月体","繊維細胞性半月体","細胞性半月体","小半月体","癒着","偽尿細管形成","カプスラードロップ"]  # 5個のチェックボックスのラベル
        #cols = st.columns(len(checkbox_labels))  # チェックボックスの数だけ列を作成
        checkbox_states_b = []
        rows = [checkbox_labels[:4], checkbox_labels[4:]]
        for cnt,row in enumerate(rows):
            cols = st.columns(4)
            cnt*=4

            for i_, label in enumerate(row):
                tmp_i = i_+cnt
                if tmp_i in [0]:
                    tmp_i+=10
                with cols[i_]:  # 各列にチェックボックスを配置
                    checkbox_state = st.checkbox(label, key=label,help=templates["b"][str(tmp_i)])
                    checkbox_states_b.append(checkbox_state)
        st.write("============")
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
        
        target__ = "糖尿病性腎症" #str(tmp["target"].values[0])
        dbp = 90
        sbp = 140 #tmp["収縮期血圧"].values[0]
        egfr = 60#int(tmp["egfr"].values[0])
        ubp = 3.5#tmp["uprot"].values[0]
        hep = 0.5 #tmp["血尿"].values[0]
        hep = hep_dict[hep]
        caption_text= f"診断:{target__} ,血圧:{sbp}/{dbp}mmHg,eGFR:{egfr},尿蛋白:{ubp}g/gCr,血尿:{hep}"
        st.image(resized_image, use_column_width=True)
        st.markdown(f"<div style='text-align: center; font-size: 12px; font-weight: bold;'>{caption_text}</div>", unsafe_allow_html=True)
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
            ### この段階で　annotationに”が時”　がannotationsに部分文字列として含まれる場合にエラーとする
            if "が時" in annotation_text:
                st.error("エラー: アノテーションに「が時」が含まれています。修正してください。")
            else:
                annotations[current_image_file] = annotation_text
                with open(annotations_file, 'w', encoding='utf-8') as f:
                    json.dump(annotations, f, ensure_ascii=False, indent=4)                

            # 次の画像に進む
            #st.session_state.index += 1
            # テンプレート番号を空白に初期化
            #if st.session_state.index >= len(image_files):
            #    st.session_state.index = 0

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
        if not st.session_state.all_imgs==len(image_files):
            with open(annotations_file, 'r', encoding='utf-8') as f:
                annotations_data_ = f.read()
            st.download_button(
                label="アノテーションファイルをダウンロード",
                data=annotations_data_,
                file_name="annotations.json",
                mime="application/json"
            )  
            
            
            

            
    with col_button2:
        
        if st.button("テキストをクリア"):
            st.session_state['annotation_text'] = ""
            st.rerun()

with col_2:
    target__ = "糖尿病性腎症" #str(tmp["target"].values[0])
    dbp = 90
    sbp = 140 #tmp["収縮期血圧"].values[0]
    egfr = 60#int(tmp["egfr"].values[0])
    ubp = 3.5#tmp["uprot"].values[0]
    hep = 0.5 #tmp["血尿"].values[0]
    hep = hep_dict[hep]
    caption_text= f"診断:{target__} ,血圧:{sbp}/{dbp}mmHg,eGFR:{egfr},尿蛋白:{ubp}g/gCr,血尿:{hep}"
    st.image(resized_image, use_column_width=True)
    st.markdown(f"<div style='text-align: center; font-size: 12px; font-weight: bold;'>{caption_text}</div>", unsafe_allow_html=True)



