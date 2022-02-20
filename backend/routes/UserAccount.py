
import json
import bcrypt
import string
import random
import datetime
import requests
from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from backend.models.UserAccount import UserAccount
from backend.models.RevokedToken import RevokedToken


class UserAccountResource(Resource):

    def post(self, type=None):
        # ------- register -------
        if type == "register":
            user_data = request.get_json()
            if not user_data:
                return Response("user data must be sent", status=400)

            email = user_data["email"]
            password = user_data["password"]
            hash = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

            # check if a user with same email exists
            existingUser = UserAccount.objects(email=email)
            if existingUser:

                return Response("user already registered", status=200)

            else:
                new_user = UserAccount(
                    **{"email": email, "hash": hash}).save()

                # create jwt and set as cookie
                access_token = create_access_token(
                    identity={"userId": str(new_user.id)})
                response_with_cookie = Response("ok", status=200)
                response_with_cookie.set_cookie("Bearer", access_token)

                return response_with_cookie

        # ------- login -------
        elif type == "login":
            user_data = request.get_json()
            if not user_data:
                return Response("user data must be sent", status=400)

            email = user_data["email"]
            password = user_data["password"]

            # find user with given email
            user = json.loads(UserAccount.objects.get(email=email).to_json())
            if not user:
                return Response("wrong credentials", status=200)

            # check password hash matches
            isPasswordCorrect = bcrypt.checkpw(
                password.encode("utf-8"), user["hash"].encode("utf-8"))

            if not isPasswordCorrect:
                return Response("wrong credentials", status=200)

            access_token = create_access_token(
                identity={"userId": str(user["id"])})
            response_with_cookie = Response("ok", status=200)
            response_with_cookie.set_cookie("Bearer", access_token)

            return response_with_cookie

        else:
            return Response("bad request", status=400)

    @jwt_required()
    def get(self, type=None):
        userId = get_jwt()["sub"]["userId"]

        # ------- session check -------
        if type == "session":
            # return 200 only if jwt is valid
            user = json.loads(UserAccount.objects.get(id=userId).to_json())
            user = {"id": user["id"], "email": user["email"]}

            return Response(json.dumps({"userData": user}), status=200)

        # ------- logout -------
        if type == "logout":
            # logout user by adding jwt to revoked tokens collection
            jti = get_jwt()["jti"]
            now = datetime.datetime.now(datetime.timezone.utc)

            RevokedToken(
                **{"jti": jti, "created_at": now}).save()
            response_without_cookie = Response("ok", 200)
            response_without_cookie.delete_cookie("Bearer")

            return response_without_cookie

        else:

            return Response("bad request", status=400)
