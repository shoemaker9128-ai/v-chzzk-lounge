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
# 2. [CSS 스타일 설정]
# ----------------------------------------------------
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { display: none !important; }

    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 🚨 PC 모니터의 남는 바깥쪽 여백은 완전한 검은색으로 처리 */
    html, body {
        background-color: #000000 !important;
    }
    
    [class*="css"], .stApp {
        font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif !important;
        background-color: transparent !important;
        color: #F3F4F6 !important;
    }

    /* 🚨 앱 화면(스마트폰 영역)을 420px로 완벽하게 가두고 중앙에 배치 */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 5.5rem; 
        max-width: 420px !important; 
        margin: 0 auto !important;
        background-color: #0F1015 !important;
        min-height: 100vh !important;
        border-left: 1px solid rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.8);
    }

    .app-header-container {
        display: flex;
        justify-content: space-between;
        align-items: center; 
        padding: 4px 4px 16px 4px;
        margin-bottom: 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05); 
        gap: 12px; 
    }
    .app-logo {
        font-size: clamp(1.6rem, 9vw, 2.2rem); 
        font-weight: 900;
        letter-spacing: 0.5px; 
        color: #FFFFFF;
        line-height: 1;
        font-style: italic; 
        white-space: nowrap; 
        transform: scaleX(1.08); 
        transform-origin: left center;
        flex-shrink: 0; 
    }
    .app-logo span {
        color: #00FFA3;
        text-shadow: 0 0 12px rgba(0, 255, 163, 0.4); 
    }
    .app-subtitle-badge {
        display: flex;
        align-items: center;
        background-color: rgba(255, 255, 255, 0.03); 
        border: 1px solid rgba(255, 255, 255, 0.08); 
        padding: 6px 10px; 
        border-radius: 20px;
        font-size: clamp(0.7rem, 3.5vw, 0.8rem); 
        color: #9CA3AF; 
        font-weight: 600;
        letter-spacing: -0.3px; 
        line-height: 1;
        white-space: nowrap;
        flex-shrink: 1; 
    }
    .app-subtitle-badge span {
        color: #00FFA3;
        font-size: 0.4rem;
        margin-right: 6px; 
    }

    .custom-segment-box {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100%;
        margin-bottom: 14px;
        background-color: #1C1E26;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 3px;
        gap: 3px;
    }
    
    .segment-tab {
        flex: 1;
        text-align: center;
        padding: 7px 0 !important;
        font-size: 0.75rem !important;
        font-weight: 700;
        text-decoration: none !important;
        color: #9CA3AF !important;
        border-radius: 7px;
        display: block;
        line-height: 1.2;
        transition: all 0.2s ease;
    }
    
    .segment-tab.active {
        background-color: #00FFA3 !important;
        color: #111111 !important;
    }

    .stream-card { 
        position: relative !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important; 
        background: #1C1E26 !important; 
        border-radius: 14px; 
        margin-bottom: 16px !important; 
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        overflow: hidden; 
    }
    .stream-card-random { 
        position: relative !important;
        border: 2px solid #00FFA3 !important; 
        background: #1C1E26 !important; 
        border-radius: 14px; 
        margin-bottom: 16px !important; 
        box-shadow: 0 4px 12px rgba(0, 255, 163, 0.15);
        overflow: hidden;
    }

    .content-card {
        background-color: #1C1E26;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .overlay-badges-container {
        position: absolute;
        top: 10px;
        left: 10px;
        display: flex;
        align-items: center;
        gap: 0px;
        z-index: 10;
        pointer-events: none;
    }
    
    .badge-live {
        background-color: #FF3333;
        color: #FFFFFF;
        padding: 4px 6px;
        border-top-left-radius: 5px;
        border-bottom-left-radius: 5px;
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 0.3px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.4);
        display: flex;
        align-items: center;
        line-height: 1;
    }

    .badge-viewers {
        background-color: rgba(15, 16, 21, 0.95);
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
        color: #FFFFFF;
        padding: 4px 6px;
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
        font-size: 0.65rem;
        font-weight: 700;
        box-shadow: 0 2px 4px rgba(0,0,0,0.4);
        display: flex;
        align-items: center;
        line-height: 1;
    }

    .tag-badge { 
        display: inline-block; 
        background: rgba(0, 255, 163, 0.08); 
        color: #00FFA3; 
        border: 1px solid rgba(0, 255, 163, 0.35); 
        padding: 2px 5px; 
        border-radius: 5px; 
        font-size: 0.65rem; 
        margin: 3px 3px 0 0; 
    }

    /* 🚨 하단 네비게이션 바도 420px로 잠그고 모니터 정중앙에 고정 */
    .bottom-nav-container {
        position: fixed !important;
        bottom: 0 !important;
        left: 50% !important; 
        transform: translateX(-50%) !important; 
        width: 100% !important;
        max-width: 420px !important; 
        background: rgba(24, 26, 32, 0.95) !important; 
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.1) !important; 
        border-left: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.6) !important; 
        display: flex !important;
        justify-content: space-around !important;
        padding: 10px 0 10px 0 !important; 
        z-index: 900 !important;
    }
    
    .bottom-nav-item { 
        color: #525C6D !important; 
        text-decoration: none !important; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        gap: 4px;
        transition: all 0.2s ease;
    }
    
    .bottom-nav-item.active { color: #00FFA3 !important; }
    .bottom-nav-item svg { transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    .bottom-nav-item.active svg { transform: scale(1.15); filter: drop-shadow(0 0 6px rgba(0, 255, 163, 0.6)); }
    .bottom-nav-item.active span { font-weight: 800 !important; filter: drop-shadow(0 0 4px rgba(0, 255, 163, 0.3)); }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# SVG 아이콘
# ----------------------------------------------------
SVG_ICONS = {
    "live": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:100%; height:100%;"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>',
    "clip": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:100%; height:100%;"><rect x="2" y="4" width="20" height="16" rx="2"></rect><path d="M10 8l6 4-6 4V8z"></path></svg>',
    "trend": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:100%; height:100%;"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>',
    "my": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:100%; height:100%;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>',
    "my_fill": '<svg viewBox="0 0 24 24" fill="#00FFA3" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:100%;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
}

# ----------------------------------------------------
# 3. 데이터 로직 (로컬 DB)
# ----------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect('v_chzzk.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@st.cache_data(ttl=60)
def fetch_lives_from_db():
    try:
        conn = get_db_connection()
        query = '''
            SELECT l.live_id, l.channel_id, l.live_title, l.thumbnail_url, l.viewer_count,
                   s.channel_name, s.follower_count
            FROM live_streams l
            JOIN streamers s ON l.channel_id = s.channel_id
            ORDER BY l.viewer_count DESC
        '''
        lives = conn.execute(query).fetchall()
        conn.close()
        return [dict(row) for row in lives]
    except:
        return []

@st.cache_data(ttl=60)
def fetch_clips_from_db(channel_id):
    try:
        conn = get_db_connection()
        query = '''
            SELECT video_id, video_title, thumbnail_url, view_count, published_at
            FROM clips
            WHERE channel_id = ?
            ORDER BY published_at DESC LIMIT 2
        '''
        clips = conn.execute(query, (channel_id,)).fetchall()
        conn.close()
        return [dict(row) for row in clips]
    except:
        return []

def extract_dummy_tags(title):
    tags = []
    title_lower = title.lower() 
    
    if "스텔" in title: tags.append("스텔라이브")
    if "이세" in title or "이세돌" in title: tags.append("이세돌")
    if "플레" in title or "플레이브" in title: tags.append("플레이브")
    if "홀로" in title: tags.append("홀로라이브")
    
    if "마크" in title or "마인크래프트" in title: tags.append("마인크래프트")
    if "발로" in title or "발로란트" in title: tags.append("발로란트")
    if "롤" in title or "lol" in title_lower: tags.append("리그오브레전드")
    if "블아" in title or "블루아카" in title: tags.append("블루아카이브")
    if "이터널" in title or "이리" in title: tags.append("이터널 리턴")
    if "철권" in title: tags.append("철권8")
    if "종겜" in title or "종합" in title: tags.append("종합게임")
    
    if "저챗" in title or "노가리" in title or "수다" in title: tags.append("저스트채팅")
    if "노래" in title or "가창" in title or "우타와쿠" in title: tags.append("노래방")
    if "월드컵" in title or "이상형" in title: tags.append("이상형월드컵")
    
    tags.append("버튜버")
    return tags

# ----------------------------------------------------
# 4. 상태 관리 (URL 기반)
# ----------------------------------------------------
current_nav = st.query_params.get("nav", "live")
current_sort = urllib.parse.unquote(st.query_params.get("sort", "🔥 시청자순"))

bookmarks = {}
bms_raw = st.query_params.get("bms", "")
if bms_raw:
    try:
        decoded_bms = urllib.parse.unquote(bms_raw)
        for pair in decoded_bms.split("|"):
            if "^" in pair:
                k, v = pair.split("^", 1)
                bookmarks[k] = v
    except: pass

def build_url(nav, sort, bms_dict):
    pairs = []
    for k, v in bms_dict.items():
        safe_v = str(v).replace("|", "").replace("^", "")
        pairs.append(f"{k}^{safe_v}")
    bms_str = urllib.parse.quote("|".join(pairs))
    sort_str = urllib.parse.quote(sort)
    return f"?nav={nav}&sort={sort_str}&bms={bms_str}"

# ----------------------------------------------------
# 헤더 영역 렌더링
# ----------------------------------------------------
st.markdown('''<div class="app-header-container"><div class="app-logo">V-<span>CHZZK</span></div><div class="app-subtitle-badge"><span>●</span>실시간 버추얼 라운지</div></div>''', unsafe_allow_html=True)

# ----------------------------------------------------
# 5. 탭 콘텐츠 영역
# ----------------------------------------------------
if current_nav == "live":
    sort_html = '<div class="custom-segment-box">'
    for opt in ["🔥 시청자순", "⭐ 팔로워", "🎲 랜덤 픽"]:
        active_cls = "active" if current_sort == opt else ""
        opt_url = build_url("live", opt, bookmarks)
        sort_html += f'<a href="{opt_url}" target="_self" class="segment-tab {active_cls}">{opt}</a>'
    sort_html += '</div>'
    st.markdown(sort_html, unsafe_allow_html=True)
    
    lives = fetch_lives_from_db()
    
    if current_sort == "🔥 시청자순":
        sorted_lives = sorted(lives, key=lambda x: x.get("viewer_count", 0), reverse=True)
    elif current_sort == "⭐ 팔로워":
        sorted_lives = sorted(lives, key=lambda x: x.get("follower_count", 0), reverse=True)
    else:
        sorted_lives = lives.copy()
        random.shuffle(sorted_lives)

    for idx, live in enumerate(sorted_lives, 1):
        ch_id = live.get("channel_id")
        ch_name = live.get("channel_name", "스트리머")
        title = live.get("live_title", "")
        viewer_count = live.get("viewer_count", 0)
        formatted_viewers = f"{viewer_count:,}명"
        
        thumb = live.get("thumbnail_url", "")
        if not thumb or thumb.strip() == "":
            thumb = "https://via.placeholder.com/480x270/2A2D35/9CA3AF?text=No+Thumbnail"
            
        extracted_tags = extract_dummy_tags(title)
        tags_html = "".join([f'<span class="tag-badge">#{html.escape(t)}</span>' for t in extracted_tags])
        
        is_bookmarked = ch_id in bookmarks
        bm_svg = SVG_ICONS['my_fill'] if is_bookmarked else SVG_ICONS['my']
        
        card_class = "stream-card-random" if (current_sort == "🎲 랜덤 픽" and idx == 1) else "stream-card"
        
        temp_bms = bookmarks.copy()
        if is_bookmarked: del temp_bms[ch_id]
        else: temp_bms[ch_id] = ch_name
        toggle_url = build_url("live", current_sort, temp_bms)
        
        card_html = f'''
        <div class="{card_class}">
            <div class="overlay-badges-container">
                <span class="badge-live">LIVE</span>
                <span class="badge-viewers">{formatted_viewers}</span>
            </div>
            <a href="https://chzzk.naver.com/live/{ch_id}" target="_blank" style="text-decoration:none; color:inherit; display:block;">
                <img src="{thumb}" style="width:100%; aspect-ratio:16/9; object-fit:cover; display:block; border-bottom: 1px solid rgba(255,255,255,0.05);">
                <div style="padding: 12px 14px 6px 14px;">
                    <div style="font-weight:700; font-size:0.95rem; color: #FFFFFF; line-height: 1.4;">{html.escape(title)}</div>
                </div>
            </a>
            <div style="padding: 0 14px 12px 14px;">
                <div style="display:flex; align-items:center; gap:4px;">
                    <a href="{toggle_url}" target="_self" style="text-decoration:none; color:#9CA3AF; display:flex; align-items:center; justify-content:center; width:14px; height:14px; flex-shrink:0; transform: translateY(-2px);">{bm_svg}</a>
                    <a href="https://chzzk.naver.com/live/{ch_id}" target="_blank" style="text-decoration:none; font-weight:700; color:#00FFA3; font-size:0.85rem; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; line-height:1; display:flex; align-items:center;">{html.escape(ch_name)}</a>
                </div>
                <div style="margin-top:6px;">{tags_html}</div>
            </div>
        </div>'''
        st.markdown(card_html, unsafe_allow_html=True)
        
        if idx == 3:
            native_ad_html = '''<div class="content-card" style="display:flex; align-items:center; justify-content:space-between; padding: 12px 14px; margin-bottom: 16px;"><div style="display:flex; align-items:center; gap:12px; flex:1; min-width:0;"><div style="position:relative; width:80px; height:60px; flex-shrink:0; border-radius:6px; overflow:hidden; background:#2A2D35;"><img src="https://via.placeholder.com/180x135.png?text=AD" style="width:100%; height:100%; object-fit:cover; display:block;"><span style="position:absolute; top:4px; left:4px; background-color:#FF3333; color:#FFFFFF; font-size:0.5rem; font-weight:800; padding:1px 3px; border-radius:3px; line-height:1;">광고</span></div><div style="flex-grow:1; display:flex; flex-direction:column; justify-content:center; min-width:0;"><div style="font-size:0.85rem; font-weight:700; color:#FFFFFF; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; margin-bottom:4px; line-height:1.2;">(스폰서) 추천 프로모션 및 제휴 상품 안내</div><div style="font-size:0.7rem; color:#9CA3AF; display:flex; align-items:center; gap:4px; line-height:1;"><span>🌐 공식 파트너 스폰서</span></div></div></div><a href="https://your-ad-link.com" target="_blank" style="flex-shrink:0; border-left:1px solid rgba(255,255,255,0.08); padding-left:12px; margin-left:8px; text-decoration:none;"><span style="font-size:0.75rem; font-weight:700; color:#00FFA3; background:rgba(0,255,163,0.1); padding:5px 10px; border-radius:6px; display:inline-block; line-height:1;">바로가기</span></a></div>'''
            st.markdown(native_ad_html, unsafe_allow_html=True)

# ----------------------------------------------------
# 핫클립(Clip) 탭
# ----------------------------------------------------
elif current_nav == "clip":
    st.markdown(f'''<div style="display:flex; align-items:center; gap:4px; margin-bottom:14px;"><div style="color:#00FFA3; width:16px; height:16px; flex-shrink:0; display:flex; align-items:center; justify-content:center; transform: translateY(-2px);">{SVG_ICONS['clip']}</div><div style="font-weight:800; font-size:1.05rem; color:#FFF; line-height:1; margin-top:1px;">MY 핫클립</div></div>''', unsafe_allow_html=True)
    
    if not bookmarks:
        st.markdown("<div style='text-align:center; padding:30px; color:#9CA3AF; background:#1C1E26; border-radius:12px; border:1px solid rgba(255,255,255,0.1); font-size:0.85rem;'>즐겨찾기한 스트리머가 없습니다.<br>라이브 탭에서 즐겨찾기를 추가해 보세요!</div>", unsafe_allow_html=True)
    else:
        for b_id, b_name in bookmarks.items():
            videos = fetch_clips_from_db(b_id)
            
            temp_bms = bookmarks.copy()
            if b_id in temp_bms: del temp_bms[b_id]
            toggle_url = build_url("clip", current_sort, temp_bms)
            
            card_html = f'''<div class="content-card"><div style="display:flex; align-items:center; gap:4px; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.05);"><a href="{toggle_url}" target="_self" style="text-decoration:none; color:#00FFA3; width:14px; height:14px; flex-shrink:0; display:flex; align-items:center; justify-content:center; transform: translateY(-2px);">{SVG_ICONS['my_fill']}</a><div style="display:flex; align-items:center; gap:4px;"><span style="font-weight: 700; color: #00FFA3; font-size: 0.95rem; line-height:1; display:flex; align-items:center;">{html.escape(b_name)}</span><span style="font-weight: 600; color: #E5E7EB; font-size: 0.8rem; line-height:1; display:flex; align-items:center;">님의 최신 영상</span></div></div>'''
            
            if videos:
                for i, v in enumerate(videos):
                    v_id = v.get("video_id")
                    v_title = v.get("video_title", "제목 없음")
                    v_thumb = v.get("thumbnail_url", "https://via.placeholder.com/480x270/2A2D35/9CA3AF?text=No+Thumbnail")
                    v_views = v.get("view_count", 0)
                    
                    margin_style = "margin-bottom: 12px;" if i == 0 and len(videos) > 1 else ""
                    
                    card_html += f'''<a href="https://chzzk.naver.com/video/{v_id}" target="_blank" style="text-decoration:none; color:inherit; display:block; {margin_style}"><div style="display:flex; gap:12px; align-items:center;"><div style="width:105px; height:58px; background:#2A2D35; border-radius:6px; display:flex; align-items:center; justify-content:center; flex-shrink:0; position:relative; overflow:hidden;"><img src="{v_thumb}" style="width:100%; height:100%; object-fit:cover;"><span style="position:absolute; background:rgba(0,0,0,0.8); color:#FFF; font-size:0.6rem; padding:2px 4px; border-radius:3px; bottom:4px; right:4px; font-weight:600; line-height:1;">재생</span></div><div style="flex:1; min-width:0;"><div style="font-weight:700; color:#FFFFFF; font-size:0.9rem; margin-bottom:6px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; line-height:1.2;">{html.escape(v_title)}</div><div style="color:#9CA3AF; font-size:0.75rem; font-weight:500; line-height:1;">조회수 {v_views:,}회</div></div></div></a>'''
            else:
                card_html += f'''<div style="display:flex; gap:12px; align-items:center;"><div style="width:105px; height:58px; background:#2A2D35; border: 1px solid rgba(255,255,255,0.1); border-radius:6px; display:flex; align-items:center; justify-content:center; color:#9CA3AF; font-size:0.75rem; flex-shrink:0; position:relative; box-shadow: inset 0 0 10px rgba(0,0,0,0.5);"><span style="position:absolute; background:rgba(0,0,0,0.8); color:#FFF; font-size:0.6rem; padding:2px 4px; border-radius:3px; bottom:4px; right:4px; font-weight:600; line-height:1;">0:45</span>▶ 재생</div><div style="flex:1; min-width:0;"><div style="font-weight:700; color:#FFFFFF; font-size:0.9rem; margin-bottom:6px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; line-height:1.2;">{html.escape(b_name)} 채널의 최신 영상이 없습니다.</div></div></div>'''
            
            card_html += "</div>"
            st.markdown(card_html, unsafe_allow_html=True)

# ----------------------------------------------------
# 트렌드(Trend) 탭
# ----------------------------------------------------
elif current_nav == "trend":
    st.markdown(f'''<div style="display:flex; align-items:center; gap:4px; margin-bottom:14px;"><div style="color:#00FFA3; width:16px; height:16px; flex-shrink:0; display:flex; align-items:center; justify-content:center; transform: translateY(-2px);">{SVG_ICONS['trend']}</div><div style="font-weight:800; font-size:1.05rem; color:#FFF; line-height:1; margin-top:1px;">실시간 인기 태그</div></div>''', unsafe_allow_html=True)
    
    lives = fetch_lives_from_db()
    tag_stats = {}
    
    for live in lives:
        viewers = live.get("viewer_count", 0)
        tags = extract_dummy_tags(live.get("live_title", ""))
        for tag in tags:
            if tag not in tag_stats: tag_stats[tag] = 0
            tag_stats[tag] += viewers

    if not tag_stats:
        st.markdown("<div style='text-align:center; padding:30px; color:#9CA3AF; background:#1C1E26; border-radius:12px; border:1px solid rgba(255,255,255,0.1); font-size:0.85rem;'>현재 수집된 트렌드 데이터가 없습니다.</div>", unsafe_allow_html=True)
    else:
        sorted_tags = sorted(tag_stats.items(), key=lambda x: x[1], reverse=True)[:10]
        
        for idx, (tag, count) in enumerate(sorted_tags, 1):
            if idx <= 3:
                rank_style = "width: 26px; height: 26px; border-radius: 6px; background: rgba(0, 255, 163, 0.15); color: #00FFA3; font-weight: 700; font-size: 0.85rem; display: flex; align-items: center; justify-content: center; flex-shrink:0;"
            else:
                rank_style = "width: 26px; height: 26px; border-radius: 6px; background: rgba(255, 255, 255, 0.05); color: #6B7280; font-weight: 700; font-size: 0.85rem; display: flex; align-items: center; justify-content: center; flex-shrink:0;"
            st.markdown(f'''<div class="content-card" style="display:flex; align-items:center; justify-content:space-between; padding: 12px 14px;"><div style="display:flex; align-items:center; gap: 12px;"><div style="{rank_style}">{idx}</div><div style="font-size: 0.95rem; font-weight: 700; color: #E5E7EB; line-height:1;">#{html.escape(tag)}</div></div><div style="font-size: 0.8rem; font-weight: 500; color: #8E929B; display:flex; align-items:center; gap:4px; line-height:1;"><span style="color:#00FFA3; font-size:0.5rem;">●</span> {count:,}명</div></div>''', unsafe_allow_html=True)

# ----------------------------------------------------
# 마이(My) 탭
# ----------------------------------------------------
elif current_nav == "my":
    st.markdown(f'''<div style="display:flex; align-items:center; gap:4px; margin-bottom:14px;"><div style="color:#00FFA3; width:16px; height:16px; flex-shrink:0; display:flex; align-items:center; justify-content:center; transform: translateY(-2px);">{SVG_ICONS['my']}</div><div style="font-weight:800; font-size:1.05rem; color:#FFF; line-height:1; margin-top:1px;">MY 채널</div></div>''', unsafe_allow_html=True)
    if not bookmarks:
        st.markdown("<div style='text-align:center; padding:30px; color:#9CA3AF; background:#1C1E26; border-radius:12px; border:1px solid rgba(255,255,255,0.1); font-size:0.85rem;'>즐겨찾기한 스트리머가 없습니다.<br>라이브 탭에서 즐겨찾기를 추가해 보세요!</div>", unsafe_allow_html=True)
    else:
        for b_id, b_name in bookmarks.items():
            
            temp_bms = bookmarks.copy()
            if b_id in temp_bms: del temp_bms[b_id]
            toggle_url = build_url("my", current_sort, temp_bms)
            
            st.markdown(f'''<div class="content-card" style="display:flex; justify-content:space-between; align-items:center; padding: 14px;"><div style="display:flex; align-items:flex-start; gap:4px;"><a href="{toggle_url}" target="_self" style="text-decoration:none; color:#00FFA3; width:14px; height:14px; flex-shrink:0; display:flex; align-items:center; justify-content:center; transform: translateY(-2px);">{SVG_ICONS['my_fill']}</a><div><div style="font-weight:700; color:#00FFA3; font-size:0.95rem; line-height:1; margin-bottom:6px; display:flex; align-items:center;">{html.escape(b_name)}</div><div style="font-size:0.75rem; color:#9CA3AF; font-weight:500; line-height:1;">채널 ID: {b_id}</div></div></div><a href="https://chzzk.naver.com/live/{b_id}" target="_blank" style="text-decoration:none; background:rgba(0,255,163,0.1); color:#00FFA3; border:1px solid rgba(0,255,163,0.4); padding:6px 14px; border-radius:6px; font-size:0.8rem; font-weight:700; transition:all 0.2s; line-height:1;">방송 보기</a></div>''', unsafe_allow_html=True)

# ----------------------------------------------------
# 6. 하단 고정 네비게이션 바
# ----------------------------------------------------
nav_tabs_data = [("live", "live", "라이브"), ("clip", "clip", "핫클립"), ("trend", "trend", "트렌드"), ("my", "my", "마이")]
bottom_nav_html = '<div class="bottom-nav-container">'
for key, icon_key, label in nav_tabs_data:
    active_cls = "active" if current_nav == key else ""
    nav_url = build_url(key, current_sort, bookmarks)
    bottom_nav_html += f'<a href="{nav_url}" target="_self" class="bottom-nav-item {active_cls}"><div style="width:24px; height:24px; flex-shrink:0;">{SVG_ICONS[icon_key]}</div><span style="font-size: 0.65rem; font-weight: 700; line-height: 1.2; margin-top:3px;">{label}</span></a>'
bottom_nav_html += '</div>'
st.markdown(bottom_nav_html, unsafe_allow_html=True)
