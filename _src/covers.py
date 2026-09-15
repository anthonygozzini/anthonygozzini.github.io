#!/usr/bin/env python3
"""Render project covers and the social preview image into assets/img with headless Chrome."""
import base64
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
OUT = ROOT / "assets" / "img"
SHOTS = SRC / "covers"


def data_uri(name):
    mime = "image/png" if name.endswith(".png") else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode((SHOTS / name).read_bytes()).decode()


FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&display=swap">'
BASE = """
*{box-sizing:border-box;margin:0}
html,body{width:1600px;height:1000px;overflow:hidden}
body{font-family:"Geist",ui-sans-serif,system-ui,sans-serif;display:grid;place-items:center;-webkit-font-smoothing:antialiased}
.window{border-radius:22px;overflow:hidden;box-shadow:0 40px 90px rgba(0,0,0,.35),0 0 0 1px rgba(255,255,255,.1);background:#15181d}
.bar{height:44px;display:flex;align-items:center;gap:9px;padding:0 18px;background:#1d2127}
.bar i{width:13px;height:13px;border-radius:50%;background:#3b4048;display:block}
.window img{display:block;width:1180px}
.phone{width:600px;height:940px;border-radius:64px;background:#0d1014;padding:14px;box-shadow:0 40px 90px rgba(0,0,0,.35)}
.screen{width:100%;height:100%;border-radius:52px;overflow:hidden;display:flex;flex-direction:column;background:#cddbe6}
.tg-head{background:#fff;padding:34px 26px 16px;display:flex;align-items:center;gap:15px;border-bottom:1px solid #e2e7ec}
.tg-av{width:58px;height:58px;border-radius:50%;display:grid;place-items:center;color:#fff;font-weight:600;font-size:25px}
.tg-name{font-size:25px;font-weight:600;color:#101318}
.tg-sub{font-size:17px;color:#7a8591}
.tg-body{flex:1;padding:22px 18px 26px;display:flex;flex-direction:column;justify-content:flex-end;gap:12px}
.msg{max-width:88%;padding:13px 18px;border-radius:22px 22px 22px 7px;font-size:23px;line-height:1.33;color:#101318;background:#fff;box-shadow:0 1px 1px rgba(0,0,0,.07)}
.msg.out{align-self:flex-end;background:#e2f6cd;border-radius:22px 22px 7px 22px}
.msg b{font-weight:600}
.kb{display:grid;gap:8px;width:88%}
.kb.two{grid-template-columns:1fr 1fr}
.kb span{background:rgba(255,255,255,.8);border-radius:14px;padding:12px;text-align:center;font-size:21px;font-weight:500;color:#1a6ea5}
.row{display:flex;align-items:center;gap:70px}
.chan{width:420px;background:#fff;border-radius:22px;padding:22px 24px;box-shadow:0 30px 70px rgba(0,0,0,.3)}
.chan.small{width:330px;padding:16px 18px;border-radius:18px}
.chan-top{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.chan-av{width:42px;height:42px;border-radius:50%;background:#0B77BB;color:#fff;display:grid;place-items:center;font-weight:600}
.chan-name{font-size:19px;font-weight:600;color:#101318}
.chan-sub{font-size:14px;color:#7a8591}
.post{background:#f1f4f7;border-radius:14px;padding:14px 16px;font-size:16px;line-height:1.4;color:#1e2329}
.post b{display:block;font-size:17px;margin-bottom:4px}
.stack{display:flex;flex-direction:column;gap:22px}
.arrows{display:flex;flex-direction:column;gap:64px;color:#fff;font-size:44px;opacity:.9}
"""


def page(body_css, body, width=1600, height=1000):
    size = f"html,body{{width:{width}px;height:{height}px}}"
    return f"<!doctype html><html><head><meta charset='utf-8'>{FONT}<style>{BASE}{size}{body_css}</style></head><body>{body}</body></html>"


def window(img):
    return f'<div class="window"><div class="bar"><i></i><i></i><i></i></div><img src="{data_uri(img)}" alt=""></div>'


def chat(avatar_bg, letter, name, parts):
    return (f'<div class="phone"><div class="screen"><div class="tg-head"><div class="tg-av" style="background:{avatar_bg}">{letter}</div>'
            f'<div><p class="tg-name">{name}</p><p class="tg-sub">bot</p></div></div><div class="tg-body">{"".join(parts)}</div></div></div>')


COVERS = {
    "cover-guardbot.jpg": page("body{background:linear-gradient(135deg,#0E2A47,#0B5A8F)}", window("guardbot.jpg")),
    "cover-channel-miner.jpg": page("body{background:linear-gradient(135deg,#F4C265,#E39B34)}", window("channel-miner.jpg")),
    "cover-sgamers.jpg": page("body{background:linear-gradient(135deg,#1C3F63,#0E2A47)}", window("sgamers.jpg")),
    "cover-gatekeeper.jpg": page("body{background:linear-gradient(135deg,#0B77BB,#084F7D)}", chat("#0B77BB", "G", "Gatekeeper", [
        '<div class="msg">Welcome! Answer a few questions to request access to the group.</div>',
        '<div class="kb"><span>Request access</span></div>',
        '<div class="msg">Send the link to your main social profile (X, Instagram, TikTok, YouTube, GitHub or LinkedIn).</div>',
        '<div class="msg out">x.com/your_profile</div>',
        '<div class="msg">Have you read the group rules, and do you agree to follow them? (yes/no)</div>',
        '<div class="msg out">yes</div>',
        "<div class=\"msg\">You're in. Here is your one-time invite link: <b>t.me/+invite</b></div>",
    ])),
    "cover-referral.jpg": page("body{background:linear-gradient(135deg,#6CC6F5,#2E93D1)}", chat("#F2B84B", "R", "Referral bot", [
        '<div class="msg out">/start</div>',
        '<div class="msg">Join the channel and the group, then send your wallet address to get your referral link.</div>',
        '<div class="kb two"><span>Join channel</span><span>Join group</span></div>',
        '<div class="msg out">0x9f3c…a41c</div>',
        '<div class="msg">Your referral link: <b>t.me/yourbot?start=ref</b><br>Every friend who joins earns you points.</div>',
        '<div class="msg"><b>Top referrers</b><br>1. member one · 128 pts<br>2. member two · 96 pts<br>3. member three · 71 pts</div>',
    ])),
    "cover-copier.jpg": page("body{background:linear-gradient(135deg,#153F66,#0B243D)}", """
<div class="row">
  <div class="chan"><div class="chan-top"><div class="chan-av">S</div><div><p class="chan-name">Source channel</p><p class="chan-sub">new post</p></div></div>
  <div class="post"><b>Weekly update</b>New features are live. Read the full post and share it with your community.</div></div>
  <div class="arrows"><span>→</span><span>→</span><span>→</span></div>
  <div class="stack">
    <div class="chan small"><div class="chan-top"><div class="chan-av" style="background:#F2B84B">1</div><p class="chan-name">Channel one</p></div><div class="post"><b>Weekly update</b>New features are live…</div></div>
    <div class="chan small"><div class="chan-top"><div class="chan-av" style="background:#5CBCF2">2</div><p class="chan-name">Channel two</p></div><div class="post"><b>Weekly update</b>New features are live…</div></div>
    <div class="chan small"><div class="chan-top"><div class="chan-av" style="background:#E86F5B">3</div><p class="chan-name">Channel three</p></div><div class="post"><b>Weekly update</b>New features are live…</div></div>
  </div>
</div>"""),
    "cover-lod.jpg": page("""body{background:radial-gradient(circle at 30% 20%,#3A2418,#140E0B 70%);color:#F3E6D0}
.lod{text-align:center}
.lod .big{font-size:300px;font-weight:700;letter-spacing:.02em;line-height:.9;background:linear-gradient(180deg,#F6D9A0,#C98B3C);-webkit-background-clip:text;color:transparent}
.lod .title{font-size:46px;font-weight:600;margin-top:26px;letter-spacing:-.01em}
.lod .sub{font-size:26px;opacity:.7;margin-top:10px}
.lod .chips{display:flex;gap:14px;justify-content:center;margin-top:34px}
.lod .chips span{border:1px solid rgba(243,230,208,.35);border-radius:999px;padding:9px 20px;font-size:22px}""",
        '<div class="lod"><div class="big">IT</div><p class="title">The Legend of Dragoon</p><p class="sub">Severed Chains · PC</p><div class="chips"><span>611 / 950</span><span>mod · in progress</span></div></div>'),
    "og.jpg": page("""body{background:linear-gradient(115deg,#E0E7EF,#ECEFF3 50%,#F2ECEF);place-items:stretch}
.og{display:flex;align-items:center;gap:56px;padding:0 90px}
.og img{width:240px;height:240px;border-radius:50%;object-fit:cover;box-shadow:0 20px 50px rgba(0,0,0,.15)}
.og h1{font-size:76px;font-weight:500;letter-spacing:-.04em;color:#121417;line-height:1}
.og p{font-size:30px;color:#4A515B;margin-top:18px;line-height:1.35}""",
        f'<div class="og"><img src="{data_uri("anthony.jpg")}" alt=""><div><h1>Anthony Gozzini</h1><p>CRM &amp; lifecycle marketing · community operations · tools I build myself</p></div></div>',
        1200, 630),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    made = 0
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name, markup in COVERS.items():
            width, height = (1200, 630) if name == "og.jpg" else (1600, 1000)
            html_file = tmp / (name + ".html")
            html_file.write_text(markup, encoding="utf-8")
            shot = tmp / (name + ".png")
            profile = tmp / ("profile-" + name)
            subprocess.run(["google-chrome", "--headless=new", f"--user-data-dir={profile}", "--hide-scrollbars",
                            f"--window-size={width},{height}", "--virtual-time-budget=6000", f"--screenshot={shot}",
                            html_file.as_uri()], capture_output=True, timeout=90)
            if not shot.exists():
                print("non generata:", name)
                continue
            im = Image.open(shot).convert("RGB")
            if name != "og.jpg":
                im = im.resize((1200, 750), Image.LANCZOS)
            im.save(OUT / name, "JPEG", quality=84, optimize=True)
            made += 1
            print(f"{name}: {im.size[0]}x{im.size[1]}, {(OUT / name).stat().st_size // 1024} KB")
    print(f"immagini generate: {made} su {len(COVERS)}")
    return 0 if made == len(COVERS) else 1


if __name__ == "__main__":
    sys.exit(main())
