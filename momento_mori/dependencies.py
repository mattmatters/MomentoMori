"""FastAPI dependencies for data loading and calculations."""

import csv
import os
from typing import Dict, List

from fastapi import HTTPException
from fastapi import status as http_status

# Global variable to store loaded data
_life_expectancy_data: List[Dict[str, str]] = []


def load_life_expectancy_data() -> None:
    """Load life expectancy data from CSV at startup."""
    global _life_expectancy_data

    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "life_expectancy.csv")

    try:
        with open(data_path, mode="r", encoding="utf-8") as file:
            _life_expectancy_data = list(csv.DictReader(file))
    except FileNotFoundError:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Life expectancy data file not found",
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading life expectancy data: {str(e)}",
        )


def calculate_life_expectancy(gender: str, age: int) -> float:
    """Calculate remaining life expectancy."""
    # Load data if not already loaded (for testing)
    if not _life_expectancy_data:
        load_life_expectancy_data()

    if age >= len(_life_expectancy_data):
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Age {age} exceeds available data",
        )

    try:
        column = f"{gender} life expectancy"
        return float(_life_expectancy_data[age][column])
    except (KeyError, ValueError) as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating life expectancy: {str(e)}",
        )
