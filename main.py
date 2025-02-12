import asyncio

from Server.input_server_path import get_server_path_user
from Server.connect import connect_to_server
from Local.input_local_path import get_local_path_user


async def main():
    await get_local_path_user()  # Получаем локальный путь от пользователя. Стартовая функция
    await asyncio.sleep(.5)
    remote_path = await get_server_path_user()  # Получаем удаленный путь на сервере

    await connect_to_server(remote_path)  # соединение с сервером, внутри функции создается папка для копирования файлов

    # async with await connect_to_server(remote_path) as ssh:
    #     await create_folder_on_server(ssh, remote_path)



asyncio.run(main())


# /home/rusov/PycharmProjects/
# /hhh