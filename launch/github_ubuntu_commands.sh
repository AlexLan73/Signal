#!/bin/bash
# SignalAnalyzer - GitHub Commands for Ubuntu
# Команды для работы с GitHub из Ubuntu

echo "🐙 SignalAnalyzer - GitHub Commands for Ubuntu"
echo "=============================================="

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка установки Git
check_git() {
    if ! command -v git &> /dev/null; then
        print_error "Git не установлен. Установите Git: sudo apt install git"
        return 1
    fi
    print_success "Git установлен: $(git --version)"
    return 0
}

# Проверка установки GitHub CLI
check_gh() {
    if ! command -v gh &> /dev/null; then
        print_warning "GitHub CLI не установлен"
        print_status "Установка GitHub CLI..."
        
        # Установка GitHub CLI
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
        sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
        sudo apt update
        sudo apt install gh
        
        print_success "GitHub CLI установлен"
    else
        print_success "GitHub CLI установлен: $(gh --version)"
    fi
}

# Настройка Git
setup_git() {
    print_status "Настройка Git..."
    
    # Проверка конфигурации
    if [ -z "$(git config --global user.name)" ]; then
        print_warning "Имя пользователя Git не настроено"
        echo "Выполните: git config --global user.name 'Ваше Имя'"
    else
        print_success "Имя пользователя Git: $(git config --global user.name)"
    fi
    
    if [ -z "$(git config --global user.email)" ]; then
        print_warning "Email пользователя Git не настроен"
        echo "Выполните: git config --global user.email 'ваш@email.com'"
    else
        print_success "Email пользователя Git: $(git config --global user.email)"
    fi
}

# Настройка GitHub CLI
setup_gh() {
    print_status "Настройка GitHub CLI..."
    
    # Проверка аутентификации
    if ! gh auth status &> /dev/null; then
        print_warning "GitHub CLI не аутентифицирован"
        print_status "Выполните аутентификацию: gh auth login"
        print_status "Выберите GitHub.com и веб-браузер для аутентификации"
    else
        print_success "GitHub CLI аутентифицирован"
        gh auth status
    fi
}

# Создание репозитория на GitHub
create_repository() {
    local repo_name="$1"
    if [ -z "$repo_name" ]; then
        echo "Использование: create_repository <имя_репозитория>"
        return 1
    fi
    
    print_status "Создание репозитория '$repo_name' на GitHub..."
    
    # Создание репозитория через GitHub CLI
    gh repo create "$repo_name" \
        --description "SignalAnalyzer - Desktop Signal Analysis Tool" \
        --public \
        --clone
    
    if [ $? -eq 0 ]; then
        print_success "Репозиторий '$repo_name' создан и клонирован"
        
        # Переход в директорию репозитория
        cd "$repo_name"
        
        # Создание README.md
        cat > README.md << 'EOF'
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
EOF
        
        # Добавление файлов и первый коммит
        git add .
        git commit -m "Initial commit: SignalAnalyzer project setup"
        git push -u origin main
        
        print_success "Репозиторий настроен и загружен на GitHub"
    else
        print_error "Ошибка при создании репозитория"
        return 1
    fi
}

# Клонирование репозитория
clone_repository() {
    local repo_url="$1"
    if [ -z "$repo_url" ]; then
        echo "Использование: clone_repository <URL_репозитория>"
        return 1
    fi
    
    print_status "Клонирование репозитория '$repo_url'..."
    
    git clone "$repo_url"
    
    if [ $? -eq 0 ]; then
        print_success "Репозиторий клонирован"
        
        # Переход в директорию проекта
        local repo_name=$(basename "$repo_url" .git)
        cd "$repo_name"
        
        # Активация проекта
        if [ -f "activate_project.sh" ]; then
            source activate_project.sh
        fi
        
        print_success "Проект готов к работе"
    else
        print_error "Ошибка при клонировании репозитория"
        return 1
    fi
}

# Синхронизация с удаленным репозиторием
sync_repository() {
    print_status "Синхронизация с удаленным репозиторием..."
    
    # Получение изменений
    git fetch origin
    
    # Проверка статуса
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "Есть несохраненные изменения"
        print_status "Добавление изменений..."
        git add .
        git commit -m "Update: $(date '+%Y-%m-%d %H:%M:%S')"
    fi
    
    # Отправка изменений
    git push origin main
    
    if [ $? -eq 0 ]; then
        print_success "Репозиторий синхронизирован"
    else
        print_error "Ошибка при синхронизации"
        return 1
    fi
}

# Создание релиза
create_release() {
    local version="$1"
    local message="$2"
    
    if [ -z "$version" ]; then
        echo "Использование: create_release <версия> [сообщение]"
        return 1
    fi
    
    if [ -z "$message" ]; then
        message="Release version $version"
    fi
    
    print_status "Создание релиза v$version..."
    
    # Создание тега
    git tag -a "v$version" -m "$message"
    git push origin "v$version"
    
    # Создание релиза через GitHub CLI
    gh release create "v$version" \
        --title "Release v$version" \
        --notes "$message" \
        --latest
    
    if [ $? -eq 0 ]; then
        print_success "Релиз v$version создан"
    else
        print_error "Ошибка при создании релиза"
        return 1
    fi
}

# Показать справку
show_help() {
    echo "Доступные команды:"
    echo ""
    echo "  setup                     - Настройка Git и GitHub CLI"
    echo "  create <repo_name>        - Создать новый репозиторий"
    echo "  clone <repo_url>          - Клонировать репозиторий"
    echo "  sync                      - Синхронизировать с удаленным репозиторием"
    echo "  release <version> [msg]   - Создать релиз"
    echo "  status                    - Показать статус Git"
    echo "  help                      - Показать эту справку"
    echo ""
    echo "Примеры:"
    echo "  ./github_ubuntu_commands.sh setup"
    echo "  ./github_ubuntu_commands.sh create signalanalyzer"
    echo "  ./github_ubuntu_commands.sh clone https://github.com/user/signalanalyzer.git"
    echo "  ./github_ubuntu_commands.sh sync"
    echo "  ./github_ubuntu_commands.sh release 1.0.0 'Initial release'"
}

# Показать статус
show_status() {
    print_status "Статус Git репозитория:"
    git status
    
    echo ""
    print_status "Информация о репозитории:"
    if [ -d ".git" ]; then
        echo "Репозиторий: $(git remote get-url origin 2>/dev/null || echo 'Локальный репозиторий')"
        echo "Ветка: $(git branch --show-current)"
        echo "Последний коммит: $(git log -1 --oneline)"
    else
        print_warning "Текущая директория не является Git репозиторием"
    fi
}

# Основная функция
main() {
    local command="$1"
    local arg1="$2"
    local arg2="$3"
    
    case "$command" in
        "setup")
            check_git
            check_gh
            setup_git
            setup_gh
            ;;
        "create")
            create_repository "$arg1"
            ;;
        "clone")
            clone_repository "$arg1"
            ;;
        "sync")
            sync_repository
            ;;
        "release")
            create_release "$arg1" "$arg2"
            ;;
        "status")
            show_status
            ;;
        "help"|"--help"|"-h"|"")
            show_help
            ;;
        *)
            print_error "Неизвестная команда: $command"
            show_help
            exit 1
            ;;
    esac
}

# Запуск основной функции
main "$@"
