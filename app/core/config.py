from pydantic import BaseSettings
from typing import Optional
from pydantic import BaseSettings, EmailStr
# для работы с переменными окружения создаем класс,
# унаследованный от BaseSettings из библиотеки pydantic
# этот класс позволяет считывать из оперюсистемы переменные окружения
# напрямую обращаться к файлу .env


class Settings(BaseSettings):
    # добавим аттрибут app_title - в нем будет храниться название приложения
    # в аннотации укажем, что это строковый тип данных и зададим значение
    # по умолчанию
    app_title: str = 'QRKot'
    app_description: str = 'Сервис для поддержки котиков!'
    database_url: str = 'sqlite+aiosqlite:///./qrkot.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    # Переменные для Google API
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


# создаем глобальную переменную settings с экземпляром класса Settings
# чтобы его можно было импортировать в любую часть приложения, где
# потребуется доступ к настройкам
settings = Settings()
