# Setting this up

## 1. The special repo

GitHub profile READMEs only render when they live in a public repo named
exactly the same as your username:

```
FarhanDipto/FarhanDipto
```

Create it if it doesn't exist yet (public, no description or license
needed), then copy this whole bundle into the root of it:

```
README.md
SETUP.md
assets/                       custom images plus the script that makes them
.github/workflows/            the daily workflow for the 3D calendar
.github/profile-3d-contrib.json   the calendar's colors
```

Keep the folder names. `README.md` points at `assets/...` with relative
paths, and the workflow points at `.github/profile-3d-contrib.json`.

## 2. What renders immediately

Everything except the 3D calendar shows up the moment the files are on
GitHub:

- The hero, section headings, profile card and footer are static SVGs in
  `assets/`. They are part of the repo, so they never depend on a third
  party being up.
- The badges, typing line, tech icons, stats cards, streak card and
  activity graph are live images from public services (shields.io,
  readme-typing-svg, skillicons.dev, github-readme-stats, streak-stats,
  github-readme-activity-graph). They update on their own as your
  activity changes.

The hero, headings and footer each come in more than one version, and the
README picks the right one with a `<picture>` tag: dark or light text to
match the GitHub theme, and a stacked, larger-type layout on screens under
600px wide so the page stays readable on phones. Check both themes at
least once: GitHub menu, Settings, Appearance.

## 3. The 3D contribution calendar

This one is generated inside your repo rather than fetched live, so it
needs a one-time kick:

1. Make sure `.github/workflows/profile-3d-contrib.yml` and
   `.github/profile-3d-contrib.json` are in the repo.
2. Open the repo's **Actions** tab. If GitHub asks you to enable workflows,
   enable them.
3. Open **GitHub-Profile-3D-Contrib** in the left sidebar, then
   **Run workflow**, then **Run workflow** again to confirm.
4. When it finishes it commits `profile-3d-contrib/profile-nebula.svg`,
   which is the file the README already points to. The colors come from
   `.github/profile-3d-contrib.json` and match the rest of the page.
5. From then on it re-runs once a day (the cron in the workflow file) and
   keeps the calendar current.

If it fails on the push step with a permissions error, go to
**Settings, Actions, General, Workflow permissions** in the repo and set it
to **Read and write permissions**.

If you would rather have one of the stock designs, delete the
`SETTING_JSON` line from the workflow. The action then writes ten files
such as `profile-night-rainbow.svg` and `profile-green-animate.svg` into
`profile-3d-contrib/`; point the README at whichever you like.

## 4. Changing the text in the custom images

The hero, headings, profile card and footer have their text converted to
outlines, which is why they look identical everywhere instead of falling
back to whatever font the viewer happens to have. The trade-off is that
you can't edit the words in the SVG by hand. Instead:

1. Open `assets/build_svgs.py` and edit the strings in the `CONTENT` block
   at the top (name, role line, tagline, the JSON on the profile card, the
   heading titles, the footer line).
2. Run it once:

   ```
   pip install fonttools uharfbuzz
   python3 assets/build_svgs.py
   ```

   The first run downloads two open-source fonts (Space Grotesk and
   JetBrains Mono) into `~/.cache/profile-svgs/` and reuses them after that.

3. Commit the regenerated SVGs.

Adding a new section is the same idea: add a `(slug, "Title")` pair to
`HEADINGS`, run the script, and reference the four new files with a
`<picture>` block copied from any existing section in `README.md`.

## 5. Palette

Everything is themed around these values. The custom images read them
from the `PALETTE` block in `assets/build_svgs.py`; the badges, cards and
calendar settings carry the same hex codes inline.

| Role | Hex |
|---|---|
| Background (navy) | `#0B0E23` |
| Raised surface (indigo) | `#271F4D` |
| Accent (cyan) | `#4DD0E1` |
| Accent (violet) | `#9B5DE5` |
| Secondary text (lavender) | `#C9B8FF` |
| Primary text | `#E8E8F0` |

To reskin the whole page: change the values in `build_svgs.py`, re-run it,
then find-and-replace the same hex codes in `README.md` and
`.github/profile-3d-contrib.json`.
