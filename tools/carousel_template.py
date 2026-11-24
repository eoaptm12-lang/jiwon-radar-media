from PIL import Image, ImageDraw, ImageFont
import os, math

W, H = 1080, 1350
FD = "/usr/share/fonts/opentype/noto/"
def F(w, s): return ImageFont.truetype(FD + f"NotoSansCJK-{w}.ttc", s, index=1)
BG, YEL, GRN, INK, SUB, CARD = "#fffdf5", "#ffd43b", "#12b886", "#1a1a1a", "#666666", "#f1f3f5"
OUT = "/home/claude/posts/out"; os.makedirs(OUT, exist_ok=True)
logo = Image.open("tools/logo.png").resize((84, 84), Image.LANCZOS)
mask = Image.new("L", (84, 84), 0); ImageDraw.Draw(mask).ellipse((0, 0, 84, 84), fill=255)

def center(d, y, text, font, fill, spacing=16):
    for line in text.split("\n"):
        w = d.textlength(line, font=font); d.text(((W-w)/2, y), line, font=font, fill=fill); y += font.size + spacing
    return y

def left(d, x, y, text, font, fill, spacing=14):
    for line in text.split("\n"):
        d.text((x, y), line, font=font, fill=fill); y += font.size + spacing
    return y

def base(page, total, src=None):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    im.paste(logo, (70, 64), mask)
    d.text((170, 106), "지원금 레이더", font=F("Black", 38), fill=INK, anchor="lm")
    d.text((W-70, 100), f"{page}/{total}", font=F("Bold", 28), fill=SUB, anchor="rm")
    if src: center(d, H-80, src, F("Regular", 24), SUB)
    return im, d

def cover(title, hl, sub, page, total, src=None, badge=None):
    im, d = base(page, total, src)
    y = 380
    if badge:
        bw = d.textlength(badge, font=F("Bold", 36)) + 60
        d.rounded_rectangle(((W-bw)/2, y-110, (W+bw)/2, y-40), 35, fill=INK)
        d.text((W/2, y-75), badge, font=F("Bold", 36), fill=YEL, anchor="mm")
    y = center(d, y, title, F("Black", 104), INK, 20)
    hf = F("Black", 120); hw = d.textlength(hl, font=hf)
    d.rectangle(((W-hw)/2-20, y+95, (W+hw)/2+20, y+150), fill=YEL)
    center(d, y+10, hl, hf, INK)
    center(d, y+220, sub, F("Bold", 50), GRN)
    d.text((W/2, H-170), "옆으로 넘겨보세요  →", font=F("Medium", 34), fill=SUB, anchor="mm")
    return im

def save(im, name): im.save(f"{OUT}/{name}.jpg", quality=92)

# ---------- 게시물 1: 계정 소개 ----------
T = 4
save(cover("모르면\n못 받는", "나라돈", "지원금 레이더가 대신 찾아드려요", 1, T), "p1_1")

im, d = base(2, T)
center(d, 250, "이런 걸 알려드려요", F("Black", 76), INK)
rows = [("청년", "적금 · 월세 · 취업 지원"), ("직장인", "연말정산 · 근로장려금"), ("신혼 · 육아", "결혼 · 출산 · 양육 지원"), ("생활", "난방비 · 숨은 환급금")]
y = 420
for k, v in rows:
    d.rounded_rectangle((90, y, 990, y+150), 30, fill=CARD)
    d.rounded_rectangle((120, y+40, 380, y+110), 35, fill=YEL)
    d.text((250, y+75), k, font=F("Black", 38), fill=INK, anchor="mm")
    d.text((420, y+75), v, font=F("Bold", 44), fill=INK, anchor="lm")
    y += 180
save(im, "p1_2")

im, d = base(3, T)
center(d, 250, "이렇게 올라와요", F("Black", 76), INK)
rows = [("언제", "월 · 화 · 목 · 금 · 토 낮 12시"), ("릴스", "핵심만 15초"), ("카드뉴스", "저장해두고 보는 정리"), ("매달 말", "다음 달 신청 달력")]
y = 420
for k, v in rows:
    d.rounded_rectangle((90, y, 990, y+150), 30, fill=CARD)
    d.text((140, y+75), k, font=F("Black", 44), fill=GRN, anchor="lm")
    d.text((380, y+75), v, font=F("Bold", 44), fill=INK, anchor="lm")
    y += 180
save(im, "p1_3")

im, d = base(4, T)
center(d, 250, "지원금 레이더의\n약속 3가지", F("Black", 76), INK)
rows = ["정부 공식 발표 · 공고로 확인해요", "예산안인지 확정인지 꼭 표시해요", "내용이 바뀌면 바로 알려드려요"]
y = 540
for i, v in enumerate(rows, 1):
    d.ellipse((110, y, 200, y+90), fill=YEL)
    d.text((155, y+45), str(i), font=F("Black", 48), fill=INK, anchor="mm")
    d.text((240, y+45), v, font=F("Bold", 46), fill=INK, anchor="lm")
    y += 140
d.rounded_rectangle((240, 1010, 840, 1130), 60, fill=GRN)
d.text((540, 1070), "팔로우하고 놓치지 마세요", font=F("Black", 44), fill="#ffffff", anchor="mm")
save(im, "p1_4")

# ---------- 게시물 2: 12월 마감 일정 ----------
T = 5
SRC2 = "출처: 국세청 · 복지로 (2026.11 확인)"
save(cover("놓치면 끝!\n12월에 마감되는", "지원금 3가지", "", 1, T, SRC2, badge="마감 임박"), "p2_1")

items = [
    ("1", "근로장려금 기한 후 신청", "12월 1일(화) 마감", "5월 정기신청을 놓쳤다면 지금이 마지막\n늦게 신청하면 산정액의 95%만 지급\n신청: 홈택스 · 손택스"),
    ("2", "연말정산 미리보기", "12월 18일(금)까지", "1~9월 카드 사용액으로 예상 세액 계산\n남은 기간 공제 전략 세우기\n경로: 홈택스 → 장려금·연말정산·기부금"),
    ("3", "에너지바우처", "12월 31일(목) 신청 마감", "전기 · 가스 · 등유 등 난방비 지원\n대상: 생계·의료·주거·교육급여 수급 가구\n+ 노인·영유아·장애인 등 세대원 기준 충족"),
]
for i, (n, t, dl, desc) in enumerate(items, start=2):
    im, d = base(i, T, SRC2)
    d.ellipse((440, 260, 640, 460), fill=YEL)
    d.text((540, 360), n, font=F("Black", 110), fill=INK, anchor="mm")
    center(d, 510, t, F("Black", 70), INK)
    dlf = F("Black", 64); dw = d.textlength(dl, font=dlf)
    d.rounded_rectangle(((W-dw)/2-40, 630, (W+dw)/2+40, 740), 55, fill=GRN)
    d.text((W/2, 685), dl, font=dlf, fill="#ffffff", anchor="mm")
    d.rounded_rectangle((90, 800, 990, 1180), 30, fill=CARD)
    center(d, 850, desc, F("Medium", 42), INK, 30)
    save(im, f"p2_{i}")

im, d = base(5, T, SRC2)
center(d, 360, "달력에 표시하고\n가족에게도 알려주세요", F("Black", 72), INK, 24)
center(d, 640, "부모님 · 자취하는 동생 · 신혼 친구\n한 명만 챙겨도 수십만 원이에요", F("Medium", 44), SUB, 24)
d.rounded_rectangle((200, 900, 880, 1030), 65, fill=GRN)
d.text((540, 965), "저장 + 공유하기", font=F("Black", 54), fill="#ffffff", anchor="mm")
save(im, "p2_5")

# ---------- 게시물 3: 보조금24 ----------
T = 4
SRC3 = "출처: 행정안전부 · 정부24 (2026.11 확인)"
save(cover("내가 받을 수 있는\n지원금", "1분 만에 찾기", "정부 공식 서비스 '보조금24'", 1, T, SRC3), "p3_1")

im, d = base(2, T, SRC3)
center(d, 250, "이렇게 하세요", F("Black", 76), INK)
steps = [("정부24 접속", "앱 또는 홈페이지"), ("'보조금24' 누르기", "첫 화면에 있어요"), ("간편인증", "카카오 · 네이버 · 토스 · PASS"), ("맞춤 혜택 확인", "받을 수 있는 혜택이 한눈에")]
y = 400
for i, (t, s) in enumerate(steps, 1):
    d.rounded_rectangle((90, y, 990, y+160), 30, fill=CARD)
    d.ellipse((120, y+35, 210, y+125), fill=YEL)
    d.text((165, y+80), str(i), font=F("Black", 46), fill=INK, anchor="mm")
    d.text((250, y+52), t, font=F("Black", 46), fill=INK, anchor="lm")
    d.text((250, y+112), s, font=F("Medium", 34), fill=SUB, anchor="lm")
    y += 190
save(im, "p3_2")

im, d = base(3, T, SRC3)
center(d, 250, "조회할 때 꿀팁", F("Black", 76), INK)
tips = [("중앙정부 + 우리 동네", "지자체 혜택까지 같이 나와요"), ("이사 · 출산 · 결혼 후엔", "꼭 다시 조회하세요"), ("조회만으론 안 들어와요", "대부분 직접 신청해야 받아요")]
y = 440
for t, s in tips:
    d.rounded_rectangle((90, y, 990, y+190), 30, fill=CARD)
    d.text((140, y+65), t, font=F("Black", 48), fill=GRN, anchor="lm")
    d.text((140, y+135), s, font=F("Bold", 44), fill=INK, anchor="lm")
    y += 220
save(im, "p3_3")

im, d = base(4, T, SRC3)
center(d, 380, "찾은 혜택이 있으면\n댓글로 알려주세요", F("Black", 72), INK, 24)
center(d, 640, "어떻게 신청하는지\n지원금 레이더가 정리해드릴게요", F("Medium", 46), SUB, 24)
d.rounded_rectangle((200, 900, 880, 1030), 65, fill=GRN)
d.text((540, 965), "저장 + 팔로우", font=F("Black", 54), fill="#ffffff", anchor="mm")
save(im, "p3_4")

# contact sheet
names = sorted(f for f in os.listdir(OUT) if f.endswith(".jpg"))
th = [Image.open(f"{OUT}/{n}").resize((270, 338)) for n in names]
cols = 5; rows_ = math.ceil(len(th)/cols)
sh = Image.new("RGB", (cols*280, rows_*348), "white")
for i, t in enumerate(th): sh.paste(t, ((i % cols)*280, (i//cols)*348))
sh.save("/home/claude/posts/sheet.jpg", quality=85)
print(names)
