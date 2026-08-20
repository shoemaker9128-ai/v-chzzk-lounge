import streamlit as st
import sqlite3
import random
import urllib.parse
import html

# ----------------------------------------------------
# 1. 웹 페이지 기본 설정
# ----------------------------------------------------
st.set_page_config(
    page_title="V-CHZZK | 실시간 버추얼 라운지",
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------------------------------
# 2. [CSS 스타일 설정] - 배경 완벽 고정
# ----------------------------------------------------
st.markdown("""
<style>
    /* 전체 배경을 딥블랙으로 고정 */
    [data-testid="stAppViewContainer"], [data-testid="stMain"], .stApp {
        background-color: #090A0F !important;
    }
    
    /* 헤더 및 불필요한 요소 숨김 */
    header[data-testid="stHeader"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { display: none !important; }

    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 앱 영역 스타일 */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 5.5rem !important; 
        max-width: 420px !important; 
        margin: 0 auto !important;
        background-color: #0F1015 !important;
        min-height: 100vh !important;
        border-left: 1px solid rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 0 40px rgba(0, 0, 0, 0.95);
    }

    /* 나머지 디자인 요소는 그대로 유지 */
    .app-header-container { display: flex; justify-content: space-between; align-items: center; padding: 4px 4px 16px 4px; margin-bottom: 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); gap: 12px; }
    .app-logo { font-size: clamp(1.6rem, 9vw, 2.2rem); font-weight: 900; letter-spacing: 0.5px; color: #FFFFFF; line-height: 1; font-style: italic; white-space: nowrap; transform: scaleX(1.08); transform-origin: left center; flex-shrink: 0; }
    .app-logo span { color: #00FFA3; text-shadow: 0 0 12px rgba(0, 255, 163, 0.4); }
    .app-subtitle-badge { display: flex; align-items: center; background-color: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); padding: 6px 10px; border-radius: 20px; font-size: clamp(0.7rem, 3.5vw, 0.8rem); color: #9CA3AF; font-weight: 600; letter-spacing: -0.3px; line-height: 1; white-space: nowrap; flex-shrink: 1; }
    .app-subtitle-badge span { color: #00FFA3; font-size: 0.4rem; margin-right: 6px; }
    .custom-segment-box { display: flex !important; flex-direction: row !important; justify-content: space-between !important; align-items: center !important; width: 100%; margin-bottom: 14px; background-color: #1C1E26; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 10px; padding: 3px; gap: 3px; }
    .segment-tab { flex: 1; text-align: center; padding: 7px 0 !important; font-size: 0.75rem !important; font-weight: 700; text-decoration: none !important; color: #9CA3AF !important; border-radius: 7px; display: block; line-height: 1.2; transition: all 0.2s ease; }
    .segment-tab.active { background-color: #00FFA3 !important; color: #111111 !important; }
    .stream-card { position: relative !important; border: 1px solid rgba(255, 255, 255, 0.15) !important; background: #1C1E26 !important; border-radius: 14px; margin-bottom: 16px !important; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4); overflow: hidden; }
    .stream-card-random { position: relative !important; border: 2px solid #00FFA3 !important; background: #1C1E26 !important; border-radius: 14px; margin-bottom: 16px !important; box-shadow: 0 4px 12px rgba(0, 255, 163, 0.15); overflow: hidden; }
    .content-card { background-color: #1C1E26; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 12px 14px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); }
    .overlay-badges-container { position: absolute; top: 10px; left: 10px; display: flex; align-items: center; gap: 0px; z-index: 10; pointer-events: none; }
    .badge-live { background-color: #FF3333; color: #FFFFFF; padding: 4px 6px; border-top-left-radius: 5px; border-bottom-left-radius: 5px; font-size: 0.65rem; font-weight: 800; letter-spacing: 0.3px; box-shadow: 0 2px 4px rgba(0,0,0,0.4); display: flex; align-items: center; line-height: 1; }
    .badge-viewers { background-color: rgba(15, 16, 21, 0.95); border-top: 1px solid rgba(255, 255, 255, 0.2); border-bottom: 1px solid rgba(255, 255, 255, 0.2); border-right: 1px solid rgba(255, 255, 255, 0.2); color: #FFFFFF; padding: 4px 6px; border-top-right-radius: 5px; border-bottom-right-radius: 5px; font-size: 0.65rem; font-weight: 700; box-shadow: 0 2px 4px rgba(0,0,0,0.4); display: flex; align-items: center; line-height: 1; }
    .tag-badge { display: inline-block; background: rgba(0, 255, 163, 0.08); color: #00FFA3; border: 1px solid rgba(0, 255, 163, 0.35); padding: 2px 5px; border-radius: 5px; font-size: 0.65rem; margin: 3px 3px 0 0; }
    .bottom-nav-container { position: fixed !important; bottom: 0 !important; left: 50% !important; transform: translateX(-50%) !important; width: 100% !important; max-width: 420px !important; background: rgba(24, 26, 32, 0.95) !important; backdrop-filter: blur(16px) !important; -webkit-backdrop-filter: blur(16px) !important; border-top: 1px solid rgba(255, 255, 255, 0.1) !important; border-left: 1px solid rgba(255, 255, 255, 0.08) !important; border-right: 1px solid rgba(255, 255, 255, 0.08) !important; box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.6) !important; display: flex !important; justify-content: space-around !important; padding: 10px 0 10px 0 !important; z-index: 900 !important; }
    .bottom-nav-item { color: #525C6D !important; text-decoration: none !important; display: flex; flex-direction: column; align-items: center; gap: 4px; transition: all 0.2s ease; }
    .bottom-nav-item.active { color: #00FFA3 !important; }
    .bottom-nav-item.active svg { transform: scale(1.15); filter: drop-shadow(0 0 6px rgba(0, 255, 163, 0.6)); }
    .bottom-nav-item.active span { font-weight: 800 !important; filter: drop-shadow(0 0 4px rgba(0, 255, 163, 0.3)); }
</style>
""", unsafe_allow_html=True)

# (이하 파이썬 코드는 동일합니다)
# ... (코드 생략, 기존과 동일하게 넣으시면 됩니다)
