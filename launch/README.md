# SignalAnalyzer - Launch Scripts

Скрипты для запуска и настройки SignalAnalyzer на Windows и Ubuntu.

## 📁 Структура папки launch

```
launch/
├── README.md                    # Этот файл
├── ubuntu_setup.sh             # Установка для Ubuntu
├── windows_setup.ps1           # Установка для Windows
├── github_ubuntu_commands.sh   # GitHub команды для Ubuntu
├── github_windows_commands.ps1 # GitHub команды для Windows
├── gui/
│   └── main_app.py             # Основное GUI приложение
└── tests/
    ├── strobe_system_test.py   # Тест системы стробов
    ├── math_engine_test.py     # Тест математического движка
    └── full_integration_test.py # Полный интеграционный тест
```

## 🚀 Быстрый старт

### Ubuntu

1. **Установка зависимостей:**
   ```bash
   chmod +x launch/ubuntu_setup.sh
   ./launch/ubuntu_setup.sh
   ```

2. **Активация проекта:**
   ```bash
   source activate_project.sh
   ```

3. **Запуск приложения:**
   ```bash
   python launch/gui/main_app.py
   ```

### Windows

1. **Установка зависимостей:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\launch\windows_setup.ps1
   ```

2. **Активация проекта:**
   ```powershell
   .\activate_project.ps1
   ```

3. **Запуск приложения:**
   ```powershell
   python launch\gui\main_app.py
   ```

## 🐙 Работа с GitHub

### Ubuntu

```bash
# Настройка Git и GitHub CLI
chmod +x launch/github_ubuntu_commands.sh
./launch/github_ubuntu_commands.sh setup

# Создание репозитория
./launch/github_ubuntu_commands.sh create signalanalyzer

# Клонирование репозитория
./launch/github_ubuntu_commands.sh clone https://github.com/user/signalanalyzer.git

# Синхронизация
./launch/github_ubuntu_commands.sh sync

# Создание релиза
./launch/github_ubuntu_commands.sh release 1.0.0 "Initial release"
```

### Windows

```powershell
# Настройка Git и GitHub CLI
.\launch\github_windows_commands.ps1 setup

# Создание репозитория
.\launch\github_windows_commands.ps1 create signalanalyzer

# Клонирование репозитория
.\launch\github_windows_commands.ps1 clone https://github.com/user/signalanalyzer.git

# Синхронизация
.\launch\github_windows_commands.ps1 sync

# Создание релиза
.\launch\github_windows_commands.ps1 release 1.0.0 "Initial release"
```

## 🧪 Тестирование

### Запуск тестов

**Ubuntu:**
```bash
# Тест системы стробов
python launch/tests/strobe_system_test.py

# Тест математического движка
python launch/tests/math_engine_test.py

# Полный интеграционный тест
python launch/tests/full_integration_test.py
```

**Windows:**
```powershell
# Тест системы стробов
python launch\tests\strobe_system_test.py

# Тест математического движка
python launch\tests\math_engine_test.py

# Полный интеграционный тест
python launch\tests\full_integration_test.py
```

## 📊 Структура данных

После установки создается следующая структура:

```
data/
├── strobes/
│   ├── generated/     # Сгенерированные стробы
│   ├── templates/     # Шаблоны стробов
│   └── archived/      # Архивные стробы
└── signals/
    ├── generated/     # Сгенерированные сигналы
    ├── templates/     # Шаблоны сигналов
    └── archived/      # Архивные сигналы

reports/
└── YYYY/MM/DD/        # Отчеты по датам

logs/                   # Логи приложения
```

## 🔧 Настройка

### Git конфигурация

**Ubuntu/Windows:**
```bash
git config --global user.name "Ваше Имя"
git config --global user.email "ваш@email.com"
```

### GitHub CLI аутентификация

**Ubuntu/Windows:**
```bash
gh auth login
```

Выберите:
- GitHub.com
- HTTPS
- Yes (аутентификация через браузер)

## 🐛 Устранение неполадок

### Ubuntu

1. **Ошибка прав доступа:**
   ```bash
   chmod +x launch/ubuntu_setup.sh
   chmod +x launch/github_ubuntu_commands.sh
   ```

2. **Ошибка Python:**
   ```bash
   sudo apt update
   sudo apt install python3.12 python3.12-venv python3-pip
   ```

3. **Ошибка PyQt6:**
   ```bash
   sudo apt install qt6-base-dev qt6-tools-dev
   pip install PyQt6
   ```

### Windows

1. **Ошибка выполнения скриптов:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Ошибка Python:**
   - Скачайте Python 3.12+ с https://python.org
   - Установите с опцией "Add to PATH"

3. **Ошибка PyQt6:**
   ```powershell
   pip install PyQt6
   ```

## 📝 Логи

Логи сохраняются в папке `logs/`:
- `app.log` - основные логи приложения
- `errors.log` - ошибки
- `debug.log` - отладочная информация

## 🎯 Следующие шаги

1. **Настройте Git и GitHub CLI**
2. **Создайте репозиторий на GitHub**
3. **Загрузите проект в репозиторий**
4. **Настройте автоматические тесты**
5. **Создайте первый релиз**

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи в папке `logs/`
2. Убедитесь, что все зависимости установлены
3. Проверьте версии Python, Git и GitHub CLI
4. Создайте issue в репозитории проекта

---

**SignalAnalyzer** - Desktop Signal Analysis Tool  
Поддерживается на Windows и Ubuntu
