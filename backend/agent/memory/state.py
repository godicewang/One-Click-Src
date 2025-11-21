from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class State:
    target_ip_info_list: Optional[Dict[str, Any]] = None
    