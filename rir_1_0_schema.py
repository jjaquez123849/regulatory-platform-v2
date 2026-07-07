RIR_1_0_SCHEMA = {
    "type": "object",
    "required": [
        "rir_version",
        "document",
        "request",
        "evidence",
        "ai_analysis",
        "validation",
    ],
    "properties": {
        "rir_version": {"type": "string", "const": "1.0"},

        "document": {"type": "object"},
        "authorities": {"type": "array", "items": {"type": "object"}},
        "authority_relationships": {"type": "array", "items": {"type": "object"}},
        "authority_chain": {"type": "object"},
        "legal_instruments": {"type": "array", "items": {"type": "object"}},
        "request": {"type": "object"},
        "parties": {"type": "array", "items": {"type": "object"}},
        "party_groups": {"type": "array", "items": {"type": "object"}},
        "party_relationships": {"type": "array", "items": {"type": "object"}},
        "requested_items": {"type": "array", "items": {"type": "object"}},
        "attachments": {"type": "array", "items": {"type": "object"}},
        "evidence": {"type": "array", "items": {"type": "object"}},
        "ai_analysis": {"type": "object"},
        "validation": {"type": "object"},
    },
}
