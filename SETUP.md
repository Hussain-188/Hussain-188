# Hussain's GitHub profile

Public profile: [Hussain-188](https://github.com/Hussain-188). Publication repository: [`Hussain-188/Hussain-188`](https://github.com/Hussain-188/Hussain-188), default branch `main`.

The profile README uses Mohamed Hussain M's supplied photo, CV, contact links, skills, experience, and projects. The layout adapts the original [Mohanraj1232 profile](https://github.com/Mohanraj1232/Mohanraj1232).

## Features

- Desktop and mobile banners with an embedded portrait, entrance animation, cycling focus text, blinking cursor, and subtle moving vector texture.
- Developer ID on desktop and mobile: entrance, sway, card wobble, shine, border glow, initials, skill tags, and decorative barcode.
- Nine skill categories with local vector icons, covering the supplied CV's technologies, architecture, tools, and CS coursework.
- Local Email, GitHub, LinkedIn, and LeetCode icon badges.
- Live GitHub statistics, repository language breakdown, contribution streak, LeetCode problem and contest statistics, and profile view counter.
- A daily contribution graph and animated snake generated from this account's GitHub contributions.
- Selected project links, education, internship, certifications, and hackathon achievement.

## Update artwork

1. Replace `github profile.png` with the next portrait.
2. Run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/prepare_portrait.ps1` to create optimized desktop/mobile JPEGs.
3. Edit the text in `scripts/build_assets.py`, then run `python scripts/build_assets.py` to rebuild the twelve local SVGs.
4. Update corresponding text and image descriptions in `README.md` when changing profile details.
5. Commit and push to `Hussain-188/Hussain-188`.

The supplied portrait is embedded in the banners. The JPEGs and original PNG are retained so edits are reproducible. `image.png` is a preview, not a README dependency. Local previews, dependencies, and audit reports are ignored by Git.

## Daily contribution artwork

`.github/workflows/snake.yml` runs daily at 00:00 UTC (05:30 IST), on relevant pushes, and on manual dispatch under **Update contribution artwork**. It is restricted to `Hussain-188/Hussain-188`.

`scripts/build_activity.py` reads GitHub's contribution calendar through the GraphQL API and renders desktop/mobile SVG graphs of weekly totals over the last year. It uses Python's standard library and the workflow's automatic `GITHUB_TOKEN`; no personal access token or paid chart service is needed. The graph reports its actual data period.

[Platane/snk](https://github.com/Platane/snk) generates light and dark contribution snakes. The graph and snakes are published to the `output` branch, and the README loads those generated files directly. The workflow requires `contents: write`, already declared in the file.

For a local graph rebuild, set `GH_TOKEN` in the environment and run `python scripts/build_activity.py --output-dir dist`. Do not put credentials in source files. A failed API request fails the build rather than publishing invented activity.

## Animation and accessibility

Local motion uses CSS transforms, opacity, and the chart's line-drawing animation. There are no scripts, external fonts, blur filters, or raster noise in the generated artwork. Reduced-motion preferences stop all local decorative animations and leave one readable focus phrase. The third-party stats cards and snake are controlled by their respective generators.

The README selects compact layouts below 600 pixels. Each image has an accessible description. Social icons are local assets, so they do not depend on a badge service. Stats, streaks, LeetCode, and the view counter remain external services and may have temporary outages or cache delays; their cards link to the source profiles.

## Content sources

- Name and location: the owner's GitHub account.
- Education, internship, skills, certifications, hackathon result, email, LinkedIn, and LeetCode: the supplied CV.
- Project descriptions: the CV and public project repositories.
- Activity and statistics: the account-specific GitHub and LeetCode services linked in the README.

The CV, telephone number, credentials, and private local audit files are not published.
