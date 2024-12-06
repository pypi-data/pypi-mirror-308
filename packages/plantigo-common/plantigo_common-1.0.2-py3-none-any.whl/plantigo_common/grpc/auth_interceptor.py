import grpc
from fastapi import HTTPException
from plantigo_common.auth.token_service import verify_token


class AuthInterceptor(grpc.ServerInterceptor):

    def __init__(self, jwt_secret_key: str, jwt_algorithm: str):
        self.jwt_secret_key = jwt_secret_key
        self.jwt_algorithm = jwt_algorithm

    def intercept_service(self, continuation, handler_call_details):
        metadata = dict(handler_call_details.invocation_metadata)
        auth_token = metadata.get("authorization")

        if not auth_token or not auth_token.startswith("Bearer "):
            return grpc.unary_unary_rpc_method_handler(
                lambda request, context: context.abort(
                    grpc.StatusCode.UNAUTHENTICATED, "Unauthenticated"
                )
            )

        token = auth_token.split(" ")[1]

        try:
            token_data = verify_token(token, self.jwt_secret_key, self.jwt_algorithm)
        except HTTPException as e:
            return grpc.unary_unary_rpc_method_handler(
                lambda request, context: context.abort(
                    grpc.StatusCode.UNAUTHENTICATED, "Unauthenticated"
                )
            )

        return continuation(handler_call_details)
