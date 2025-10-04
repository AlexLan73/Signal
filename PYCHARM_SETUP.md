# Настройка PyCharm Community для глобальных библиотек

## 1. Создание проекта в PyCharm

1. Откройте PyCharm Community
2. Создайте новый проект:
   - File → New Project
   - Выберите "Pure Python"
   - Укажите путь к папке проекта
   - **Важно**: Не создавайте виртуальное окружение (Virtualenv)

## 2. Настройка интерпретатора

1. File → Settings (Ctrl+Alt+S)
2. Project → Python Interpreter
3. Нажмите на шестеренку → Add...
4. Выберите "System Interpreter"
5. Укажите путь к глобальному Python:
   - Windows: `C:\Python311\python.exe` (или ваш путь)
   - Ubuntu: `/usr/bin/python3` или `/usr/bin/python3.11`

## 3. Установка зависимостей

В терминале PyCharm выполните:
```bash
pip install -r requirements.txt
```

## 4. Настройка запуска

1. Run → Edit Configurations...
2. Добавьте новую конфигурацию:
   - Name: "Main"
   - Script path: `main.py`
   - Working directory: `путь_к_проекту`
   - Python interpreter: выберите глобальный интерпретатор

## 5. Настройка форматирования кода

1. File → Settings → Tools → External Tools
2. Добавьте инструменты:
   - **Black**: `black $FilePath$`
   - **isort**: `isort $FilePath$`
   - **flake8**: `flake8 $FilePath$`

## 6. Настройка Git (опционально)

1. File → Settings → Version Control → Git
2. Укажите путь к git.exe
3. Инициализируйте репозиторий: VCS → Enable Version Control Integration

## 7. Проверка настройки

Запустите проект:
```bash
python main.py
```

Если все работает, то библиотеки установлены глобально и проект готов к переносу на Ubuntu.

## Перенос на Ubuntu

1. Скопируйте папку проекта на Ubuntu
2. Установите Python 3.11:
   ```bash
   sudo apt update
   sudo apt install python3.11 python3.11-pip
   ```
3. Установите зависимости:
   ```bash
   pip3.11 install -r requirements.txt
   ```
4. Запустите проект:
   ```bash
   python3.11 main.py
   ```
