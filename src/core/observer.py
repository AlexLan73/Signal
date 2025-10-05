"""Observer pattern implementation for SignalAnalyzer."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable
from enum import Enum

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class DataEventType(Enum):
    """Типы событий данных."""
    SIGNAL_GENERATED = "signal_generated"
    STROBE_GENERATED = "strobe_generated"
    ANALYSIS_COMPLETED = "analysis_completed"
    PLOT_UPDATED = "plot_updated"
    CONFIGURATION_CHANGED = "configuration_changed"
    ERROR_OCCURRED = "error_occurred"


class Observer(ABC):
    """Абстрактный класс наблюдателя."""
    
    @abstractmethod
    def update(self, event_type: DataEventType, data: Any) -> None:
        """
        Обновление наблюдателя.
        
        Args:
            event_type: Тип события
            data: Данные события
        """
        pass


class Subject(ABC):
    """Абстрактный класс субъекта (издателя)."""
    
    def __init__(self):
        """Инициализация субъекта."""
        self._observers: List[Observer] = []
        logger.debug(f"Subject initialized: {self.__class__.__name__}")
    
    def attach(self, observer: Observer) -> None:
        """
        Прикрепить наблюдателя.
        
        Args:
            observer: Наблюдатель для прикрепления
        """
        if observer not in self._observers:
            self._observers.append(observer)
            logger.debug(f"Observer attached: {observer.__class__.__name__}")
    
    def detach(self, observer: Observer) -> None:
        """
        Открепить наблюдателя.
        
        Args:
            observer: Наблюдатель для открепления
        """
        if observer in self._observers:
            self._observers.remove(observer)
            logger.debug(f"Observer detached: {observer.__class__.__name__}")
    
    def notify(self, event_type: DataEventType, data: Any = None) -> None:
        """
        Уведомить всех наблюдателей.
        
        Args:
            event_type: Тип события
            data: Данные события
        """
        for observer in self._observers:
            try:
                observer.update(event_type, data)
            except Exception as e:
                logger.error(f"Error notifying observer {observer.__class__.__name__}: {e}")
        
        logger.debug(f"Notified {len(self._observers)} observers: {event_type.value}")
    
    def get_observer_count(self) -> int:
        """
        Получить количество наблюдателей.
        
        Returns:
            Количество наблюдателей
        """
        return len(self._observers)


class CallbackObserver(Observer):
    """Наблюдатель на основе callback функций."""
    
    def __init__(self, callback: Callable[[DataEventType, Any], None]):
        """
        Инициализация callback наблюдателя.
        
        Args:
            callback: Callback функция для обработки событий
        """
        self.callback = callback
        logger.debug(f"CallbackObserver initialized with {callback.__name__}")
    
    def update(self, event_type: DataEventType, data: Any) -> None:
        """
        Обновление через callback.
        
        Args:
            event_type: Тип события
            data: Данные события
        """
        try:
            self.callback(event_type, data)
        except Exception as e:
            logger.error(f"Error in callback observer: {e}")


class FilteredObserver(Observer):
    """Наблюдатель с фильтрацией событий."""
    
    def __init__(self, observer: Observer, event_types: List[DataEventType]):
        """
        Инициализация фильтрованного наблюдателя.
        
        Args:
            observer: Базовый наблюдатель
            event_types: Типы событий для фильтрации
        """
        self.observer = observer
        self.event_types = set(event_types)
        logger.debug(f"FilteredObserver initialized for {len(event_types)} event types")
    
    def update(self, event_type: DataEventType, data: Any) -> None:
        """
        Обновление с фильтрацией.
        
        Args:
            event_type: Тип события
            data: Данные события
        """
        if event_type in self.event_types:
            self.observer.update(event_type, data)


class EventBus:
    """Глобальная шина событий."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Инициализация шины событий."""
        if not self._initialized:
            self._subjects: Dict[str, Subject] = {}
            self._global_observers: List[Observer] = []
            self._initialized = True
            logger.info("EventBus initialized")
    
    def register_subject(self, name: str, subject: Subject) -> None:
        """
        Зарегистрировать субъекта.
        
        Args:
            name: Имя субъекта
            subject: Субъект для регистрации
        """
        self._subjects[name] = subject
        logger.debug(f"Subject registered: {name}")
    
    def unregister_subject(self, name: str) -> None:
        """
        Отменить регистрацию субъекта.
        
        Args:
            name: Имя субъекта
        """
        if name in self._subjects:
            del self._subjects[name]
            logger.debug(f"Subject unregistered: {name}")
    
    def get_subject(self, name: str) -> Subject:
        """
        Получить субъекта по имени.
        
        Args:
            name: Имя субъекта
            
        Returns:
            Субъект или None
        """
        return self._subjects.get(name)
    
    def attach_global_observer(self, observer: Observer) -> None:
        """
        Прикрепить глобального наблюдателя.
        
        Args:
            observer: Наблюдатель для прикрепления
        """
        self._global_observers.append(observer)
        logger.debug(f"Global observer attached: {observer.__class__.__name__}")
    
    def detach_global_observer(self, observer: Observer) -> None:
        """
        Открепить глобального наблюдателя.
        
        Args:
            observer: Наблюдатель для открепления
        """
        if observer in self._global_observers:
            self._global_observers.remove(observer)
            logger.debug(f"Global observer detached: {observer.__class__.__name__}")
    
    def publish_event(self, event_type: DataEventType, data: Any = None, source: str = None) -> None:
        """
        Опубликовать событие.
        
        Args:
            event_type: Тип события
            data: Данные события
            source: Источник события
        """
        # Уведомляем глобальных наблюдателей
        for observer in self._global_observers:
            try:
                observer.update(event_type, data)
            except Exception as e:
                logger.error(f"Error in global observer {observer.__class__.__name__}: {e}")
        
        # Уведомляем субъектов
        for subject in self._subjects.values():
            subject.notify(event_type, data)
        
        logger.debug(f"Event published: {event_type.value} from {source or 'unknown'}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Получить статистику шины событий.
        
        Returns:
            Словарь со статистикой
        """
        return {
            'subjects_count': len(self._subjects),
            'global_observers_count': len(self._global_observers),
            'total_observers': sum(subject.get_observer_count() for subject in self._subjects.values()),
            'subjects': list(self._subjects.keys())
        }


# Глобальная шина событий
event_bus = EventBus()

