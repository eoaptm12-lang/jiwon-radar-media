from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1920
FD = "/usr/share/fonts/opentype/noto/"
def F(w, s):
    return ImageFont.truetype(FD + f"NotoSansCJK-{w}.ttc", s, index=1)  # index 1 = KR

OUT = "/home/claude/reels/frames"
os.makedirs(OUT, exist_ok=True)

def center(d, y, text, font, fill, spacing=18):
    for line in text.split("\n"):
        w = d.textlength(line, font=font)
        d.text(((W - w) / 2, y), line, font=font, fill=fill)
        y += font.size + spacing
    return y

def left(d, x, y, text, font, fill, spacing=14):
    for line in text.split("\n"):
        d.text((x, y), line, font=font, fill=fill)
        y += font.size + spacing
    return y

# ---------------- Reel A: AI 퇴근요정 ----------------
NAVY, NAVY2, MINT, WHITE, GREY = "#0f1b2d", "#1b2b44", "#3ee6b4", "#ffffff", "#9fb0c8"

def baseA():
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    d.text((80, 150), "AI 퇴근요정", font=F("Bold", 40), fill=MINT)
    d.text((80, 205), "@ai.toegeun", font=F("Regular", 32), fill=GREY)
    return im, d

im, d = baseA()
center(d, 640, "회의록,", F("Black", 120), WHITE)
center(d, 800, "아직도 직접\n쓰세요?", F("Black", 120), MINT)
center(d, 1200, "AI한테 30초 만에 맡기는 법", F("Medium", 48), GREY)
im.save(f"{OUT}/a1.png")

im, d = baseA()
center(d, 520, "STEP", F("Bold", 44), MINT)
steps = [("1", "회의 녹음 → 텍스트 변환"), ("2", "AI 채팅창에 붙여넣기"), ("3", "아래 프롬프트 한 줄 추가")]
y = 640
for n, t in steps:
    d.rounded_rectangle((100, y, 980, y + 170), 32, fill=NAVY2)
    d.ellipse((140, y + 45, 220, y + 125), fill=MINT)
    d.text((180, y + 85), n, font=F("Black", 48), fill=NAVY, anchor="mm")
    d.text((260, y + 85), t, font=F("Bold", 50), fill=WHITE, anchor="lm")
    y += 210
im.save(f"{OUT}/a2.png")

im, d = baseA()
d.text((100, 420), "복붙용 프롬프트 ✂", font=F("Bold", 52), fill=MINT)
d.rounded_rectangle((100, 520, 980, 1350), 40, fill="#e8fff7")
left(d, 150, 580,
     "아래 회의 내용을 정리해줘.\n\n1. 결정된 사항\n2. 할 일 (담당자 · 마감일)\n3. 다음 회의 안건\n\n표로 만들고,\n애매한 건 '확인 필요'로\n표시해줘.",
     F("Bold", 50), NAVY, spacing=18)
center(d, 1420, "저장해두면 매번 복붙만 하면 끝", F("Medium", 42), GREY)
im.save(f"{OUT}/a3.png")

im, d = baseA()
d.text((100, 420), "AI가 정리해준 결과", font=F("Bold", 52), fill=MINT)
d.rounded_rectangle((100, 520, 980, 1400), 40, fill=NAVY2)
rows = [("결정", "신제품 출시일 1/15 확정"),
        ("할 일", "김대리 · 보도자료 초안 · 12/5"),
        ("할 일", "이과장 · 예산안 수정 · 12/8"),
        ("안건", "홍보 채널 선정"),
        ("확인 필요", "행사 장소 (미정)")]
y = 580
for k, v in rows:
    d.rounded_rectangle((140, y, 330, y + 100), 20, fill=MINT if k != "확인 필요" else "#ffcf5c")
    d.text((235, y + 50), k, font=F("Bold", 36), fill=NAVY, anchor="mm")
    d.text((360, y + 50), v, font=F("Medium", 40), fill=WHITE, anchor="lm")
    y += 155
center(d, 1460, "※ 예시 회의 내용입니다", F("Regular", 34), GREY)
im.save(f"{OUT}/a4.png")

im, d = baseA()
center(d, 600, "회의록 정리", F("Bold", 64), GREY)
center(d, 720, "10분 → 30초", F("Black", 140), MINT)
center(d, 1010, "저장해두고\n내일 회의 때 써보세요", F("Bold", 64), WHITE)
d.rounded_rectangle((240, 1300, 840, 1420), 60, fill=MINT)
d.text((540, 1360), "팔로우하고 꿀팁 받기", font=F("Bold", 46), fill=NAVY, anchor="mm")
im.save(f"{OUT}/a5.png")

# ---------------- Reel B: 지원금 레이더 ----------------
BG, YEL, GRN, INK, SUB = "#fffdf5", "#ffd43b", "#12b886", "#1a1a1a", "#666666"
SRC = "출처: 정부 '청년예산 언박싱 2027' (2026.8.28) · 예산안 기준"

def baseB():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((80, 150), "지원금 레이더", font=F("Black", 40), fill=GRN)
    d.text((80, 205), "@jiwon.radar", font=F("Regular", 32), fill=SUB)
    center(d, 1560, SRC, F("Regular", 28), SUB)
    return im, d

im, d = baseB()
d.rounded_rectangle((300, 470, 780, 560), 45, fill=INK)
d.text((540, 515), "정부 예산안 기준", font=F("Bold", 40), fill=YEL, anchor="mm")
center(d, 640, "2027년\n청년예산", F("Black", 110), INK)
d.rectangle((170, 1095, 910, 1160), fill=YEL)
center(d, 940, "43.3조", F("Black", 170), INK)
center(d, 1250, "내년부터 달라지는 4가지", F("Bold", 62), GRN)
im.save(f"{OUT}/b1.png")

items = [
    ("1", "혼인지원금", "100만 원", "혼인신고한 부부\n소득 상관없이 생애 1회"),
    ("2", "아이맞이지원금", "1,000~2,000만 원", "2027년 7월 신설 예정\n아동수당·부모급여·첫만남이용권 통합\n출생 순위·지역 따라 4회 나눠 지급"),
    ("3", "구직촉진수당", "60만 → 65만 원", "국민취업지원제도 인상\n취업 경험 없는 청년도 참여 가능\n(청년 첫취업 지원제도 신설)"),
    ("4", "병 내일준비적금", "정부 100% 매칭", "군 복무 청년\n월 최대 55만 원 납입액을\n정부가 똑같이 얹어줌"),
]
for i, (n, title, amt, desc) in enumerate(items, start=2):
    im, d = baseB()
    d.ellipse((440, 380, 640, 580), fill=YEL)
    d.text((540, 480), n, font=F("Black", 110), fill=INK, anchor="mm")
    center(d, 650, title, F("Black", 96), INK)
    af = F("Black", 100 if len(amt) <= 8 else 84)
    center(d, 820, amt, af, GRN)
    nl = desc.count("\n") + 1
    d.rounded_rectangle((110, 1020, 970, 1020 + 100 + nl * 72), 36, fill="#f1f3f5")
    center(d, 1070, desc, F("Medium", 46), INK, spacing=26)
    im.save(f"{OUT}/b{i}.png")

im, d = baseB()
center(d, 560, "⚠", F("Black", 100), INK)
center(d, 700, "아직 국회 심의 전인\n예산안이에요", F("Black", 84), INK)
center(d, 950, "금액·시기는 바뀔 수 있어요.\n확정되면 바로 정리해드릴게요!", F("Medium", 50), SUB)
d.rounded_rectangle((200, 1220, 880, 1350), 65, fill=GRN)
d.text((540, 1285), "저장 + 팔로우", font=F("Black", 56), fill="#ffffff", anchor="mm")
im.save(f"{OUT}/b6.png")
print("ok")
