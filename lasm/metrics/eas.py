from lasm.systems.system_model import LLMSystem, AttackerProfile, EASResult, SystemScope, EntryPointType
from lasm.metrics.las import LASEvaluator
from typing import Dict, Any

class EASEvaluator:
    def __init__(self, las_evaluator: LASEvaluator):
        self.las_evaluator = las_evaluator
        self.xi = {
            EntryPointType.SYSTEM_PROMPT: 1.0,
            EntryPointType.USER_PROMPT: 1.0, 
            EntryPointType.RETRIEVED_CONTEXT: 1.2,
            EntryPointType.TOOL_API_CALL: 1.0,
            EntryPointType.AGENT_MESSAGE: 2.0,
            EntryPointType.MEMORY_STORE: 2.5
        }

    def estimate_target_value(self, system: LLMSystem) -> float:
        base_values = {
            SystemScope.SINGLE_LLM: 200,
            SystemScope.RAG_PIPELINE: 25000,
            SystemScope.LLM_AGENT: 150000,
            SystemScope.MULTI_AGENT: 500000
        }
        v = base_values.get(system.scope, 1000)

        if system.data_sensitivity == "PII":
            v *= 3.0
        elif system.data_sensitivity == "financial":
            v *= 10.0
            
        if system.transaction_volume > 1000000:
            v *= 2.0
        if system.is_public_facing:
            v *= 0.5
            
        return v

    def _estimate_detection_probability(self, i: EntryPointType, defenses: Dict[str, Any]) -> float:
        # Placeholder for real detection logic based on defenses dict
        return 0.1

    def compute_eas(self, system: LLMSystem, time: float, budget_NQU: float, profile: AttackerProfile, V_target_override: float = None) -> EASResult:
        """Algorithm 6: EAS Computation"""
        
        las_result = self.las_evaluator.compute_las(system, time, budget_NQU)
        las_total = las_result.LAS_score
        
        v_target = V_target_override if V_target_override is not None else self.estimate_target_value(system)
        
        eas_score = 0.0
        rational_entry_points = []
        
        for ep in system.entry_points:
            ep_key = f"{ep.node_id}_{ep.ep_type.value}"
            contribution = las_result.per_entry_point.get(ep_key, 0.0)
            
            w_i = ep.exposure_weight
            h_i = self.las_evaluator.taxonomy.get_harm_weight(ep.ep_type)
            
            if w_i * h_i == 0:
                continue
                
            p_i = contribution / (w_i * h_i) # back out probability
            
            p_detection = self._estimate_detection_probability(ep.ep_type, system.defenses)
            g_a = p_i * v_target * (1 - p_detection) * self.xi.get(ep.ep_type, 1.0)
            
            # Select optimal attack mock values
            c_compute = 100 * profile.C_compute_per_NQU
            c_expertise = 2.0 * profile.hourly_rate
            c_a = c_compute + c_expertise + profile.epsilon_opportunity
            
            if g_a - c_a > profile.epsilon_opportunity:
                eas_score += contribution
                rational_entry_points.append({
                    "entry_point": (ep.node_id, ep.ep_type),
                    "gain": g_a,
                    "cost": c_a,
                    "net_value": g_a - c_a,
                    "LAS_contribution": contribution
                })
                
        las_max = self.las_evaluator._compute_theoretical_max(budget_NQU, len(system.entry_points))
        eas_norm = 100 * eas_score / las_max if las_max > 0 else 0.0
        deterrence_ratio = 1 - (eas_score / las_total) if las_total > 0 else 1.0
        
        return EASResult(
            system=system,
            time=time,
            budget_NQU=budget_NQU,
            attacker_profile=profile,
            EAS_score=eas_score,
            EAS_norm=eas_norm,
            LAS_norm=las_result.LAS_norm,
            deterrence_ratio=deterrence_ratio,
            deterred_surface=las_result.LAS_norm - eas_norm,
            rational_entry_points=rational_entry_points,
            V_target=v_target
        )
