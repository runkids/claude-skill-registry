```markdown
# skills/frontend/lightweight-charts-skill.md
---
name: "Lightweight Charts Visualization"
description: "Implementation details for TradingView's Lightweight Charts library."
---

## Setup
* **Library**: `lightweight-charts` (npm).
* **Theme**: Dark Mode required.
    * `layout: { backgroundColor: '#131722', textColor: '#d1d4dc' }`
    * `grid: { vertLines: { color: '#363c4e' }, horzLines: { color: '#363c4e' } }`

## Series Management
1.  **Candlestick Series**: Main price action.
    * UpColor: `#4caf50`, DownColor: `#f23645`
2.  **Volume Series**: Histogram overlay.
    * Match colors to the candle (Green/Red).
3.  **Markers**: Use `series.setMarkers()` to plot Buy/Sell signals from the backend.
    * Shape: `arrowUp` (Buy), `arrowDown` (Sell).

## Real-Time Updates
* Use `series.update(lastCandle)` for live ticks.
* **Do not** redraw the whole chart on every tick.
* Handle `ws.onmessage` -> Parse JSON -> Update Chart Series.