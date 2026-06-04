from marshmallow import Schema, fields


class FieldErrorSchema(Schema):
    field = fields.String(required=True)
    message = fields.String(required=True)


class ApiErrorResponseSchema(Schema):
    status = fields.Integer(required=True)
    message = fields.String(required=True)
    errors = fields.List(fields.Nested(FieldErrorSchema), required=True)


def build_api_error(status: int, message: str, errors=None) -> dict:
    if errors is None:
        errors = []
    return {"status": status, "message": message, "errors": errors}
