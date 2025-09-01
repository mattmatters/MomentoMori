"""Momento Mori FastAPI App - Clean implementation following best practices."""

import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from momento_mori.dependencies import calculate_life_expectancy
from momento_mori.models import Gender, LifeExpectancyResponse
from momento_mori.template_utils import register_template_filters

app = FastAPI(
    title="Momento Mori",
    description="Life expectancy/Anti Procrastination App",
    version="0.2.0",
)

# Static files and templates
base_dir = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(base_dir, "static")),
    name="static",
)
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))
templates = register_template_filters(templates)


# Web endpoints (HTML)
@app.get("/", response_class=HTMLResponse, tags=["Web"])
def homepage(request: Request):
    """Homepage with life expectancy calculator form."""
    return templates.TemplateResponse(request, "landing.html")


@app.get("/expectancy", response_class=HTMLResponse, tags=["Web"])
def life_expectancy_page(
    request: Request,
    age: int = Query(..., ge=0, description="Age in years"),
    gender: Gender = Query(..., description="Gender"),
):
    """Life expectancy result page with death imagery."""
    if age > 122:
        return templates.TemplateResponse(request, "too_old.html")

    years_remaining = calculate_life_expectancy(gender.value, age)

    return templates.TemplateResponse(
        request,
        "result.html",
        {"years": years_remaining},
    )


# API endpoints (JSON)
@app.get(
    "/api/v1/life-expectancy",
    response_model=LifeExpectancyResponse,
    tags=["API"],
    summary="Calculate life expectancy",
    description="Calculate remaining life expectancy based on age and gender",
)
def calculate_life_expectancy_api(
    age: int = Query(..., ge=0, le=122, description="Age in years"),
    gender: Gender = Query(..., description="Gender"),
) -> LifeExpectancyResponse:
    """API endpoint for life expectancy calculation."""
    years_remaining = calculate_life_expectancy(gender.value, age)

    return LifeExpectancyResponse(
        years_remaining=years_remaining,
        age=age,
        gender=gender,
    )


# Health check
@app.get("/health", tags=["System"])
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "version": '0.2.0'}
