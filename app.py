
import pandas as pd
import streamlit as st

st.set_page_config(page_title="장기실종자 단계적 탐색 시스템", page_icon="🔎")

st.title("🔎 장기실종자 단계적 탐색 시스템")
st.caption("현재 정보를 기반으로 공개 사례와 유사도를 계산합니다.")

df = pd.read_csv("missing(Sheet1)-3.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

def age_similarity(u,d):
    return 1/(1+abs(u-d))

def blood_similarity(u,d):
    return 1.0 if u==d else 0.2

def feature_similarity(u,d):
    return 1.0 if u==d else 0.3

def compare(user,row):
    if user["gender"]!=row["gender"]:
        return None
    total=(age_similarity(user["age"],row["age"])*0.6+
           blood_similarity(user["blood_type"],row["blood_type"])*0.25+
           feature_similarity(user["feature"],row["feature"])*0.15)
    return {
        "id":row["id"],
        "score":round(total*100,2),
        "age":row["age"],
        "blood":row["blood_type"],
        "feature":row["feature"]
    }

def recommend(user):
    out=[]
    for _,row in df.iterrows():
        r=compare(user,row)
        if r:
            out.append(r)
    out.sort(key=lambda x:x["score"], reverse=True)
    return out

with st.form("search"):
    age=st.number_input("현재 나이",0,120,24)
    gender=st.selectbox("성별",[1,2],format_func=lambda x:"남" if x==1 else "여")
    blood=st.selectbox("혈액형",["A","B","O","AB"])
    feature=st.selectbox("신체 특징",[0,1],format_func=lambda x:"없음" if x==0 else "있음")
    ok=st.form_submit_button("검색")

if ok:
    user={"age":age,"gender":gender,"blood_type":blood,"feature":feature}
    res=recommend(user)
    st.subheader("검색 결과")
    for i,r in enumerate(res[:5],1):
        st.markdown(f"### {i}위 {r['id']}")
        st.write(f"유사도: {r['score']}%")
        st.write(f"나이: {r['age']}")
        st.write(f"혈액형: {r['blood']}")
        st.write(f"신체 특징: {'있음' if r['feature']==1 else '없음'}")
        st.divider()
