"""DataContext system for SignalAnalyzer data exchange."""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union, Type, Callable
from dataclasses import dataclass, asdict
from enum import Enum

from .observer import Observer, Subject, DataEventType, event_bus
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class DataType(Enum):
    """Типы данных в DataContext."""
    SIGNAL = "signal"
    STROBE = "strobe"
    ANALYSIS_RESULT = "analysis_result"
    CONFIGURATION = "configuration"
    METADATA = "metadata"
    VISUALIZATION_DATA = "visualization_data"


@dataclass
class DataRecord:
    """Запись данных в DataContext."""
    id: str
    data_type: DataType
    data: Any
    metadata: Dict[str, Any]
    timestamp: datetime
    source: str
    version: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразовать в словарь."""
        return {
            'id': self.id,
            'data_type': self.data_type.value,
            'data': self.data,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat(),
            'source': self.source,
            'version': self.version
        }
    
    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> 'DataRecord':
        """Создать из словаря."""
        return cls(
            id=data_dict['id'],
            data_type=DataType(data_dict['data_type']),
            data=data_dict['data'],
            metadata=data_dict['metadata'],
            timestamp=datetime.fromisoformat(data_dict['timestamp']),
            source=data_dict['source'],
            version=data_dict.get('version', 1)
        )


class DataValidator:
    """Валидатор данных для DataContext."""
    
    @staticmethod
    def validate_signal_data(data: Any) -> bool:
        """Валидация сигнальных данных."""
        try:
            import numpy as np
            if isinstance(data, np.ndarray):
                return len(data.shape) == 1 and data.size > 0
            elif isinstance(data, dict):
                return 'signal' in data and 'time' in data
            return False
        except ImportError:
            return isinstance(data, (list, tuple)) and len(data) > 0
    
    @staticmethod
    def validate_strobe_data(data: Any) -> bool:
        """Валидация данных стробов."""
        try:
            import numpy as np
            if isinstance(data, np.ndarray):
                return len(data.shape) == 1 and data.size > 0
            elif isinstance(data, dict):
                return all(key in data for key in ['data', 'metadata'])
            return False
        except ImportError:
            return isinstance(data, (list, tuple)) and len(data) > 0
    
    @staticmethod
    def validate_analysis_result(data: Any) -> bool:
        """Валидация результатов анализа."""
        return isinstance(data, dict) and 'result' in data
    
    @staticmethod
    def validate_configuration(data: Any) -> bool:
        """Валидация конфигурации."""
        return isinstance(data, dict) and len(data) > 0
    
    @staticmethod
    def validate_metadata(data: Any) -> bool:
        """Валидация метаданных."""
        return isinstance(data, dict)
    
    @staticmethod
    def validate_visualization_data(data: Any) -> bool:
        """Валидация данных визуализации."""
        return isinstance(data, dict) and 'plot_data' in data
    
    @classmethod
    def validate(cls, data_type: DataType, data: Any) -> bool:
        """Валидация данных по типу."""
        validators = {
            DataType.SIGNAL: cls.validate_signal_data,
            DataType.STROBE: cls.validate_strobe_data,
            DataType.ANALYSIS_RESULT: cls.validate_analysis_result,
            DataType.CONFIGURATION: cls.validate_configuration,
            DataType.METADATA: cls.validate_metadata,
            DataType.VISUALIZATION_DATA: cls.validate_visualization_data
        }
        
        validator = validators.get(data_type)
        if validator:
            return validator(data)
        return False


class DataSerializer:
    """Сериализатор данных для DataContext."""
    
    @staticmethod
    def serialize(data: Any) -> str:
        """Сериализация данных в JSON."""
        try:
            import numpy as np
            
            # Обработка numpy массивов
            if isinstance(data, np.ndarray):
                return json.dumps({
                    'type': 'numpy_array',
                    'shape': data.shape,
                    'dtype': str(data.dtype),
                    'data': data.tolist()
                })
            
            # Обработка обычных данных
            return json.dumps(data, default=str)
            
        except Exception as e:
            logger.error(f"Serialization error: {e}")
            return json.dumps(str(data))
    
    @staticmethod
    def deserialize(data_str: str) -> Any:
        """Десериализация данных из JSON."""
        try:
            data = json.loads(data_str)
            
            # Восстановление numpy массивов
            if isinstance(data, dict) and data.get('type') == 'numpy_array':
                import numpy as np
                return np.array(data['data']).astype(data['dtype']).reshape(data['shape'])
            
            return data
            
        except Exception as e:
            logger.error(f"Deserialization error: {e}")
            return None


class DataManager(Subject):
    """Менеджер данных для DataContext."""
    
    def __init__(self, name: str = "DataManager"):
        """Инициализация менеджера данных."""
        super().__init__()
        self.name = name
        self._data_store: Dict[str, DataRecord] = {}
        self._type_index: Dict[DataType, List[str]] = {dt: [] for dt in DataType}
        self._validator = DataValidator()
        self._serializer = DataSerializer()
        
        # Регистрируемся в глобальной шине событий
        event_bus.register_subject(name, self)
        
        logger.info(f"DataManager initialized: {name}")
    
    def store_data(self, data_type: DataType, data: Any, metadata: Dict[str, Any] = None, 
                   source: str = None) -> str:
        """
        Сохранить данные.
        
        Args:
            data_type: Тип данных
            data: Данные для сохранения
            metadata: Метаданные
            source: Источник данных
            
        Returns:
            ID сохраненных данных
        """
        # Валидация данных
        if not self._validator.validate(data_type, data):
            raise ValueError(f"Invalid data for type {data_type.value}")
        
        # Создание записи
        data_id = str(uuid.uuid4())
        record = DataRecord(
            id=data_id,
            data_type=data_type,
            data=data,
            metadata=metadata or {},
            timestamp=datetime.now(),
            source=source or self.name
        )
        
        # Сохранение
        self._data_store[data_id] = record
        self._type_index[data_type].append(data_id)
        
        # Уведомление наблюдателей
        self.notify(DataEventType.SIGNAL_GENERATED if data_type == DataType.SIGNAL 
                   else DataEventType.STROBE_GENERATED, record)
        
        logger.info(f"Data stored: {data_type.value} with ID {data_id}")
        return data_id
    
    def get_data(self, data_id: str) -> Optional[DataRecord]:
        """
        Получить данные по ID.
        
        Args:
            data_id: ID данных
            
        Returns:
            Запись данных или None
        """
        return self._data_store.get(data_id)
    
    def get_data_by_type(self, data_type: DataType) -> List[DataRecord]:
        """
        Получить данные по типу.
        
        Args:
            data_type: Тип данных
            
        Returns:
            Список записей данных
        """
        return [self._data_store[data_id] for data_id in self._type_index[data_type] 
                if data_id in self._data_store]
    
    def get_latest_data(self, data_type: DataType) -> Optional[DataRecord]:
        """
        Получить последние данные по типу.
        
        Args:
            data_type: Тип данных
            
        Returns:
            Последняя запись данных или None
        """
        records = self.get_data_by_type(data_type)
        if records:
            return max(records, key=lambda r: r.timestamp)
        return None
    
    def delete_data(self, data_id: str) -> bool:
        """
        Удалить данные по ID.
        
        Args:
            data_id: ID данных
            
        Returns:
            True если данные удалены
        """
        if data_id in self._data_store:
            record = self._data_store[data_id]
            del self._data_store[data_id]
            self._type_index[record.data_type].remove(data_id)
            logger.info(f"Data deleted: {data_id}")
            return True
        return False
    
    def clear_data(self, data_type: DataType = None) -> int:
        """
        Очистить данные.
        
        Args:
            data_type: Тип данных для очистки (None = все)
            
        Returns:
            Количество удаленных записей
        """
        if data_type is None:
            count = len(self._data_store)
            self._data_store.clear()
            for dt in DataType:
                self._type_index[dt].clear()
            logger.info(f"All data cleared: {count} records")
            return count
        else:
            data_ids = self._type_index[data_type].copy()
            for data_id in data_ids:
                del self._data_store[data_id]
            self._type_index[data_type].clear()
            logger.info(f"Data cleared for type {data_type.value}: {len(data_ids)} records")
            return len(data_ids)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Получить статистику данных.
        
        Returns:
            Словарь со статистикой
        """
        return {
            'total_records': len(self._data_store),
            'records_by_type': {dt.value: len(ids) for dt, ids in self._type_index.items()},
            'memory_usage': len(self._serializer.serialize(self._data_store)),
            'oldest_record': min((r.timestamp for r in self._data_store.values()), default=None),
            'newest_record': max((r.timestamp for r in self._data_store.values()), default=None)
        }
    
    def export_data(self, filepath: str, data_ids: List[str] = None) -> bool:
        """
        Экспорт данных в файл.
        
        Args:
            filepath: Путь к файлу
            data_ids: ID данных для экспорта (None = все)
            
        Returns:
            True если экспорт успешен
        """
        try:
            if data_ids is None:
                data_ids = list(self._data_store.keys())
            
            export_data = {
                'export_timestamp': datetime.now().isoformat(),
                'exported_by': self.name,
                'records': [self._data_store[data_id].to_dict() for data_id in data_ids 
                           if data_id in self._data_store]
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Data exported to {filepath}: {len(data_ids)} records")
            return True
            
        except Exception as e:
            logger.error(f"Export error: {e}")
            return False
    
    def import_data(self, filepath: str) -> int:
        """
        Импорт данных из файла.
        
        Args:
            filepath: Путь к файлу
            
        Returns:
            Количество импортированных записей
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            count = 0
            for record_dict in import_data.get('records', []):
                record = DataRecord.from_dict(record_dict)
                self._data_store[record.id] = record
                self._type_index[record.data_type].append(record.id)
                count += 1
            
            logger.info(f"Data imported from {filepath}: {count} records")
            return count
            
        except Exception as e:
            logger.error(f"Import error: {e}")
            return 0


class DataPublisher:
    """Издатель данных для DataContext."""
    
    def __init__(self, data_manager: DataManager, name: str = "DataPublisher"):
        """Инициализация издателя данных."""
        self.data_manager = data_manager
        self.name = name
        logger.debug(f"DataPublisher initialized: {name}")
    
    def publish_signal(self, signal_data: Any, metadata: Dict[str, Any] = None) -> str:
        """Опубликовать сигнальные данные."""
        return self.data_manager.store_data(DataType.SIGNAL, signal_data, metadata, self.name)
    
    def publish_strobe(self, strobe_data: Any, metadata: Dict[str, Any] = None) -> str:
        """Опубликовать данные стробов."""
        return self.data_manager.store_data(DataType.STROBE, strobe_data, metadata, self.name)
    
    def publish_analysis_result(self, result_data: Any, metadata: Dict[str, Any] = None) -> str:
        """Опубликовать результаты анализа."""
        return self.data_manager.store_data(DataType.ANALYSIS_RESULT, result_data, metadata, self.name)
    
    def publish_configuration(self, config_data: Any, metadata: Dict[str, Any] = None) -> str:
        """Опубликовать конфигурацию."""
        return self.data_manager.store_data(DataType.CONFIGURATION, config_data, metadata, self.name)
    
    def publish_visualization_data(self, viz_data: Any, metadata: Dict[str, Any] = None) -> str:
        """Опубликовать данные визуализации."""
        return self.data_manager.store_data(DataType.VISUALIZATION_DATA, viz_data, metadata, self.name)


class DataSubscriber(Observer):
    """Подписчик данных для DataContext."""
    
    def __init__(self, data_manager: DataManager, name: str = "DataSubscriber"):
        """Инициализация подписчика данных."""
        self.data_manager = data_manager
        self.name = name
        self._callbacks: Dict[DataType, List[Callable[[DataRecord], None]]] = {}
        
        # Подписываемся на менеджер данных
        self.data_manager.attach(self)
        
        logger.debug(f"DataSubscriber initialized: {name}")
    
    def subscribe_to_type(self, data_type: DataType, callback: Callable[[DataRecord], None]) -> None:
        """
        Подписаться на тип данных.
        
        Args:
            data_type: Тип данных
            callback: Callback функция
        """
        if data_type not in self._callbacks:
            self._callbacks[data_type] = []
        self._callbacks[data_type].append(callback)
        logger.debug(f"Subscribed to {data_type.value}")
    
    def unsubscribe_from_type(self, data_type: DataType, callback: Callable[[DataRecord], None]) -> None:
        """
        Отписаться от типа данных.
        
        Args:
            data_type: Тип данных
            callback: Callback функция
        """
        if data_type in self._callbacks and callback in self._callbacks[data_type]:
            self._callbacks[data_type].remove(callback)
            logger.debug(f"Unsubscribed from {data_type.value}")
    
    def update(self, event_type: DataEventType, data: Any) -> None:
        """Обновление подписчика."""
        if isinstance(data, DataRecord):
            callbacks = self._callbacks.get(data.data_type, [])
            for callback in callbacks:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Error in callback for {data.data_type.value}: {e}")
    
    def get_latest_data(self, data_type: DataType) -> Optional[DataRecord]:
        """Получить последние данные по типу."""
        return self.data_manager.get_latest_data(data_type)
    
    def get_all_data(self, data_type: DataType) -> List[DataRecord]:
        """Получить все данные по типу."""
        return self.data_manager.get_data_by_type(data_type)


class DataContext:
    """Центральный контекст данных для SignalAnalyzer."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Инициализация контекста данных."""
        if not self._initialized:
            self.data_manager = DataManager("SignalAnalyzer_DataManager")
            self.publisher = DataPublisher(self.data_manager, "SignalAnalyzer_Publisher")
            self.subscribers: Dict[str, DataSubscriber] = {}
            self._initialized = True
            logger.info("DataContext initialized")
    
    def create_subscriber(self, name: str) -> DataSubscriber:
        """
        Создать подписчика.
        
        Args:
            name: Имя подписчика
            
        Returns:
            Подписчик данных
        """
        subscriber = DataSubscriber(self.data_manager, name)
        self.subscribers[name] = subscriber
        return subscriber
    
    def get_subscriber(self, name: str) -> Optional[DataSubscriber]:
        """
        Получить подписчика по имени.
        
        Args:
            name: Имя подписчика
            
        Returns:
            Подписчик или None
        """
        return self.subscribers.get(name)
    
    def remove_subscriber(self, name: str) -> bool:
        """
        Удалить подписчика.
        
        Args:
            name: Имя подписчика
            
        Returns:
            True если подписчик удален
        """
        if name in self.subscribers:
            subscriber = self.subscribers[name]
            self.data_manager.detach(subscriber)
            del self.subscribers[name]
            logger.info(f"Subscriber removed: {name}")
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Получить статистику контекста данных.
        
        Returns:
            Словарь со статистикой
        """
        return {
            'data_manager': self.data_manager.get_stats(),
            'subscribers': {name: type(sub).__name__ for name, sub in self.subscribers.items()},
            'event_bus': event_bus.get_stats()
        }
    
    def export_all_data(self, filepath: str) -> bool:
        """Экспорт всех данных."""
        return self.data_manager.export_data(filepath)
    
    def import_data(self, filepath: str) -> int:
        """Импорт данных."""
        return self.data_manager.import_data(filepath)
    
    def clear_all_data(self) -> int:
        """Очистка всех данных."""
        return self.data_manager.clear_data()


# Глобальный экземпляр контекста данных
data_context = DataContext()

