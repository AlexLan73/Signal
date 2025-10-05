#!/bin/bash
# SignalAnalyzer - Ubuntu Setup Script
# Инициализация библиотек и зависимостей для Ubuntu

echo "🚀 SignalAnalyzer - Ubuntu Setup"
echo "================================="

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

# Проверка версии Ubuntu
check_ubuntu_version() {
    print_status "Проверка версии Ubuntu..."
    if [ -f /etc/lsb-release ]; then
        . /etc/lsb-release
        print_success "Ubuntu версия: $DISTRIB_DESCRIPTION"
    else
        print_warning "Не удалось определить версию Ubuntu"
    fi
}

# Обновление системы
update_system() {
    print_status "Обновление системы..."
    sudo apt update && sudo apt upgrade -y
    print_success "Система обновлена"
}

# Установка Python и базовых инструментов
install_python() {
    print_status "Установка Python и инструментов разработки..."
    
    # Установка Python 3.12
    sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip
    
    # Установка инструментов разработки
    sudo apt install -y build-essential cmake pkg-config
    
    # Установка Git
    sudo apt install -y git
    
    # Установка curl и wget
    sudo apt install -y curl wget
    
    print_success "Python и инструменты разработки установлены"
}

# Установка математических библиотек
install_math_libraries() {
    print_status "Установка математических библиотек..."
    
    # BLAS и LAPACK
    sudo apt install -y libblas-dev liblapack-dev
    
    # ATLAS
    sudo apt install -y libatlas-base-dev
    
    # FFTW
    sudo apt install -y libfftw3-dev
    
    print_success "Математические библиотеки установлены"
}

# Установка GUI библиотек
install_gui_libraries() {
    print_status "Установка GUI библиотек..."
    
    # Qt6 для PyQt6
    sudo apt install -y qt6-base-dev qt6-tools-dev
    
    # X11 для GUI
    sudo apt install -y libx11-dev libxext-dev libxrender-dev
    
    # OpenGL
    sudo apt install -y libgl1-mesa-dev libglu1-mesa-dev
    
    print_success "GUI библиотеки установлены"
}

# Установка Python пакетов
install_python_packages() {
    print_status "Установка Python пакетов..."
    
    # Создание виртуального окружения
    python3.12 -m venv venv
    source venv/bin/activate
    
    # Обновление pip
    pip install --upgrade pip setuptools wheel
    
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
    
    print_success "Python пакеты установлены"
}

# Установка GPU ускорения (опционально)
install_gpu_acceleration() {
    print_status "Установка GPU ускорения (опционально)..."
    
    # Проверка NVIDIA GPU
    if command -v nvidia-smi &> /dev/null; then
        print_status "NVIDIA GPU обнаружен"
        
        # Установка CUDA toolkit
        wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
        sudo dpkg -i cuda-keyring_1.0-1_all.deb
        sudo apt update
        sudo apt install -y cuda-toolkit
        
        # Установка CuPy
        pip install cupy-cuda12x>=12.0.0
        
        print_success "GPU ускорение установлено"
    else
        print_warning "NVIDIA GPU не обнаружен, пропускаем установку GPU ускорения"
    fi
}

# Настройка Git
setup_git() {
    print_status "Настройка Git..."
    
    # Глобальная конфигурация Git (пользователь должен настроить сам)
    echo "Для настройки Git выполните:"
    echo "git config --global user.name 'Ваше Имя'"
    echo "git config --global user.email 'ваш@email.com'"
    
    print_success "Git готов к настройке"
}

# Создание структуры проекта
create_project_structure() {
    print_status "Создание структуры проекта..."
    
    # Создание необходимых папок
    mkdir -p data/strobes/generated
    mkdir -p data/strobes/templates
    mkdir -p data/strobes/archived
    mkdir -p data/signals/generated
    mkdir -p data/signals/templates
    mkdir -p data/signals/archived
    mkdir -p reports/$(date +%Y)/$(date +%m)/$(date +%d)
    mkdir -p logs
    mkdir -p tests
    
    print_success "Структура проекта создана"
}

# Создание скрипта активации
create_activation_script() {
    print_status "Создание скрипта активации..."
    
    cat > activate_project.sh << 'EOF'
#!/bin/bash
# Активация проекта SignalAnalyzer

echo "🚀 Активация SignalAnalyzer..."

# Активация виртуального окружения
source venv/bin/activate

# Установка PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Переход в корневую директорию проекта
cd "$(dirname "$0")"

echo "✅ Проект активирован!"
echo "📁 Рабочая директория: $(pwd)"
echo "🐍 Python: $(which python)"
echo "📦 Виртуальное окружение: активировано"
echo ""
echo "Доступные команды:"
echo "  python launch/gui/main_app.py          # Основное GUI приложение"
echo "  python launch/tests/strobe_system_test.py # Тест системы стробов"
echo "  python launch/tests/math_engine_test.py   # Тест математического движка"
echo "  python launch/tests/full_integration_test.py # Полный интеграционный тест"
EOF

    chmod +x activate_project.sh
    print_success "Скрипт активации создан"
}

# Основная функция
main() {
    echo "Начинаем установку SignalAnalyzer для Ubuntu..."
    echo ""
    
    check_ubuntu_version
    echo ""
    
    update_system
    echo ""
    
    install_python
    echo ""
    
    install_math_libraries
    echo ""
    
    install_gui_libraries
    echo ""
    
    install_python_packages
    echo ""
    
    install_gpu_acceleration
    echo ""
    
    setup_git
    echo ""
    
    create_project_structure
    echo ""
    
    create_activation_script
    echo ""
    
    print_success "Установка завершена!"
    echo ""
    echo "Следующие шаги:"
    echo "1. Настройте Git: git config --global user.name 'Ваше Имя'"
    echo "2. Настройте Git: git config --global user.email 'ваш@email.com'"
    echo "3. Активируйте проект: source activate_project.sh"
    echo "4. Запустите приложение: python launch/gui/main_app.py"
    echo ""
    echo "🎉 SignalAnalyzer готов к работе на Ubuntu!"
}

# Запуск основной функции
main "$@"
