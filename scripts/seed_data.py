from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.recipe import Recipe

SEED_RECIPES = [
    (
        "Tomato Soup",
        "tomatoes, onion, garlic, vegetable broth, olive oil, basil",
        "Saute onion and garlic in olive oil. Add tomatoes and broth, simmer 20 minutes, then blend until smooth.",
    ),
    (
        "Chicken Noodle Soup",
        "chicken, egg noodles, carrots, celery, onion, garlic, chicken broth",
        "Simmer chicken in broth with vegetables until tender. Shred chicken, return to pot, and cook noodles until done.",
    ),
    (
        "Tomato Basil Pasta",
        "tomatoes, pasta, garlic, basil, olive oil, parmesan",
        "Cook pasta. Saute garlic in olive oil, add tomatoes, toss with pasta, basil, and parmesan.",
    ),
    (
        "Chocolate Chip Cookies",
        "flour, butter, sugar, eggs, vanilla, chocolate chips, baking soda, salt",
        "Cream butter and sugar, mix in eggs and vanilla, fold in dry ingredients and chips, bake at 350F for 10-12 minutes.",
    ),
    (
        "Cornbread",
        "cornmeal, flour, milk, eggs, butter, sugar, baking powder, salt",
        "Mix dry ingredients, whisk wet ingredients, combine, and bake in a buttered pan until golden.",
    ),
    (
        "Minestrone Soup",
        "tomatoes, beans, pasta, carrots, celery, onion, garlic, vegetable broth",
        "Saute onion, celery, carrots, and garlic. Add broth, tomatoes, and beans; simmer. Stir in pasta until tender.",
    ),
    (
        "Brownies",
        "chocolate, flour, butter, eggs, sugar, vanilla, salt",
        "Melt chocolate and butter, whisk in sugar and eggs, fold in flour and salt, bake until set.",
    ),
    (
        "Mac and Cheese",
        "macaroni, cheddar cheese, milk, butter, flour, salt, pepper",
        "Cook macaroni. Make a butter-flour roux, whisk in milk and cheese until smooth, toss with pasta.",
    ),
    (
        "Pancakes",
        "flour, milk, eggs, butter, sugar, baking powder, salt, maple syrup",
        "Whisk dry and wet ingredients separately, combine until just mixed, cook on a griddle until golden, serve with syrup.",
    ),
    (
        "Poha",
        "flattened rice, onion, potato, peanuts, mustard seeds, turmeric, curry leaves, cilantro, lime",
        "Rinse poha and drain. Temper mustard seeds and turmeric, saute onion and potato, add poha and peanuts, finish with cilantro and lime.",
    ),
    (
        "Sambar",
        "toor dal, drumstick, carrot, tomato, onion, tamarind, sambar powder, mustard seeds, curry leaves",
        "Cook dal with vegetables until soft. Add tamarind and sambar powder, simmer, then temper with mustard seeds and curry leaves.",
    ),
    (
        "Chana Masala",
        "chickpeas, onion, tomato, ginger, garlic, cumin, coriander, garam masala, cilantro",
        "Saute onion with ginger and garlic. Add tomatoes and spices, simmer chickpeas until thick, garnish with cilantro.",
    ),
    (
        "Rajma",
        "kidney beans, onion, tomato, ginger, garlic, cumin, red chili powder, garam masala, cilantro",
        "Soak and boil kidney beans until tender. Cook onion-tomato masala with spices, add beans, and simmer until saucy.",
    ),
    (
        "Lemon Rice",
        "rice, lemon juice, peanuts, mustard seeds, turmeric, curry leaves, green chili, cilantro",
        "Cook rice and cool slightly. Temper mustard seeds, turmeric, and curry leaves, toss with rice, peanuts, lemon, and cilantro.",
    ),
    (
        "Dhokla",
        "gram flour, yogurt, ginger, green chili, eno, mustard seeds, curry leaves, cilantro, sugar",
        "Ferment gram flour batter with yogurt and spices, steam until spongy, then temper with mustard seeds and curry leaves.",
    ),
    (
        "Avial",
        "mixed vegetables, coconut, yogurt, green chili, curry leaves, coconut oil, cumin",
        "Cook vegetables until just tender. Mix coconut and yogurt into a mild sauce, simmer briefly, and finish with curry leaves and coconut oil.",
    ),
    (
        "Upma",
        "semolina, onion, ginger, green chili, mustard seeds, urad dal, curry leaves, cilantro, ghee",
        "Dry-roast semolina. Temper mustard seeds and dal, saute onion and chili, add water, stir in semolina until fluffy.",
    ),
    (
        "Masala Dosa",
        "rice, urad dal, potato, onion, mustard seeds, turmeric, curry leaves, oil, salt",
        "Ferment rice-dal batter overnight. Pan-fry thin crepes. Fill with spiced potato masala tempered with mustard seeds and curry leaves.",
    ),
]


def seed_if_empty(db: Session) -> int:
    count = db.scalar(select(func.count()).select_from(Recipe))
    if count and count > 0:
        return 0

    now = datetime.now()
    for name, ingredients, instructions in SEED_RECIPES:
        db.add(
            Recipe(
                name=name,
                ingredients=ingredients,
                instructions=instructions,
                created_at=now,
                updated_at=now,
            )
        )

    db.commit()
    return len(SEED_RECIPES)
