"""Generate desktop/mobile activity charts from GitHub's contribution calendar.

Uses only Python's standard library. Set GH_TOKEN to a GitHub token; the workflow
uses its automatic GITHUB_TOKEN. No credentials or raw API responses are saved.
"""
import argparse
from datetime import date
from html import escape
import json
import os
from pathlib import Path
import urllib.request


def get_weeks(username):
    query = """query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks { contributionDays { date contributionCount } }
          }
        }
      }
    }"""
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"login": username}}).encode(),
        headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"],
                 "User-Agent": "Hussain-188-profile", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        data = json.load(response)
    if data.get("errors") or not data.get("data", {}).get("user"):
        raise RuntimeError("GitHub did not return a contribution calendar")
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    if not weeks or any(not week["contributionDays"] for week in weeks):
        raise ValueError("Contribution calendar is empty")
    return weeks


def chart(username, weeks, mobile=False):
    width, height = (480, 320) if mobile else (960, 300)
    left, right, top, bottom = 46, width - 28, 106, height - 64
    counts = [sum(day["contributionCount"] for day in week["contributionDays"]) for week in weeks]
    maximum = max(2, max(counts))
    maximum += maximum % 2
    points = [(left + i * (right-left)/max(1, len(counts)-1),
               bottom - count/maximum*(bottom-top)) for i, count in enumerate(counts)]
    path = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in points)
    first = weeks[0]["contributionDays"][0]["date"]
    last = weeks[-1]["contributionDays"][-1]["date"]
    description = f"{username}: {sum(counts)} contributions from {first} to {last}, grouped by week."
    body = f'<text x="28" y="36" font-size="20" fill="#f0f5fc" font-weight="600">Contribution activity</text>'
    body += f'<text x="28" y="63" font-size="13">{escape(username)} / weekly totals over the last year</text>'
    for tick in [0, maximum//2, maximum]:
        y = bottom - tick/maximum*(bottom-top)
        body += f'<path d="M{left} {y}H{right}" stroke="#243345"/><text x="{left-10}" y="{y+4}" text-anchor="end" font-size="11">{tick}</text>'
    body += f'<path d="{path} L{right},{bottom} L{left},{bottom}Z" fill="#63b3ff" opacity=".1"/>'
    body += f'<path class="draw" d="{path}" pathLength="1" stroke="#63b3ff" stroke-width="2.5" fill="none" stroke-linejoin="round"/>'
    for week, count, (x, y) in zip(weeks, counts, points):
        body += f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.5" fill="#6ee7c2"><title>Week of {week["contributionDays"][0]["date"]}: {count} contributions</title></circle>'
    for index in sorted({0, len(weeks)//4, len(weeks)//2, 3*len(weeks)//4, len(weeks)-1}):
        day = date.fromisoformat(weeks[index]["contributionDays"][0]["date"])
        label = day.strftime("%b %y")
        anchor = "start" if index == 0 else "end" if index == len(weeks)-1 else "middle"
        body += f'<text x="{points[index][0]:.2f}" y="{bottom+24}" text-anchor="{anchor}" font-size="11">{label}</text>'
    body += f'<text x="28" y="{height-17}" font-size="11">{sum(counts)} contributions / through {last}</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(username)} contribution activity</title><desc id="desc">{escape(description)}</desc>
<style>text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; fill: #a8b7c9; }}
@keyframes draw {{ from {{ stroke-dashoffset: 1; }} to {{ stroke-dashoffset: 0; }} }}
.draw {{ stroke-dasharray: 1; animation: draw 1.2s ease-out backwards; }}
@media (prefers-reduced-motion: reduce) {{ .draw {{ animation: none; }} }}</style>
<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="18" fill="#080c12" stroke="#243345"/>
{body}
</svg>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", default="Hussain-188")
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    args = parser.parse_args()
    weeks = get_weeks(args.username)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for mobile, name in [(False, "activity.svg"), (True, "activity-mobile.svg")]:
        (args.output_dir / name).write_text(chart(args.username, weeks, mobile), encoding="utf-8", newline="\n")
    print(f"Generated contribution graphs for {args.username} from {len(weeks)} weeks of GitHub data.")


if __name__ == "__main__":
    main()
