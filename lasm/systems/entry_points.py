from typing import List, Tuple
from lasm.systems.system_model import LLMSystem, EntryPoint, EntryPointType

def enumerate_entry_points(system_graph, system_def=None) -> List[Tuple[str, EntryPointType]]:
    """
    Deterministically enumerate entry points from an LLM system architecture graph.
    Returns a list of (node_id, entry_point_type) pairs.
    """
    entry_points = []
    
    # In a full implementation, this parses the system_graph (networkx Graph)
    # For now, it returns the mocked entry points if passed in system_def.
    if system_def and hasattr(system_def, 'entry_points'):
        for ep in system_def.entry_points:
            entry_points.append((ep.node_id, ep.ep_type))
            
    return entry_points

def compute_exposure_weight(node_id: str, ep_type: EntryPointType, system: LLMSystem) -> float:
    """
    Compute architectural exposure weight for an entry point.
    """
    # Placeholder: assume equal weighting for now
    return 1.0
