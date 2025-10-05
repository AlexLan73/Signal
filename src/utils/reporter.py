"""Система отчетов для SignalAnalyzer."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class ReportType(Enum):
    """Типы отчетов."""
    STROBE_GENERATION = "strobe_generation"
    SIGNAL_ANALYSIS = "signal_analysis"
    GUI_TEST = "gui_test"
    PERFORMANCE = "performance"
    VALIDATION = "validation"
    ERROR = "error"
    GENERAL = "general"


class ReportFormat(Enum):
    """Форматы отчетов."""
    JSON = "json"
    HTML = "html"
    TXT = "txt"
    PDF = "pdf"


@dataclass
class ReportMetadata:
    """Метаданные отчета."""
    report_id: str
    report_type: ReportType
    title: str
    author: str
    created_at: datetime
    version: str = "1.0"
    tags: List[str] = None
    description: str = ""
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class ReportContent:
    """Содержимое отчета."""
    metadata: ReportMetadata
    data: Dict[str, Any]
    summary: str
    details: str
    recommendations: List[str] = None
    attachments: List[str] = None
    
    def __post_init__(self):
        if self.recommendations is None:
            self.recommendations = []
        if self.attachments is None:
            self.attachments = []


class ReportGenerator:
    """Генератор отчетов."""
    
    def __init__(self, project_root: Path = None):
        """Инициализация генератора отчетов."""
        self.project_root = project_root or Path.cwd()
        self.reports_dir = self.project_root / "reports"
        self._ensure_directories()
        logger.info("ReportGenerator initialized")
    
    def _ensure_directories(self):
        """Создание необходимых директорий."""
        # Создаем базовые директории
        self.reports_dir.mkdir(exist_ok=True)
        
        # Создаем директории по датам (текущий год/месяц/день)
        now = datetime.now()
        date_dir = self.reports_dir / str(now.year) / f"{now.month:02d}" / f"{now.day:02d}"
        date_dir.mkdir(parents=True, exist_ok=True)
        
        # Создаем функциональные директории
        functional_dirs = [
            "strobe_analysis",
            "signal_generation", 
            "gui_tests",
            "performance",
            "validation",
            "error_reports"
        ]
        
        for func_dir in functional_dirs:
            (self.reports_dir / func_dir).mkdir(exist_ok=True)
    
    def _get_report_filename(self, report_type: ReportType, format_type: ReportFormat, 
                           timestamp: datetime = None) -> str:
        """Генерация имени файла отчета."""
        if timestamp is None:
            timestamp = datetime.now()
        
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        return f"{report_type.value}_{timestamp_str}.{format_type.value}"
    
    def _get_report_path(self, report_type: ReportType, format_type: ReportFormat,
                        use_date_dir: bool = True, custom_dir: str = None) -> Path:
        """Получение пути для сохранения отчета."""
        filename = self._get_report_filename(report_type, format_type)
        
        if custom_dir:
            return self.reports_dir / custom_dir / filename
        elif use_date_dir:
            now = datetime.now()
            date_dir = self.reports_dir / str(now.year) / f"{now.month:02d}" / f"{now.day:02d}"
            return date_dir / filename
        else:
            # Функциональная директория
            func_dir = self._get_functional_directory(report_type)
            return self.reports_dir / func_dir / filename
    
    def _get_functional_directory(self, report_type: ReportType) -> str:
        """Получение функциональной директории для типа отчета."""
        mapping = {
            ReportType.STROBE_GENERATION: "strobe_analysis",
            ReportType.SIGNAL_ANALYSIS: "signal_generation",
            ReportType.GUI_TEST: "gui_tests",
            ReportType.PERFORMANCE: "performance",
            ReportType.VALIDATION: "validation",
            ReportType.ERROR: "error_reports",
            ReportType.GENERAL: "general"
        }
        return mapping.get(report_type, "general")
    
    def generate_json_report(self, content: ReportContent, custom_dir: str = None) -> Path:
        """Генерация JSON отчета."""
        try:
            report_path = self._get_report_path(
                content.metadata.report_type, 
                ReportFormat.JSON,
                custom_dir=custom_dir
            )
            
            # Подготавливаем данные для JSON
            report_data = {
                'metadata': asdict(content.metadata),
                'data': content.data,
                'summary': content.summary,
                'details': content.details,
                'recommendations': content.recommendations,
                'attachments': content.attachments,
                'generated_at': datetime.now().isoformat()
            }
            
            # Сохраняем JSON
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"JSON report generated: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Error generating JSON report: {e}")
            raise
    
    def generate_html_report(self, content: ReportContent, custom_dir: str = None) -> Path:
        """Генерация HTML отчета."""
        try:
            report_path = self._get_report_path(
                content.metadata.report_type,
                ReportFormat.HTML,
                custom_dir=custom_dir
            )
            
            # Генерируем HTML содержимое
            html_content = self._generate_html_content(content)
            
            # Сохраняем HTML
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML report generated: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Error generating HTML report: {e}")
            raise
    
    def _generate_html_content(self, content: ReportContent) -> str:
        """Генерация HTML содержимого."""
        metadata = content.metadata
        
        html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{metadata.title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 2px solid #2196F3;
            padding-bottom: 20px;
            margin-bottom: 20px;
        }}
        .header h1 {{
            color: #2196F3;
            margin: 0;
        }}
        .metadata {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .metadata table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .metadata td {{
            padding: 5px 10px;
            border-bottom: 1px solid #ddd;
        }}
        .metadata td:first-child {{
            font-weight: bold;
            width: 200px;
        }}
        .section {{
            margin-bottom: 25px;
        }}
        .section h2 {{
            color: #333;
            border-left: 4px solid #2196F3;
            padding-left: 10px;
        }}
        .summary {{
            background-color: #e8f5e8;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #4CAF50;
        }}
        .details {{
            background-color: #fff3e0;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #FF9800;
        }}
        .recommendations {{
            background-color: #f3e5f5;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #9C27B0;
        }}
        .recommendations ul {{
            margin: 0;
            padding-left: 20px;
        }}
        .data-section {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #607D8B;
        }}
        .data-section pre {{
            background-color: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 12px;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{metadata.title}</h1>
        </div>
        
        <div class="metadata">
            <table>
                <tr><td>ID отчета:</td><td>{metadata.report_id}</td></tr>
                <tr><td>Тип отчета:</td><td>{metadata.report_type.value}</td></tr>
                <tr><td>Автор:</td><td>{metadata.author}</td></tr>
                <tr><td>Создан:</td><td>{metadata.created_at.strftime('%d.%m.%Y %H:%M:%S')}</td></tr>
                <tr><td>Версия:</td><td>{metadata.version}</td></tr>
                <tr><td>Теги:</td><td>{', '.join(metadata.tags) if metadata.tags else 'Нет'}</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>Краткое резюме</h2>
            <div class="summary">
                {content.summary}
            </div>
        </div>
        
        <div class="section">
            <h2>Детали</h2>
            <div class="details">
                {content.details}
            </div>
        </div>
        
        {f'''
        <div class="section">
            <h2>Данные</h2>
            <div class="data-section">
                <pre>{json.dumps(content.data, indent=2, ensure_ascii=False, default=str)}</pre>
            </div>
        </div>
        ''' if content.data else ''}
        
        {f'''
        <div class="section">
            <h2>Рекомендации</h2>
            <div class="recommendations">
                <ul>
                    {''.join(f'<li>{rec}</li>' for rec in content.recommendations)}
                </ul>
            </div>
        </div>
        ''' if content.recommendations else ''}
        
        {f'''
        <div class="section">
            <h2>Вложения</h2>
            <div class="details">
                <ul>
                    {''.join(f'<li>{att}</li>' for att in content.attachments)}
                </ul>
            </div>
        </div>
        ''' if content.attachments else ''}
        
        <div class="footer">
            <p>Отчет сгенерирован автоматически системой SignalAnalyzer</p>
            <p>Время генерации: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def generate_txt_report(self, content: ReportContent, custom_dir: str = None) -> Path:
        """Генерация текстового отчета."""
        try:
            report_path = self._get_report_path(
                content.metadata.report_type,
                ReportFormat.TXT,
                custom_dir=custom_dir
            )
            
            # Генерируем текстовое содержимое
            txt_content = self._generate_txt_content(content)
            
            # Сохраняем текстовый файл
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(txt_content)
            
            logger.info(f"Text report generated: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Error generating text report: {e}")
            raise
    
    def _generate_txt_content(self, content: ReportContent) -> str:
        """Генерация текстового содержимого."""
        metadata = content.metadata
        
        txt = f"""
{'='*80}
{metadata.title}
{'='*80}

МЕТАДАННЫЕ:
-----------
ID отчета: {metadata.report_id}
Тип отчета: {metadata.report_type.value}
Автор: {metadata.author}
Создан: {metadata.created_at.strftime('%d.%m.%Y %H:%M:%S')}
Версия: {metadata.version}
Теги: {', '.join(metadata.tags) if metadata.tags else 'Нет'}

{'='*80}
КРАТКОЕ РЕЗЮМЕ
{'='*80}

{content.summary}

{'='*80}
ДЕТАЛИ
{'='*80}

{content.details}

{'='*80}
ДАННЫЕ
{'='*80}

{json.dumps(content.data, indent=2, ensure_ascii=False, default=str) if content.data else 'Нет данных'}

{'='*80}
РЕКОМЕНДАЦИИ
{'='*80}

{chr(10).join(f'• {rec}' for rec in content.recommendations) if content.recommendations else 'Нет рекомендаций'}

{'='*80}
ВЛОЖЕНИЯ
{'='*80}

{chr(10).join(f'• {att}' for att in content.attachments) if content.attachments else 'Нет вложений'}

{'='*80}
СИСТЕМНАЯ ИНФОРМАЦИЯ
{'='*80}

Отчет сгенерирован автоматически системой SignalAnalyzer
Время генерации: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
        """
        
        return txt
    
    def create_report(self, report_type: ReportType, title: str, data: Dict[str, Any],
                     summary: str, details: str = "", author: str = "System",
                     recommendations: List[str] = None, tags: List[str] = None,
                     formats: List[ReportFormat] = None, custom_dir: str = None) -> List[Path]:
        """
        Создание отчета в указанных форматах.
        
        Args:
            report_type: Тип отчета
            title: Заголовок отчета
            data: Данные отчета
            summary: Краткое резюме
            details: Детали (опционально)
            author: Автор отчета
            recommendations: Рекомендации (опционально)
            tags: Теги (опционально)
            formats: Форматы для генерации (по умолчанию JSON)
            custom_dir: Пользовательская директория
            
        Returns:
            Список путей к созданным отчетам
        """
        if formats is None:
            formats = [ReportFormat.JSON]
        
        if recommendations is None:
            recommendations = []
        
        if tags is None:
            tags = []
        
        # Создаем метаданные
        metadata = ReportMetadata(
            report_id=f"RPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            report_type=report_type,
            title=title,
            author=author,
            created_at=datetime.now(),
            tags=tags,
            description=summary
        )
        
        # Создаем содержимое отчета
        content = ReportContent(
            metadata=metadata,
            data=data,
            summary=summary,
            details=details,
            recommendations=recommendations
        )
        
        # Генерируем отчеты в указанных форматах
        generated_reports = []
        
        for format_type in formats:
            try:
                if format_type == ReportFormat.JSON:
                    report_path = self.generate_json_report(content, custom_dir)
                elif format_type == ReportFormat.HTML:
                    report_path = self.generate_html_report(content, custom_dir)
                elif format_type == ReportFormat.TXT:
                    report_path = self.generate_txt_report(content, custom_dir)
                else:
                    logger.warning(f"Unsupported format: {format_type}")
                    continue
                
                generated_reports.append(report_path)
                
            except Exception as e:
                logger.error(f"Error generating {format_type.value} report: {e}")
        
        logger.info(f"Generated {len(generated_reports)} reports for {report_type.value}")
        return generated_reports
    
    def list_reports(self, report_type: ReportType = None, 
                    date_from: datetime = None, date_to: datetime = None) -> List[Path]:
        """
        Получение списка отчетов.
        
        Args:
            report_type: Фильтр по типу отчета
            date_from: Начальная дата
            date_to: Конечная дата
            
        Returns:
            Список путей к отчетам
        """
        reports = []
        
        # Сканируем все директории отчетов
        for report_path in self.reports_dir.rglob("*"):
            if report_path.is_file() and report_path.suffix in ['.json', '.html', '.txt']:
                # Проверяем фильтры
                if report_type and report_type.value not in report_path.name:
                    continue
                
                if date_from or date_to:
                    file_time = datetime.fromtimestamp(report_path.stat().st_mtime)
                    if date_from and file_time < date_from:
                        continue
                    if date_to and file_time > date_to:
                        continue
                
                reports.append(report_path)
        
        return sorted(reports, key=lambda x: x.stat().st_mtime, reverse=True)
    
    def get_report_stats(self) -> Dict[str, Any]:
        """Получение статистики отчетов."""
        all_reports = self.list_reports()
        
        stats = {
            'total_reports': len(all_reports),
            'by_format': {},
            'by_type': {},
            'by_date': {},
            'total_size': 0
        }
        
        for report_path in all_reports:
            # По формату
            format_type = report_path.suffix[1:]
            stats['by_format'][format_type] = stats['by_format'].get(format_type, 0) + 1
            
            # По типу
            for report_type in ReportType:
                if report_type.value in report_path.name:
                    stats['by_type'][report_type.value] = stats['by_type'].get(report_type.value, 0) + 1
                    break
            
            # По дате
            file_date = datetime.fromtimestamp(report_path.stat().st_mtime).date()
            date_str = file_date.isoformat()
            stats['by_date'][date_str] = stats['by_date'].get(date_str, 0) + 1
            
            # Общий размер
            stats['total_size'] += report_path.stat().st_size
        
        return stats


# Глобальный экземпляр генератора отчетов
report_generator = ReportGenerator()

