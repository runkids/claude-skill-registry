# skills/finance/technical-analysis-skill.md
---
name: "Comprehensive Indicator Library"
description: "Exhaustive catalog of mathematical transforms, indicators, and efficient pattern detection."
---

## Efficient Candlestick Pattern Detection
Do not iterate rows. Use Vectorized Boolean Logic (NumPy) for efficiency.
* **Doji**: `abs(Open - Close) <= (High - Low) * 0.1`
* **Hammer**: `(High - Low) > 3 * (Open - Close)` AND `(Close - Low) / (0.001 + High - Low) > 0.6`
* **Engulfing**: `(Open[1] > Close[1])` AND `(Close > Open)` AND `(Close > Open[1])` AND `(Open < Close[1])`

## The Indicator Library (from indicators.txt)
We dynamically select from this catalog based on Feature Selection scores.

### [cite_start]1. Trend & Averaging [cite: 22, 23, 24, 25]
* **Standard**: `SMA`, `EMA` (Exponential), `WMA` (Weighted).
* **Advanced**:
    * `DEMA` (Double EMA), `TEMA` (Triple EMA).
    * `HMA` (Hull MA - reduced lag).
    * `ZLEMA` (Zero-Lag EMA).
    * `KAMA` (Kaufman Adaptive MA - adjusts for volatility).

### [cite_start]2. Momentum & Oscillators [cite: 26, 27]
* `RSI`: Relative Strength Index (plus `RSI_Above_50` flag).
* `MACD`: Line, Signal, and Histogram.
* `Cross_Over`: Binary flag for MACD Histogram zero-cross.

### [cite_start]3. Volatility [cite: 28, 29, 30]
* `ATR`: Average True Range.
* `Bollinger Bands`: Upper, Lower, Width, `Percent_B`, `Above/Below_BB`.
* `Keltner Channels`: Upper/Lower (using EMA +/- 2*ATR).
* `Donchian Channels`: Rolling High/Low.
* `Chaikin Volatility`: Change in High-Low spread.

### [cite_start]4. Volume & Flow [cite: 31, 32, 33, 34]
* `OBV`: On-Balance Volume.
* `VPT`: Volume Price Trend.
* `NVI` / `PVI`: Negative/Positive Volume Index.
* `AD_Line`: Accumulation/Distribution.
* `MFI`: Money Flow Index.
* `CMF`: Chaikin Money Flow.

### [cite_start]5. VWAP & Statistics [cite: 35, 36, 37, 39]
* `VWAP`: Volume Weighted Average Price.
* `TWAP`: Time Weighted Average Price.
* `Rolling Stats`: Mean, Std, `Z-Score`, `Percentile_Rank`, `Autocorr`, `Skew`, `Kurtosis`.

### [cite_start]6. Derivatives & Deltas [cite: 40, 41, 42]
* `Price_Delta` / `Volume_Delta`.
* `Finite_Diffs`: 1st derivative (velocity) and 2nd derivative (acceleration) for Price and Volume.
* `Crossovers`: Zero-crossing events for derivatives.

### [cite_start]7. FFT (Fast Fourier Transform) Smoothing [cite: 47, 48, 50]
* `FFT_Smooth`: Low-pass filtered price series.
* `FFT_Residual`: The noise removed from the smooth series.
* `FFT_Indicators`: Calculation of MACD, RSI, and Bollinger Bands *on the smoothed FFT series* to reduce false signals.