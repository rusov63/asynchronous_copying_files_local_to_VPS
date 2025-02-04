import asyncio

from connect import get_server_path_user, connect_to_server
from Local.input_local_path import get_local_path_user


async def main():
    await get_local_path_user() # получаем локальный путь от пользователя. Стартовая функция

    await asyncio.sleep(.5)


    path_folder = await get_server_path_user()  # удаленный путь на сервере
    await connect_to_server(path_folder)  # соединение с сервером



asyncio.run(main())