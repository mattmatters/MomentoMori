"""Pydantic models for request/response validation."""

from enum import Enum

from pydantic import BaseModel, Field


class Gender(str, Enum):
    """Gender options for life expectancy calculation."""

    MALE = "male"
    FEMALE = "female"


class LifeExpectancyRequest(BaseModel):
    """Request model for life expectancy calculation."""

    age: int = Field(..., ge=0, le=200, description="Age in years")
    gender: Gender = Field(..., description="Gender for calculation")


class LifeExpectancyResponse(BaseModel):
    """Response model for life expectancy API endpoint."""

    years_remaining: float = Field(..., description="Years of life remaining")
    age: int = Field(..., description="Current age")
    gender: Gender = Field(..., description="Gender used in calculation")
