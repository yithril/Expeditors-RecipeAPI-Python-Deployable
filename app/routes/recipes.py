from flask import Blueprint, g, jsonify, request
from marshmallow import ValidationError

from app.schemas.errors import build_api_error
from app.schemas.recipe import (
    RecipeCreateSchema,
    RecipePatchSchema,
    RecipeUpdateSchema,
    marshmallow_errors_to_api_errors,
)
from app.services.recipe_service import RecipeService

recipes_bp = Blueprint("recipes", __name__)

create_schema = RecipeCreateSchema()
update_schema = RecipeUpdateSchema()
patch_schema = RecipePatchSchema()


def _service() -> RecipeService:
    return RecipeService(g.db)


def _parse_id(raw_id: str):
    try:
        return int(raw_id), None
    except (TypeError, ValueError):
        return None, (
            jsonify(build_api_error(400, "Invalid value for parameter 'id'", [])),
            400,
        )


def _load_json():
    if not request.data:
        return {}, None

    try:
        payload = request.get_json(force=False, silent=False)
    except Exception:
        return None, (
            jsonify(build_api_error(400, "Malformed JSON request body", [])),
            400,
        )

    if payload is None:
        return None, (
            jsonify(build_api_error(400, "Malformed JSON request body", [])),
            400,
        )

    if not isinstance(payload, dict):
        return None, (
            jsonify(build_api_error(400, "Malformed JSON request body", [])),
            400,
        )

    return payload, None


def _validation_response(err: ValidationError):
    message, errors = marshmallow_errors_to_api_errors(err)
    return jsonify(build_api_error(400, message, errors)), 400


@recipes_bp.get("/api/recipes")
def get_all_recipes():
    """
    List recipes
    ---
    tags:
      - recipes
    parameters:
      - name: name
        in: query
        type: string
        required: false
      - name: ingredients
        in: query
        type: string
        required: false
    responses:
      200:
        description: A list of recipes
    """
    name = request.args.get("name")
    ingredients = request.args.get("ingredients")
    return jsonify(_service().find_all(name, ingredients)), 200


@recipes_bp.get("/api/recipes/<recipe_id>")
def get_recipe(recipe_id: str):
    """
    Get a recipe by id
    ---
    tags:
      - recipes
    parameters:
      - name: recipe_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Recipe found
      404:
        description: Recipe not found
    """
    parsed_id, error = _parse_id(recipe_id)
    if error:
        return error

    recipe = _service().find_by_id(parsed_id)
    if recipe is None:
        return "", 404
    return jsonify(recipe), 200


@recipes_bp.post("/api/recipes")
def create_recipe():
    """
    Create a recipe
    ---
    tags:
      - recipes
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name, ingredients, instructions]
          properties:
            name:
              type: string
            ingredients:
              type: string
            instructions:
              type: string
    responses:
      201:
        description: Recipe created
      400:
        description: Validation error
    """
    payload, error = _load_json()
    if error:
        return error

    try:
        data = create_schema.load(payload)
    except ValidationError as err:
        return _validation_response(err)

    return jsonify(_service().create(data)), 201


@recipes_bp.put("/api/recipes/<recipe_id>")
def update_recipe(recipe_id: str):
    """
    Replace a recipe
    ---
    tags:
      - recipes
    parameters:
      - name: recipe_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name, ingredients, instructions]
          properties:
            name:
              type: string
            ingredients:
              type: string
            instructions:
              type: string
    responses:
      200:
        description: Recipe updated
      404:
        description: Recipe not found
    """
    parsed_id, error = _parse_id(recipe_id)
    if error:
        return error

    payload, error = _load_json()
    if error:
        return error

    try:
        data = update_schema.load(payload)
    except ValidationError as err:
        return _validation_response(err)

    recipe = _service().update(parsed_id, data)
    if recipe is None:
        return "", 404
    return jsonify(recipe), 200


@recipes_bp.patch("/api/recipes/<recipe_id>")
def patch_recipe(recipe_id: str):
    """
    Partially update a recipe
    ---
    tags:
      - recipes
    parameters:
      - name: recipe_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            ingredients:
              type: string
            instructions:
              type: string
    responses:
      200:
        description: Recipe patched
      400:
        description: Validation error
      404:
        description: Recipe not found
    """
    parsed_id, error = _parse_id(recipe_id)
    if error:
        return error

    payload, error = _load_json()
    if error:
        return error

    try:
        data = patch_schema.load(payload, partial=True)
    except ValidationError as err:
        return _validation_response(err)

    recipe = _service().patch(parsed_id, data)
    if recipe is None:
        return "", 404
    return jsonify(recipe), 200


@recipes_bp.delete("/api/recipes/<recipe_id>")
def delete_recipe(recipe_id: str):
    """
    Delete a recipe
    ---
    tags:
      - recipes
    parameters:
      - name: recipe_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Recipe deleted
      404:
        description: Recipe not found
    """
    parsed_id, error = _parse_id(recipe_id)
    if error:
        return error

    if _service().delete(parsed_id):
        return "", 204
    return "", 404
