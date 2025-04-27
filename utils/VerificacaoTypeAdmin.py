from flask_jwt_extended import get_jwt, get_jwt_identity


def is_admin_user():
    jwt_data = get_jwt()
    username = get_jwt_identity()
    role = jwt_data.get("role", None)

    return role == "admin" or username.endswith("_admin")
