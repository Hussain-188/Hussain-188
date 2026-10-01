"""Build self-contained profile SVGs with Python 3 (no dependencies).

Run scripts/prepare_portrait.ps1 after changing github profile.png, then rerun.
"""
import base64
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BG, PANEL, LINE = "#080c12", "#101823", "#243345"
WHITE, MUTED, BLUE = "#f0f5fc", "#a8b7c9", "#63b3ff"


def text(x, y, value, size=16, color=MUTED, weight=400, extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(value)}</text>'


def label(x, y, value):
    return text(x, y, value, 11, BLUE, 600, 'letter-spacing="2"')


def line(x1, y1, x2, y2):
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{LINE}"/>'


def wrap(width, height, title, description, body, defs=""):
    # Include animation CSS only in assets that use it. Keep static cards static.
    motion = ""
    if 'class="enter"' in body:
        motion += """
      @keyframes enter { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
      .enter { animation: enter .6s cubic-bezier(.22,1,.36,1) backwards; }
"""
    if 'class="sway"' in body:
        motion += """
      @keyframes sway { from { transform: rotate(-3.8deg); } to { transform: rotate(3.8deg); } }
      .sway { transform-box: view-box; transform-origin: 152px 0; animation: sway 1.8s cubic-bezier(.45,0,.55,1) infinite alternate; }
      @keyframes settle { 0% { transform: translateY(-430px); } 55% { transform: translateY(0) rotate(5deg); } 75% { transform: rotate(-3deg); } 100% { transform: rotate(0); } }
      .settle { transform-origin: 152px 0; animation: settle 1.6s ease-out backwards; }
      @keyframes wobble { from { transform: rotate(1.1deg); } to { transform: rotate(-1.1deg); } }
      .wobble { transform-origin: 152px 153px; animation: wobble 1.8s ease-in-out infinite alternate; }
      @keyframes shine { 0%, 12% { transform: translateX(-160px); } 60%, 100% { transform: translateX(300px); } }
      .shine { animation: shine 4.5s ease-in-out infinite; }
      @keyframes glow { from { opacity: .15; } to { opacity: .6; } }
      .glow { animation: glow 3s ease-in-out infinite alternate; }
"""
    if 'class="focus-cycle"' in body:
        motion += """
      @keyframes focusCycle {
        0%, 27% { transform: translateY(0); }
        33%, 60% { transform: translateY(-32px); }
        66%, 93% { transform: translateY(-64px); }
        100% { transform: translateY(-96px); }
      }
      .focus-cycle { animation: focusCycle 7.2s cubic-bezier(.4,0,.2,1) infinite; }
      @keyframes blink { 0%, 49% { opacity: .8; } 50%, 100% { opacity: 0; } }
      .cursor { animation: blink 1s steps(1) infinite; }
      @keyframes texture { 0%, 100% { transform: translate(0, 0); } 50% { transform: translate(2px, -2px); } }
      .grain { animation: texture 3s steps(2) infinite; }
"""
    if motion:
        motion += "      @media (prefers-reduced-motion: reduce) { .enter, .settle, .sway, .wobble, .shine, .glow, .focus-cycle, .cursor, .grain { animation: none; } .shine { opacity: 0; } }"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(description)}</desc>
  <defs>
    <style>
      text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; }}
      .mono {{ font-family: 'Cascadia Code', Consolas, monospace; }}
      {motion}
    </style>
    {defs}
  </defs>
  <rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="18" fill="{BG}" stroke="{LINE}"/>
  {body}
</svg>
'''


def pill(x, y, width, value):
    return f'<rect x="{x}" y="{y}" width="{width}" height="28" rx="7" fill="{PANEL}" stroke="{LINE}"/>' + text(x+width/2, y+19, value, 12, BLUE, 500, 'text-anchor="middle"')


def rotating_focus(x, y, size):
    # A repeated first line makes the loop reset visually seamless.
    # One clipped transform avoids crossfading overlapping text.
    phrases = ["Full stack development.", "Applied machine learning.",
               "From React interfaces to Java APIs.", "Full stack development."]
    return f'<rect class="cursor" x="{x}" y="{y-size+2}" width="2" height="{size}" fill="{BLUE}"/><g clip-path="url(#focusClip)"><g class="focus-cycle">' + ''.join(
        text(x+12, y+i*32, phrase, size, BLUE, 500)
        for i, phrase in enumerate(phrases)
    ) + '</g></g>'


def banner(portrait, mobile=False):
    if mobile:
        w, h = 480, 540
        body = label(28, 38, "HUSSAIN-188 / CHENNAI, IN") + line(28, 56, 452, 56)
        body += label(28, 91, "FULL STACK DEVELOPER")
        body += '<g class="enter">' + text(28, 145, "Mohamed", 46, WHITE, 700) + text(28, 198, "Hussain M", 46, WHITE, 700) + '</g>'
        body += text(28, 237, "Web applications. Java backends.", 17) + rotating_focus(28, 263, 17)
        body += pill(28, 287, 80, "React") + pill(116, 287, 112, "Spring Boot") + pill(236, 287, 80, "Python")
        body += label(28, 373, "BUILDING WITH") + text(28, 404, "Purpose.", 28, WHITE, 600) + text(28, 438, "From UI to API.", 17)
        body += text(28, 507, "github.com/Hussain-188", 13, BLUE, 500, 'class="mono"')
        px, py, pw, ph = 310, 342, 140, 168
    else:
        w, h = 960, 420
        body = label(44, 38, "HUSSAIN-188") + text(916, 38, "CHENNAI, IN", 11, MUTED, 600, 'letter-spacing="2" text-anchor="end"') + line(44, 56, 916, 56)
        body += label(44, 101, "FULL STACK DEVELOPER")
        body += '<g class="enter">' + text(42, 171, "Mohamed", 60, WHITE, 700, 'letter-spacing="-2"') + text(42, 239, "Hussain M", 60, WHITE, 700, 'letter-spacing="-2"') + '</g>'
        body += text(44, 282, "Web applications. Java backends.", 19) + rotating_focus(44, 310, 19)
        body += pill(44, 339, 84, "React") + pill(138, 339, 120, "Spring Boot") + pill(268, 339, 88, "Python")
        body += text(916, 394, "github.com/Hussain-188", 12, MUTED, 400, 'text-anchor="end" class="mono"')
        px, py, pw, ph = 608, 82, 308, 292
    focus_x, focus_y, focus_width = (28, 241, 424) if mobile else (44, 288, 520)
    body = f'<rect class="grain" x="8" y="8" width="{w-16}" height="{h-16}" rx="12" fill="url(#texture)" opacity=".12"/>' + body
    defs = f'<clipPath id="portraitClip"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12"/></clipPath><clipPath id="focusClip"><rect x="{focus_x}" y="{focus_y}" width="{focus_width}" height="28"/></clipPath><linearGradient id="portraitFade" x2="0" y2="1"><stop offset=".6" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}" stop-opacity=".9"/></linearGradient>'
    defs += f'<pattern id="texture" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".6" fill="{MUTED}"/></pattern>'
    body += '<g class="enter" style="animation-delay:.2s">'
    body += f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
    body += f'<image x="{px}" y="{py}" width="{pw}" height="{ph}" href="data:image/jpeg;base64,{portrait}" preserveAspectRatio="xMidYMin slice" clip-path="url(#portraitClip)"/>'
    body += f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="url(#portraitFade)"/>'
    body += '</g>'
    return wrap(w, h, "Mohamed Hussain M | Full Stack Developer", "Portrait of Mohamed Hussain M. Hussain-188, Chennai. React, Spring Boot and Python.", body, defs)


def badge():
    body = '<g class="settle"><g class="sway">'
    body += '<path d="M138 0H166L163 107H141Z" fill="url(#strap)"/>'
    body += text(157, 14, "HUSSAIN-188", 9, WHITE, 600, 'writing-mode="tb" letter-spacing="2"')
    body += '<rect x="135" y="105" width="34" height="21" rx="5" fill="#8296ac"/><rect x="145" y="111" width="14" height="5" rx="2" fill="#34465c"/><circle cx="152" cy="137" r="10" stroke="#8296ac" stroke-width="4"/>'
    body += '<g class="wobble">'
    body += f'<rect x="38" y="153" width="228" height="270" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
    body += f'<rect class="glow" x="38" y="153" width="228" height="270" rx="12" stroke="{BLUE}" stroke-width="1.5" opacity=".3"/>'
    body += label(55, 179, "DEVELOPER ID") + text(249, 179, "H-188", 10, BLUE, 600, 'text-anchor="end"')
    body += f'<circle cx="152" cy="232" r="33" fill="{BG}" stroke="{BLUE}" stroke-opacity=".45"/>'
    body += text(152, 243, "MH", 27, WHITE, 700, 'text-anchor="middle"')
    body += text(152, 290, "Mohamed Hussain M", 19, WHITE, 600, 'text-anchor="middle"')
    body += text(152, 315, "FULL STACK DEVELOPER", 10, MUTED, 500, 'text-anchor="middle" letter-spacing="1"')
    body += text(152, 337, "@Hussain-188", 13, BLUE, 400, 'text-anchor="middle" class="mono"')
    body += line(56, 355, 248, 355) + text(152, 377, "JAVA  /  REACT  /  PYTHON", 10, MUTED, 500, 'text-anchor="middle" letter-spacing="1"')
    for i in range(35):
        body += f'<rect x="{66+i*5}" y="391" width="{1+i%3}" height="15" fill="{MUTED}" opacity=".5"/>'
    body += '<g clip-path="url(#cardClip)"><rect class="shine" x="38" y="153" width="75" height="270" fill="url(#shine)"/></g>'
    return body + '</g></g></g>'


BADGE_DEFS = f'<linearGradient id="strap"><stop stop-color="#183552"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="#183552"/></linearGradient>'
BADGE_DEFS += '<linearGradient id="shine"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient><clipPath id="cardClip"><rect x="38" y="153" width="228" height="270" rx="12"/></clipPath>'


def about(mobile=False):
    if mobile:
        body = label(28, 36, "01 / ABOUT ME") + line(28, 54, 452, 54)
        body += text(28, 93, "From interface to implementation.", 21, WHITE, 600)
        rows = ["I'm a Computer Science engineering student", "in Chennai, building web applications with", "React, Java / Spring Boot and Node.js.", "I also work with Python and computer vision."]
        for i, row in enumerate(rows): body += text(28, 132+i*27, row, 17)
        body += line(28, 239, 452, 239) + label(28, 270, "EDUCATION")
        body += text(28, 301, "B.E. Computer Science", 20, WHITE, 600) + text(28, 330, "St. Joseph's Institute of Technology", 16)
        body += label(28, 378, "EXPERIENCE") + text(28, 408, "Front End Developer Intern", 20, WHITE, 600)
        body += text(28, 437, "GEM3S Technologies | Jun - Jul 2025", 16)
        body += line(28, 463, 452, 463) + text(28, 495, "Full stack development + applied ML", 16, BLUE)
        body += '<g transform="translate(103 520) scale(.9)">' + badge() + '</g>'
        body += text(240, 932, "Open to collaborate", 15, BLUE, 500, 'text-anchor="middle"')
        return wrap(480, 960, "About Mohamed Hussain M", "Computer Science engineering student at St. Joseph's Institute of Technology. Front End Developer Intern at GEM3S Technologies, June to July 2025. Animated developer ID.", body, BADGE_DEFS)
    body = badge() + line(306, 32, 306, 414) + label(344, 42, "01 / ABOUT ME")
    body += text(344, 84, "From interface to implementation.", 27, WHITE, 600)
    rows = ["I'm a Computer Science engineering student in Chennai.", "I build web applications with React, Java / Spring Boot", "and Node.js, and work with Python and computer vision."]
    for i, row in enumerate(rows): body += text(344, 126+i*29, row, 17)
    body += line(344, 210, 918, 210) + label(344, 244, "EDUCATION")
    body += text(344, 273, "B.E. Computer Science", 21, WHITE, 600) + text(344, 300, "St. Joseph's Institute of Technology", 16)
    body += label(344, 345, "EXPERIENCE") + text(344, 374, "Front End Developer Intern", 21, WHITE, 600)
    body += text(344, 401, "GEM3S Technologies | Jun - Jul 2025", 16)
    body += text(152, 446, "Open to collaborate", 12, BLUE, 500, 'text-anchor="middle"')
    return wrap(960, 464, "About Mohamed Hussain M", "Computer Science engineering student in Chennai. Full stack development and applied machine learning. Internship at GEM3S Technologies, June to July 2025.", body, BADGE_DEFS)


STACK = [
    ("LANGUAGES", ["Java / JavaScript / TypeScript", "Python / SQL / PL/SQL"]),
    ("FRONTEND", ["React / Next.js / Angular", "HTML / CSS / Tailwind CSS"]),
    ("BACKEND", ["Spring Boot / Spring MVC", "Spring Security", "Node.js / Express.js"]),
    ("DATA", ["MongoDB / MySQL / PostgreSQL", "Supabase / Redis"]),
    ("AI & COMPUTER VISION", ["TensorFlow / Keras / PyTorch", "OpenCV / Scikit-learn", "Transfer learning / ML"]),
    ("CLOUD & DEVOPS", ["AWS / Docker / CI/CD", "GitHub Actions / Postman"]),
    ("ARCHITECTURE", ["MVC / OOP / SOLID", "Design patterns", "Microservices"]),
    ("DEVELOPER TOOLS", ["Git / GitHub / VS Code", "IntelliJ / Figma", "Agile / Scrum"]),
    ("CS FUNDAMENTALS", ["Data structures & algorithms", "System design / OS", "Networks / DBMS"]),
]


def category_icon(x, y, index):
    shapes = [
        '<path d="m8 5-6 7 6 7m8-14 6 7-6 7m-3-17-2 20"/>',
        '<rect x="2" y="3" width="20" height="18" rx="3"/><path d="M2 8h20m-13 0v13"/>',
        '<rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><path d="M6 6h1m-1 12h1m5-12h6m-6 12h6"/>',
        '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 4 18 4 18 0V5M3 12c0 4 18 4 18 0"/>',
        '<circle cx="12" cy="12" r="4"/><path d="M12 2v6m0 8v6M2 12h6m8 0h6M5 5l4 4m6 6 4 4M5 19l4-4m6-6 4-4"/>',
        '<path d="M7 18H6a4 4 0 0 1-1-8 7 7 0 0 1 14-1 5 5 0 0 1-1 9h-1m-9-3 4-4 4 4m-4-4v11"/>',
        '<rect x="8" y="2" width="8" height="6" rx="1"/><rect x="1" y="16" width="8" height="6" rx="1"/><rect x="15" y="16" width="8" height="6" rx="1"/><path d="M12 8v4H5v4m7-4h7v4"/>',
        '<path d="m14 3 7 7M3 21l5-1L20 8l-4-4L4 16Z"/>',
        '<path d="m2 7 10-5 10 5-10 5Zm3 2v8c5 4 9 4 14 0V9m3-2v12"/>',
    ]
    return f'<g transform="translate({x} {y}) scale(.8)" stroke="{BLUE}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{shapes[index]}</g>'


def social_badges():
    icons = {
        "email": ('Email', '#EA4335', '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 5 10 8L22 5"/>'),
        "github": ('GitHub', '#a8b7c9', '<path d="M9 21c-5 1-5-3-7-3m14 6v-4a3.5 3.5 0 0 0-1-3c3.3-.4 7-1.6 7-7a5.5 5.5 0 0 0-1.5-3.8A5 5 0 0 0 20.4 2S19.2 1.6 16 3.5a13 13 0 0 0-7 0C5.8 1.6 4.6 2 4.6 2a5 5 0 0 0-.1 4.2A5.5 5.5 0 0 0 3 10c0 5.4 3.7 6.6 7 7a3.5 3.5 0 0 0-1 3v4" transform="translate(1 -1) scale(.9)"/>'),
        "linkedin": ('LinkedIn', '#63b3ff', '<path d="M4 9v12m0-17v.1M10 21V9m0 5c0-6 10-6 10 0v7" stroke-width="3.5"/>'),
        "leetcode": ('LeetCode', '#FFA116', '<path d="m15 2-9 9a5 5 0 0 0 0 7l4 4a5 5 0 0 0 7 0l3-3M6 11l4-4a5 5 0 0 1 7 0l3 3M11 15h11"/>'),
    }
    outputs = {}
    for key, (name, color, shape) in icons.items():
        body = f'<g transform="translate(13 9) scale(.85)" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{shape}</g>'
        body += text(43, 26, name, 14, WHITE, 600)
        outputs[f'assets/{key}.svg'] = wrap(132, 40, name, f"Connect with Mohamed Hussain M on {name}", body)
    return outputs


def tech_stack(mobile=False):
    w, h = (480, 1340) if mobile else (960, 506)
    body = label(28 if mobile else 32, 38, "02 / TECH STACK")
    for i, (name, rows) in enumerate(STACK):
        x, y = (28, 71+i*140) if mobile else (32+(i % 3)*304, 68+(i//3)*142)
        cw = 424 if mobile else 288
        body += f'<rect x="{x}" y="{y}" width="{cw}" height="126" rx="10" fill="{PANEL}" stroke="{LINE}"/>'
        body += category_icon(x+16, y+13, i) + text(x+44, y+27, name, 11, BLUE, 600, 'letter-spacing="1"')
        for j, row in enumerate(rows): body += text(x+16, y+57+j*24, row, 17 if mobile else 15, WHITE if j == 0 else MUTED)
    return wrap(w, h, "Mohamed Hussain M | Tech Stack", "; ".join(name+": "+", ".join(rows) for name, rows in STACK), body)


def main():
    portrait = base64.b64encode((ROOT / "portrait-desktop.jpg").read_bytes()).decode("ascii")
    mobile_portrait = base64.b64encode((ROOT / "portrait-mobile.jpg").read_bytes()).decode("ascii")
    outputs = {
        "banner.svg": banner(portrait), "banner-mobile.svg": banner(mobile_portrait, True),
        "about.svg": about(), "about-mobile.svg": about(True),
        "tech-stack.svg": tech_stack(), "tech-stack-mobile.svg": tech_stack(True),
        "lanyard.svg": wrap(304, 444, "Mohamed Hussain M | Developer ID", "Hussain-188. Full Stack Developer. Java, React and Python.", badge(), BADGE_DEFS),
    }
    outputs["ref-lanyard.svg"] = outputs["lanyard.svg"]
    outputs.update(social_badges())
    for name, content in outputs.items():
        content = "\n".join(row.rstrip() for row in content.splitlines()) + "\n"
        (ROOT / name).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / name).write_text(content, encoding="utf-8", newline="\n")
    print(f"Built {len(outputs)} SVGs for Hussain-188.")


if __name__ == "__main__":
    main()
