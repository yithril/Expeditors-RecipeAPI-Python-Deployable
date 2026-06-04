from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.recipe import Recipe
from app.schemas.recipe import RecipeResponseSchema


class RecipeService:
    def __init__(self, db: Session):
        self.db = db
        self.response_schema = RecipeResponseSchema()

    def find_all(self, name: str | None, ingredients: str | None) -> list[dict]:
        query = select(Recipe)

        if name is not None and ingredients is not None:
            query = query.where(
                Recipe.name.contains(name),
                Recipe.ingredients.contains(ingredients),
            )
        elif name is not None:
            query = query.where(Recipe.name.contains(name))
        elif ingredients is not None:
            query = query.where(Recipe.ingredients.contains(ingredients))

        recipes = self.db.scalars(query.order_by(Recipe.id)).all()
        return [self._to_response(recipe) for recipe in recipes]

    def find_by_id(self, recipe_id: int) -> dict | None:
        recipe = self.db.get(Recipe, recipe_id)
        if recipe is None:
            return None
        return self._to_response(recipe)

    def create(self, data: dict) -> dict:
        recipe = Recipe(
            name=data["name"],
            ingredients=data["ingredients"],
            instructions=data["instructions"],
        )
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        return self._to_response(recipe)

    def update(self, recipe_id: int, data: dict) -> dict | None:
        recipe = self.db.get(Recipe, recipe_id)
        if recipe is None:
            return None

        recipe.name = data["name"]
        recipe.ingredients = data["ingredients"]
        recipe.instructions = data["instructions"]
        recipe.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(recipe)
        return self._to_response(recipe)

    def patch(self, recipe_id: int, data: dict) -> dict | None:
        recipe = self.db.get(Recipe, recipe_id)
        if recipe is None:
            return None

        if "name" in data and data["name"] is not None:
            recipe.name = data["name"]
        if "ingredients" in data and data["ingredients"] is not None:
            recipe.ingredients = data["ingredients"]
        if "instructions" in data and data["instructions"] is not None:
            recipe.instructions = data["instructions"]

        recipe.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(recipe)
        return self._to_response(recipe)

    def delete(self, recipe_id: int) -> bool:
        recipe = self.db.get(Recipe, recipe_id)
        if recipe is None:
            return False
        self.db.delete(recipe)
        self.db.commit()
        return True

    def _to_response(self, recipe: Recipe) -> dict:
        return self.response_schema.dump(recipe)
