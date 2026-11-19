# Axiom

A scientific calculator for Android. Textbook display, exact answers, plain-English errors.
No adverts, no accounts, fully offline.

Author: Jonathan Jackson

- Website and download: https://customgpter.github.io/axiom/
- Latest app file: https://github.com/CustomGPTer/axiom/releases/latest/download/Axiom.apk
- The website's own files are in `docs/`. They are written by `python3 site-src/gen.py`.

## Modes

| Mode | What it does |
|---|---|
| Calculate | Sums, and algebra with the letters x, y and z. Memories A to F each keep one answer. |
| More (on any answer) | Prime factors, divisors, other bases, repeating decimals and more for a number; expanding, factorising, derivative, integral and zeros for a formula. |
| Equations | Quadratic, cubic, and two or three simultaneous equations, with the working. |
| Statistics | Mean, median, mode, quartiles and standard deviations of a list of values. |
| Matrix | Determinant, inverse, transpose, square, and A + B, A − B, A × B, for matrices up to 4 × 4 with exact entries. |
| Base-N | Whole-number sums in binary, octal, decimal and hexadecimal, with AND, OR, XOR and NOT. |
| Graph | Up to four formulas in x: pan, pinch to zoom, read a curve, find where curves cross the axis, turn and meet, and a table of values. |
| Tools | Unit converter (exact factors), areas and volumes, triangle solver, constants (2022 CODATA values) and formula sheets. |

On its side or on a tablet the keys sit beside the working area.

Also: eight themes with six accent colours and a stronger-contrast option; a home-screen widget for everyday sums
that uses the same exact arithmetic; and a backup file (Settings, Backup) holding history, memories, functions and
settings, for safe keeping or moving to another phone.

Complex numbers need no mode: any sum in Calculate that contains `i` is worked as a complex number.
Your own functions are saved from the "x · A" sheet and used like `sin` or `log`.

## Reading rules

1. Brackets and functions
2. Powers, `!`, `%`, `×10ˣ` (apply to what stands just before them)
3. Numbers written together, `2π` or `3(4+1)`, are multiplied before `×` and `÷`
4. `nPr`, `nCr`
5. A leading minus sign, so `−3²` is `−9`
6. `×` and `÷`, left to right
7. `+` and `−`, left to right

`100 + 20%` adds 20% of 100. Where a rule could surprise, a note under the answer says how it was read.

## Licence

© 2026 Jonathan Jackson. All rights reserved. The app's source code is not published; this repository holds the website and the app releases.
The software Axiom is built on, including the Symja algebra library under the LGPL-3.0, is credited on the
[licences page](https://customgpter.github.io/axiom/licences.html) and in the app under Settings, Open-source licences.
