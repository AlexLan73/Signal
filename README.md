# Python Project

Описание проекта.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Скопируйте конфигурационный файл:
```bash
cp env.example .env
```

3. Отредактируйте `.env` под свои нужды

## Запуск

```bash
python main.py
```

## Структура проекта

```
├── main.py              # Главный файл
├── requirements.txt     # Зависимости
├── env.example         # Пример конфигурации
├── src/                # Исходный код
│   ├── __init__.py
│   ├── config.py       # Конфигурация
│   └── utils/          # Утилиты
│       ├── __init__.py
│       └── logger.py   # Логирование
├── tests/              # Тесты
│   ├── __init__.py
│   └── test_main.py
├── logs/               # Логи (создается автоматически)
└── data/               # Данные (создается автоматически)
```

## Разработка

### Форматирование кода
```bash
black src/ tests/
isort src/ tests/
```

### Проверка стиля
```bash
flake8 src/ tests/
```

### Типизация
```bash
mypy src/
```

### Тесты
```bash
pytest
```

## Перенос на Ubuntu

Проект готов к переносу. Все зависимости указаны в `requirements.txt` и будут установлены глобально при переносе.
