import numpy as np, sys
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100

def note(f, dur, amp=0.15, attack=0.04, release=0.4, kind="pad"):
    t = np.arange(int(dur * SR)) / SR
    if kind == "pad":
        w = (np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*f*2*t+0.3) + 0.25*np.sin(2*np.pi*f*3*t+0.7))
        w *= 1 + 0.003*np.sin(2*np.pi*5*t)
    elif kind == "pluck":
        w = np.sin(2*np.pi*f*t) * np.exp(-t*6) + 0.3*np.sin(2*np.pi*f*2*t)*np.exp(-t*9)
    env = np.minimum(1, t/attack) * np.minimum(1, np.maximum(0, (dur - t)/release))
    return amp * w * env

def hz(m): return 440 * 2 ** ((m - 69) / 12)

def lowpass(x, fc):
    b, a = butter(2, fc / (SR/2)); return lfilter(b, a, x)

def kick(amp=0.5):
    t = np.arange(int(0.35*SR))/SR
    f = 110*np.exp(-t*18)+42
    return amp*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)

def hat(amp=0.05):
    t = np.arange(int(0.06*SR))/SR
    n = np.random.default_rng(1).standard_normal(len(t))
    b, a = butter(2, 7000/(SR/2), "high")
    return amp*lfilter(b, a, n)*np.exp(-t*60)

def whoosh(amp=0.18, dur=0.45):
    t = np.arange(int(dur*SR))/SR
    n = np.random.default_rng(2).standard_normal(len(t))
    out = np.zeros_like(n); step = 512
    for i in range(0, len(n), step):
        fc = 400 + 5000*(i/len(n))
        b, a = butter(2, [fc*0.7/(SR/2), min(fc*1.3, 20000)/(SR/2)], "band")
        out[i:i+step] = lfilter(b, a, n[i:i+step])
    env = np.sin(np.pi*t/dur)**2
    return amp*out*env

def ding(amp=0.16):
    return note(hz(88), 0.9, amp, 0.005, 0.85, "pluck") + note(hz(95), 0.9, amp*0.5, 0.005, 0.85, "pluck")

def add(buf, x, at):
    i = int(at*SR); j = min(len(buf), i+len(x)); buf[i:j] += x[:j-i]

def make(total, bpm, prog, changes, end_ding, out, bright=False):
    buf = np.zeros(int(total*SR)+SR)
    beat = 60/bpm; bar = beat*4
    t = 0; k = 0
    while t < total:
        root = prog[k % len(prog)]
        mn = root % 12 in (2, 9)
        chord = [root, root+(3 if mn else 4), root+7, root+(10 if mn else 11)]
        for m in chord: add(buf, note(hz(m), bar+0.3, 0.035), t)
        add(buf, note(hz(root-12), bar, 0.07, 0.02, 0.3), t)
        for b in range(4):
            add(buf, kick(0.32 if b in (0, 2) else 0.0), t+b*beat)
            add(buf, hat(), t+b*beat+beat/2)
            if bright: add(buf, note(hz(chord[(b+k) % 4]+12), beat, 0.03, 0.005, 0.2, "pluck"), t+b*beat)
        t += bar; k += 1
    buf = lowpass(buf, 5000 if bright else 3200)
    for c in changes: add(buf, whoosh(), max(0, c-0.25))
    add(buf, ding(), end_ding)
    buf = buf[:int(total*SR)]
    fade = int(1.2*SR); buf[-fade:] *= np.linspace(1, 0, fade)
    buf[:int(0.05*SR)] *= np.linspace(0, 1, int(0.05*SR))
    buf = buf / np.max(np.abs(buf)) * 0.85
    wavfile.write(out, SR, (buf*32767).astype(np.int16))

# A: 차분한 로파이 (Dm9 - Bbmaj - F - C), 장면 전환 2.5/5.5/11.5/16.5, 끝 장면 16.5
make(20, 84, [62, 58, 65, 60], [2.5, 5.5, 11.5], 16.6, "bgm_a.wav")
# B: 밝은 팝 (C - G - Am - F), 장면 전환 2.5/6.5/11/15.5/19.5
make(23, 104, [60, 55, 57, 53], [2.5, 6.5, 11.0, 15.5], 19.6, "bgm_b.wav", bright=True)
print("ok")
