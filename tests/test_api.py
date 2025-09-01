"""Tests for the Momento Mori FastAPI application."""

import pytest
from fastapi.testclient import TestClient

from momento_mori.main import app


class TestMomentoMoriAPI:
    """Test suite for Momento Mori API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_homepage(self, client):
        """Test homepage loads correctly."""
        response = client.get("/")
        assert response.status_code == 200
        assert "Momento Mori" in response.text
        assert "Anti-Procrastination App" in response.text

    def test_life_expectancy_api_valid_input(self, client):
        """Test API endpoint with valid input."""
        response = client.get("/api/v1/life-expectancy?age=25&gender=female")
        assert response.status_code == 200

        data = response.json()
        assert "years_remaining" in data
        assert "age" in data
        assert "gender" in data
        assert data["age"] == 25
        assert data["gender"] == "female"
        assert data["years_remaining"] > 0

    def test_life_expectancy_web_valid_input(self, client):
        """Test web endpoint with valid input."""
        response = client.get("/expectancy?age=25&gender=female")
        assert response.status_code == 200
        assert "years left" in response.text

    def test_life_expectancy_api_young_person(self, client):
        """Test API endpoint for young person."""
        response = client.get("/api/v1/life-expectancy?age=20&gender=male")
        assert response.status_code == 200

        data = response.json()
        assert data["years_remaining"] > 50

    def test_life_expectancy_api_old_person(self, client):
        """Test API endpoint for very old person."""
        response = client.get("/api/v1/life-expectancy?age=100&gender=male")
        assert response.status_code == 200

        data = response.json()
        assert data["years_remaining"] < 10

    def test_too_old_handling(self, client):
        """Test handling of extremely old age."""
        response = client.get("/expectancy?age=150&gender=male")
        assert response.status_code == 200
        assert "The Ambassadors" in response.text

    def test_invalid_age_negative(self, client):
        """Test handling of negative age."""
        response = client.get("/api/v1/life-expectancy?age=-5&gender=male")
        assert response.status_code == 422

    def test_invalid_age_too_high(self, client):
        """Test handling of age over limit."""
        response = client.get("/api/v1/life-expectancy?age=200&gender=female")
        assert response.status_code == 422

    def test_invalid_gender(self, client):
        """Test handling of invalid gender."""
        response = client.get("/api/v1/life-expectancy?age=25&gender=other")
        assert response.status_code == 422

    def test_missing_parameters(self, client):
        """Test handling of missing parameters."""
        response = client.get("/api/v1/life-expectancy")
        assert response.status_code == 422

    def test_web_page_includes_death_imagery(self, client):
        """Test that web page includes death imagery based on age."""
        response = client.get("/expectancy?age=25&gender=female")
        assert response.status_code == 200
        # Should contain image tag with death imagery
        assert "death-" in response.text or "time-gentle" in response.text
