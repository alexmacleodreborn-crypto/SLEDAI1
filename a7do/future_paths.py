# a7do/future_paths.py
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import uuid
import time


@dataclass
class FuturePath:
    path_id: str
    type: str                 # place | person | object | routine
    proposal: Dict[str, Any]
    unlock: Dict[str, Any]
    priority: float = 0.5
    novelty_cost: float = 0.3
    status: str = "proposed"  # proposed | approved | scheduled | experienced
    created_at: float = field(default_factory=time.time)
    notes: List[str] = field(default_factory=list)


class FuturePathRegistry:
    def __init__(self):
        self.paths: Dict[str, FuturePath] = {}

    def propose(
        self,
        type: str,
        proposal: Dict[str, Any],
        unlock: Dict[str, Any],
        priority: float = 0.5,
        novelty_cost: float = 0.3,
        notes: Optional[List[str]] = None,
    ) -> str:
        pid = str(uuid.uuid4())[:8]
        self.paths[pid] = FuturePath(
            path_id=pid,
            type=type,
            proposal=proposal,
            unlock=unlock,
            priority=priority,
            novelty_cost=novelty_cost,
            notes=notes or [],
        )
        return pid

    def list(self, status: Optional[str] = None) -> List[FuturePath]:
        items = list(self.paths.values())
        if status:
            items = [p for p in items if p.status == status]
        return sorted(items, key=lambda p: (-p.priority, p.created_at))

    def approve(self, path_id: str):
        if path_id in self.paths:
            self.paths[path_id].status = "approved"

    def mark_scheduled(self, path_id: str):
        if path_id in self.paths:
            self.paths[path_id].status = "scheduled"

    def mark_experienced(self, path_id: str):
        if path_id in self.paths:
            self.paths[path_id].status = "experienced"