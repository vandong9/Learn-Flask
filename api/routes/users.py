from flask import Blueprint
from flask import request
from flask import url_for, render_template_string
from flask_jwt_extended import create_access_token
from api.utils.database import db
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.users import User, UserSchema
from api.utils.token import generate_verification_token, confirm_verification_token
from api.utils.email import send_email

import datetime


user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/", methods=["POST"])
def create_user():
    """
    Create user endpoint
    ---
    parameters:
        - in: body
          name: body
          schema:
            id: UserSignup
            required:
                - username
                - password
                - email
            properties:
                username:
                    type: string
                    description: Unique username of the user
                    default: "Johndoe"
                password:
                    type: string
                    description: Password of the user
                    default: "somethingstrong"
            email:
                type: string
                description: email of the user
                default: "someemail@provider.com"
            responses:
                    201:
                        description: User successfully created
                        schema:
                        id: UserSignUpSchema
                        properties:
                            code:
                            type: string
                    422:
                        description: Invalid input arguments
                        schema:
                        id: invalidInput
                        properties:
                            code:
                                type: string
                            message:
                                type: string
    """
    try:
        data = request.get_json()
        if (
            User.find_by_email(data["email"]) is not None
            or User.find_by_username(data["username"]) is not None
        ):
            return response_with(resp.INVALID_FIELD_NAME_SENT_422)
        data["password"] = User.generate_hash(data["password"])
        user_schema = UserSchema()
        user = user_schema.load(data)
        token = generate_verification_token(data["email"])
        verification_email = url_for(
            "user_routes.verify_email", token=token, _external=True
        )
        html = render_template_string(
            "<p>Welcome! Thanks for signing up. Please follow this link to activate your account:</p> <p><a href='{{ verification_email }}'>{{ verification_email }}</a></p> <br> <p>Thanks!</p>",
            verification_email=verification_email,
        )
        subject = "Please Verify your email"
        # send_email(user.email, subject, html)
        result = user_schema.dump(user.create())
        return response_with(resp.SUCCESS_201)

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_FIELD_NAME_SENT_422)


@user_routes.route("/confirm/<token>", methods=["GET"])
def verify_email(token):
    try:
        email = confirm_verification_token(token)
    except Exception as e:
        return response_with(resp.SERVER_ERROR_404)

    user = User.query.filter_by(email=email).first_or_404()
    if user.isVerified:
        return response_with(resp.INVALID_FIELD_NAME_SENT_422)
    else:
        user.isVerified = True
        db.session.add(user)
        db.session.commit()
        return response_with(
            resp.SUCCESS_200,
            value={"message": "E-mail verified, you can proceed to login now."},
        )


@user_routes.route("/login", methods=["POST"])
def authenticate_user():
    """
    User Login
    ---
    parameters:
        - in: body
          name: body
          schema:
            id: UserLogin
            required:
                - password
                - username
            properties:
                username:
                    type: string
                    description: username of the user
                    default: "test1"
                password:
                    type: string
                    description: Password of the user
                    default: "123456"
            responses:
                200:
                    description: User successfully logged In
                    schema:
                    id: UserLoggedIn
                    properties:
                        code:
                        type: string
                        message:
                        type: string
                        value:
                        schema:
                            id: UserToken
                            properties:
                                access_token:
                                    type: string
                                code:
                                    type: string
                                message:
                                    type: string
                401:
                    description: Invalid input arguments
                    schema:
                        id: invalidInput
                        properties:
                            code:
                                type: string
                            message:
                                type: string
    """

    try:
        data = request.get_json()
        if data.get("email"):
            current_user = User.find_by_email(data["email"])
        elif data.get("username"):
            current_user = User.find_by_username(data["username"])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404)
        if current_user and not current_user.isVerified:
            return response_with(resp.BAD_REQUEST_400)
        if User.verify_hash(data["password"], current_user.password):
            access_token = create_access_token(identity=current_user.username)
            return response_with(
                resp.SUCCESS_200,
                value={"message": "Logged in as admin", "access_token": access_token},
            )
        else:
            return response_with(resp.UNAUTHORIZED_401)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)