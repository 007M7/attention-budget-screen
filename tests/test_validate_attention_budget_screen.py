import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATOR = os.path.join(ROOT, "scripts", "validate_attention_budget_screen.py")
SIGNALS = [
    "concrete_takeaway",
    "source_specificity",
    "author_footprint",
    "cognitive_progress",
]


def content_stage(status="evaluated"):
    not_run = status == "not_run"
    return {
        "status": status,
        "slop_risk": "not_run" if not_run else "medium",
        "input_coverage": "metadata_only" if not_run else "sampled_content",
        "inspected_sections": [] if not_run else ["opening", "sampled_body"],
        "signals": {
            name: {
                "rating": "not_run" if not_run else "mixed",
                "evidence": "未运行内容阶段。" if not_run else f"检查了 {name} 的样本证据。",
                "confidence": "high" if not_run else "medium",
            }
            for name in SIGNALS
        },
        "basis": "未运行内容阶段。" if not_run else "样本足以做一个有边界的内容质量筛查。",
    }


def attention_stage(status="evaluated", decision="quick_read_now"):
    not_run = status == "not_run"
    return {
        "status": status,
        "triage_decision": "not_run" if not_run else decision,
        "basis": "未运行注意力阶段。" if not_run else "当前目标支持先进行有限筛读。",
        "input_coverage": "metadata_only" if not_run else "abstract_and_toc",
        "inspected_sections": [] if not_run else ["title", "summary"],
        "fit_target": "未运行" if not_run else "个人阅读队列",
        "expected_deep_read_cost": "unknown" if not_run else "medium",
        "expected_decision_impact": "unknown" if not_run else "medium",
        "expected_attention_saved": "unknown" if not_run else "medium",
        "confidence": "low" if not_run else "medium",
        "uncertainty": "未运行注意力阶段。" if not_run else "尚未核查全文事实和长期项目适配度。",
        "not_inferred": "未运行注意力阶段。" if not_run else "不把筛查结果当成事实证明。",
        "revisit_trigger": "用户提出明确阅读目标。",
        "recommended_next_gate": "提供更多上下文或按建议进行下一步筛读。",
    }


def artifact(mode="full_workflow"):
    if mode == "content_quality_only":
        content = content_stage()
        attention = attention_stage("not_run")
        decision = "quality_screen_only"
    elif mode == "attention_only":
        content = content_stage("not_run")
        attention = attention_stage()
        decision = "quick_read_now"
    else:
        content = content_stage()
        attention = attention_stage()
        decision = attention["triage_decision"]
    return {
        "schema_version": "0.1",
        "run_id": "test-001",
        "created_at": "2026-07-15T00:00:00Z",
        "mode": mode,
        "source": {
            "title": "Example source",
            "path_or_url": "https://example.com/source",
            "source_type": "article",
            "sensitivity": "public",
        },
        "workflow_decision": decision,
        "content_quality": content,
        "attention_gate": attention,
        "uncertainty": "两阶段结果都是有边界的启发式判断。",
        "not_inferred": "不推断 AI 作者身份、事实真伪或作者动机。",
        "recommended_next_gate": "根据注意力决策进行有限筛读或来源核验。",
        "writeback_status": "none",
    }


def run_validator(data):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "artifact.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle)
        result = subprocess.run(
            [sys.executable, VALIDATOR, path], capture_output=True, text=True, check=False
        )
        return result.returncode, json.loads(result.stdout)


class TestValidateAttentionBudgetScreen(unittest.TestCase):
    def test_full_workflow_valid(self):
        code, result = run_validator(artifact("full_workflow"))
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

    def test_content_quality_only_valid(self):
        code, result = run_validator(artifact("content_quality_only"))
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

    def test_attention_only_valid(self):
        code, result = run_validator(artifact("attention_only"))
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

    def test_high_risk_does_not_change_attention_decision_contract(self):
        data = artifact("full_workflow")
        data["content_quality"]["slop_risk"] = "high"
        code, result = run_validator(data)
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")

    def test_full_workflow_cannot_skip_attention_stage(self):
        data = artifact("full_workflow")
        data["attention_gate"] = attention_stage("not_run")
        code, result = run_validator(data)
        self.assertEqual(code, 2)
        self.assertIn("full_workflow", " ".join(result["errors"]))

    def test_wrong_neighbor_decision_invalid(self):
        data = artifact("content_quality_only")
        data["workflow_decision"] = "do_not_invest_further_now"
        code, result = run_validator(data)
        self.assertEqual(code, 2)
        self.assertIn("quality_screen_only", " ".join(result["errors"]))

    def test_forbidden_ai_field_invalid(self):
        data = artifact("full_workflow")
        data["ai_generated"] = True
        code, result = run_validator(data)
        self.assertEqual(code, 2)
        self.assertIn("forbidden", " ".join(result["errors"]))

    def test_indeterminate_content_can_continue_attention(self):
        data = artifact("full_workflow")
        data["content_quality"]["status"] = "indeterminate"
        data["content_quality"]["slop_risk"] = "indeterminate"
        for item in data["content_quality"]["signals"].values():
            item["rating"] = "unknown"
        code, result = run_validator(data)
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "valid")


if __name__ == "__main__":
    unittest.main()
