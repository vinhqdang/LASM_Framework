from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any
import networkx as nx

class EntryPointType(Enum):
    SYSTEM_PROMPT = "EP_SP"
    USER_PROMPT = "EP_UP"
    RETRIEVED_CONTEXT = "EP_RC"
    TOOL_API_CALL = "EP_TC"
    AGENT_MESSAGE = "EP_AM"
    MEMORY_STORE = "EP_MS"

class SystemScope(Enum):
    SINGLE_LLM = "S1"
    RAG_PIPELINE = "S2"
    LLM_AGENT = "S3"
    MULTI_AGENT = "S4"

@dataclass
class EntryPoint:
    node_id: str
    ep_type: EntryPointType
    exposure_weight: float      # w_i in [0, 1]
    harm_weight: float          # h_i in [1, 10]
    description: str = ""

@dataclass
class LLMSystem:
    name: str
    scope: SystemScope
    components: List['LLMSystem']  # Sub-systems for multi-agent
    graph: nx.DiGraph              # Communication graph
    entry_points: List[EntryPoint]
    trust_weights: Dict[tuple, float]  # edge -> trust level tau(e)
    data_sensitivity: str = "standard" # standard, PII, financial
    transaction_volume: int = 1000
    is_public_facing: bool = True
    defenses: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LASResult:
    system: LLMSystem
    time: float                    # Unix timestamp
    budget_NQU: float
    LAS_score: float               # Raw LAS
    LAS_norm: float                # Normalized [0, 100]
    per_entry_point: Dict[str, float]   # Breakdown by entry point
    interaction_term: float        # alpha * LAS_interaction
    confidence_interval: tuple     # 95% CI

@dataclass
class SASRResult:
    attack: str
    defense: str
    prompt_set: str
    budget_NQU: float
    SASR_score: float              # in [0, 1]
    judge_kappa: float             # Inter-judge Cohen's kappa
    credible: bool                 # kappa >= 0.6
    per_prompt_SR: Dict[str, float]
    budget_tier: str               # B_low / B_mid / B_high / B_adaptive

@dataclass
class TRCResult:
    defense: str
    t0: float
    T_months: int
    TRC: Dict[float, float]        # time -> SASR
    DHL: Optional[float]           # Defense Half-Life in months
    DR: float                      # Degradation Rate (SASR/month)
    STB: Dict[float, Optional[float]]  # threshold -> breach time
    is_prospective: bool

@dataclass
class AttackerProfile:
    name: str                          # "script_kiddie" | "researcher" | "criminal" | "nation_state"
    C_compute_per_NQU: float           # USD per NQU of API queries
    hourly_rate: float                 # USD per hour of human expertise
    epsilon_opportunity: float         # USD opportunity cost threshold
    typical_budget_NQU: float          # Typical budget in NQU for this profile

@dataclass
class EASResult:
    system: LLMSystem
    time: float
    budget_NQU: float
    attacker_profile: AttackerProfile
    EAS_score: float                   # Raw EAS
    EAS_norm: float                    # Normalized [0, 100]
    LAS_norm: float                    # Corresponding LAS for comparison
    deterrence_ratio: float            # 1 - (EAS_norm / LAS_norm), in [0, 1]
    deterred_surface: float            # LAS_norm - EAS_norm
    rational_entry_points: List[dict]  # Entry points with positive net value
    V_target: float                    # Estimated target value in USD

@dataclass
class ADTResult:
    defense: str
    attacker_profile: AttackerProfile
    target_system: LLMSystem
    ADT: float                         # Minimum defense strength to deter all attacks
    ADT_per_entry_point: Dict[str, float]  # Per-entry-point deterrence thresholds
    cost_curve: Dict[float, float]     # defense_strength -> defender_cost (USD)
    benefit_curve: Dict[float, float]  # defense_strength -> EAS reduction
    DHL_tech: Optional[float]          # Technical defense half-life (months)
    DHL_econ: Optional[float]          # Economic defense half-life (months)
    dual_TRC: Dict[float, tuple]       # time -> (TRC_technical, TRC_economic)
