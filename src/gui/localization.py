"""Russian localization for SignalAnalyzer GUI."""

# Russian translations for GUI elements
TRANSLATIONS = {
    # Main window
    "SignalAnalyzer - Desktop Signal Analysis Tool": "SignalAnalyzer - Настольный анализатор сигналов",
    "SignalAnalyzer GUI Test": "Тест GUI SignalAnalyzer",
    
    # Menu items
    "&File": "&Файл",
    "&Edit": "&Правка", 
    "&View": "&Вид",
    "&Analysis": "&Анализ",
    "&Help": "&Справка",
    
    "&New Signal": "&Новый сигнал",
    "&Open...": "&Открыть...",
    "&Save": "&Сохранить",
    "E&xit": "В&ыход",
    
    "&Copy": "&Копировать",
    "&Paste": "&Вставить",
    
    "&Fullscreen": "&Полный экран",
    "&FFT Analysis": "&БПФ анализ",
    "&Spectral Analysis": "&Спектральный анализ",
    
    "&About": "&О программе",
    
    # Toolbar
    "New": "Новый",
    "Generate": "Генерировать",
    "Play": "Воспроизвести",
    "Record": "Записать",
    "Zoom In": "Увеличить",
    "Zoom Out": "Уменьшить",
    
    # Status messages
    "Ready": "Готов",
    "SignalAnalyzer ready": "SignalAnalyzer готов",
    "Creating new signal...": "Создание нового сигнала...",
    "Opening file...": "Открытие файла...",
    "Saving file...": "Сохранение файла...",
    "Exited fullscreen": "Выход из полноэкранного режима",
    "Entered fullscreen": "Полноэкранный режим",
    "Performing FFT analysis...": "Выполнение БПФ анализа...",
    "Performing spectral analysis...": "Выполнение спектрального анализа...",
    "Toggling playback...": "Переключение воспроизведения...",
    "Toggling recording...": "Переключение записи...",
    "Zooming in...": "Увеличение...",
    "Zooming out...": "Уменьшение...",
    "Signal generated successfully": "Сигнал успешно сгенерирован",
    "Analysis completed": "Анализ завершен",
    "Plot updated": "График обновлен",
    "Application closing": "Закрытие приложения",
    
    # Tab names
    "Signal Generator": "Генератор сигналов",
    "2D Plot": "2D График",
    "3D Plot": "3D График", 
    "Spectrum": "Спектр",
    "Oscilloscope": "Осциллограф",
    
    # Signal configuration
    "Signal Configuration": "Конфигурация сигнала",
    "Frequency:": "Частота:",
    "Amplitude:": "Амплитуда:",
    "Law Type:": "Тип закона:",
    "Generate Signal": "Генерировать сигнал",
    
    # Analysis controls
    "Analysis Controls": "Элементы управления анализом",
    "FFT Analysis": "БПФ анализ",
    "Spectral Analysis": "Спектральный анализ",
    
    # Plot placeholders
    "Signal Generator": "Генератор сигналов",
    "Configure signal parameters in the left panel": "Настройте параметры сигнала в левой панели",
    "Click 'Generate Signal' to create a mathematical signal": "Нажмите 'Генерировать сигнал' для создания математического сигнала",
    "Use the tabs above to visualize the signal": "Используйте вкладки выше для визуализации сигнала",
    
    "2D Plot Visualization": "Визуализация 2D графика",
    "2D Plot Area": "Область 2D графика",
    "Matplotlib integration will be displayed here": "Интеграция matplotlib будет отображена здесь",
    "Real-time signal visualization": "Визуализация сигнала в реальном времени",
    "Interactive zoom and pan": "Интерактивное увеличение и панорама",
    "Note: matplotlib not available": "Примечание: matplotlib недоступен",
    
    "3D Plot Visualization": "Визуализация 3D графика",
    "3D Plot Area": "Область 3D графика",
    "PyOpenGL 3D visualization will be displayed here": "3D визуализация PyOpenGL будет отображена здесь",
    "Interactive 3D surface plots": "Интерактивные 3D поверхностные графики",
    "GPU-accelerated rendering": "Рендеринг с GPU ускорением",
    
    "Spectrum Analysis": "Спектральный анализ",
    "Spectrum Analysis Area": "Область спектрального анализа",
    "FFT and spectral analysis results will be displayed here": "Результаты БПФ и спектрального анализа будут отображены здесь",
    "Harmonic components visualization": "Визуализация гармонических компонентов",
    "Frequency domain analysis": "Анализ в частотной области",
    
    "Real-time Oscilloscope": "Осциллограф в реальном времени",
    "Oscilloscope Display": "Дисплей осциллографа",
    "Real-time signal monitoring will be displayed here": "Мониторинг сигнала в реальном времени будет отображен здесь",
    "Multi-channel oscilloscope": "Многоканальный осциллограф",
    "60+ FPS performance target": "Целевая производительность 60+ FPS",
    
    # About dialog
    "About SignalAnalyzer": "О SignalAnalyzer",
    "SignalAnalyzer v1.0.0": "SignalAnalyzer v1.0.0",
    "Desktop Signal Analysis Tool": "Настольный анализатор сигналов",
    "Mathematical signal generation and visualization": "Генерация и визуализация математических сигналов",
    "Built with PyQt6, matplotlib, and PyOpenGL": "Создано с PyQt6, matplotlib и PyOpenGL",
    
    # Plot controls
    "Plot Signal": "Построить сигнал",
    "Clear": "Очистить",
    "Toggle Grid": "Сетка",
    "Samples:": "Образцы:",
    "Ready to plot": "Готов к построению",
    "Plotted:": "Построено:",
    "Plot cleared": "График очищен",
    "Grid enabled": "Сетка включена",
    "Grid disabled": "Сетка выключена",
    "Custom signal plotted:": "Построен пользовательский сигнал:",
    "points": "точек",
    "Plot saved:": "График сохранен:",
    "Error saving:": "Ошибка сохранения:",
    
    # Signal types
    "Sine": "Синус",
    "Cosine": "Косинус", 
    "Square": "Прямоугольный",
    "Sawtooth": "Пилообразный",
    "Triangle": "Треугольный",
    "Noise": "Шум",
    "Chirp": "Чирп",
    "Pulse": "Импульс",
    "Complex": "Сложный"
}


def tr(text: str) -> str:
    """Translate text to Russian."""
    return TRANSLATIONS.get(text, text)


def translate_widget(widget):
    """Translate widget text to Russian."""
    if hasattr(widget, 'setText'):
        widget.setText(tr(widget.text()))
    if hasattr(widget, 'setWindowTitle'):
        widget.setWindowTitle(tr(widget.windowTitle()))
    if hasattr(widget, 'setStatusTip'):
        widget.setStatusTip(tr(widget.statusTip()))
    if hasattr(widget, 'setToolTip'):
        widget.setToolTip(tr(widget.toolTip()))
    
    # Translate children
    for child in widget.children():
        if hasattr(child, 'children'):
            translate_widget(child)

