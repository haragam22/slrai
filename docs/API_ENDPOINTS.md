# API Endpoints

## Workbench (H4)

All routes under `app/api/workbench.py`, prefixed `/cases`.

- ✅ `GET /cases/{case_id}/workbench`
  Returns `{low_confidence_items, not_found_items, conflict_items, total_pending, all_resolved}`.

- ✅ `GET /cases/{case_id}/facts`
  Returns all `case_facts` rows: `field_name, field_value, confidence, human_confirmed`.

- ✅ `PATCH /cases/{case_id}/facts/{fact_id}`
  Body: `{corrected_value?, human_confirmed}`. Sets `human_confirmed=True`, triggers downstream recompute of prayer boolean fields.

- ✅ `PATCH /cases/{case_id}/workbench/conflicts/{conflict_id}`
  Body: `{resolution: "candidate_a"|"candidate_b"|"custom", custom_value?}`. Updates `case_fact`, sets `human_confirmed=True`, marks conflict resolved.

- ✅ `POST /cases/{case_id}/workbench/confirm-all`
  Body: `{trigger_analysis: bool}`. Validates all required fields confirmed and no unresolved FATAL/ABSOLUTE_BAR unknowns. 422 if `sa_applicant_type` unconfirmed (routing field). On success fires Chain B via Celery, returns `{status: "ANALYSING", case_id}`. 422 with `{unconfirmed_fields: [...]}` on failed preconditions.
