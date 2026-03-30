import math
import typing
from typing import Dict, List, Any
from lasm.systems.system_model import LLMSystem, LASResult, EntryPointType, EntryPoint
from lasm.metrics.taxonomy import TaxonomyManager
from lasm.systems.entry_points import enumerate_entry_points, compute_exposure_weight

class LASEvaluator:
    def __init__(self, taxonomy: TaxonomyManager):
        self.taxonomy = taxonomy
        # Mock values for alpha and interaction term for now
        self.alpha = 1.0

    def compute_las(self, system: LLMSystem, time: float, budget_NQU: float) -> LASResult:
        """
        Algorithm 1: LAS Computation
        """
        entry_points = enumerate_entry_points(system.graph, system)
        
        las_base = 0.0
        contributions = {}
        
        for ep in system.entry_points:
            w_i = ep.exposure_weight
            h_i = self.taxonomy.get_harm_weight(ep.ep_type)
            p_i = self._estimate_exploitation_probability(ep.ep_type, time, budget_NQU)
            
            # |E_i| is effectively 1 per individual entry point listed here
            contribution = w_i * 1.0 * p_i * h_i
            contributions[f"{ep.node_id}_{ep.ep_type.value}"] = contribution
            las_base += contribution
            
        interaction_term = 0.0
        if len(system.components) > 1:
            interaction_term = self._compute_interaction_surface(system, time, budget_NQU)
            
        las_score = las_base + self.alpha * interaction_term
        
        las_max = self._compute_theoretical_max(budget_NQU, len(system.entry_points))
        # Protect against div zero
        las_norm = 100 * las_score / las_max if las_max > 0 else 0.0
        
        return LASResult(
            system=system,
            time=time,
            budget_NQU=budget_NQU,
            LAS_score=las_score,
            LAS_norm=las_norm,
            per_entry_point=contributions,
            interaction_term=self.alpha * interaction_term,
            confidence_interval=(las_score * 0.9, las_score * 1.1) # Mock CI
        )

    def _estimate_exploitation_probability(self, ep_type: EntryPointType, time: float, B: float) -> float:
        """Algorithm 2: Exploitation Probability Estimation"""
        # Conservative priors from plan
        priors = {
            EntryPointType.SYSTEM_PROMPT: 0.45,
            EntryPointType.USER_PROMPT: 0.35,
            EntryPointType.RETRIEVED_CONTEXT: 0.52,
            EntryPointType.TOOL_API_CALL: 0.58,
            EntryPointType.AGENT_MESSAGE: 0.72,
            EntryPointType.MEMORY_STORE: 0.61,
        }
        return priors.get(ep_type, 0.5)

    def _compute_interaction_surface(self, system: LLMSystem, time: float, B: float) -> float:
        # Mock calculation of interaction surface for multi-agent
        return 10.0

    def _compute_theoretical_max(self, B: float, ep_count: int) -> float:
        # p_i=1.0, w_i=1.0, h_i=10.0 for all ep_count
        return ep_count * 1.0 * 1.0 * 10.0

