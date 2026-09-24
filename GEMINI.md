# Vlada Health MCP

Vlada serves measured US healthcare data: hospital and payer negotiated prices, Medicare fee-for-service, Medicare Advantage benefits, Star ratings and enrollment, Part D, the ACA Marketplace, Medicaid managed-care enrollment, providers, quality and drugs.

How to use it well:
- Start with `find_data_sources`, then `describe_data_source`, then a typed tool (`get_pbp_benefit`, `get_stars`, `get_enrollment`, `get_negotiated_rate`, `compare_hospital_rates`) or `query_substrate` for read-only SQL.
- Issue independent calls in parallel. Pin a year on annual tables and a state on hospital price tables.
- Every answer carries its source, vintage, method and caveats. Quote them. A refusal is not an absence: follow its `recover_with`.
- Never blend payment bases in one median (fee schedule, per diem, percent of charge), and never mix employer-plan prices with Medicare Advantage.
