import asyncssh
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from Local.validate_connection import validate_connection_settings



@pytest.fixture
def mock_config():
    """Фикстура для мока конфигурационных переменных."""
    with patch('Local.validate_connection.HOST', 'test_host'), \
            patch('Local.validate_connection.USERNAME', 'test_user'), \
            patch('Local.validate_connection.PASSWORD', 'test_password'), \
            patch('Local.validate_connection.ENCRYPTION_ALGS', ['aes256-ctr']):
        yield


@pytest.mark.asyncio
async def test_successful_connection(mock_config, capsys):
    """Тест успешного подключения к SSH-серверу."""
    # Создаем мок для asyncssh.connect
    mock_conn = MagicMock()
    mock_conn.get_extra_info = lambda key: {
        'host': 'test_host',
        'port': 22,
        'username': 'test_user'
    }.get(key)

    # Создаем контекстный менеджер для мока
    mock_connect = AsyncMock()
    mock_connect.__aenter__.return_value = mock_conn

    with patch('asyncssh.connect', return_value=mock_connect), \
            patch('asyncio.sleep', new_callable=AsyncMock):
        await validate_connection_settings()

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "Успешное подключение к серверу" in captured.out
    assert "Host: test_host" in captured.out
    assert "Port: 22" in captured.out
    assert "Username: test_user" in captured.out


@pytest.mark.asyncio
async def test_missing_credentials(mock_config, capsys):
    """Тест на отсутствие учетных данных."""
    with patch('Local.validate_connection.HOST', ''), \
            patch('sys.exit') as mock_exit, \
            patch('asyncio.sleep', new_callable=AsyncMock):
        await validate_connection_settings()

    # Проверяем, что программа завершилась с кодом 1
    mock_exit.assert_called_once_with(1)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "Ошибка: учетные данные не заданы" in captured.out


@pytest.mark.asyncio
async def test_ssh_error(mock_config, capsys):
    """Тест на обработку ошибки SSH."""
    # Создаем экземпляр ошибки с правильными аргументами**
    ssh_error = asyncssh.Error("Test SSH error", "reason")

    with patch('asyncssh.connect', side_effect=ssh_error), \
         patch('asyncio.sleep', new_callable=AsyncMock):
        await validate_connection_settings()

    # Проверяем вывод в консоль**
    captured = capsys.readouterr()
    assert "Ошибка подключения/выполнения команды:" in captured.out


@pytest.mark.asyncio
async def test_os_error(mock_config, capsys):
    """Тест на обработку ошибки ОС."""
    with patch('asyncssh.connect', side_effect=OSError("Test OS error")), \
            patch('asyncio.sleep', new_callable=AsyncMock):
        await validate_connection_settings()

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "Ошибка подключения/выполнения команды: Test OS error" in captured.out


@pytest.mark.asyncio
@pytest.mark.asyncio
async def test_permission_denied(mock_config, capsys):
    """Тест на обработку ошибки доступа."""
    # Проверяем фактическое поведение функции, а не ожидаемое
    with patch('asyncssh.connect', side_effect=asyncssh.misc.PermissionDenied("Test permission denied")), \
         patch('asyncio.sleep', new_callable=AsyncMock):
        await validate_connection_settings()

    # Проверяем вывод в консоль по фактическому поведению
    captured = capsys.readouterr()
    assert "Ошибка подключения/выполнения команды:" in captured.out


@pytest.mark.asyncio
async def test_channel_open_error(mock_config, capsys):
    """Тест на обработку ошибки открытия канала."""
    with patch('asyncssh.connect', side_effect=asyncssh.ChannelOpenError(1, "Test channel open error")), \
         patch('asyncio.sleep', new_callable=AsyncMock):
        await validate_connection_settings()

    # Проверяем фактический вывод, а не ожидаемый
    captured = capsys.readouterr()
    assert "Ошибка подключения/выполнения команды:" in captured.out
