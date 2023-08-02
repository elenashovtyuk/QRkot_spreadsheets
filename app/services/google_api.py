# в этом файле будут функции взаимодействия приложения с Google API
# а затем они будут добавлены в эндпоинты

# сначала добавим импорты
from datetime import datetime
from aiogoogle import Aiogoogle
from app.core.config import settings

# задаем формат времени
FORMAT = "%Y/%m/%d %H:%M:%S"


# 1-ая функция для создания гугл-таблицы с отчетом
# на вход она получает экземпляр класса Aiogoogle
async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    # получаем текущую дату для заголовка документа
    now_date_time = datetime.now().strftime(FORMAT)
    # далее создаем экземпляр класса Resource для работы с ресурсами Google Sheets API
    # для этого используем метод discover модуля wrapper_services
    service = await wrapper_services.discover('sheets', 'v4')
    # формируем тело запроса для создания таблицы-документа
    # в котором сначала задаем свойства для всего документа
    # название и локаль
    # а вторым шагом описываем свойства первого листа
    spreadsheet_body = {
        'properties': {'title': f'Отчет от {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]}

    # после того, как тело сформировано нужно подготовить и
    # отправить запрос к GoogleAPI
    # с помощью create сформируем запрос к Google Sheets API
    # на создание таблицы
    # в параметрах передаем json c телом запроса
    # именно json, а не body - это особенность асинхронной библы
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    # возвращаем айдишник документа
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


# 2-ая функция для предоставления прав доступа нашему аккаунту
# к созданному документу
# эта функция должна принимать строку с ID документа,
# для которого нужно получить права доступа
# а также она должна принимать экземпляр класса Aiogoogle
async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    # формируем тело запроса на выдачу прав аккаунту
    permission_body = {'type': 'user',
                       'role': 'writer',
                       'emailAddress': settings.email}
    # создаем экземпляр класса Resource для работы с ресурсами
    # Google Sheets API
    service = await wrapper_services.discover('driver', 'v3')

    # формируем и выполняем запрос на выдачу прав вашему аккаунту
    # в функцию create передаем айдишник документа, к которому нужно дать права доступа,
    # также передаем тело запроса с почтой нашего аккаунта,
    await wrapper_services.as_service_account(
        service.permissions.create(
            field=spreadsheetid,
            json=permission_body,
            fields='id'
        ))


# 3-я функция - для обновления данных в документе(таблице) -
# для записи полученной из базы данных информации в документ с таблицами
# Для наполнения таблицы нам нужен айдишник документа, который возвращает
# функция spreadsheets_create
# в качестве параметров эта ф-ция должна принимать
# ID документа
# инфо из базы данных для наполнения
# и объект Aiogoogle
async def spreadsheets_update_value(
    spreadsheetid: str,
    projects: list,
    wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    # создаем экземпляр класса Resource для работы с ресурсами
    # Google Sheets API
    service = await wrapper_services.discover('sheets', 'v4')
    # формируем тело таблицы
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    # далее добавляем строки в таблицу
    for res in projects:
        new_row = [(res['name'], str(res['interval']), res['description'])]
        table_values.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        ))
