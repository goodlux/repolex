"""
📊 PAC-MAN's System Status Monitor 📊

The ultimate system monitoring dashboard for Repolex's semantic intelligence!
Monitor PAC-MAN's health, performance, and arcade cabinet diagnostics!

WAKA WAKA! Keeping the semantic arcade running smoothly!
"""

import logging
import platform
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

import psutil
from pydantic import BaseModel, Field

from .config_manager import get_config, get_setting

logger = logging.getLogger(__name__)


class SystemStatus(str, Enum):
    """🟡 PAC-MAN's system health status"""
    EXCELLENT = "excellent"     # 🟢 Perfect health - WAKA WAKA!
    GOOD = "good"              # 🟡 Running well
    WARNING = "warning"        # 🟠 Some issues detected
    CRITICAL = "critical"      # 🔴 Major problems
    ERROR = "error"           # 💥 System errors


class ComponentStatus(str, Enum):
    """🔧 Individual component status"""
    ONLINE = "online"          # ✅ Working perfectly
    DEGRADED = "degraded"     # ⚠️ Working but with issues
    OFFLINE = "offline"       # ❌ Not working
    UNKNOWN = "unknown"       # ❓ Status unclear
    MAINTENANCE = "maintenance" # 🔧 Under maintenance


@dataclass
class SystemMetrics:
    """📊 PAC-MAN's system performance metrics"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_available_mb: float
    disk_usage_percent: float
    disk_free_gb: float
    active_connections: int
    uptime_seconds: float
    
    def to_dict(self) -> Dict[str, Any]:
        """📊 Convert to dictionary"""
        return asdict(self)


@dataclass 
class ComponentHealth:
    """🔧 Individual component health status"""
    name: str
    status: ComponentStatus
    health_score: float  # 0.0 to 1.0
    last_check: str
    details: Dict[str, Any]
    errors: List[str]
    warnings: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """🔧 Convert to dictionary"""
        return asdict(self)


class SystemMonitor:
    """📊 PAC-MAN's System Status Monitor - The Arcade Cabinet Health Checker!"""
    
    def __init__(self):
        """📊 Initialize PAC-MAN's system monitor"""
        self.start_time = time.time()
        self.metrics_history: List[SystemMetrics] = []
        self.component_health: Dict[str, ComponentHealth] = {}
        self.alerts: List[Dict[str, Any]] = []
        self.max_history_size = get_setting('system.max_history_items', 1000)
        
        logger.info("🟡 PAC-MAN System Monitor initialized - arcade diagnostics online!")
    
    def get_system_info(self) -> Dict[str, Any]:
        """📊 Get basic PAC-MAN system information"""
        try:
            return {
                "platform": platform.platform(),
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "hostname": platform.node(),
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                "Repolex_version": "2.0.0",
                "pac_man_mode": "🟡 ACTIVATED",
                "waka_waka_level": "MAXIMUM"
            }
        except Exception as e:
            logger.error(f"💥 Failed to get system info: {e}")
            return {"error": str(e)}
    
    def collect_metrics(self) -> SystemMetrics:
        """📊 Collect current PAC-MAN system metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_mb = memory.available / (1024 * 1024)
            
            # Disk metrics
            disk_usage = psutil.disk_usage('/')
            disk_usage_percent = (disk_usage.used / disk_usage.total) * 100
            disk_free_gb = disk_usage.free / (1024 * 1024 * 1024)
            
            # Network connections
            active_connections = len(psutil.net_connections())
            
            # Uptime
            uptime_seconds = time.time() - self.start_time
            
            metrics = SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent, 
                memory_available_mb=memory_available_mb,
                disk_usage_percent=disk_usage_percent,
                disk_free_gb=disk_free_gb,
                active_connections=active_connections,
                uptime_seconds=uptime_seconds
            )
            
            # Add to history
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > self.max_history_size:
                self.metrics_history = self.metrics_history[-self.max_history_size:]
            
            logger.debug(f"🟡 PAC-MAN metrics collected: CPU {cpu_percent:.1f}%, Memory {memory_percent:.1f}%")
            return metrics
            
        except Exception as e:
            logger.error(f"💥 Failed to collect PAC-MAN metrics: {e}")
            # Return empty metrics on error
            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_available_mb=0.0,
                disk_usage_percent=0.0,
                disk_free_gb=0.0,
                active_connections=0,
                uptime_seconds=0.0
            )
    
    def check_component_health(self, component_name: str) -> ComponentHealth:
        """🔧 Check health of a specific PAC-MAN component"""
        try:
            now = datetime.now().isoformat()
            errors = []
            warnings = []
            health_score = 1.0
            status = ComponentStatus.ONLINE
            details = {}
            
            if component_name == "database":
                # Check database component
                config = get_config()
                db_path = Path(config.database.storage_path).expanduser()
                
                if not db_path.exists():
                    errors.append("Database storage path does not exist")
                    health_score -= 0.5
                    status = ComponentStatus.OFFLINE
                else:
                    details["storage_path"] = str(db_path)
                    details["path_exists"] = True
                    
                    # Check available space
                    try:
                        disk_usage = psutil.disk_usage(str(db_path))
                        free_gb = disk_usage.free / (1024 * 1024 * 1024)
                        details["free_space_gb"] = round(free_gb, 2)
                        
                        if free_gb < 1.0:  # Less than 1GB free
                            errors.append(f"Low disk space: {free_gb:.1f}GB free")
                            health_score -= 0.3
                            status = ComponentStatus.DEGRADED
                        elif free_gb < 5.0:  # Less than 5GB free
                            warnings.append(f"Disk space getting low: {free_gb:.1f}GB free")
                            health_score -= 0.1
                    except Exception as e:
                        warnings.append(f"Could not check disk space: {e}")
                        health_score -= 0.1
            
            elif component_name == "tui":
                # Check TUI component
                try:
                    # Test if Textual is available
                    import textual
                    details["textual_version"] = getattr(textual, '__version__', 'unknown')
                    details["tui_available"] = True
                    
                    # Check TUI settings
                    config = get_config()
                    details["theme"] = config.tui.theme
                    details["animations_enabled"] = config.tui.animations_enabled
                    
                except ImportError:
                    errors.append("Textual TUI framework not available")
                    health_score = 0.0
                    status = ComponentStatus.OFFLINE
            
            elif component_name == "oxigraph":
                # Check Oxigraph database engine
                try:
                    import pyoxigraph
                    details["pyoxigraph_version"] = getattr(pyoxigraph, '__version__', 'unknown')
                    details["oxigraph_available"] = True
                    
                    # Test basic store creation
                    from pyoxigraph import Store
                    test_store = Store()  # In-memory store for testing
                    details["store_creation"] = "success"
                    
                except ImportError:
                    errors.append("pyoxigraph not available")
                    health_score = 0.0
                    status = ComponentStatus.OFFLINE
                except Exception as e:
                    warnings.append(f"Oxigraph test failed: {e}")
                    health_score -= 0.2
                    status = ComponentStatus.DEGRADED
            
            elif component_name == "git":
                # Check Git operations
                try:
                    import git
                    details["gitpython_version"] = git.__version__
                    details["git_available"] = True
                    
                    # Test git executable
                    try:
                        git_version = git.cmd.Git().version()
                        details["git_version"] = git_version
                    except Exception as e:
                        warnings.append(f"Git executable issue: {e}")
                        health_score -= 0.2
                        
                except ImportError:
                    errors.append("GitPython not available")
                    health_score = 0.0
                    status = ComponentStatus.OFFLINE
            
            elif component_name == "memory":
                # Check memory usage
                memory = psutil.virtual_memory()
                details["total_mb"] = round(memory.total / (1024 * 1024))
                details["available_mb"] = round(memory.available / (1024 * 1024))
                details["percent_used"] = memory.percent
                
                if memory.percent > 90:
                    errors.append(f"Very high memory usage: {memory.percent:.1f}%")
                    health_score -= 0.4
                    status = ComponentStatus.DEGRADED
                elif memory.percent > 80:
                    warnings.append(f"High memory usage: {memory.percent:.1f}%")
                    health_score -= 0.2
            
            elif component_name == "cpu":
                # Check CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_count = psutil.cpu_count()
                details["percent_used"] = cpu_percent
                details["cpu_count"] = cpu_count
                
                if cpu_percent > 90:
                    errors.append(f"Very high CPU usage: {cpu_percent:.1f}%")
                    health_score -= 0.4
                    status = ComponentStatus.DEGRADED
                elif cpu_percent > 80:
                    warnings.append(f"High CPU usage: {cpu_percent:.1f}%")
                    health_score -= 0.2
            
            else:
                # Unknown component
                warnings.append(f"Unknown component: {component_name}")
                health_score = 0.5
                status = ComponentStatus.UNKNOWN
            
            # Determine final status based on health score
            if health_score >= 0.9:
                status = ComponentStatus.ONLINE
            elif health_score >= 0.7:
                status = ComponentStatus.DEGRADED if status == ComponentStatus.ONLINE else status
            elif health_score >= 0.3:
                status = ComponentStatus.DEGRADED
            else:
                status = ComponentStatus.OFFLINE
            
            health = ComponentHealth(
                name=component_name,
                status=status,
                health_score=health_score,
                last_check=now,
                details=details,
                errors=errors,
                warnings=warnings
            )
            
            # Store in component health cache
            self.component_health[component_name] = health
            
            logger.debug(f"🟡 PAC-MAN component {component_name} health: {status.value} ({health_score:.2f})")
            return health
            
        except Exception as e:
            logger.error(f"💥 Failed to check PAC-MAN component {component_name}: {e}")
            return ComponentHealth(
                name=component_name,
                status=ComponentStatus.ERROR,
                health_score=0.0,
                last_check=datetime.now().isoformat(),
                details={"error": str(e)},
                errors=[f"Health check failed: {e}"],
                warnings=[]
            )
    
    def get_overall_status(self) -> Tuple[SystemStatus, Dict[str, Any]]:
        """🟡 Get overall PAC-MAN system status"""
        try:
            # Check key components
            components_to_check = ["database", "tui", "oxigraph", "git", "memory", "cpu"]
            component_scores = []
            critical_errors = []
            warnings = []
            
            for component in components_to_check:
                health = self.check_component_health(component)
                component_scores.append(health.health_score)
                
                if health.errors:
                    critical_errors.extend(health.errors)
                if health.warnings:
                    warnings.extend(health.warnings)
            
            # Calculate overall health score
            overall_score = sum(component_scores) / len(component_scores) if component_scores else 0.0
            
            # Determine system status
            if critical_errors:
                status = SystemStatus.CRITICAL
            elif overall_score >= 0.9:
                status = SystemStatus.EXCELLENT
            elif overall_score >= 0.8:
                status = SystemStatus.GOOD
            elif overall_score >= 0.6:
                status = SystemStatus.WARNING
            else:
                status = SystemStatus.CRITICAL
            
            # Get current metrics
            current_metrics = self.collect_metrics()
            
            summary = {
                "status": status.value,
                "health_score": round(overall_score, 3),
                "components_checked": len(components_to_check),
                "critical_errors": len(critical_errors),
                "warnings": len(warnings),
                "uptime_hours": round(current_metrics.uptime_seconds / 3600, 2),
                "cpu_percent": current_metrics.cpu_percent,
                "memory_percent": current_metrics.memory_percent,
                "disk_free_gb": current_metrics.disk_free_gb,
                "last_check": datetime.now().isoformat(),
                "pac_man_status": "🟡 WAKA WAKA!" if status in [SystemStatus.EXCELLENT, SystemStatus.GOOD] else "👻 GHOST TROUBLES!"
            }
            
            logger.info(f"🟡 PAC-MAN overall status: {status.value} (score: {overall_score:.3f})")
            return status, summary
            
        except Exception as e:
            logger.error(f"💥 Failed to get PAC-MAN overall status: {e}")
            return SystemStatus.ERROR, {
                "status": SystemStatus.ERROR.value,
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }
    
    def get_performance_stats(self, hours_back: int = 24) -> Dict[str, Any]:
        """📈 Get PAC-MAN performance statistics"""
        try:
            if not self.metrics_history:
                return {"message": "No performance data available yet"}
            
            # Filter metrics by time window
            cutoff_time = datetime.now() - timedelta(hours=hours_back)
            recent_metrics = [
                m for m in self.metrics_history 
                if datetime.fromisoformat(m.timestamp) >= cutoff_time
            ]
            
            if not recent_metrics:
                return {"message": f"No performance data for last {hours_back} hours"}
            
            # Calculate statistics
            cpu_values = [m.cpu_percent for m in recent_metrics]
            memory_values = [m.memory_percent for m in recent_metrics]
            
            stats = {
                "time_window_hours": hours_back,
                "data_points": len(recent_metrics),
                "cpu_stats": {
                    "average": round(sum(cpu_values) / len(cpu_values), 2),
                    "max": round(max(cpu_values), 2),
                    "min": round(min(cpu_values), 2),
                    "current": cpu_values[-1] if cpu_values else 0
                },
                "memory_stats": {
                    "average": round(sum(memory_values) / len(memory_values), 2),
                    "max": round(max(memory_values), 2),
                    "min": round(min(memory_values), 2),
                    "current": memory_values[-1] if memory_values else 0
                },
                "uptime_hours": round(recent_metrics[-1].uptime_seconds / 3600, 2) if recent_metrics else 0,
                "generated_at": datetime.now().isoformat()
            }
            
            logger.debug(f"🟡 PAC-MAN performance stats generated: {stats['data_points']} points")
            return stats
            
        except Exception as e:
            logger.error(f"💥 Failed to get PAC-MAN performance stats: {e}")
            return {"error": str(e)}
    
    def create_alert(self, level: str, component: str, message: str, details: Dict[str, Any] = None) -> None:
        """🚨 Create a PAC-MAN system alert"""
        try:
            alert = {
                "id": f"alert_{int(time.time())}_{len(self.alerts)}",
                "timestamp": datetime.now().isoformat(),
                "level": level,  # info, warning, error, critical
                "component": component,
                "message": message,
                "details": details or {},
                "resolved": False
            }
            
            self.alerts.append(alert)
            
            # Keep only recent alerts (last 1000)
            if len(self.alerts) > 1000:
                self.alerts = self.alerts[-1000:]
            
            logger.warning(f"🚨 PAC-MAN Alert [{level}] {component}: {message}")
            
        except Exception as e:
            logger.error(f"💥 Failed to create PAC-MAN alert: {e}")
    
    def get_alerts(self, unresolved_only: bool = False, hours_back: int = 24) -> List[Dict[str, Any]]:
        """🚨 Get PAC-MAN system alerts"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours_back)
            
            filtered_alerts = []
            for alert in self.alerts:
                alert_time = datetime.fromisoformat(alert['timestamp'])
                
                # Filter by time
                if alert_time < cutoff_time:
                    continue
                
                # Filter by resolution status
                if unresolved_only and alert.get('resolved', False):
                    continue
                
                filtered_alerts.append(alert)
            
            # Sort by timestamp (newest first)
            filtered_alerts.sort(key=lambda x: x['timestamp'], reverse=True)
            
            logger.debug(f"🟡 PAC-MAN alerts retrieved: {len(filtered_alerts)} alerts")
            return filtered_alerts
            
        except Exception as e:
            logger.error(f"💥 Failed to get PAC-MAN alerts: {e}")
            return []
    
    def get_system_diagnostics(self) -> Dict[str, Any]:
        """🔧 Get comprehensive PAC-MAN system diagnostics"""
        try:
            overall_status, summary = self.get_overall_status()
            system_info = self.get_system_info()
            performance_stats = self.get_performance_stats()
            recent_alerts = self.get_alerts(hours_back=24)
            
            diagnostics = {
                "system_info": system_info,
                "overall_status": summary,
                "component_health": {
                    name: health.to_dict() 
                    for name, health in self.component_health.items()
                },
                "performance_stats": performance_stats,
                "recent_alerts": recent_alerts,
                "diagnostics_generated_at": datetime.now().isoformat(),
                "pac_man_says": "🟡 WAKA WAKA! System diagnostics complete!"
            }
            
            logger.info("🟡 PAC-MAN system diagnostics generated successfully")
            return diagnostics
            
        except Exception as e:
            logger.error(f"💥 Failed to generate PAC-MAN diagnostics: {e}")
            return {
                "error": str(e),
                "diagnostics_generated_at": datetime.now().isoformat(),
                "pac_man_says": "👻 Ghost in the machine! Diagnostics failed!"
            }
    
    def start_monitoring(self, interval_seconds: int = 60) -> None:
        """🟡 Start continuous PAC-MAN system monitoring"""
        logger.info(f"🟡 Starting PAC-MAN system monitoring (interval: {interval_seconds}s)")
        
        try:
            while True:
                # Collect metrics
                metrics = self.collect_metrics()
                
                # Check for alerts
                if metrics.cpu_percent > 90:
                    self.create_alert("critical", "cpu", f"CPU usage critical: {metrics.cpu_percent:.1f}%")
                elif metrics.cpu_percent > 80:
                    self.create_alert("warning", "cpu", f"CPU usage high: {metrics.cpu_percent:.1f}%")
                
                if metrics.memory_percent > 90:
                    self.create_alert("critical", "memory", f"Memory usage critical: {metrics.memory_percent:.1f}%")
                elif metrics.memory_percent > 80:
                    self.create_alert("warning", "memory", f"Memory usage high: {metrics.memory_percent:.1f}%")
                
                if metrics.disk_free_gb < 1.0:
                    self.create_alert("critical", "disk", f"Disk space critical: {metrics.disk_free_gb:.1f}GB free")
                elif metrics.disk_free_gb < 5.0:
                    self.create_alert("warning", "disk", f"Disk space low: {metrics.disk_free_gb:.1f}GB free")
                
                # Wait for next check
                asyncio.sleep(interval_seconds)
                
        except Exception as e:
            logger.error(f"💥 PAC-MAN monitoring error: {e}")
            self.create_alert("error", "monitor", f"Monitoring system error: {e}")


# Global system monitor instance
_system_monitor: Optional[SystemMonitor] = None


def get_system_monitor() -> SystemMonitor:
    """🟡 Get the global PAC-MAN system monitor"""
    global _system_monitor
    if _system_monitor is None:
        _system_monitor = SystemMonitor()
    return _system_monitor


def get_system_status() -> Tuple[SystemStatus, Dict[str, Any]]:
    """🟡 Get current PAC-MAN system status"""
    return get_system_monitor().get_overall_status()


def get_system_metrics() -> SystemMetrics:
    """🟡 Get current PAC-MAN system metrics"""
    return get_system_monitor().collect_metrics()


def get_system_diagnostics() -> Dict[str, Any]:
    """🟡 Get comprehensive PAC-MAN system diagnostics"""
    return get_system_monitor().get_system_diagnostics()


# Example usage for PAC-MAN's system monitoring!
if __name__ == "__main__":
    # 🟡 PAC-MAN System Monitor Demo!
    monitor = SystemMonitor()
    
    print("🟡 PAC-MAN System Diagnostics Demo!")
    print("=" * 50)
    
    # Get system info
    print("\n📊 System Information:")
    system_info = monitor.get_system_info()
    for key, value in system_info.items():
        print(f"  {key}: {value}")
    
    # Get overall status
    print("\n🟡 Overall Status:")
    status, summary = monitor.get_overall_status()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Check component health
    print("\n🔧 Component Health:")
    components = ["database", "tui", "oxigraph", "git", "memory", "cpu"]
    for component in components:
        health = monitor.check_component_health(component)
        print(f"  {component}: {health.status.value} (score: {health.health_score:.2f})")
    
    # Get performance stats
    print("\n📈 Performance Stats:")
    stats = monitor.get_performance_stats(hours_back=1)
    if "cpu_stats" in stats:
        print(f"  CPU: {stats['cpu_stats']['current']:.1f}% current")
        print(f"  Memory: {stats['memory_stats']['current']:.1f}% current")
    
    print("\n🟡 WAKA WAKA! System monitoring complete!")