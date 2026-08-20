import streamlit as st
import sqlite3
import random
import urllib.parse
import html

# 1. 페이지 설정
st.set_page_config(page_title="V-CHZZK", layout="wide", initial_sidebar_state="collapsed")

# 2. 안전한 CSS (배경 강제 주입)
st.markdown("""
<style>
    /* 전체 배경을 딥블랙으로 */
    body { background-color: #090A0F !important; }
    .stApp { background-color: #090A0F !important; }
    
    /* 콘텐츠 컨테이너 */
    .block-container {
        max-width: 420px !important;
        margin: 0 auto !important;
        background-color: #0F1015 !important;
        padding-top: 1rem !important;
    }
    
    /* 나머지 디자인은 유지 */
    .app-header-container { display: flex; justify-content: space-between; align-items: center; padding: 0 4px 16px 4px; border-bottom: 1px solid #1f2937; margin-bottom: 16px; }
    .app-logo { font-size: 2rem; font-weight: 900; color: #fff; font-style: italic; transform: scaleX(1.08); }
    .app-logo span { color: #00FFA3; }
    .stream-card { background: #1C1E26; border-radius: 14px; margin-bottom: 16px; padding: 12px; border: 1px solid #374151; }
    .bottom-nav-container { position: fixed; bottom: 0; left: 50%; transform: translateX(-50%); width: 100%; max-width: 420px; background: #181a20; border-top: 1px solid #374151; display: flex; justify-content: space-around; padding: 10px 0; z-index: 999; }
</style>
""", unsafe_allow_html=True)

# 3. 데이터 로직 (생략 - 이전 버전과 동일)
def get_db_connection():
    conn = sqlite3.connect('v_chzzk.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# (중략 - 이전 코드 그대로 사용하셔도 무방합니다)
# ... [이하 이전 코드의 데이터 로직 및 탭 구현 부분 그대로 복붙] ...
