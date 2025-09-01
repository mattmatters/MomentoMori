"""Momento Mori FastAPI App."""

import csv
import os
from functools import lru_cache

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="Momento Mori", description="Life expectancy/Anti Procrastination App"
)

base_dir = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/static", StaticFiles(directory=os.path.join(base_dir, "static")), name="static"
)
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))


@lru_cache()
def load_data():
    """Load CSV data once and cache it."""
    data_path = os.path.join(base_dir, "data", "life_expectancy.csv")
    with open(data_path, mode="r") as file:
        return list(csv.DictReader(file))


def calculate_years(gender: str, age: int) -> float:
    """Calculate remaining life expectancy."""
    data = load_data()
    if age >= len(data):
        raise HTTPException(status_code=400, detail="Age out of range")

    column = f"{gender} life expectancy"
    return float(data[age][column])


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Main page."""
    return templates.TemplateResponse(request, "landing.html")


@app.get("/expectancy", response_class=HTMLResponse)
def get_expectancy(
    request: Request,
    age: int = Query(..., ge=0),
    gender: str = Query(..., pattern="^(male|female)$"),
):
    """Get life expectancy."""
    if age > 122:
        return templates.TemplateResponse(request, "too_old.html")

    years = calculate_years(gender, age)
    return templates.TemplateResponse(request, "result.html", {"years": years})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
