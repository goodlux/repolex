"""
⏰ PAC-MAN's Time Pellet Event Generator ⏰

This is where PAC-MAN tracks temporal changes using magical time pellets!
Each release change creates an ABC event - a temporal shift in the code maze!

WAKA WAKA! Time flows differently in the semantic dimension!
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass
import logging

from ..models.function import FunctionInfo
from ..models.results import ParsedRepository
from ..models.abc import ABCEvent, FunctionChangeEvent, RepositoryChangeEvent
from ..models.exceptions import ProcessingError
from ..models.git import CommitInfo

logger = logging.getLogger(__name__)


@dataclass
class TimePelletStats:
    """⏰ PAC-MAN's temporal tracking statistics!"""
    time_pellets_consumed: int = 0  # ABC events generated
    function_changes_detected: int = 0  # Function-level changes
    new_functions_discovered: int = 0  # Functions added
    vanished_functions_mourned: int = 0  # Functions removed
    signature_transformations: int = 0  # Signature changes
    temporal_anomalies: int = 0  # Unexpected changes


class ABCTimeNavigator:
    """
    ⏰ PAC-MAN's Time Navigation System! ⏰
    
    Simple but powerful implementation of ABC (A Boring Core) temporal events!
    Tracks how the code maze transforms through time pellets!
    """

    def __init__(self):
        self.stats = TimePelletStats()
        self.logger = logging.getLogger(__name__)
        
        logger.info("⏰ PAC-MAN's time machine activated!")

    def generate_temporal_events(self, old_repository: ParsedRepository, 
                                new_repository: ParsedRepository) -> List[ABCEvent]:
        """
        ⏰ GENERATE ALL TIME PELLET EVENTS! ⏰
        
        Compare two repository states and generate ABC events for all changes!
        This is the CORE of temporal understanding!
        """
        try:
            self.logger.info(f"⏰ Generating time pellets between {old_repository.release} → {new_repository.release}")
            
            events = []
            
            # Create repository-level change event
            repo_event = self._create_repository_change_event(old_repository, new_repository)
            events.append(repo_event)
            
            # Generate function-level changes
            function_events = self._detect_all_function_changes(old_repository, new_repository)
            events.extend(function_events)
            
            # Generate file-level changes
            file_events = self._detect_file_changes(old_repository, new_repository)
            events.extend(file_events)
            
            self.logger.info(f"⏰ Time pellet generation complete! {len(events)} events created")
            
            return events
            
        except Exception as e:
            raise ProcessingError(f"Failed to generate ABC events: {e}")

    def _create_repository_change_event(self, old_repo: ParsedRepository,
                                      new_repo: ParsedRepository) -> RepositoryChangeEvent:
        """⏰ Create the main repository transformation event!"""
        
        old_function_count = old_repo.total_functions
        new_function_count = new_repo.total_functions
        function_delta = new_function_count - old_function_count
        
        old_class_count = old_repo.total_classes
        new_class_count = new_repo.total_classes
        class_delta = new_class_count - old_class_count
        
        change_magnitude = abs(function_delta) + abs(class_delta)
        
        # Classify the type of repository change
        if change_magnitude > 20:
            change_type = "major_release"
        elif change_magnitude > 5:
            change_type = "minor_release"
        elif change_magnitude > 0:
            change_type = "patch_release"
        else:
            change_type = "maintenance_release"
        
        event = RepositoryChangeEvent(
            event_id=f"repo_change_{old_repo.release}_to_{new_repo.release}",
            repository_name=old_repo.name,
            from_version=old_repo.release,
            to_version=new_repo.release,
            change_type=change_type,
            timestamp=datetime.now(timezone.utc),
            function_delta=function_delta,
            class_delta=class_delta,
            change_magnitude=change_magnitude,
            summary=f"Repository transformed: {function_delta:+d} functions, {class_delta:+d} classes"
        )
        
        self.stats.time_pellets_consumed += 1
        return event

    def _detect_all_function_changes(self, old_repo: ParsedRepository,
                                   new_repo: ParsedRepository) -> List[FunctionChangeEvent]:
        """⏰ Detect all function-level temporal changes!"""
        
        # Build function lookup maps
        old_functions = self._build_function_map(old_repo)
        new_functions = self._build_function_map(new_repo)
        
        events = []
        
        # Find function changes
        for func_name, old_func in old_functions.items():
            if func_name in new_functions:
                # Function exists in both - check for changes
                new_func = new_functions[func_name]
                change_event = self._analyze_function_change(old_func, new_func, 
                                                           old_repo.release, new_repo.release)
                if change_event:
                    events.append(change_event)
            else:
                # Function was removed
                removal_event = self._create_function_removal_event(old_func, 
                                                                  old_repo.release, new_repo.release)
                events.append(removal_event)
                self.stats.vanished_functions_mourned += 1
        
        # Find new functions
        for func_name, new_func in new_functions.items():
            if func_name not in old_functions:
                addition_event = self._create_function_addition_event(new_func, 
                                                                    old_repo.release, new_repo.release)
                events.append(addition_event)
                self.stats.new_functions_discovered += 1
        
        return events

    def _build_function_map(self, repository: ParsedRepository) -> Dict[str, FunctionInfo]:
        """🗺️ Build a map of all functions for easy lookup"""
        function_map = {}
        
        for file in repository.files:
            for func in file.functions:
                # Use function name + file path as unique key
                # This handles cases where same function name appears in different files
                key = f"{func.name}@{func.file_path}"
                function_map[key] = func
        
        return function_map

    def _analyze_function_change(self, old_func: FunctionInfo, new_func: FunctionInfo,
                               from_version: str, to_version: str) -> Optional[FunctionChangeEvent]:
        """⏰ Analyze what changed about a specific function!"""
        
        changes_detected = []
        change_details = {}
        
        # Check signature changes
        if old_func.signature != new_func.signature:
            changes_detected.append("signature_changed")
            change_details["old_signature"] = old_func.signature
            change_details["new_signature"] = new_func.signature
            self.stats.signature_transformations += 1
        
        # Check docstring changes
        old_doc = old_func.docstring_info.description if old_func.docstring_info else ""
        new_doc = new_func.docstring_info.description if new_func.docstring_info else ""
        if old_doc != new_doc:
            changes_detected.append("docstring_changed")
            change_details["docstring_change"] = "updated"
        
        # Check parameter changes
        old_param_names = [p.name for p in old_func.parameters]
        new_param_names = [p.name for p in new_func.parameters]
        if old_param_names != new_param_names:
            changes_detected.append("parameters_changed")
            change_details["parameter_change"] = {
                "old_params": old_param_names,
                "new_params": new_param_names
            }
        
        # Check return type changes
        if old_func.return_type != new_func.return_type:
            changes_detected.append("return_type_changed")
            change_details["old_return_type"] = old_func.return_type
            change_details["new_return_type"] = new_func.return_type
        
        # Check decorator changes
        if set(old_func.decorators) != set(new_func.decorators):
            changes_detected.append("decorators_changed")
            change_details["decorator_change"] = {
                "old_decorators": old_func.decorators,
                "new_decorators": new_func.decorators
            }
        
        # Check visibility changes
        if old_func.visibility != new_func.visibility:
            changes_detected.append("visibility_changed")
            change_details["old_visibility"] = old_func.visibility
            change_details["new_visibility"] = new_func.visibility
        
        # If no changes detected, return None
        if not changes_detected:
            return None
        
        # Determine change severity
        severity = self._determine_change_severity(changes_detected)
        
        event = FunctionChangeEvent(
            event_id=f"func_change_{old_func.name}_{from_version}_to_{to_version}",
            function_name=old_func.name,
            from_version=from_version,
            to_version=to_version,
            change_types=changes_detected,
            change_severity=severity,
            timestamp=datetime.now(timezone.utc),
            old_function=old_func,
            new_function=new_func,
            change_details=change_details
        )
        
        self.stats.function_changes_detected += 1
        self.stats.time_pellets_consumed += 1
        
        return event

    def _create_function_addition_event(self, new_func: FunctionInfo,
                                      from_version: str, to_version: str) -> FunctionChangeEvent:
        """⭐ Create event for new function addition!"""
        
        event = FunctionChangeEvent(
            event_id=f"func_added_{new_func.name}_{to_version}",
            function_name=new_func.name,
            from_version=from_version,
            to_version=to_version,
            change_types=["function_added"],
            change_severity="minor",
            timestamp=datetime.now(timezone.utc),
            old_function=None,
            new_function=new_func,
            change_details={"addition_reason": "new_functionality"}
        )
        
        self.stats.time_pellets_consumed += 1
        return event

    def _create_function_removal_event(self, old_func: FunctionInfo,
                                     from_version: str, to_version: str) -> FunctionChangeEvent:
        """💥 Create event for function removal!"""
        
        # Determine if this might be a breaking change
        severity = "major" if old_func.visibility == "public" else "minor"
        
        event = FunctionChangeEvent(
            event_id=f"func_removed_{old_func.name}_{to_version}",
            function_name=old_func.name,
            from_version=from_version,
            to_version=to_version,
            change_types=["function_removed"],
            change_severity=severity,
            timestamp=datetime.now(timezone.utc),
            old_function=old_func,
            new_function=None,
            change_details={"removal_reason": "deprecated_or_refactored"}
        )
        
        self.stats.time_pellets_consumed += 1
        return event

    def _detect_file_changes(self, old_repo: ParsedRepository,
                           new_repo: ParsedRepository) -> List[ABCEvent]:
        """📁 Detect file-level changes between versions"""
        
        old_files = {str(f.path): f for f in old_repo.files}
        new_files = {str(f.path): f for f in new_repo.files}
        
        events = []
        
        # Find new files
        for file_path in new_files:
            if file_path not in old_files:
                event = ABCEvent(
                    event_id=f"file_added_{file_path.replace('/', '_')}_{new_repo.release}",
                    event_type="file_added",
                    timestamp=datetime.now(timezone.utc),
                    from_version=old_repo.release,
                    to_version=new_repo.release,
                    affected_entity=file_path,
                    change_details={"file_path": file_path}
                )
                events.append(event)
                self.stats.time_pellets_consumed += 1
        
        # Find removed files
        for file_path in old_files:
            if file_path not in new_files:
                event = ABCEvent(
                    event_id=f"file_removed_{file_path.replace('/', '_')}_{new_repo.release}",
                    event_type="file_removed",
                    timestamp=datetime.now(timezone.utc),
                    from_version=old_repo.release,
                    to_version=new_repo.release,
                    affected_entity=file_path,
                    change_details={"file_path": file_path}
                )
                events.append(event)
                self.stats.time_pellets_consumed += 1
        
        return events

    def _determine_change_severity(self, change_types: List[str]) -> str:
        """🎯 Determine how severe the changes are"""
        
        major_changes = ["signature_changed", "parameters_changed", "return_type_changed", "visibility_changed"]
        minor_changes = ["docstring_changed", "decorators_changed"]
        
        has_major = any(change in major_changes for change in change_types)
        has_minor = any(change in minor_changes for change in change_types)
        
        if has_major:
            return "major"
        elif has_minor:
            return "minor"
        else:
            return "patch"

    def link_to_stable_identities(self, events: List[ABCEvent], org: str, repo: str) -> List[ABCEvent]:
        """🔗 Link ABC events to stable function identities"""
        
        for event in events:
            if hasattr(event, 'function_name'):
                # Link to stable function URI
                stable_uri = f"function:{org}/{repo}/{event.function_name}"
                event.stable_function_uri = stable_uri
        
        return events


class ABCGenerator:
    """
    ⏰ PAC-MAN's ABC Event Generation System! ⏰
    
    The main interface for generating temporal change events!
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.navigator = ABCTimeNavigator()

    async def generate_events(self, old_release: ParsedRepository, 
                            new_release: ParsedRepository) -> List[ABCEvent]:
        """
        ⏰ Generate ABC events for changes between releases ⏰
        
        Main method for temporal change detection!
        """
        try:
            self.logger.info(f"⏰ Generating ABC events: {old_release.release} → {new_release.release}")
            
            events = self.navigator.generate_temporal_events(old_release, new_release)
            
            self.logger.info(f"⏰ ABC event generation complete! {len(events)} time pellets created")
            return events
            
        except Exception as e:
            raise ProcessingError(f"Failed to generate ABC events: {e}")

    async def detect_function_changes(self, old_functions: List[FunctionInfo], 
                                    new_functions: List[FunctionInfo]) -> List[FunctionChangeEvent]:
        """Detect changes to function signatures, docstrings, etc."""
        
        # Create mock repositories for the function change detection
        old_repo = ParsedRepository(
            name="temp",
            release="old",
            files=[],  # Not used in this context
            total_functions=len(old_functions),
            total_classes=0,
            processing_stats=None
        )
        
        new_repo = ParsedRepository(
            name="temp",
            release="new", 
            files=[],  # Not used in this context
            total_functions=len(new_functions),
            total_classes=0,
            processing_stats=None
        )
        
        # Use the navigator to detect changes
        return self.navigator._detect_all_function_changes(old_repo, new_repo)

    def link_to_stable_function_identities(self, events: List[ABCEvent], 
                                         org: str, repo: str) -> List[ABCEvent]:
        """Link ABC events to stable function identities"""
        return self.navigator.link_to_stable_identities(events, org, repo)


# ⏰ PAC-MAN says: "WAKA WAKA! Time flows differently in the semantic dimension!" ⏰
def create_abc_generator() -> ABCGenerator:
    """Factory function to create PAC-MAN's ABC generator!"""
    return ABCGenerator()
