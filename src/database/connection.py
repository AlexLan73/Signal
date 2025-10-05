"""Database connection management for SignalAnalyzer application."""

import os
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool, StaticPool
from sqlalchemy.exc import SQLAlchemyError
import logging

from .models import Base, DatabaseConnection

logger = logging.getLogger(__name__)


class DatabaseConnectionManager:
    """Manages database connections for SignalAnalyzer application."""
    
    def __init__(self, database_type: str = "sqlite", **connection_params):
        """
        Initialize database connection manager.
        
        Args:
            database_type: Type of database ('sqlite' or 'postgresql')
            **connection_params: Database connection parameters
        """
        self.database_type = database_type.lower()
        self.connection_params = connection_params
        self.engine: Optional[Engine] = None
        self.session_factory: Optional[sessionmaker] = None
        self._connection_pool = {}
        self._max_pool_size = connection_params.get('pool_size', 5)
        
        logger.info(f"Initializing database connection manager for {self.database_type}")
    
    def initialize(self) -> bool:
        """
        Initialize database connection.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            if self.database_type == "sqlite":
                success = self._initialize_sqlite()
            elif self.database_type == "postgresql":
                success = self._initialize_postgresql()
            else:
                logger.error(f"Unsupported database type: {self.database_type}")
                return False
            
            if success:
                self._create_session_factory()
                self._create_tables()
                logger.info("Database connection initialized successfully")
            else:
                logger.error("Failed to initialize database connection")
            
            return success
            
        except Exception as e:
            logger.error(f"Error initializing database connection: {e}")
            return False
    
    def _initialize_sqlite(self) -> bool:
        """Initialize SQLite database connection."""
        try:
            database_path = self.connection_params.get('database_path', ':memory:')
            
            # Create directory if it doesn't exist
            if database_path != ':memory:' and not os.path.exists(os.path.dirname(database_path)):
                os.makedirs(os.path.dirname(database_path), exist_ok=True)
            
            # Create SQLite engine
            self.engine = create_engine(
                f"sqlite:///{database_path}",
                poolclass=StaticPool,
                connect_args={
                    "check_same_thread": False,
                    "timeout": 30
                },
                echo=self.connection_params.get('echo', False)
            )
            
            logger.info(f"SQLite database initialized: {database_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing SQLite database: {e}")
            return False
    
    def _initialize_postgresql(self) -> bool:
        """Initialize PostgreSQL database connection."""
        try:
            # Extract connection parameters
            host = self.connection_params.get('host', 'localhost')
            port = self.connection_params.get('port', 5432)
            database = self.connection_params.get('database', 'signal_analyzer')
            username = self.connection_params.get('username', 'postgres')
            password = self.connection_params.get('password', '')
            
            # Build connection string
            connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
            
            # Create PostgreSQL engine
            self.engine = create_engine(
                connection_string,
                poolclass=QueuePool,
                pool_size=self._max_pool_size,
                max_overflow=10,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=self.connection_params.get('echo', False)
            )
            
            logger.info(f"PostgreSQL database initialized: {host}:{port}/{database}")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing PostgreSQL database: {e}")
            return False
    
    def _create_session_factory(self):
        """Create session factory for database operations."""
        if self.engine is None:
            raise RuntimeError("Database engine not initialized")
        
        self.session_factory = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False
        )
    
    def _create_tables(self):
        """Create database tables."""
        if self.engine is None:
            raise RuntimeError("Database engine not initialized")
        
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise
    
    def is_connected(self) -> bool:
        """
        Check if database connection is active.
        
        Returns:
            bool: True if connected, False otherwise
        """
        if self.engine is None:
            return False
        
        try:
            with self.engine.connect() as connection:
                connection.execute("SELECT 1")
            return True
        except SQLAlchemyError as e:
            logger.warning(f"Database connection check failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from database."""
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None
            self.session_factory = None
            logger.info("Database connection closed")
    
    def reconnect(self) -> bool:
        """
        Reconnect to database.
        
        Returns:
            bool: True if reconnection successful, False otherwise
        """
        logger.info("Attempting to reconnect to database")
        self.disconnect()
        return self.initialize()
    
    @contextmanager
    def get_session(self) -> Session:
        """
        Get database session context manager.
        
        Yields:
            Session: SQLAlchemy session
        """
        if self.session_factory is None:
            raise RuntimeError("Session factory not initialized")
        
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def get_connection(self) -> Session:
        """
        Get database connection from pool.
        
        Returns:
            Session: SQLAlchemy session
        """
        if self.session_factory is None:
            raise RuntimeError("Session factory not initialized")
        
        return self.session_factory()
    
    def return_connection(self, session: Session):
        """
        Return database connection to pool.
        
        Args:
            session: SQLAlchemy session to return
        """
        try:
            session.close()
        except Exception as e:
            logger.warning(f"Error closing session: {e}")
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test database connection and return status information.
        
        Returns:
            Dict[str, Any]: Connection status information
        """
        result = {
            "connected": False,
            "database_type": self.database_type,
            "error": None,
            "connection_info": {}
        }
        
        try:
            if self.engine is None:
                result["error"] = "Engine not initialized"
                return result
            
            with self.engine.connect() as connection:
                # Test basic connectivity
                connection.execute("SELECT 1")
                result["connected"] = True
                
                # Get connection information
                if self.database_type == "sqlite":
                    result["connection_info"] = {
                        "database_path": self.connection_params.get('database_path', ':memory:'),
                        "sqlite_version": connection.execute("SELECT sqlite_version()").scalar()
                    }
                elif self.database_type == "postgresql":
                    result["connection_info"] = {
                        "host": self.connection_params.get('host', 'localhost'),
                        "port": self.connection_params.get('port', 5432),
                        "database": self.connection_params.get('database', 'signal_analyzer'),
                        "postgresql_version": connection.execute("SELECT version()").scalar()
                    }
                
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Database connection test failed: {e}")
        
        return result
    
    def get_memory_info(self) -> Dict[str, int]:
        """
        Get database memory information.
        
        Returns:
            Dict[str, int]: Memory information
        """
        if self.engine is None:
            return {"total": 0, "free": 0, "used": 0}
        
        try:
            with self.engine.connect() as connection:
                if self.database_type == "sqlite":
                    # SQLite doesn't have built-in memory info, return estimates
                    return {
                        "total": 1000000000,  # 1GB estimate
                        "free": 800000000,    # 800MB estimate
                        "used": 200000000     # 200MB estimate
                    }
                elif self.database_type == "postgresql":
                    # Get PostgreSQL memory information
                    result = connection.execute("""
                        SELECT 
                            setting::bigint as total_memory,
                            (SELECT setting::bigint FROM pg_settings WHERE name = 'shared_buffers') as shared_buffers
                        FROM pg_settings 
                        WHERE name = 'total_memory'
                    """).fetchone()
                    
                    if result:
                        total = result[0] if result[0] else 1000000000
                        shared = result[1] if result[1] else 100000000
                        return {
                            "total": total,
                            "free": total - shared,
                            "used": shared
                        }
                    
        except Exception as e:
            logger.warning(f"Could not get memory info: {e}")
        
        return {"total": 0, "free": 0, "used": 0}
    
    def backup_database(self, backup_path: str) -> bool:
        """
        Backup database to specified path.
        
        Args:
            backup_path: Path to save backup
            
        Returns:
            bool: True if backup successful, False otherwise
        """
        try:
            if self.database_type == "sqlite":
                return self._backup_sqlite(backup_path)
            elif self.database_type == "postgresql":
                return self._backup_postgresql(backup_path)
            else:
                logger.error(f"Backup not supported for database type: {self.database_type}")
                return False
                
        except Exception as e:
            logger.error(f"Error backing up database: {e}")
            return False
    
    def _backup_sqlite(self, backup_path: str) -> bool:
        """Backup SQLite database."""
        try:
            database_path = self.connection_params.get('database_path', ':memory:')
            if database_path == ':memory:':
                logger.error("Cannot backup in-memory database")
                return False
            
            import shutil
            shutil.copy2(database_path, backup_path)
            logger.info(f"SQLite database backed up to: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error backing up SQLite database: {e}")
            return False
    
    def _backup_postgresql(self, backup_path: str) -> bool:
        """Backup PostgreSQL database."""
        try:
            # This would require pg_dump utility
            # For now, return False as it's not implemented
            logger.warning("PostgreSQL backup not implemented")
            return False
            
        except Exception as e:
            logger.error(f"Error backing up PostgreSQL database: {e}")
            return False
    
    def restore_database(self, backup_path: str) -> bool:
        """
        Restore database from backup.
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            bool: True if restore successful, False otherwise
        """
        try:
            if self.database_type == "sqlite":
                return self._restore_sqlite(backup_path)
            elif self.database_type == "postgresql":
                return self._restore_postgresql(backup_path)
            else:
                logger.error(f"Restore not supported for database type: {self.database_type}")
                return False
                
        except Exception as e:
            logger.error(f"Error restoring database: {e}")
            return False
    
    def _restore_sqlite(self, backup_path: str) -> bool:
        """Restore SQLite database from backup."""
        try:
            if not os.path.exists(backup_path):
                logger.error(f"Backup file not found: {backup_path}")
                return False
            
            database_path = self.connection_params.get('database_path', ':memory:')
            if database_path == ':memory:':
                logger.error("Cannot restore to in-memory database")
                return False
            
            import shutil
            shutil.copy2(backup_path, database_path)
            logger.info(f"SQLite database restored from: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring SQLite database: {e}")
            return False
    
    def _restore_postgresql(self, backup_path: str) -> bool:
        """Restore PostgreSQL database from backup."""
        try:
            # This would require pg_restore utility
            # For now, return False as it's not implemented
            logger.warning("PostgreSQL restore not implemented")
            return False
            
        except Exception as e:
            logger.error(f"Error restoring PostgreSQL database: {e}")
            return False


class DatabaseConnectionFactory:
    """Factory for creating database connections."""
    
    @staticmethod
    def create_connection(database_type: str, **connection_params) -> DatabaseConnectionManager:
        """
        Create database connection manager.
        
        Args:
            database_type: Type of database ('sqlite' or 'postgresql')
            **connection_params: Database connection parameters
            
        Returns:
            DatabaseConnectionManager: Database connection manager
        """
        return DatabaseConnectionManager(database_type, **connection_params)
    
    @staticmethod
    def create_sqlite_connection(database_path: str = "signal_analyzer.db", **kwargs) -> DatabaseConnectionManager:
        """
        Create SQLite database connection.
        
        Args:
            database_path: Path to SQLite database file
            **kwargs: Additional connection parameters
            
        Returns:
            DatabaseConnectionManager: SQLite connection manager
        """
        params = {"database_path": database_path, **kwargs}
        return DatabaseConnectionManager("sqlite", **params)
    
    @staticmethod
    def create_postgresql_connection(
        host: str = "localhost",
        port: int = 5432,
        database: str = "signal_analyzer",
        username: str = "postgres",
        password: str = "",
        **kwargs
    ) -> DatabaseConnectionManager:
        """
        Create PostgreSQL database connection.
        
        Args:
            host: Database host
            port: Database port
            database: Database name
            username: Database username
            password: Database password
            **kwargs: Additional connection parameters
            
        Returns:
            DatabaseConnectionManager: PostgreSQL connection manager
        """
        params = {
            "host": host,
            "port": port,
            "database": database,
            "username": username,
            "password": password,
            **kwargs
        }
        return DatabaseConnectionManager("postgresql", **params)
