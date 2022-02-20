from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from backend.routes.UserAccount import UserAccountResource
from backend.models.RevokedToken import RevokedToken


def add_routes_to_app(app):
    CORS(app, supports_credentials=True)

    class CustomApi(Api):
        def handle_error(self, e):
            for val in app.error_handler_spec.values():
                for handler in val.values():
                    registered_error_handlers = list(
                        filter(lambda x: isinstance(e, x), handler.keys()))
                    if len(registered_error_handlers) > 0:
                        raise e
            return super().handle_error(e)

    api = CustomApi(app, prefix='/api/v1')

    jwt = JWTManager(app)

    # configure revoked jwt loader
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        existing_revoked_token = RevokedToken.objects(jti=jti)
        return len(existing_revoked_token) > 0

    # jwt._set_error_handler_callbacks(api)

    api.add_resource(
        UserAccountResource, "/user", "/user/<type>", endpoint="userAccount"
    )
