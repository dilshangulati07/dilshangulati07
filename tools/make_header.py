"""Builds assets/header-dark.svg and assets/header-light.svg.

The header is a small rail map: each project is a station on one line,
and the team game hangs off an interchange as a branch line.
Run from the repo root:  python tools/make_header.py
"""
from pathlib import Path

THEMES = {
    "dark": dict(
        bg="#0e1217", panel="#151b22", grid="#1c242d", ink="#eef2f6", muted="#93a1b0",
        a="#2dd4bf", b="#a78bfa", branch="#5b6776", station="#0e1217", tag_bg="#1c242d",
    ),
    "light": dict(
        bg="#f7f4ee", panel="#fffdf8", grid="#ebe5da", ink="#151a20", muted="#5b6573",
        a="#0f9488", b="#7c3aed", branch="#9aa3ae", station="#fffdf8", tag_bg="#efe9de",
    ),
}

FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'Cascadia Code', SFMono-Regular, Consolas, monospace"

# (x, y, name, note, label side)
STATIONS = [
    (742, 118, "RIGSMITH", "3D PC builder", "up"),
    (884, 118, "METRO BUDDY", "rail routes + fares", "up"),
    (1046, 206, "KAFÉ BANGKOK", "café finder", "up"),
    (1124, 206, "JARVIS", "voice assistant", "down"),
]
LINE = "M 712 118 H 922 L 1010 206 H 1156"
BRANCH = "M 884 118 V 300"


def station(x, y, name, note, side, c):
    ty = y - 40 if side == "up" else y + 34
    return f"""
  <circle cx="{x}" cy="{y}" r="9" fill="{c['station']}" stroke="{c['ink']}" stroke-width="3.5"/>
  <text x="{x}" y="{ty}" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" letter-spacing="1.2" fill="{c['ink']}">{name}</text>
  <text x="{x}" y="{ty + 17}" text-anchor="middle" font-family="{FONT}" font-size="12.5" fill="{c['muted']}">{note}</text>"""


def build(c):
    grid = "".join(
        f'<line x1="{x}" y1="24" x2="{x}" y2="336" stroke="{c["grid"]}" stroke-width="1"/>'
        for x in range(700, 1200, 40)
    )
    stations = "".join(station(*s, c) for s in STATIONS)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 360" width="1200" height="360" role="img" aria-label="Dilshan Gulati. I build web apps, 3D tools and a voice assistant that runs on my own PC. Final-year IT student in Bangkok.">
  <defs>
    <linearGradient id="route" gradientUnits="userSpaceOnUse" x1="712" y1="0" x2="1170" y2="0">
      <stop offset="0" stop-color="{c['a']}"/>
      <stop offset="1" stop-color="{c['b']}"/>
    </linearGradient>
    <clipPath id="map"><rect x="680" y="24" width="496" height="312" rx="14"/></clipPath>
  </defs>
  <rect width="1200" height="360" rx="18" fill="{c['bg']}"/>

  <!-- left: who I am -->
  <text x="56" y="80" font-family="{MONO}" font-size="14" font-weight="700" letter-spacing="2.4" fill="{c['a']}">DILSHAN GULATI</text>
  <text font-family="{FONT}" font-size="38" font-weight="700" fill="{c['ink']}" letter-spacing="-0.6">
    <tspan x="56" y="138">I build web apps, 3D tools</tspan>
    <tspan x="56" y="184">and a voice assistant that</tspan>
    <tspan x="56" y="230">runs on my own PC.</tspan>
  </text>
  <rect x="56" y="262" width="296" height="32" rx="16" fill="{c['tag_bg']}"/>
  <circle cx="76" cy="278" r="5" fill="{c['a']}"/>
  <text x="90" y="283" font-family="{FONT}" font-size="14.5" fill="{c['muted']}">Final-year IT student · Bangkok</text>

  <!-- right: projects as a rail line -->
  <rect x="680" y="24" width="496" height="312" rx="14" fill="{c['panel']}"/>
  <g clip-path="url(#map)">{grid}</g>
  <path d="{BRANCH}" fill="none" stroke="{c['branch']}" stroke-width="6" stroke-dasharray="2 12" stroke-linecap="round"/>
  <circle cx="884" cy="300" r="7" fill="{c['station']}" stroke="{c['branch']}" stroke-width="3"/>
  <text x="904" y="297" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="1.1" fill="{c['muted']}">TEAM LINE</text>
  <text x="904" y="313" font-family="{FONT}" font-size="12.5" fill="{c['muted']}">horror game in Godot</text>
  <path id="track" d="{LINE}" fill="none" stroke="url(#route)" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  {stations}
  <circle r="5" fill="{c['ink']}">
    <animateMotion dur="9s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" calcMode="linear">
      <mpath href="#track"/>
    </animateMotion>
  </circle>
</svg>
"""


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    for name, colours in THEMES.items():
        (out / f"header-{name}.svg").write_text(build(colours), encoding="utf-8")
        print("wrote", out / f"header-{name}.svg")
