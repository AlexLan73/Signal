# SignalAnalyzer - Windows Setup Script
# Инициализация библиотек и зависимостей для Windows

Write-Host "🚀 SignalAnalyzer - Windows Setup" -ForegroundColor Blue
Write-Host "=================================" -ForegroundColor Blue

# Функция для вывода сообщений
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Проверка версии Windows
function Test-WindowsVersion {
    Write-Status "Проверка версии Windows..."
    $os = Get-WmiObject -Class Win32_OperatingSystem
    Write-Success "Windows версия: $($os.Caption) $($os.Version)"
}

# Проверка Python
function Test-Python {
    Write-Status "Проверка Python..."
    
    try {
        $pythonVersion = python --version 2>&1
        Write-Success "Python версия: $pythonVersion"
        return $true
    }
    catch {
        Write-Error "Python не найден. Установите Python 3.12+ с https://python.org"
        return $false
    }
}

# Установка Python пакетов
function Install-PythonPackages {
    Write-Status "Установка Python пакетов..."
    
    # Создание виртуального окружения
    python -m venv venv
    
    # Активация виртуального окружения
    & ".\venv\Scripts\Activate.ps1"
    
    # Обновление pip
    python -m pip install --upgrade pip setuptools wheel
    
    # Установка основных пакетов
    pip install numpy>=1.25.0
    pip install matplotlib>=3.8.0
    pip install scipy>=1.11.0
    pip install sympy>=1.11.0
    
    # Установка GUI пакетов
    pip install PyQt6>=6.5.0
    
    # Установка утилит
    pip install loguru>=0.7.0
    pip install python-dotenv>=1.0.0
    pip install requests>=2.31.0
    
    # Установка инструментов разработки
    pip install pytest>=7.4.0
    pip install pytest-qt>=4.2.0
    pip install black>=23.0.0
    pip install flake8>=6.0.0
    pip install isort>=5.12.0
    pip install mypy>=1.5.0
    
    Write-Success "Python пакеты установлены"
}

# Установка GPU ускорения (опционально)
function Install-GPUAcceleration {
    Write-Status "Проверка GPU ускорения..."
    
    try {
        # Проверка NVIDIA GPU
        $gpu = Get-WmiObject -Class Win32_VideoController | Where-Object { $_.Name -like "*NVIDIA*" }
        if ($gpu) {
            Write-Success "NVIDIA GPU обнаружен: $($gpu.Name)"
            Write-Status "Установка CuPy..."
            pip install cupy-cuda12x>=12.0.0
            Write-Success "GPU ускорение установлено"
        }
        else {
            Write-Warning "NVIDIA GPU не обнаружен, пропускаем установку GPU ускорения"
        }
    }
    catch {
        Write-Warning "Не удалось проверить GPU, пропускаем установку GPU ускорения"
    }
}

# Настройка Git
function Setup-Git {
    Write-Status "Проверка Git..."
    
    try {
        $gitVersion = git --version 2>&1
        Write-Success "Git версия: $gitVersion"
        
        Write-Status "Глобальная конфигурация Git (пользователь должен настроить сам):"
        Write-Host "git config --global user.name 'Ваше Имя'" -ForegroundColor Yellow
        Write-Host "git config --global user.email 'ваш@email.com'" -ForegroundColor Yellow
    }
    catch {
        Write-Warning "Git не найден. Установите Git с https://git-scm.com"
    }
}

# Создание структуры проекта
function New-ProjectStructure {
    Write-Status "Создание структуры проекта..."
    
    # Создание необходимых папок
    $folders = @(
        "data\strobes\generated",
        "data\strobes\templates", 
        "data\strobes\archived",
        "data\signals\generated",
        "data\signals\templates",
        "data\signals\archived",
        "reports\$(Get-Date -Format 'yyyy')\$(Get-Date -Format 'MM')\$(Get-Date -Format 'dd')",
        "logs",
        "tests"
    )
    
    foreach ($folder in $folders) {
        if (!(Test-Path $folder)) {
            New-Item -ItemType Directory -Path $folder -Force | Out-Null
        }
    }
    
    Write-Success "Структура проекта создана"
}

# Создание скрипта активации
function New-ActivationScript {
    Write-Status "Создание скрипта активации..."
    
    $scriptContent = @'
# SignalAnalyzer - Windows Activation Script
# Активация проекта SignalAnalyzer

Write-Host "🚀 Активация SignalAnalyzer..." -ForegroundColor Blue

# Активация виртуального окружения
& ".\venv\Scripts\Activate.ps1"

# Установка PYTHONPATH
$env:PYTHONPATH = "$env:PYTHONPATH;$(Get-Location)"

# Переход в корневую директорию проекта
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "✅ Проект активирован!" -ForegroundColor Green
Write-Host "📁 Рабочая директория: $(Get-Location)" -ForegroundColor Cyan
Write-Host "🐍 Python: $(where.exe python)" -ForegroundColor Cyan
Write-Host "📦 Виртуальное окружение: активировано" -ForegroundColor Cyan
Write-Host ""
Write-Host "Доступные команды:" -ForegroundColor Yellow
Write-Host "  python launch\gui\main_app.py          # Основное GUI приложение" -ForegroundColor White
Write-Host "  python launch\tests\strobe_system_test.py # Тест системы стробов" -ForegroundColor White
Write-Host "  python launch\tests\math_engine_test.py   # Тест математического движка" -ForegroundColor White
Write-Host "  python launch\tests\full_integration_test.py # Полный интеграционный тест" -ForegroundColor White
'@
    
    $scriptContent | Out-File -FilePath "activate_project.ps1" -Encoding UTF8
    Write-Success "Скрипт активации создан"
}

# Основная функция
function Main {
    Write-Host "Начинаем установку SignalAnalyzer для Windows..." -ForegroundColor Green
    Write-Host ""
    
    Test-WindowsVersion
    Write-Host ""
    
    if (!(Test-Python)) {
        Write-Error "Python не найден. Установите Python 3.12+ и повторите установку."
        return
    }
    Write-Host ""
    
    Install-PythonPackages
    Write-Host ""
    
    Install-GPUAcceleration
    Write-Host ""
    
    Setup-Git
    Write-Host ""
    
    New-ProjectStructure
    Write-Host ""
    
    New-ActivationScript
    Write-Host ""
    
    Write-Success "Установка завершена!"
    Write-Host ""
    Write-Host "Следующие шаги:" -ForegroundColor Yellow
    Write-Host "1. Настройте Git: git config --global user.name 'Ваше Имя'" -ForegroundColor White
    Write-Host "2. Настройте Git: git config --global user.email 'ваш@email.com'" -ForegroundColor White
    Write-Host "3. Активируйте проект: .\activate_project.ps1" -ForegroundColor White
    Write-Host "4. Запустите приложение: python launch\gui\main_app.py" -ForegroundColor White
    Write-Host ""
    Write-Host "🎉 SignalAnalyzer готов к работе на Windows!" -ForegroundColor Green
}

# Запуск основной функции
Main
