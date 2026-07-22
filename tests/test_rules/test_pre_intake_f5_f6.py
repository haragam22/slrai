"""F5/F6 pre-intake routing flag tests — non-terminating, unlike F1-F4."""
from app.services.compliance.pre_intake import run_route_flags


def test_f5_routes_third_party_ats():
    flags = run_route_flags({"sa_applicant_type": "THIRD_PARTY_ATS"})
    ids = {f["filter_id"] for f in flags}
    assert "F5" in ids
    f5 = next(f for f in flags if f["filter_id"] == "F5")
    assert f5["result_label"] == "ROUTE_TO_M10"


def test_f5_does_not_fire_for_borrower():
    flags = run_route_flags({"sa_applicant_type": "BORROWER"})
    assert not any(f["filter_id"] == "F5" for f in flags)


def test_f5_does_not_fire_when_unset():
    flags = run_route_flags({})
    assert not any(f["filter_id"] == "F5" for f in flags)


def test_f6_fires_when_sale_certificate_issued():
    flags = run_route_flags({"sale_certificate_issued": True, "sale_certificate_date": "01.04.2025"})
    ids = {f["filter_id"] for f in flags}
    assert "F6" in ids
    f6 = next(f for f in flags if f["filter_id"] == "F6")
    assert f6["result_label"] == "HIGH_THRESHOLD_CHALLENGE"


def test_f6_does_not_fire_when_not_issued():
    flags = run_route_flags({"sale_certificate_issued": False})
    assert not any(f["filter_id"] == "F6" for f in flags)


def test_f5_and_f6_both_fire_non_terminating():
    flags = run_route_flags({
        "sa_applicant_type": "THIRD_PARTY_ATS",
        "sale_certificate_issued": True,
    })
    ids = {f["filter_id"] for f in flags}
    assert ids == {"F5", "F6"}
