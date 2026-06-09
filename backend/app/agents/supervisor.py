from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from app.agents.appeal import AppealRecommendationAgent
from app.agents.claim_denial import ClaimDenialExplanationAgent
from app.agents.comparison import PolicyComparisonAgent
from app.agents.exclusion import ExclusionDetectionAgent
from app.agents.pdf_parsing import PDFParsingAgent
from app.agents.risk import RiskDetectionAgent
from app.agents.summary import PolicySummaryAgent
from app.providers.base import LLMProvider
from app.services.supabase_client import SupabaseService


class AnalysisState(TypedDict, total=False):
    user_id: str
    policy_id: str
    file_url: str
    pdf_content: bytes
    document_text: str
    insurance_type: str
    summary: str
    exclusions: str
    risks: str
    denial_explanations: str
    appeal_recommendations: str
    policy_comparison: str


class PolicyAnalysisSupervisor:
    def __init__(self, provider: LLMProvider, supabase: SupabaseService):
        self.provider = provider
        self.supabase = supabase
        self.pdf_agent = PDFParsingAgent(provider)
        self.summary_agent = PolicySummaryAgent(provider)
        self.exclusion_agent = ExclusionDetectionAgent(provider)
        self.risk_agent = RiskDetectionAgent(provider)
        self.denial_agent = ClaimDenialExplanationAgent(provider)
        self.appeal_agent = AppealRecommendationAgent(provider)
        self.comparison_agent = PolicyComparisonAgent(provider)
        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AnalysisState)
        workflow.add_node("parse_pdf", self._parse_pdf)
        workflow.add_node("summarize", self._summarize)
        workflow.add_node("detect_exclusions", self._detect_exclusions)
        workflow.add_node("detect_risks", self._detect_risks)
        workflow.add_node("explain_denials", self._explain_denials)
        workflow.add_node("recommend_appeal", self._recommend_appeal)
        workflow.add_node("compare_policy", self._compare_policy)
        workflow.add_node("persist", self._persist)

        workflow.set_entry_point("parse_pdf")
        workflow.add_edge("parse_pdf", "summarize")
        workflow.add_edge("summarize", "detect_exclusions")
        workflow.add_edge("detect_exclusions", "detect_risks")
        workflow.add_edge("detect_risks", "explain_denials")
        workflow.add_edge("explain_denials", "recommend_appeal")
        workflow.add_edge("recommend_appeal", "compare_policy")
        workflow.add_edge("compare_policy", "persist")
        workflow.add_edge("persist", END)
        return workflow.compile()

    async def run(self, initial_state: AnalysisState) -> AnalysisState:
        return await self.graph.ainvoke(initial_state)

    async def _parse_pdf(self, state: AnalysisState) -> dict[str, Any]:
        pdf_content = state.get("pdf_content") or await self.supabase.download_policy_pdf(state["file_url"])
        parsed = await self.pdf_agent.run(pdf_content)
        await self.supabase.update_policy_type(state["policy_id"], parsed.get("insurance_type"))
        return parsed

    async def _summarize(self, state: AnalysisState) -> dict[str, str]:
        return {"summary": await self.summary_agent.run(state["document_text"])}

    async def _detect_exclusions(self, state: AnalysisState) -> dict[str, str]:
        return {"exclusions": await self.exclusion_agent.run(state["document_text"])}

    async def _detect_risks(self, state: AnalysisState) -> dict[str, str]:
        return {"risks": await self.risk_agent.run(state["document_text"])}

    async def _explain_denials(self, state: AnalysisState) -> dict[str, str]:
        return {"denial_explanations": await self.denial_agent.run(state["document_text"])}

    async def _recommend_appeal(self, state: AnalysisState) -> dict[str, str]:
        return {
            "appeal_recommendations": await self.appeal_agent.run(
                state["document_text"],
                state["denial_explanations"],
            )
        }

    async def _compare_policy(self, state: AnalysisState) -> dict[str, str]:
        return {"policy_comparison": await self.comparison_agent.run(state["document_text"])}

    async def _persist(self, state: AnalysisState) -> dict[str, str]:
        await self.supabase.insert_row(
            "analyses",
            {
                "policy_id": state["policy_id"],
                "summary": state.get("summary"),
                "exclusions": state.get("exclusions"),
                "risks": state.get("risks"),
                "denial_explanations": state.get("denial_explanations"),
                "appeal_recommendations": state.get("appeal_recommendations"),
                "policy_comparison": state.get("policy_comparison"),
            },
        )
        return {}

