from typing import Type

from flask import jsonify, request
from flask.views import MethodView

from models import Session, User
from validate_scheme import CreateUser, PatchUser
from security import HttpError, hash_password

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError


def validate(json_data: dict,
             model_class: Type[CreateUser] | Type[PatchUser]):
    try:
        model_item = model_class(**json_data)
        return model_item.model_dump(exclude_none=True)
    except ValidationError as err:
        raise HttpError(400, err.errors())


def get_user(user_id: int, session: Session) -> User:
    user = session.get(User, user_id)
    if user is None:
        raise HttpError(404, message='user not found')
    return user


class UserView(MethodView):

    def get(self, user_id: int):
        """Найти"""
        with Session() as session:
            user = get_user(user_id, session)
            return jsonify({
                "id": user.id,
                "username": user.username,
                "creation_time": user.creation_time.isoformat()
            })

    def post(self):
        """Добавить"""
        json_data = validate(request.json, CreateUser)
        pwd: str = json_data["password"]
        json_data["password"] = hash_password(pwd)

        with Session() as session:
            new_user = User(**json_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError as err:
                raise HttpError(
                    409,
                    f'user already exists with the same username   {err}'
                )
            return jsonify({
                "status": "user add success",
                "id": new_user.id
            })

    def patch(self, user_id: int):
        """Редактировать"""
        json_data = validate(request.json, PatchUser)
        if 'password' in json_data:
            json_data["password"] = hash_password(json_data["password"])

        with Session() as session:
            user = get_user(user_id, session)
            for field, value in json_data.items():
                setattr(user, field, value)
            try:
                session.commit()
            except IntegrityError as err:
                raise HttpError(409, 'username is busy')

            return jsonify({
                "status": "user patch success",
                "id": user.id
            })

    def delete(self, user_id: int):
        """Удалить"""
        with Session() as session:
            user = get_user(user_id, session)
            session.delete(user)
            session.commit()

            return jsonify({
                "status": "user delete success",
                "id": user.id,
                "username": user.username,
                "creation_time": user.creation_time.isoformat()

            })
