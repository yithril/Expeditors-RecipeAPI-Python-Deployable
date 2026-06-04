from marshmallow import Schema, ValidationError, fields, validates, validates_schema


def _validate_not_blank(value: str, message: str):
    if value is None or not str(value).strip():
        raise ValidationError(message)


class RecipeResponseSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    ingredients = fields.String(required=True)
    instructions = fields.String(required=True)
    created_at = fields.DateTime(required=True, format="iso", data_key="createdAt")
    updated_at = fields.DateTime(required=True, format="iso", data_key="updatedAt")


class RecipeCreateSchema(Schema):
    name = fields.String(required=True)
    ingredients = fields.String(required=True)
    instructions = fields.String(required=True)

    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value or not value.strip():
            raise ValidationError("Name is mandatory")
        if len(value) < 3 or len(value) > 50:
            raise ValidationError("Name must be between 3 and 50 characters")

    @validates("ingredients")
    def validate_ingredients(self, value, **kwargs):
        _validate_not_blank(value, "Ingredients are mandatory")

    @validates("instructions")
    def validate_instructions(self, value, **kwargs):
        _validate_not_blank(value, "Instructions are mandatory")


class RecipeUpdateSchema(RecipeCreateSchema):
    pass


class RecipePatchSchema(Schema):
    name = fields.String(required=False, allow_none=True)
    ingredients = fields.String(required=False, allow_none=True)
    instructions = fields.String(required=False, allow_none=True)

    @validates_schema
    def validate_patch(self, data, **kwargs):
        name = data.get("name")
        ingredients = data.get("ingredients")
        instructions = data.get("instructions")

        if name is None and ingredients is None and instructions is None:
            raise ValidationError(
                "At least one field (name, ingredients, instructions) must be provided"
            )

        if ingredients is not None and not str(ingredients).strip():
            raise ValidationError(
                {"ingredients": ["Ingredients cannot be blank"]}
            )

        if instructions is not None and not str(instructions).strip():
            raise ValidationError(
                {"instructions": ["Instructions cannot be blank"]}
            )

        if name is not None:
            if not str(name).strip():
                raise ValidationError({"name": ["Name must be between 3 and 50 characters"]})
            if len(name) < 3 or len(name) > 50:
                raise ValidationError({"name": ["Name must be between 3 and 50 characters"]})


def marshmallow_errors_to_api_errors(err: ValidationError) -> tuple[str, list[dict]]:
    messages = err.messages
    if isinstance(messages, list):
        return messages[0], []

    if isinstance(messages, dict):
        if "_schema" in messages:
            return messages["_schema"][0], []

        field_errors = []
        for field, field_messages in messages.items():
            if field == "_schema":
                continue
            message = field_messages[0] if isinstance(field_messages, list) else str(field_messages)
            field_errors.append({"field": field, "message": message})

        if field_errors:
            return "Validation failed", field_errors

        first_field = next(iter(messages))
        first_message = messages[first_field]
        if isinstance(first_message, list):
            return first_message[0], []
        return str(first_message), []

    return str(messages), []
