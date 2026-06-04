import pytest

from app import create_app, destroy_app_context
from app.config import TestConfig


@pytest.fixture
def app():
    application = create_app(TestConfig)
    yield application
    destroy_app_context()


@pytest.fixture
def client(app):
    return app.test_client()


def test_context_loads(app):
    assert app is not None


def test_get_all_returns_list(client):
    response = client.get("/api/recipes")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_all_with_seed_data(client):
    client.post(
        "/api/recipes",
        json={
            "name": "Test Soup",
            "ingredients": "water, salt",
            "instructions": "Boil water and add salt.",
        },
    )
    response = client.get("/api/recipes?name=Soup")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
    assert all("Soup" in recipe["name"] for recipe in data)


def test_create_recipe_returns_201_with_id(client):
    response = client.post(
        "/api/recipes",
        json={
            "name": "Grilled Cheese",
            "ingredients": "bread, cheddar, butter",
            "instructions": "Butter bread, add cheese, grill until melted.",
        },
    )
    assert response.status_code == 201
    body = response.get_json()
    assert body["id"] is not None
    assert body["name"] == "Grilled Cheese"
    assert "createdAt" in body
    assert "updatedAt" in body


def test_validation_error_400(client):
    response = client.post(
        "/api/recipes",
        json={
            "name": "AB",
            "ingredients": "",
            "instructions": "Do something.",
        },
    )
    assert response.status_code == 400
    body = response.get_json()
    assert body["status"] == 400
    assert body["message"] == "Validation failed"
    assert len(body["errors"]) >= 1


def test_patch_empty_body_400(client):
    create_response = client.post(
        "/api/recipes",
        json={
            "name": "Patch Me",
            "ingredients": "one, two",
            "instructions": "Mix and serve.",
        },
    )
    recipe_id = create_response.get_json()["id"]

    response = client.patch(f"/api/recipes/{recipe_id}", json={})
    assert response.status_code == 400
    body = response.get_json()
    assert body["message"] == (
        "At least one field (name, ingredients, instructions) must be provided"
    )
    assert body["errors"] == []


def test_delete_returns_204(client):
    create_response = client.post(
        "/api/recipes",
        json={
            "name": "Delete Me",
            "ingredients": "nothing",
            "instructions": "Discard immediately.",
        },
    )
    recipe_id = create_response.get_json()["id"]

    response = client.delete(f"/api/recipes/{recipe_id}")
    assert response.status_code == 204
    assert response.data == b""

    get_response = client.get(f"/api/recipes/{recipe_id}")
    assert get_response.status_code == 404


def test_get_recipe_invalid_id_400(client):
    response = client.get("/api/recipes/abc")
    assert response.status_code == 400
    body = response.get_json()
    assert body["message"] == "Invalid value for parameter 'id'"


def test_get_recipe_not_found_404(client):
    response = client.get("/api/recipes/999999")
    assert response.status_code == 404
    assert response.data == b""


def test_malformed_json_400(client):
    response = client.post(
        "/api/recipes",
        data="{not-json",
        content_type="application/json",
    )
    assert response.status_code == 400
    body = response.get_json()
    assert body["message"] == "Malformed JSON request body"
