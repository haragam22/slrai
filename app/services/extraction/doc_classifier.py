"""Keyword-rule document type classifier. NO AI. Deterministic."""

DOC_TYPE_KEYWORDS = {
    "SA":                ["securitisation application", "section 17", "drt", "applicant"],
    "DEMAND_NOTICE":     ["section 13(2)", "13(2)", "demand notice", "60 days", "discharge"],
    "OBJECTION":         ["representation", "objection", "reply", "aggrieved"],
    "BANK_REPLY":        ["13(3a)", "section 13(3a)", "considered your objection"],
    "POSSESSION_NOTICE": ["section 13(4)", "symbolic possession", "possession notice"],
    "SALE_NOTICE":       ["rule 8", "sale notice", "auction", "reserve price", "e-auction"],
    "VALUATION_REPORT":  ["valuation", "valuer", "fair market value", "distress value"],
    "LOAN_AGREEMENT":    ["loan agreement", "sanction letter", "terms and conditions"],
    "GUARANTEE":         ["guarantee", "guarantor", "personal guarantee"],
    "ACCOUNT_STATEMENT": ["account statement", "outstanding", "principal", "interest"],
    "UDYAM_CERT":        ["udyam", "msme", "ministry of micro"],
    "LEASE_DEED":        ["lease deed", "rent agreement", "tenancy agreement", "lessee"],
    "MORTGAGE_DEED":     ["mortgage deed", "mortgagor", "mortgagee", "equitable mortgage"],
    "DRT_ORDER":         ["drt order", "interim order", "tribunal order", "stay order"],
    "SALE_AGREEMENT":    ["agreement to sell", "agreement for sale", "ats", "sale agreement"],
}


def classify_document(first_500_chars: str) -> str:
    text_lower = first_500_chars.lower()
    scores = {}
    for doc_type, keywords in DOC_TYPE_KEYWORDS.items():
        scores[doc_type] = sum(1 for kw in keywords if kw in text_lower)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "OTHER"
