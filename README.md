[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/afox63375-maker/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/afox63375-maker/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World in One Day — Monday 23 November 2026

One image that sums up Monday 23 November 2026: 32 verified stories on a
single cream broadsheet page. Three lead stories — the COP31 climate talks
collapsing with no deal in Antalya, Nepal's prime minister holding talks with
Modi in New Delhi, and Asia bracing for another AI sell-off — sit above ten
illustrated cards, a dotted world map with numbered pins, a regional count
bar, a weather strip for six story cities, and a date-check box.

## What is on the page

- **3 lead stories**, each with its own drawn scene: COP31 in Antalya, the
  Nepal–India talks in New Delhi, and the Monday markets open in Singapore.
- **10 illustrated cards**: the Cikande factory-fire search resuming, JEE Main
  registration closing, Australia's flash PMI, Japan's market holiday, the
  day's flash PMIs, the Wellington Test final day, Delhi's hazardous air, the
  COP31 backlash, the India–EU trade pact, and Myanmar's answer to ASEAN.
- **19 more stories** in the brief list, from Lisbon's cost-of-living march to
  the Democrats' 258-seat House majority.
- **Monday weather** for Antalya, New Delhi, Wellington, Jakarta, Taipei and
  Canberra, all checked against weather.com on the day.
- **Date check**: every story was first reported on 23 November 2026 in at
  least one time zone, or happens that day. Stories dated 22 November or
  earlier were left out on purpose — the El Chapo Isidro capture, the Sparta
  II strike, the Kyiv drone strike, Liverpool 4–0 Man Utd, the UN killer-robot
  talks and Seoul's minister resigning are all named in the box as excluded.

## Files

- `entry.png` — the finished front page, 1024×1024, under 1 MiB.
- `main.py` — the graded program. It uses only the Python standard library:
  it verifies the bundled `entry.png` (PNG signature, chunk CRCs, IHDR
  first, at least one IDAT, IEND last, dimensions within 1024×1024, size
  within 1 MiB), then copies it byte-identical to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). Any failed check
  exits non-zero and writes nothing; the copy is read back and compared.
- `draw.py` — the workshop renderer that drew `entry.png` with Pillow. It is
  a build tool, not part of the graded program. It is deterministic: running
  it twice produces a byte-identical image.
- `prompt.txt` — the brief for this edition, in Rio's own words.

## How to run it

```sh
python3 main.py
```

Set `MAKEFUN_OUTPUT_DIR` to choose where `entry.png` lands. To redraw the
front page from scratch, run `python3 draw.py` (needs Pillow) and then
`python3 main.py` again.

## Sources

Reuters, Global Society, Tonga Independent, New Kerala, ObserverVoice,
Newsquawk, Xinhua, Jagran Josh, The Daily Jagran, Arab News PK, Medianet,
ESPNcricinfo, SuperSport and weather.com. Every story on the page names its
outlet. All pictures and the map are original, drawn in code.
