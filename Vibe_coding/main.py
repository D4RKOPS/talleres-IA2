"""Compatibility wrapper exposing the FastAPI app as a top-level module.

This allows running ``uvicorn main:app`` even though the actual application
lives under ``src.main``. Tests and developer tooling that expect a ``main``
module can continue to work without modification.
"""

from src.main import app

__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
