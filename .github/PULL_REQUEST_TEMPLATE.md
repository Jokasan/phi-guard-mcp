## Summary

Describe the change and why it is needed.

## Impact

- [ ] PHI detection rules
- [ ] Redaction output
- [ ] Audit or validation output
- [ ] CLI behavior
- [ ] MCP behavior
- [ ] Documentation only

## Tests

List the commands or checks run.

```bash
python -m pytest -q
ruff check .
phi-guard gate --config .phi-guard.toml
```

## Privacy and Safety

- [ ] This PR uses synthetic data only.
- [ ] This PR does not include real PHI, credentials, private emails, private IPs, or account tokens.
- [ ] This PR does not add diagnosis, treatment, triage, medication, clinical risk scoring, or HIPAA compliance claims.
