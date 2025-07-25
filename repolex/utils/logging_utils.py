"""🟡 PAC-MAN Logging & Monitoring Powerhouse

The ultimate logging system with PAC-MAN-level intelligence and ghost-tracking capabilities!
PAC-MAN logs everything with perfect precision, structured data, and delightful themes!
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional, Callable, Union, List
from datetime import datetime
from contextlib import contextmanager
import traceback
import functools

try:
    from loguru import logger
    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False
    # Fallback to standard logging
    import logging
    logger = logging.getLogger(__name__)

from repolex.utils.path_utils import get_logs_directory, ensure_directory


class PAC_MAN_LogLevel:
    """🟡 PAC-MAN Log Levels with Ghost-Busting Power!"""
    TRACE = "TRACE"      # 🔍 Microscopic PAC-MAN movements
    DEBUG = "DEBUG"      # 🟡 PAC-MAN's internal thoughts  
    INFO = "INFO"        # 🟢 PAC-MAN's successful chomps
    SUCCESS = "SUCCESS"  # ✅ PAC-MAN's victories
    WARNING = "WARNING"  # 🟠 Ghost proximity warnings
    ERROR = "ERROR"      # 🔴 Ghost encounters
    CRITICAL = "CRITICAL" # 💀 Game over scenarios


class PAC_MAN_LogFormatter:
    """🟡 PAC-MAN's Log Formatting Powerhouse!"""
    
    @staticmethod
    def colorful_format() -> str:
        """PAC-MAN's colorful log format with emojis!"""
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    @staticmethod
    def json_format() -> str:
        """Structured JSON format for PAC-MAN's data analysis!"""
        return "{time} | {level} | {name}:{function}:{line} | {message}"
    
    @staticmethod
    def performance_format() -> str:
        """Performance-focused format for PAC-MAN's speed tracking!"""
        return (
            "<green>{time:HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<yellow>{elapsed}</yellow> | "
            "<level>{message}</level>"
        )


class PAC_MAN_Logger:
    """🟡 PAC-MAN's Ultimate Logging Powerhouse!"""
    
    def __init__(self, name: str = "Repolex", logs_dir: Optional[Path] = None):
        """
        Initialize PAC-MAN's logging system.
        
        Args:
            name: Logger name
            logs_dir: Directory for log files
        """
        self.name = name
        self.logs_dir = logs_dir or get_logs_directory()
        self.start_time = time.time()
        self.request_counter = 0
        self.error_counter = 0
        
        # Ensure logs directory exists
        ensure_directory(self.logs_dir)
        
        # Configure logger
        self._configure_logger()
    
    def _configure_logger(self) -> None:
        """Configure the PAC-MAN logging system."""
        if not LOGURU_AVAILABLE:
            self._configure_standard_logging()
            return
        
        # Remove default handler
        logger.remove()
        
        # Add console handler with PAC-MAN colors
        logger.add(
            sys.stderr,
            format=PAC_MAN_LogFormatter.colorful_format(),
            level="INFO",
            colorize=True,
            backtrace=True,
            diagnose=True
        )
        
        # Add file handler for all logs
        logger.add(
            self.logs_dir / "Repolex.log",
            format=PAC_MAN_LogFormatter.json_format(),
            level="DEBUG",
            rotation="10 MB",
            retention="30 days",
            compression="zip",
            serialize=False,
            backtrace=True,
            diagnose=True
        )
        
        # Add error-only file handler
        logger.add(
            self.logs_dir / "errors.log",
            format=PAC_MAN_LogFormatter.json_format(),
            level="ERROR",
            rotation="5 MB",
            retention="90 days",
            compression="zip",
            serialize=False,
            backtrace=True,
            diagnose=True
        )
        
        # Add performance log handler
        logger.add(
            self.logs_dir / "performance.log",
            format=PAC_MAN_LogFormatter.performance_format(),
            level="INFO",
            rotation="5 MB",
            retention="7 days",
            compression="zip",
            filter=lambda record: "PERF" in record["extra"]
        )
        
        # Add JSON structured logs for analysis
        logger.add(
            self.logs_dir / "structured.jsonl",
            format="{time} | {level} | {name}:{function}:{line} | {message}",
            level="INFO",
            rotation="20 MB",
            retention="60 days",
            compression="zip",
            serialize=True
        )
    
    def _configure_standard_logging(self) -> None:
        """Fallback configuration using standard logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s',
            handlers=[
                logging.StreamHandler(sys.stderr),
                logging.FileHandler(self.logs_dir / "Repolex.log"),
            ]
        )
    
    def pac_man_startup(self) -> None:
        """🟡 Log PAC-MAN's startup sequence!"""
        logger.info("🟡 PAC-MAN STARTING UP - Ready to chomp through code repositories!")
        logger.info(f"🏠 PAC-MAN Home: {self.logs_dir}")
        logger.info(f"⚡ Loguru Available: {LOGURU_AVAILABLE}")
        logger.info("🎮 PAC-MAN's semantic maze navigation system initialized!")
    
    def pac_man_shutdown(self) -> None:
        """🟡 Log PAC-MAN's shutdown sequence!"""
        uptime = time.time() - self.start_time
        logger.info(f"🟡 PAC-MAN SHUTTING DOWN after {uptime:.2f} seconds")
        logger.info(f"📊 Requests processed: {self.request_counter}")
        logger.info(f"❌ Errors encountered: {self.error_counter}")
        logger.info("👻 All ghosts successfully avoided! See you next time!")
    
    def log_repository_operation(self, operation: str, org: str, repo: str, 
                               version: Optional[str] = None, **kwargs) -> None:
        """🟡 Log repository operations with structured data."""
        extra_data = {
            "operation": operation,
            "org": org, 
            "repo": repo,
            "version": version,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        }
        
        if LOGURU_AVAILABLE:
            logger.bind(**extra_data).info(
                f"🟡 {operation.upper()}: {org}/{repo}" + 
                (f"@{version}" if version else "")
            )
        else:
            logger.info(f"🟡 {operation.upper()}: {org}/{repo}" + 
                       (f"@{version}" if version else ""))
    
    def log_graph_operation(self, operation: str, graph_count: int, 
                           duration: float, **kwargs) -> None:
        """🟡 Log graph operations with performance metrics."""
        extra_data = {
            "operation": operation,
            "graph_count": graph_count,
            "duration_seconds": duration,
            "graphs_per_second": graph_count / duration if duration > 0 else 0,
            "PERF": True,
            **kwargs
        }
        
        if LOGURU_AVAILABLE:
            logger.bind(**extra_data).info(
                f"📊 {operation.upper()}: {graph_count} graphs in {duration:.2f}s "
                f"({graph_count/duration:.1f} graphs/sec)"
            )
        else:
            logger.info(f"📊 {operation.upper()}: {graph_count} graphs in {duration:.2f}s")
    
    def log_export_operation(self, format: str, org: str, repo: str, 
                           version: str, file_size: int, duration: float) -> None:
        """🟡 Log export operations with file metrics."""
        file_size_mb = file_size / (1024 * 1024)
        
        extra_data = {
            "operation": "export",
            "format": format,
            "org": org,
            "repo": repo, 
            "version": version,
            "file_size_bytes": file_size,
            "file_size_mb": file_size_mb,
            "duration_seconds": duration,
            "mb_per_second": file_size_mb / duration if duration > 0 else 0
        }
        
        if LOGURU_AVAILABLE:
            logger.bind(**extra_data).success(
                f"📦 EXPORT {format.upper()}: {org}/{repo}@{version} "
                f"({file_size_mb:.1f}MB in {duration:.2f}s)"
            )
        else:
            logger.info(f"📦 EXPORT {format.upper()}: {org}/{repo}@{version}")
    
    def log_query_operation(self, query_type: str, query: str, 
                           result_count: int, duration: float) -> None:
        """🟡 Log query operations with performance data."""
        extra_data = {
            "operation": "query",
            "query_type": query_type,
            "query_length": len(query),
            "result_count": result_count,
            "duration_seconds": duration,
            "results_per_second": result_count / duration if duration > 0 else 0,
            "PERF": True
        }
        
        if LOGURU_AVAILABLE:
            logger.bind(**extra_data).info(
                f"🔍 QUERY {query_type.upper()}: {result_count} results in {duration:.3f}s"
            )
        else:
            logger.info(f"🔍 QUERY {query_type.upper()}: {result_count} results")
    
    def log_error_with_context(self, error: Exception, context: Dict[str, Any]) -> None:
        """🟡 Log errors with full context and ghost-busting suggestions."""
        self.error_counter += 1
        
        error_data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "traceback": traceback.format_exc(),
            "error_count": self.error_counter
        }
        
        if LOGURU_AVAILABLE:
            logger.bind(**error_data).error(
                f"👻 GHOST ENCOUNTER: {type(error).__name__} - {error}"
            )
        else:
            logger.error(f"👻 GHOST ENCOUNTER: {type(error).__name__} - {error}")
    
    def log_performance_metric(self, metric_name: str, value: float, 
                             unit: str = "seconds", **kwargs) -> None:
        """🟡 Log performance metrics for PAC-MAN optimization."""
        extra_data = {
            "metric_name": metric_name,
            "metric_value": value,
            "metric_unit": unit,
            "PERF": True,
            **kwargs
        }
        
        if LOGURU_AVAILABLE:
            logger.bind(**extra_data).info(
                f"⚡ PERFORMANCE: {metric_name} = {value:.3f} {unit}"
            )
        else:
            logger.info(f"⚡ PERFORMANCE: {metric_name} = {value:.3f} {unit}")


# Global PAC-MAN logger instance
_pac_man_logger: Optional[PAC_MAN_Logger] = None


def get_pac_man_logger() -> PAC_MAN_Logger:
    """🟡 Get the global PAC-MAN logger instance."""
    global _pac_man_logger
    if _pac_man_logger is None:
        _pac_man_logger = PAC_MAN_Logger()
    return _pac_man_logger


def setup_logging(logs_dir: Optional[Path] = None, level: str = "INFO") -> PAC_MAN_Logger:
    """🟡 Setup PAC-MAN's logging system."""
    global _pac_man_logger
    _pac_man_logger = PAC_MAN_Logger(logs_dir=logs_dir)
    _pac_man_logger.pac_man_startup()
    return _pac_man_logger


def shutdown_logging() -> None:
    """🟡 Shutdown PAC-MAN's logging system."""
    global _pac_man_logger
    if _pac_man_logger:
        _pac_man_logger.pac_man_shutdown()


@contextmanager
def log_operation(operation_name: str, **context):
    """🟡 Context manager for logging operations with timing."""
    pac_logger = get_pac_man_logger()
    start_time = time.time()
    
    try:
        logger.info(f"🟡 STARTING: {operation_name}")
        yield
        duration = time.time() - start_time
        logger.success(f"✅ COMPLETED: {operation_name} in {duration:.3f}s")
        pac_logger.log_performance_metric(f"{operation_name}_duration", duration)
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(f"👻 FAILED: {operation_name} after {duration:.3f}s")
        pac_logger.log_error_with_context(e, {"operation": operation_name, **context})
        raise


def log_function_performance(func: Callable) -> Callable:
    """🟡 Decorator to log function performance."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function_name = f"{func.__module__}.{func.__name__}"
        
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            if LOGURU_AVAILABLE:
                logger.bind(
                    function=function_name,
                    duration=duration,
                    PERF=True
                ).debug(f"⚡ {function_name} completed in {duration:.3f}s")
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            pac_logger = get_pac_man_logger()
            pac_logger.log_error_with_context(e, {
                "function": function_name,
                "duration": duration,
                "args_count": len(args),
                "kwargs_keys": list(kwargs.keys())
            })
            raise
    
    return wrapper


def log_memory_usage(operation: str) -> None:
    """🟡 Log current memory usage for PAC-MAN optimization."""
    try:
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        
        logger.info(
            f"🧠 MEMORY: {operation} - "
            f"RSS: {memory_info.rss / 1024 / 1024:.1f}MB, "
            f"VMS: {memory_info.vms / 1024 / 1024:.1f}MB"
        )
    except ImportError:
        logger.debug("psutil not available for memory monitoring")


def log_system_info() -> None:
    """🟡 Log system information for PAC-MAN diagnostics."""
    import platform
    
    info = {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "architecture": platform.architecture()[0],
        "processor": platform.processor() or "unknown",
        "hostname": platform.node(),
        "loguru_available": LOGURU_AVAILABLE
    }
    
    if LOGURU_AVAILABLE:
        logger.bind(**info).info("🖥️  SYSTEM INFO: PAC-MAN environment detected")
    else:
        logger.info(f"🖥️  SYSTEM INFO: {info}")


def create_audit_log(operation: str, user: str, resource: str, 
                    action: str, success: bool, **metadata) -> None:
    """🟡 Create audit log entry for security tracking."""
    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "user": user,
        "resource": resource,
        "action": action,
        "success": success,
        "metadata": metadata
    }
    
    # Write to separate audit log file
    audit_file = get_logs_directory() / "audit.jsonl"
    ensure_directory(audit_file.parent)
    
    with open(audit_file, 'a') as f:
        f.write(json.dumps(audit_entry) + '\n')
    
    if LOGURU_AVAILABLE:
        logger.bind(**audit_entry).info(
            f"🔐 AUDIT: {user} {action} {resource} - {'SUCCESS' if success else 'FAILED'}"
        )


# PAC-MAN convenience logging functions
def pac_log_info(message: str, **kwargs) -> None:
    """🟡 PAC-MAN info log with context."""
    if LOGURU_AVAILABLE:
        logger.bind(**kwargs).info(f"🟡 {message}")
    else:
        logger.info(f"🟡 {message}")


def pac_log_success(message: str, **kwargs) -> None:
    """🟡 PAC-MAN success log with celebration."""
    if LOGURU_AVAILABLE:
        logger.bind(**kwargs).success(f"✅ {message}")
    else:
        logger.info(f"✅ {message}")


def pac_log_warning(message: str, **kwargs) -> None:
    """🟡 PAC-MAN warning log with ghost alert."""
    if LOGURU_AVAILABLE:
        logger.bind(**kwargs).warning(f"🟠 GHOST DETECTED: {message}")
    else:
        logger.warning(f"🟠 GHOST DETECTED: {message}")


def pac_log_error(message: str, **kwargs) -> None:
    """🟡 PAC-MAN error log with ghost encounter."""
    if LOGURU_AVAILABLE:
        logger.bind(**kwargs).error(f"👻 GHOST ENCOUNTER: {message}")
    else:
        logger.error(f"👻 GHOST ENCOUNTER: {message}")


def pac_log_debug(message: str, **kwargs) -> None:
    """🟡 PAC-MAN debug log with internal thoughts."""
    if LOGURU_AVAILABLE:
        logger.bind(**kwargs).debug(f"🔍 {message}")
    else:
        logger.debug(f"🔍 {message}")


# Initialize logging on import
if not _pac_man_logger:
    setup_logging()