import sqlite3
import requests
import datetime
import time

VTUBER_KEYWORDS = ["버추얼", "버튜버", "버츄얼", "붜츄얼", "v튜버", "vtuber", "virtual", "브이튜버", "이세계", "스텔라이브", "이세돌", "플레이브"]

# ----------------------------------------------------
# 1. DB 연결 및 3대 테이블 생성 (스트리머, 라이브, 핫클립)
# ----------------------------------------------------
def init_db():
    conn = sqlite3.connect('v_chzzk.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS streamers (
        channel_id TEXT PRIMARY KEY, channel_name TEXT NOT NULL, follower_count INTEGER DEFAULT 0, updated_at TIMESTAMP)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS live_streams (
        live_id INTEGER PRIMARY KEY, channel_id TEXT NOT NULL, live_title TEXT, thumbnail_url TEXT, viewer_count INTEGER DEFAULT 0, updated_at TIMESTAMP,
        FOREIGN KEY (channel_id) REFERENCES streamers(channel_id))''')

    # [신규] 핫클립 저장용 자식 테이블
    cursor.execute('''CREATE TABLE IF NOT EXISTS clips (
        video_id TEXT PRIMARY KEY, channel_id TEXT NOT NULL, video_title TEXT, thumbnail_url TEXT, view_count INTEGER DEFAULT 0, published_at TEXT, updated_at TIMESTAMP,
        FOREIGN KEY (channel_id) REFERENCES streamers(channel_id))''')
        
    conn.commit()
    return conn

# ----------------------------------------------------
# 2. 실시간 라이브 수집
# ----------------------------------------------------
def fetch_and_save_lives(conn):
    headers = {"User-Agent": "Mozilla/5.0"}
    raw_lives = []
    url = "https://api.chzzk.naver.com/service/v1/lives?size=50&sortType=POPULAR"
    
    print("📡 치지직 라이브 API 탐색 중...")
    for _ in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=3.0)
            if res.status_code != 200: break
            content = res.json().get("content", {})
            raw_lives.extend(content.get("data", []))
            
            page_info = content.get('page', {}).get('next', {})
            if not page_info: break
            url = f"https://api.chzzk.naver.com/service/v1/lives?size=50&sortType=POPULAR&concurrentUserCount={page_info.get('concurrentUserCount')}&liveId={page_info.get('liveId')}"
        except: break

    cursor = conn.cursor()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    saved_count = 0

    for live in raw_lives:
        if not any(kw in str(live).lower() for kw in VTUBER_KEYWORDS): continue
            
        channel_id = live.get("channel", {}).get("channelId")
        channel_name = live.get("channel", {}).get("channelName", "스트리머")
        
        cursor.execute('''INSERT INTO streamers (channel_id, channel_name, updated_at) VALUES (?, ?, ?)
            ON CONFLICT(channel_id) DO UPDATE SET channel_name=excluded.channel_name, updated_at=excluded.updated_at''', 
            (channel_id, channel_name, current_time))
        
        live_id = live.get("liveId")
        live_title = live.get("liveTitle", "")
        thumb = (live.get("liveImageUrl") or "").replace("{type}", "480")
        viewers = live.get("concurrentUserCount", 0)
        
        cursor.execute('''INSERT OR REPLACE INTO live_streams (live_id, channel_id, live_title, thumbnail_url, viewer_count, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)''', (live_id, channel_id, live_title, thumb, viewers, current_time))
        saved_count += 1

    cursor.execute("DELETE FROM live_streams WHERE updated_at < datetime(?, '-10 minutes')", (current_time,))
    conn.commit()
    print(f"✅ 현재 방송 중인 버튜버 {saved_count}명 저장 완료!")

# ----------------------------------------------------
# 3. 핫클립 영상 수집 (신규)
# ----------------------------------------------------
def fetch_and_save_clips(conn):
    headers = {"User-Agent": "Mozilla/5.0"}
    cursor = conn.cursor()
    
    # DB에 저장된 모든 스트리머 채널 ID를 꺼내옵니다.
    cursor.execute("SELECT channel_id, channel_name FROM streamers")
    channels = cursor.fetchall()
    
    print(f"🎬 총 {len(channels)}개 채널의 핫클립 수집 시작 (IP 보호를 위해 천천히 진행됩니다)...")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    saved_count = 0
    
    for cid, cname in channels:
        url = f"https://api.chzzk.naver.com/service/v1/channels/{cid}/videos?sortType=LATEST&size=2"
        try:
            res = requests.get(url, headers=headers, timeout=2.0)
            if res.status_code == 200:
                videos = res.json().get("content", {}).get("data", [])
                for v in videos:
                    v_id = str(v.get("videoNo"))
                    v_title = v.get("videoTitle", "제목 없음")
                    v_thumb = (v.get("thumbnailImageUrl") or "").replace("{type}", "480")
                    v_views = v.get("readCount", 0)
                    v_date = v.get("publishDate", "")
                    
                    cursor.execute('''INSERT OR REPLACE INTO clips 
                        (video_id, channel_id, video_title, thumbnail_url, view_count, published_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', (v_id, cid, v_title, v_thumb, v_views, v_date, current_time))
                    saved_count += 1
        except:
            pass
        
        # 🚨 IP 차단 방어 (0.1초 휴식)
        time.sleep(0.1)
        
    conn.commit()
    print(f"✅ 총 {saved_count}개의 최신 핫클립 DB 저장 완료!")

# ----------------------------------------------------
# 메인 실행부
# ----------------------------------------------------
if __name__ == "__main__":
    print("🚀 [최종] 치지직 데이터 자동 수집기 가동...")
    db_conn = init_db()
    fetch_and_save_lives(db_conn)
    fetch_and_save_clips(db_conn)
    db_conn.close()
    print("🏁 모든 파이프라인 작업 종료. 안전하게 DB에 적재되었습니다.")