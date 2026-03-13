# Проект home-work

## Описание
Проект для обработки данных о банковских операциях. Содержит функции фильтрации и сортировки операций.

## Требования
- Python >= 3.13
- Poetry >= 2.0.0

## Установка и настройка

## Тестирование

Проект покрыт unit-тестами с использованием pytest.

### Структура тестов
tests/
├── conftest.py # Фикстуры для тестов
├── test_integration.py # Интеграционные тесты
├── test_masks.py # Тесты для модуля masks
├── test_processing.py # Тесты для модуля processing
└── test_widget.py # Тесты для модуля widget

### Запуск тестов

```bash
# Установка зависимостей
pip install pytest pytest-cov isort flake8

# Запуск всех тестов
pytest tests/ -v

# Запуск с проверкой покрытия
pytest --cov=src tests/

# Проверка стиля кода
flake8 src/ tests/
isort --check src/ tests/

### Предварительные требования
- **Python**: версия 3.13 или выше
- **Poetry**: версия 2.0.0 или выше (менеджер зависимостей)
- **Git**: для клонирования репозитория

### Пошаговая инструкция по установке


## 3. Создаем отчет о покрытии в формате HTML

```bash
# Создаем папку htmlcov с отчетом
pytest --cov=src --cov-report=html tests/

# Добавляем папку с отчетом в git
git add htmlcov/

# Создаем .gitignore для исключения временных файлов
cat > .gitignore << 'EOF'
# Byte-compiled
__pycache__/
*.py[cod]
*.pyo
*.pyd

# Virtual environment
.venv/
venv/
env/

# IDE
.vscode/
.idea/

# Test cache
.pytest_cache/
.coverage
htmlcov/

# Distribution
dist/
build/
*.egg-info/

#### Шаг 1: Клонирование репозитория
Откройте терминал и выполните:
```bash
git clone https://github.com/Nastya981/home-work.git
cd home-work