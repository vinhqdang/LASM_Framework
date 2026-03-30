import numpy as np
from typing import Dict, Tuple, List, Optional
from lasm.systems.system_model import ADTResult, LLMSystem, AttackerProfile, EntryPointType
from lasm.metrics.eas import EASEvaluator
from lasm.metrics.trc import TRCEvaluator

class ADTEvaluator:
    def __init__(self, eas_evaluator: EASEvaluator, trc_evaluator: TRCEvaluator):
        self.eas = eas_evaluator
        self.trc = trc_evaluator

    def _estimate_defense_cost(self, defense_str: str, delta: float) -> float:
        """Estimate the USD cost of deploying a defense at a given strength."""
        base_cost = 1000  # mock base cost
        return base_cost * delta**1.5

    def _scale_defense(self, system: LLMSystem, delta: float) -> LLMSystem:
        """Scale defense for the EAS simulation."""
        # Simple placeholder modifying a mock defense scalar
        new_sys = LLMSystem(
            name=system.name, scope=system.scope, components=system.components,
            graph=system.graph, entry_points=system.entry_points,
            trust_weights=system.trust_weights, data_sensitivity=system.data_sensitivity,
            transaction_volume=system.transaction_volume,
            is_public_facing=system.is_public_facing,
            defenses={**system.defenses, "strength": delta}
        )
        return new_sys

    def compute_adt(self, defense: str, profile: AttackerProfile, system: LLMSystem, delta_range: Tuple[float, float]=(0.5, 5.0), delta_step: float=0.1) -> ADTResult:
        """Algorithm 7: ADT Computation"""
        
        v_target = self.eas.estimate_target_value(system)
        adt_per_ep = {}
        
        # Determine minimum delta that deters attack on each entry point type present in the system
        for ep in system.entry_points:
            i = ep.ep_type
            p_i = self.eas.las_evaluator._estimate_exploitation_probability(i, 0, profile.typical_budget_NQU)
            
            delta = delta_range[0]
            deterred = False
            
            while delta <= delta_range[1] and not deterred:
                sys_scaled = self._scale_defense(system, delta)
                p_detection = self.eas._estimate_detection_probability(i, sys_scaled.defenses)
                g_a = p_i * v_target * (1 - p_detection) * self.eas.xi.get(i, 1.0)
                
                # Attacker Cost Mock
                # In robust implementation, this would lookup from attack registry depending on `delta`
                c_compute = (100 * delta) * profile.C_compute_per_NQU
                c_expertise = (2.0 * delta) * profile.hourly_rate
                c_a = c_compute + c_expertise + profile.epsilon_opportunity
                
                if g_a - c_a <= profile.epsilon_opportunity:
                    adt_per_ep[f"{ep.node_id}_{i.value}"] = delta
                    deterred = True
                else:
                    delta += delta_step
                    
            if not deterred:
                adt_per_ep[f"{ep.node_id}_{i.value}"] = float('inf')

        adt_overall = max(list(adt_per_ep.values()) + [0.0]) if adt_per_ep else 0.0

        # Cost curve
        cost_curve = {}
        deltas = np.arange(delta_range[0], delta_range[1] + delta_step, delta_step)
        for delta in deltas:
            cost_curve[delta] = self._estimate_defense_cost(defense, delta)
            
        # Benefit curve
        benefit_curve = {}
        t_now = 0
        las_baseline_result = self.eas.las_evaluator.compute_las(system, t_now, profile.typical_budget_NQU)
        las_norm_base = las_baseline_result.LAS_norm
        
        for delta in deltas:
            sys_scaled = self._scale_defense(system, delta)
            eas_result = self.eas.compute_eas(sys_scaled, t_now, profile.typical_budget_NQU, profile, v_target)
            benefit_curve[delta] = max(0.0, las_norm_base - eas_result.EAS_norm)

        # Dual Half-Life
        # T_months passed as 12 in typical usage
        T_months = 12
        retrospective_trc = self.trc.compute_retrospective(defense, 0.0, T_months, [], "B_mid")
        dhl_tech = retrospective_trc.DHL
        
        tech_trc = retrospective_trc.TRC
        econ_trc = {}
        dhl_econ = None
        
        for t, sasr_t in tech_trc.items():
            g_t = sasr_t * v_target
            # Mock c_t
            c_t = 100 * profile.C_compute_per_NQU + 10  
            ratio_t = g_t / c_t if c_t > 0 else float('inf')
            
            econ_trc[t] = sasr_t if ratio_t > 1 else 0.0
            
            # Using month 0 as t=0 assumption for DHL econ check logic
            t_month = t / (30 * 24 * 3600)
            if dhl_econ is None and ratio_t > 1 and t_month > 0:
                dhl_econ = float(t_month)
                
        dual_trc = {t: (tech_trc[t], econ_trc[t]) for t in tech_trc}

        return ADTResult(
            defense=defense,
            attacker_profile=profile,
            target_system=system,
            ADT=adt_overall,
            ADT_per_entry_point=adt_per_ep,
            cost_curve=cost_curve,
            benefit_curve=benefit_curve,
            DHL_tech=dhl_tech,
            DHL_econ=dhl_econ,
            dual_TRC=dual_trc
        )
