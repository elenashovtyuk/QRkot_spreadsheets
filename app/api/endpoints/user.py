# app/api/endpoints/user.py
from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.constants import ERROR_USER_DELETE
router = APIRouter()

router.include_router(
    # В роутер аутентификации
    # передается объект бэкенда аутентификации.
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)


# переопределим эндпоинт удаления пользователя
# установми запрет на удаление пользователей
@router.delete(
    '/users/{id}',
    tags=['users'],
    deprecated=True)
def delete_user(id: str):
    raise HTTPException(
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail=ERROR_USER_DELETE)
