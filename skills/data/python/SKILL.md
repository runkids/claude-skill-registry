# skills/python/fastapi-skill.md
---
name: "FastAPI & High-Frequency Concurrency"
description: "Building the high-throughput Python engine."
---

## Concurrency Model
* **WebSocket First**: Use `FastAPI.websocket_endpoint` for the frontend feed.
* **Background Tasks**: Use `asyncio.create_task` for data ingestion loops so they don't block the API.

## Thread Safety (Critical)
* **Shared State**: The Orderbook (`top_20`) and T&S (`latest_trades`) are accessed by the Ingestion Thread (Writer) and the WebSocket Thread (Reader).
* **Locking**:
    ```python
    orderbook_lock = asyncio.Lock()
    async with orderbook_lock:
        # update orderbook
    ```
* **Data Classes**: Use `pydantic` for strict schema validation of all incoming/outgoing messages.

## Numba Optimization
For heavy math:
* Decorate CPU-intensive functions with `@njit` or `@jit(nopython=True)`.
* Avoid using Pandas objects inside Numba functions; pass numpy arrays.