from flask import Blueprint
from flask import request
from flask import url_for, render_template_string
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from api.utils.database import db
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.books import Book, BookSchema
from api.utils.token import generate_verification_token, confirm_verification_token
from api.utils.email import send_email

book_routes = Blueprint("book_routes", __name__)


@book_routes.route("/", methods=["POST"])
@jwt_required
def create_book():
    try:
        data = request.get_json()
        book_schema = BookSchema()
        book = book_schema.load(data)
        result = book_schema.dump(book.create())
        return response_with(resp.SUCCESS_201, value={"book": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_FIELD_NAME_SENT_422)


@book_routes.route("/", methods=["GET"])
@jwt_required
def get_book_list():
    fetched = Book.query.all()
    book_schema = BookSchema(many=True)
    result = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"books": result})


@book_routes.route("/<int:book_id>", methods=["GET"])
@jwt_required
def get_book_detail(book_id):
    fetched = Book.query.get_or_404(book_id)
    book_schema = BookSchema()
    book = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route("/<int:book_id>", methods=["PUT"])
@jwt_required
def update_book_detail(book_id):
    data = request.get_json()
    get_book = Book.query.get_or_404(book_id)
    get_book.title = data["title"]
    get_book.year = data["year"]
    db.session.add(get_book)
    db.session.commit()
    book_schema = BookSchema()
    book = book_schema.dump(get_book)
    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route("/<int:book_id>", methods=["PATCH"])
@jwt_required
def modify_book_detail(book_id):
    data = request.get_json()
    get_book = Book.query.get_or_404(book_id)
    if data.get("title"):
        get_book.title = data["title"]
    if data.get("year"):
        get_book.year = data["year"]
    db.session.add(get_book)
    db.session.commit()
    book_schema = BookSchema()
    book = book_schema.dump(get_book)
    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route("/<int:book_id>", methods=["DELETE"])
@jwt_required
def delete_book(book_id):
    get_book = Book.query.get_or_404(book_id)
    db.session.delete(get_book)
    db.session.commit()
    return response_with(resp.SUCCESS_204)