# Attention Budget Screen 输出契约 v0.1

```json
{
  "schema_version": "0.1",
  "run_id": "optional-local-id",
  "created_at": "2026-07-15T00:00:00Z",
  "mode": "full_workflow|content_quality_only|attention_only",
  "source": {
    "title": "",
    "path_or_url": "",
    "source_type": "article|pdf|report|book|post|transcript|other",
    "sensitivity": "public|private|unknown"
  },
  "workflow_decision": "quick_read_now|read_deep_now|project_relevant_but_not_now|reference_only|defer_or_monitor|do_not_invest_further_now|pending_context|quality_screen_only",
  "content_quality": {
    "status": "evaluated|indeterminate|not_run",
    "slop_risk": "low|medium|high|indeterminate|not_run",
    "input_coverage": "metadata_only|sampled_content|full_content|other",
    "inspected_sections": [],
    "signals": {
      "concrete_takeaway": {
        "rating": "strong|mixed|weak|unknown|not_run",
        "evidence": "",
        "confidence": "low|medium|high"
      },
      "source_specificity": {
        "rating": "strong|mixed|weak|unknown|not_run",
        "evidence": "",
        "confidence": "low|medium|high"
      },
      "author_footprint": {
        "rating": "strong|mixed|weak|unknown|not_run",
        "evidence": "",
        "confidence": "low|medium|high"
      },
      "cognitive_progress": {
        "rating": "strong|mixed|weak|unknown|not_run",
        "evidence": "",
        "confidence": "low|medium|high"
      }
    },
    "basis": ""
  },
  "attention_gate": {
    "status": "evaluated|indeterminate|not_run",
    "triage_decision": "quick_read_now|read_deep_now|project_relevant_but_not_now|reference_only|defer_or_monitor|do_not_invest_further_now|pending_context|not_run",
    "basis": "",
    "input_coverage": "metadata_only|abstract_and_toc|sampled_sections|other",
    "inspected_sections": [],
    "fit_target": "",
    "expected_deep_read_cost": "low|medium|high|unknown",
    "expected_decision_impact": "low|medium|high|unknown",
    "expected_attention_saved": "low|medium|high|unknown",
    "confidence": "low|medium|high",
    "uncertainty": "",
    "not_inferred": "",
    "revisit_trigger": "",
    "recommended_next_gate": ""
  },
  "uncertainty": "",
  "not_inferred": "",
  "recommended_next_gate": "",
  "writeback_status": "none"
}
```

契约规则：

- `full_workflow`：两个阶段都不能是 `not_run`；`workflow_decision` 必须等于 attention 的 `triage_decision`。
- `content_quality_only`：attention 必须是 `not_run`；`workflow_decision` 必须是 `quality_screen_only`。
- `attention_only`：content 可以是 `not_run`；`workflow_decision` 必须等于 attention 的 `triage_decision`。
- `content_quality.status=not_run` 时，四个 signal 的 rating 必须为 `not_run`。
- `attention_gate.status=not_run` 时，`triage_decision` 必须为 `not_run`。
- 非 `metadata_only` 的阶段必须列出实际 inspected sections。
- 顶层 `uncertainty`、`not_inferred`、`recommended_next_gate` 必须非空。
- `writeback_status` 必须为 `none`。
- 不得出现 `ai_generated`、`truth_score`、`author_intent`、`automatic_action`、`telemetry`、`upload_source` 或 `durable_writeback`。
