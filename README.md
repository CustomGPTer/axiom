# Axiom

A scientific calculator for Android. Textbook display, exact answers, plain-English errors.
No adverts, no accounts, fully offline.

Author: Jonathan Jackson

- Website and download: https://customgpter.github.io/axiom/
- Latest app file: https://github.com/CustomGPTer/axiom/releases/latest/download/Axiom.apk
- The website's own files are in `docs/`.

## Layout of the project

| Folder | What it is |
|---|---|
| `engine/` | The calculator itself, with no Android code: the expression editor, the reading rules, exact arithmetic, number display and the bridge to the algebra library. Runs and is tested on any computer. |
| `app/` | The Android app: the display that draws maths in textbook form, the keypad, history and settings. |
| `tools/oracle.py` | Builds the known-answer test file with an independent maths library (mpmath). |
| `tools/stats_oracle.py`, `complex_oracle.py`, `matrix_oracle.py`, `base_oracle.py` | Build the other known-answer test files the same way. |

## How answers are kept right

- Whole numbers and fractions are worked exactly, never in floating point, so `0.1 + 0.2` is `0.3`.
- Roots, π, e, trig and logs are kept as exact expressions by the Symja algebra library and only turned
  into a decimal for display.
- Every decimal is worked out twice, the second time to double the precision, and shown only when both
  agree to 30 figures.
- Every exact form (such as `(√6 − √2)/4`) is typed back through the calculator and compared with the
  original before it is shown.
- `engine/src/test/resources/oracle.tsv` holds 4,000 expressions with answers from an independent
  library. The engine must match all of them to 15 figures on every build.

- Algebra: a simplified formula, a derivative, an integral or a factorisation is shown only after it has
  been checked against what was typed by working both out at several test points. Anything that fails
  the check is not shown.
- Equation solvers put every answer back into the original equation exactly before showing it.
- `engine/src/test/resources/stats.tsv` holds 400 data sets worked independently with exact fractions.
  Statistics must match all of them.
- `complex.tsv` (1,000 complex sums), `matrix.tsv` (300 matrices) and `base.tsv` (1,500 whole-number sums in
  four bases) are checked the same way against independent working.
- Graphs use ordinary floating-point arithmetic for speed. That arithmetic is checked against the same 4,000
  known answers and must agree to 9 figures.
- Every unit factor is the exact legal definition, held as a fraction, so conversions are exact.
- The triangle solver is checked with 400 random triangles: three measurements go in and all six must come back.
- A determinant is worked two independent ways and must agree; an inverse is multiplied back by the
  original and must give the identity.

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

## Building

Needs JDK 17 or newer and the Android SDK (platform 36, build-tools 36.0.0).

```
./gradlew :engine:test             # the accuracy tests
./gradlew :app:testDebugUnitTest   # renders the screens to app/build/shots
./gradlew :app:assembleRelease     # the APK, in app/build/outputs/apk/release
```

To sign a release, put `axiom-release.jks` and `keystore.properties` next to this file. Neither is
ever committed. Without them the build still works but the APK is unsigned.

Minimum Android version: 12 (API 31).

## Third-party software

The algebra engine is Symja (`matheclipse-core`), used unmodified under the LGPL-3.0.
The typeface is Inter, under the SIL Open Font License. The full list is in the app under
Settings, Open-source licences, and in `app/src/main/res/raw/licences.txt`.
