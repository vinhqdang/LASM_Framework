"""LASM: LLM Attack Surface Measurement Framework"""
__version__ = "1.0"

import json
from datetime import datetime
from lasm.metrics.taxonomy import TaxonomyManager
from lasm.metrics.las import LASEvaluator
from lasm.metrics.sasr import SASREvaluator
from lasm.metrics.trc import TRCEvaluator
from lasm.metrics.eas import EASEvaluator
from lasm.metrics.adt import ADTEvaluator
from lasm.systems.system_model import LLMSystem, SystemScope, EntryPointType, EntryPoint, AttackerProfile
from lasm.judges.classifier_judge import ClassifierJudge
from lasm.judges.llm_judge import LLMJudge
from lasm.data.attack_registry import AttackRegistry
from lasm.data.prompt_sets import PromptSetManager
from lasm.utils.reporting import ReportingUtils
from lasm.utils.budget import get_budget_tier

class LASMEvaluator:
    def __init__(self, config_path: str = None):
        self.taxonomy = TaxonomyManager()
        self.attack_registry = AttackRegistry()
        self.prompt_manager = PromptSetManager()
        
        # Core engines
        self.las = LASEvaluator(self.taxonomy)
        
        # Lazy load heavy judges
        self._classifier_judge = None
        self._llm_judge = None
        self._sasr = None
        self._trc = None
        
        self.eas = EASEvaluator(self.las)
        
    @property
    def sasr(self):
        if self._sasr is None:
            if self._classifier_judge is None:
                self._classifier_judge = ClassifierJudge()
            if self._llm_judge is None:
                self._llm_judge = LLMJudge()
            self._sasr = SASREvaluator(self._classifier_judge, self._llm_judge)
        return self._sasr
        
    @property
    def trc(self):
        if self._trc is None:
            self._trc = TRCEvaluator(self.attack_registry, self.sasr)
        return self._trc
        
    @property
    def adt(self):
        return ADTEvaluator(self.eas, self.trc)

    def load_system(self, file_path: str) -> LLMSystem:
        """Helper to construct LLMSystem from JSON definitions."""
        # Minimal mock logic. User would define real loading.
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Construct Dummy System based on file content
        sys = LLMSystem(
            name=data.get("name", "sys"),
            scope=SystemScope(data.get("scope", "S1")),
            components=[],
            graph=None,
            entry_points=[EntryPoint(node_id="n1", ep_type=EntryPointType.SYSTEM_PROMPT, exposure_weight=1.0, harm_weight=8.0)],
            trust_weights={}
        )
        return sys

    def compute_las(self, system: LLMSystem, time: datetime, budget_tier: str):
        # map tier to continuous budget mock
        budget_NQU = 1000 if budget_tier == "B_mid" else 100
        return self.las.compute_las(system, time.timestamp(), budget_NQU)

    def compute_sasr(self, attack: str, defense: str, prompt_set: str, budget_tier: str):
        prompts = self.prompt_manager.load_prompt_set(prompt_set)
        # Mock attack/def
        def mock_attack(q, d, b): return "compliant output"
        def mock_defense(q): return False
        b_nqu = 1000
        return self.sasr.compute_sasr(mock_attack, mock_defense, prompts, b_nqu)

    def compute_trc(self, defense: str, t0: datetime, T_months: int, retrospective: bool = True):
        prompts = self.prompt_manager.load_prompt_set("default")
        if retrospective:
            return self.trc.compute_retrospective(defense, t0.timestamp(), T_months, prompts, "B_mid")
        else:
            m, l, u = self.trc.compute_prospective(defense, t0.timestamp(), T_months, prompts)
            return m

    def compute_eas(self, system: LLMSystem, time: datetime, budget_tier: str, attacker_profile: str, V_target_override: float = None):
        prof = AttackerProfile(attacker_profile, 10.0, 100.0, 50.0, 1000)
        return self.eas.compute_eas(system, time.timestamp(), 1000, prof, V_target_override)

    def compute_eas_all_profiles(self, system: LLMSystem, time: datetime):
        profiles = ["script_kiddie", "researcher", "criminal", "nation_state"]
        return {p: self.compute_eas(system, time, "B_mid", p) for p in profiles}

    def compute_adt(self, defense: str, attacker_profile: str, system: LLMSystem, delta_range=(0.5, 5.0)):
        prof = AttackerProfile(attacker_profile, 10.0, 100.0, 50.0, 1000)
        return self.adt.compute_adt(defense, prof, system, delta_range=delta_range)

    def eas_sensitivity(self, system: LLMSystem, V_target_range, attacker_profile: str, n_points: int):
        # mock returns a class to call .to_csv on
        class SensitivityReport:
            def to_csv(self, path):
                with open(path, 'w') as f:
                    f.write("v_target,eas\n")
        return SensitivityReport()

    def generate_report(self, *results):
        class FullReport:
            def save(self, path):
                print(f"Report saved to {path} (MOCK)")
            def to_latex(self, path):
                ReportingUtils.to_latex({type(r).__name__: getattr(r, 'time', 0.0) for r in results}, path)
        return FullReport()
