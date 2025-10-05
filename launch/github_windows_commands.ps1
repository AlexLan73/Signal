# SignalAnalyzer - GitHub Commands for Windows
# Команды для работы с GitHub из Windows

Write-Host "🐙 SignalAnalyzer - GitHub Commands for Windows" -ForegroundColor Blue
Write-Host "==============================================" -ForegroundColor Blue

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

# Проверка установки Git
function Test-Git {
    try {
        $gitVersion = git --version 2>&1
        Write-Success "Git установлен: $gitVersion"
        return $true
    }
    catch {
        Write-Error "Git не установлен. Установите Git с https://git-scm.com"
        return $false
    }
}

# Проверка установки GitHub CLI
function Test-GitHubCLI {
    try {
        $ghVersion = gh --version 2>&1
        Write-Success "GitHub CLI установлен: $ghVersion"
        return $true
    }
    catch {
        Write-Warning "GitHub CLI не установлен"
        Write-Status "Установка GitHub CLI..."
        
        # Установка через winget
        try {
            winget install --id GitHub.cli
            Write-Success "GitHub CLI установлен"
            return $true
        }
        catch {
            Write-Error "Не удалось установить GitHub CLI. Установите вручную с https://cli.github.com"
            return $false
        }
    }
}

# Настройка Git
function Set-Git {
    Write-Status "Настройка Git..."
    
    # Проверка конфигурации
    $userName = git config --global user.name
    $userEmail = git config --global user.email
    
    if ([string]::IsNullOrEmpty($userName)) {
        Write-Warning "Имя пользователя Git не настроено"
        Write-Host "Выполните: git config --global user.name 'Ваше Имя'" -ForegroundColor Yellow
    }
    else {
        Write-Success "Имя пользователя Git: $userName"
    }
    
    if ([string]::IsNullOrEmpty($userEmail)) {
        Write-Warning "Email пользователя Git не настроен"
        Write-Host "Выполните: git config --global user.email 'ваш@email.com'" -ForegroundColor Yellow
    }
    else {
        Write-Success "Email пользователя Git: $userEmail"
    }
}

# Настройка GitHub CLI
function Set-GitHubCLI {
    Write-Status "Настройка GitHub CLI..."
    
    # Проверка аутентификации
    try {
        gh auth status 2>$null
        Write-Success "GitHub CLI аутентифицирован"
        gh auth status
    }
    catch {
        Write-Warning "GitHub CLI не аутентифицирован"
        Write-Status "Выполните аутентификацию: gh auth login"
        Write-Status "Выберите GitHub.com и веб-браузер для аутентификации"
    }
}

# Создание репозитория на GitHub
function New-GitHubRepository {
    param(
        [Parameter(Mandatory=$true)]
        [string]$RepositoryName
    )
    
    Write-Status "Создание репозитория '$RepositoryName' на GitHub..."
    
    try {
        # Создание репозитория через GitHub CLI
        gh repo create $RepositoryName `
            --description "SignalAnalyzer - Desktop Signal Analysis Tool" `
            --public `
            --clone
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Репозиторий '$RepositoryName' создан и клонирован"
            
            # Переход в директорию репозитория
            Set-Location $RepositoryName
            
            # Создание README.md
            $readmeContent = @"
# SignalAnalyzer

Desktop Signal Analysis Tool for Windows and Ubuntu

## Features

- Signal generation and analysis
- Strobe system with ray configuration
- Real-time visualization
- Mathematical engine with FFT analysis
- Cross-platform support (Windows/Ubuntu)

## Installation

### Ubuntu
```bash
./launch/ubuntu_setup.sh
source activate_project.sh
```

### Windows
```powershell
.\launch\windows_setup.ps1
.\activate_project.ps1
```

## Usage

```bash
python launch/gui/main_app.py
```

## License

MIT License
"@
            
            $readmeContent | Out-File -FilePath "README.md" -Encoding UTF8
            
            # Добавление файлов и первый коммит
            git add .
            git commit -m "Initial commit: SignalAnalyzer project setup"
            git push -u origin main
            
            Write-Success "Репозиторий настроен и загружен на GitHub"
        }
        else {
            Write-Error "Ошибка при создании репозитория"
            return $false
        }
    }
    catch {
        Write-Error "Ошибка при создании репозитория: $_"
        return $false
    }
}

# Клонирование репозитория
function Copy-GitHubRepository {
    param(
        [Parameter(Mandatory=$true)]
        [string]$RepositoryUrl
    )
    
    Write-Status "Клонирование репозитория '$RepositoryUrl'..."
    
    try {
        git clone $RepositoryUrl
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Репозиторий клонирован"
            
            # Переход в директорию проекта
            $repoName = [System.IO.Path]::GetFileNameWithoutExtension($RepositoryUrl)
            Set-Location $repoName
            
            # Активация проекта
            if (Test-Path "activate_project.ps1") {
                & ".\activate_project.ps1"
            }
            
            Write-Success "Проект готов к работе"
        }
        else {
            Write-Error "Ошибка при клонировании репозитория"
            return $false
        }
    }
    catch {
        Write-Error "Ошибка при клонировании репозитория: $_"
        return $false
    }
}

# Синхронизация с удаленным репозиторием
function Sync-GitHubRepository {
    Write-Status "Синхронизация с удаленным репозиторием..."
    
    try {
        # Получение изменений
        git fetch origin
        
        # Проверка статуса
        $status = git status --porcelain
        if ($status) {
            Write-Warning "Есть несохраненные изменения"
            Write-Status "Добавление изменений..."
            git add .
            git commit -m "Update: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        }
        
        # Отправка изменений
        git push origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Репозиторий синхронизирован"
        }
        else {
            Write-Error "Ошибка при синхронизации"
            return $false
        }
    }
    catch {
        Write-Error "Ошибка при синхронизации: $_"
        return $false
    }
}

# Создание релиза
function New-GitHubRelease {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Version,
        [string]$Message = ""
    )
    
    if ([string]::IsNullOrEmpty($Message)) {
        $Message = "Release version $Version"
    }
    
    Write-Status "Создание релиза v$Version..."
    
    try {
        # Создание тега
        git tag -a "v$Version" -m $Message
        git push origin "v$Version"
        
        # Создание релиза через GitHub CLI
        gh release create "v$Version" `
            --title "Release v$Version" `
            --notes $Message `
            --latest
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Релиз v$Version создан"
        }
        else {
            Write-Error "Ошибка при создании релиза"
            return $false
        }
    }
    catch {
        Write-Error "Ошибка при создании релиза: $_"
        return $false
    }
}

# Показать справку
function Show-Help {
    Write-Host "Доступные команды:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  setup                     - Настройка Git и GitHub CLI" -ForegroundColor White
    Write-Host "  create <repo_name>        - Создать новый репозиторий" -ForegroundColor White
    Write-Host "  clone <repo_url>          - Клонировать репозиторий" -ForegroundColor White
    Write-Host "  sync                      - Синхронизировать с удаленным репозиторием" -ForegroundColor White
    Write-Host "  release <version> [msg]   - Создать релиз" -ForegroundColor White
    Write-Host "  status                    - Показать статус Git" -ForegroundColor White
    Write-Host "  help                      - Показать эту справку" -ForegroundColor White
    Write-Host ""
    Write-Host "Примеры:" -ForegroundColor Yellow
    Write-Host "  .\github_windows_commands.ps1 setup" -ForegroundColor White
    Write-Host "  .\github_windows_commands.ps1 create signalanalyzer" -ForegroundColor White
    Write-Host "  .\github_windows_commands.ps1 clone https://github.com/user/signalanalyzer.git" -ForegroundColor White
    Write-Host "  .\github_windows_commands.ps1 sync" -ForegroundColor White
    Write-Host "  .\github_windows_commands.ps1 release 1.0.0 'Initial release'" -ForegroundColor White
}

# Показать статус
function Show-Status {
    Write-Status "Статус Git репозитория:"
    git status
    
    Write-Host ""
    Write-Status "Информация о репозитории:"
    if (Test-Path ".git") {
        try {
            $remoteUrl = git remote get-url origin 2>$null
            if ($remoteUrl) {
                Write-Host "Репозиторий: $remoteUrl" -ForegroundColor Cyan
            }
            else {
                Write-Host "Репозиторий: Локальный репозиторий" -ForegroundColor Cyan
            }
        }
        catch {
            Write-Host "Репозиторий: Локальный репозиторий" -ForegroundColor Cyan
        }
        
        $currentBranch = git branch --show-current
        Write-Host "Ветка: $currentBranch" -ForegroundColor Cyan
        
        $lastCommit = git log -1 --oneline
        Write-Host "Последний коммит: $lastCommit" -ForegroundColor Cyan
    }
    else {
        Write-Warning "Текущая директория не является Git репозиторием"
    }
}

# Основная функция
function Main {
    param(
        [string]$Command = "help",
        [string]$Arg1 = "",
        [string]$Arg2 = ""
    )
    
    switch ($Command.ToLower()) {
        "setup" {
            Test-Git
            Test-GitHubCLI
            Set-Git
            Set-GitHubCLI
        }
        "create" {
            if ($Arg1) {
                New-GitHubRepository -RepositoryName $Arg1
            }
            else {
                Write-Error "Использование: create <имя_репозитория>"
            }
        }
        "clone" {
            if ($Arg1) {
                Copy-GitHubRepository -RepositoryUrl $Arg1
            }
            else {
                Write-Error "Использование: clone <URL_репозитория>"
            }
        }
        "sync" {
            Sync-GitHubRepository
        }
        "release" {
            if ($Arg1) {
                New-GitHubRelease -Version $Arg1 -Message $Arg2
            }
            else {
                Write-Error "Использование: release <версия> [сообщение]"
            }
        }
        "status" {
            Show-Status
        }
        "help" {
            Show-Help
        }
        default {
            Write-Error "Неизвестная команда: $Command"
            Show-Help
        }
    }
}

# Запуск основной функции
Main @args
