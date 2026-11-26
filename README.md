# THE WORLD TODAY — Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/ayukwulan/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/ayukwulan/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A newspaper front page summing up Wednesday 25 November 2026 in one image:
35 stories across 6 continents, all numbered in reading order with a
REGION · BEAT tag on each one.

The lead story is the Strait of Hormuz: two oil tankers struck naval
mines, exploded and caught fire, according to Iran's Revolutionary Guard.
Around it: Houthi strikes on Saudi Arabia's Ras Tanura refinery and on
Riyadh's tallest tower, the killing of a Hamas security chief in Gaza,
Russian strikes on Odesa and Kyiv, the leaked figure of 490,334 Russian
soldiers dead since 2022, and Pope Leo calling the COP31 failure
"troubling". The page also carries the US tariff proposal for 14 trading
partners, October US inflation at 3.8%, the Nasdaq sliding towards bear
market, Huawei's conviction in a US court, Shenzhou-24 docking at
Tiangong with Pakistan's first astronaut aboard, a record 2,100+ migrants
reaching the Canary Islands in a day, and a world map with 12 numbered
pins plus a BY THE NUMBERS strip.

Every fact on the page was checked against named reporting (Reuters, AP,
AFP, BBC, Al Jazeera, Xinhua, US Bureau of Economic Analysis) for events
that happened, or were first reported, on 25 November 2026.

## How it is built

`draw.py` draws `entry.png` (1024x1024) with Pillow alone — no network,
no photos, no downloaded assets; the tanker illustration, the dotted
world map and every icon are drawn from shapes. Running it twice produces
a byte-identical image. `main.py` (Python standard library only) copies
`entry.png` to `$MAKEFUN_OUTPUT_DIR`.
