from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

from app.constants import (
    FORMAT,
    SERVICE_VERSION_FOR_AUTH,
    SERVICE_VERSION_FOR_UPDATE)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {'title': f'Отчет от {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 11}}}]}

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    permission_body = {'type': 'user',
                       'role': 'writer',
                       'emailAddress': settings.email}
    service = await wrapper_services.discover('driver', SERVICE_VERSION_FOR_AUTH)

    await wrapper_services.as_service_account(
        service.permissions.create(
            field=spreadsheetid,
            json=permission_body,
            fields='id'
        ))


async def spreadsheets_update_value(
    spreadsheetid: str,
    projects: list,
    wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', SERVICE_VERSION_FOR_UPDATE)
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for res in projects:
        new_row = [(res['name'], str(res['interval']), res['description'])]
        table_values.append(new_row)
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        ))
