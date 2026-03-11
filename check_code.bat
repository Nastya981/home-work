@echo off
echo Запуск flake8...
poetry run flake8 src/ test_processing.py
echo.
echo Запуск mypy...
poetry run mypy src/ test_processing.py
echo.
echo Запуск black (проверка форматирования)...
poetry run black --check src/ test_processing.py
echo.
echo Запуск isort (проверка импортов)...
poetry run isort --check src/ test_processing.py
echo.
echo Все проверки завершены!