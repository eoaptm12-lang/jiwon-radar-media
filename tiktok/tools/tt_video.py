"""호기심 충전소 틱톡 영상 생성기 (퀴즈 / 1분 상식)
사용: python3 tt_video.py spec.json out_dir
"""
import json, os, sys, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, SR = 1080, 1920, 30, 44100
BLACK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BG = "#0e0e1a"; CARD = "#1d1d33"
PINK = "#ff2d75"; CYAN = "#22d3ee"; YEL = "#ffd60a"; LIME = "#b8f24a"
WHITE = "#ffffff"; GRAY = "#9aa0b4"
BRAND = "호기심 충전소"
MAXW = 820  # 오른쪽 틱톡 버튼 피하는 안전 폭
COL = {"pink": PINK, "cyan": CYAN, "yel": YEL, "lime": LIME, "white": WHITE, "gray": GRAY}


def F(n, black=True):
    return ImageFont.truetype(BLACK if black else REG, n, index=1)


def wrap(d, text, font, maxw=MAXW):
    out = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split(" "):
            t = (cur + " " + word).strip()
            if d.textlength(t, font=font) <= maxw or not cur:
                cur = t
            else:
                out.append(cur); cur = word
        out.append(cur)
    return out


def block(d, y, text, size, color, black=True, gap=0.28, maxw=MAXW):
    f = F(size, black)
    n_explicit = len(text.split("\n"))
    while True:
        lines = wrap(d, text, f, maxw)
        if (len(lines) == n_explicit and all(d.textlength(l, font=f) <= maxw for l in lines)) or f.size < 40:
            break
        f = F(f.size - 4, black)
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text(((W - w) / 2 - 20, y), ln, font=f, fill=color)
        y += int(f.size * (1 + gap))
    return y


def mini_battery(d, x, y, h=56, accent=None):
    w = h * 1.7; lw = max(4, int(h * 0.1))
    d.rounded_rectangle((x + w, y + h * 0.32, x + w + h * 0.16, y + h * 0.68), 3, fill=WHITE)
    d.rounded_rectangle((x, y, x + w, y + h), int(h * 0.22), outline=WHITE, width=lw)
    pad = lw * 1.6; iw = (w - 2 * pad - 2 * lw * 0.8) / 3
    for i, c in enumerate([PINK, CYAN, LIME]):
        cx = x + pad + i * (iw + lw * 0.8)
        d.rounded_rectangle((cx, y + pad, cx + iw, y + h - pad), 3, fill=c)
    return x + w + h * 0.16


def frame(accent, tag, progress):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    x = mini_battery(d, 60, 178)
    d.text((x + 18, 176), BRAND, font=F(42), fill=WHITE)
    if tag:
        tw = d.textlength(tag, font=F(34))
        d.rounded_rectangle((W - 100 - tw, 176, W - 60, 236), 30, outline=accent, width=4)
        d.text((W - 80 - tw, 181), tag, font=F(34), fill=accent)
    # 진행 바 (완주 유도)
    d.rounded_rectangle((60, 268, W - 60, 280), 6, fill="#26263d")
    d.rounded_rectangle((60, 268, 60 + (W - 120) * max(0.02, progress), 280), 6, fill=accent)
    return im, d


# ---------------- scene renderers ----------------

def r_hook(s, p, accent):
    im, d = frame(accent, s.get("tag"), p)
    y = 520
    if s.get("kicker"):
        y = block(d, y, s["kicker"], 140, COL.get(s.get("kicker_color", "yel"))) + 30
    y = block(d, y, s["title"], s.get("size", 120), WHITE, gap=0.15) + 60
    if s.get("pill"):
        f = F(52); w = d.textlength(s["pill"], font=f)
        d.rounded_rectangle(((W - w) / 2 - 70, y, (W + w) / 2 + 30, y + 100), 50, fill=accent)
        d.text(((W - w) / 2 - 20, y + 18), s["pill"], font=f, fill=WHITE if accent != LIME else BG)
    if s.get("sub"):
        block(d, 1480, s["sub"], 50, GRAY, black=False)
    return im


def r_question(s, p, accent, count=None):
    im, d = frame(accent, s.get("tag"), p)
    y = block(d, 400, s["q"], s.get("size", 96), WHITE, gap=0.2)
    if s.get("qtype", "ox") == "ox":
        for i, (lab, col) in enumerate([("O", CYAN), ("X", PINK)]):
            x0 = 130 + i * 420
            d.rounded_rectangle((x0, 900, x0 + 360, 1250), 40, outline=col, width=10)
            lw = d.textlength(lab, font=F(210))
            d.text((x0 + (360 - lw) / 2, 935), lab, font=F(210), fill=col)
    if count is not None:
        d.ellipse((430, 1360, 630, 1560), outline=YEL, width=12)
        f = F(110); w = d.textlength(str(count), font=f)
        d.text((530 - w / 2, 1385), str(count), font=f, fill=YEL)
    return im


def r_answer(s, p, accent):
    im, d = frame(accent, s.get("tag"), p)
    block(d, 400, "정답은", 66, GRAY, black=False)
    ans = s["a"]; col = CYAN if ans == "O" else PINK
    d.rounded_rectangle((385, 510, 675, 800), 40, fill=col)
    f = F(210); w = d.textlength(ans, font=f)
    d.text((530 - w / 2, 525), ans, font=f, fill=WHITE if ans == "X" else BG)
    y = block(d, 920, s["why"], 76, WHITE, gap=0.25)
    if s.get("more"):
        block(d, y + 40, s["more"], 50, GRAY, black=False)
    return im


def r_balance(s, p, accent):
    im, d = frame(CYAN, s.get("tag", "밸런스게임"), p)
    block(d, 340, s.get("title", "평생 하나만 고른다면?"), 70, WHITE)
    for i, (lab, txt, col, y0) in enumerate([("A", s["a"], CYAN, 520), ("B", s["b"], PINK, 1130)]):
        d.rounded_rectangle((90, y0, W - 130, y0 + 440), 40, fill=CARD, outline=col, width=6)
        block(d, y0 + 40, lab, 90, col)
        block(d, y0 + 170, txt, 80, WHITE, gap=0.12, maxw=700)
    block(d, 1000, "VS", 80, YEL)
    block(d, 1640, "댓글로 A or B", 54, GRAY)
    return im


def r_result(s, p, accent):
    im, d = frame(accent, "결과", p)
    block(d, 520, s.get("title", "몇 개 맞혔어요?"), 100, WHITE)
    block(d, 740, s["lines"], 70, YEL, gap=0.4)
    f = F(56); t = s.get("pill", "팔로우하면 내일 2탄"); w = d.textlength(t, font=f)
    d.rounded_rectangle(((W - w) / 2 - 70, 1250, (W + w) / 2 + 30, 1360), 55, fill=accent)
    d.text(((W - w) / 2 - 20, 1270), t, font=f, fill=WHITE if accent != LIME else BG)
    return im


def r_text(s, p, accent):
    im, d = frame(accent, s.get("tag"), p)
    y = s.get("y", 500)
    if s.get("kicker"):
        y = block(d, y, s["kicker"], 84, COL.get(s.get("kicker_color", "lime"), accent)) + 30
    y = block(d, y, s["body"], s.get("size", 84), WHITE, gap=0.25) + 50
    if s.get("hl"):
        y = block(d, y, s["hl"], s.get("hl_size", 76), COL.get(s.get("hl_color", "lime"), accent), gap=0.25) + 40
    if s.get("icon") == "square":
        d.rectangle((400, 1100, 660, 1360), outline=WHITE, width=14)
        for (x, yy) in [(400, 1100), (660, 1100), (400, 1360), (660, 1360)]:
            d.ellipse((x - 28, yy - 28, x + 28, yy + 28), outline=PINK, width=8)
    if s.get("icon") == "round":
        d.rounded_rectangle((390, 1080, 670, 1460), 140, outline=WHITE, width=14)
        d.rounded_rectangle((430, 1120, 630, 1420), 100, fill="#1d2a3a")
    if s.get("icon") == "hole":
        d.rounded_rectangle((390, 1080, 670, 1460), 140, outline=WHITE, width=14)
        d.ellipse((520, 1380, 540, 1400), fill=LIME)
    if s.get("sub"):
        block(d, 1560, s["sub"], 48, GRAY, black=False)
    return im


# ---------------- audio ----------------

def tone(f, dur, vol=0.3, decay=6.0):
    t = np.arange(int(SR * dur)) / SR
    return vol * np.sin(2 * np.pi * f * t) * np.exp(-decay * t)


def sfx(kind):
    if kind == "tick":
        return tone(1800, 0.06, 0.25, 60)
    if kind == "ding":
        return tone(1046, 0.6, 0.28, 5) + tone(1568, 0.6, 0.18, 6)
    if kind == "whoosh":
        n = int(SR * 0.28); noise = np.random.randn(n)
        env = np.sin(np.linspace(0, np.pi, n)) ** 2
        k = np.ones(30) / 30
        return 0.12 * np.convolve(noise, k, "same") * env
    if kind == "pop":
        t = np.arange(int(SR * 0.12)) / SR
        return 0.3 * np.sin(2 * np.pi * (600 - 3000 * t) * t) * np.exp(-25 * t)
    return np.zeros(1)


def bgm(total, bpm=100, seed=0):
    rng = np.random.default_rng(seed)
    n = int(SR * total); out = np.zeros(n)
    beat = 60 / bpm
    chords = [[261.6, 329.6, 392.0], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7]]
    t_all = np.arange(n) / SR
    for bar in range(int(total / (beat * 4)) + 1):
        start = bar * beat * 4
        ch = chords[bar % 4]
        i0 = int(start * SR); i1 = min(n, int((start + beat * 4) * SR))
        if i0 >= n: break
        t = t_all[i0:i1] - start
        pad = sum(np.sin(2 * np.pi * f * t) for f in ch) / 3
        out[i0:i1] += 0.045 * pad * (0.6 + 0.4 * np.exp(-t))
        for b in range(4):
            bs = int((start + b * beat) * SR)
            if bs >= n: break
            k = tone(55, 0.25, 0.22, 18)
            out[bs:bs + len(k)] += k[: n - bs]
            hs = int((start + b * beat + beat / 2) * SR)
            if hs < n:
                h = 0.03 * rng.standard_normal(int(SR * 0.04)) * np.exp(-np.linspace(0, 8, int(SR * 0.04)))
                out[hs:hs + len(h)] += h[: n - hs]
            # arpeggio
            ns = int((start + b * beat) * SR)
            a = tone(ch[b % 3] * 2, beat * 0.9, 0.035, 4)
            out[ns:ns + len(a)] += a[: n - ns]
    fade = int(SR * 1.0)
    out[-fade:] *= np.linspace(1, 0, fade)
    return out


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


# ---------------- build ----------------

def overlay_bar(im, accent, p):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((60, 268, W - 60, 280), 6, fill="#26263d")
    d.rounded_rectangle((60, 268, 60 + (W - 120) * max(0.02, min(1, p)), 280), 6, fill=accent)


def pop(base, k):
    """k: 0..1 진행, 장면 시작 때 살짝 커지며 등장"""
    if k >= 1:
        return base.copy()
    s = 0.90 + 0.10 * (1 - (1 - k) ** 3)
    top = 300
    region = base.crop((0, top, W, H))
    rw, rh = int(W * s), int((H - top) * s)
    region = region.resize((rw, rh), Image.BILINEAR)
    im = base.copy()
    ImageDraw.Draw(im).rectangle((0, top, W, H), fill=BG)
    im.paste(region, ((W - rw) // 2, top + ((H - top) - rh) // 2))
    return im


def countdown_overlay(im, frac_left, num):
    d = ImageDraw.Draw(im)
    d.ellipse((430, 1360, 630, 1560), outline="#33334d", width=12)
    d.arc((430, 1360, 630, 1560), -90, -90 + 360 * frac_left, fill=YEL, width=12)
    f = F(110); w = d.textlength(str(num), font=f)
    d.text((530 - w / 2, 1385), str(num), font=f, fill=YEL)


def build(spec, out):
    out = os.path.abspath(out); os.makedirs(out, exist_ok=True)
    accent = COL[spec.get("accent", "pink")]
    cd = spec.get("countdown", 2.1)
    segs = []  # dict(base, dur, fx, cd)
    for s in spec["scenes"]:
        typ = s["type"]
        if typ == "hook": segs.append(dict(img=r_hook(s, 0, accent), dur=s["dur"], fx="pop"))
        elif typ == "question":
            segs.append(dict(img=r_question(s, 0, accent), dur=s["dur"] + cd, fx="whoosh", cd=cd))
        elif typ == "answer": segs.append(dict(img=r_answer(s, 0, accent), dur=s["dur"], fx="ding"))
        elif typ == "balance": segs.append(dict(img=r_balance(s, 0, accent), dur=s["dur"], fx="whoosh", acc=CYAN))
        elif typ == "result": segs.append(dict(img=r_result(s, 0, accent), dur=s["dur"], fx="pop"))
        elif typ == "text": segs.append(dict(img=r_text(s, 0, accent), dur=s["dur"], fx="whoosh"))
    total = sum(g["dur"] for g in segs)
    mp4 = f"{out}/{spec['name']}.mp4"
    music = bgm(total, spec.get("bpm", 100), spec.get("seed", 1))
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                             "-crf", "20", "-pix_fmt", "yuv420p", f"{out}/video.mp4"], stdin=subprocess.PIPE)
    t = 0.0; fidx = 0
    for gi, g in enumerate(segs):
        nf = int(round((t + g["dur"]) * FPS)) - int(round(t * FPS))
        st = t
        e = sfx(g["fx"]); i = int(st * SR); music[i:i + len(e)] += e[: len(music) - i]
        if g.get("cd"):
            q_end = st + g["dur"] - g["cd"]
            for k in range(3):
                ts = q_end + k * g["cd"] / 3
                e = sfx("tick"); i = int(ts * SR); music[i:i + len(e)] += e[: len(music) - i]
        for f in range(nf):
            now = st + f / FPS
            im = pop(g["img"], f / 6.0)
            if g.get("cd"):
                q_end = st + g["dur"] - g["cd"]
                if now >= q_end:
                    left = (st + g["dur"] - now) / g["cd"]
                    countdown_overlay(im, left, max(1, int(np.ceil(left * 3))))
            overlay_bar(im, g.get("acc", accent), now / total)
            proc.stdin.write(im.tobytes())
        t += g["dur"]
        if gi == 0: g["img"].save(f"{out}/cover.png")
    proc.stdin.close(); proc.wait()
    write_wav(f"{out}/audio.wav", music * 0.9)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{out}/video.mp4", "-i", f"{out}/audio.wav",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", mp4], check=True)
    # 장면 미리보기 시트
    th = [g["img"].resize((216, 384)) for g in segs]
    cols = 8; rows = (len(th) + cols - 1) // cols
    sh = Image.new("RGB", (cols * 224 + 8, rows * 392 + 8), "#333")
    for i2, im2 in enumerate(th): sh.paste(im2, (8 + (i2 % cols) * 224, 8 + (i2 // cols) * 392))
    sh.save(f"{out}/sheet.jpg", quality=85)
    print(mp4, round(total, 1), "s", len(segs), "scenes")
    return mp4


if __name__ == "__main__":
    build(json.load(open(sys.argv[1])), sys.argv[2])
