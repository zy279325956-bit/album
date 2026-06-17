# 一键构建：扫描 musics/ 下的音频，生成 musics/playlist.json 和 musics/playlist.js
#   playlist.js 供本地 file:// 双击打开时读取（浏览器禁止 file:// 下 fetch 本地 json）
#   playlist.json 供 http 部署时读取；播放器优先 .js，回退 .json
#   播放器会自动读取并列表循环；换歌 / 部署前跑一次：python _build.py
import os, sys, json, urllib.parse

try:                                    # 让 Windows 控制台也能正常输出中文
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))
MUSICS = os.path.join(ROOT, "musics")
AUDIO_EXT = (".mp3", ".m4a", ".aac", ".ogg", ".oga", ".wav", ".flac")


def build_playlist():
    if not os.path.isdir(MUSICS):
        print("没有 musics/ 目录，跳过歌单", flush=True)
        return
    files = sorted(f for f in os.listdir(MUSICS) if f.lower().endswith(AUDIO_EXT))
    pl = [{"src": "musics/" + urllib.parse.quote(f),
           "title": os.path.splitext(f)[0]} for f in files]
    data = json.dumps(pl, ensure_ascii=False, indent=2)
    with open(os.path.join(MUSICS, "playlist.json"), "w", encoding="utf-8") as fp:
        fp.write(data)
    # 同名 .js 版本：file:// 双击打开时由 <script> 读取（绕开本地 fetch 限制）
    with open(os.path.join(MUSICS, "playlist.js"), "w", encoding="utf-8") as fp:
        fp.write("window.WEDDING_PLAYLIST = " + data + ";\n")
    print("歌单：musics/playlist.json + playlist.js 共 %d 首" % len(pl), flush=True)
    for it in pl:
        print("  -", it["title"], flush=True)


if __name__ == "__main__":
    build_playlist()
    print("DONE", flush=True)
