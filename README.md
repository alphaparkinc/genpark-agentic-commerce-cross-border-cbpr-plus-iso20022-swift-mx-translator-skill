# Cross-Border CBPR+ SWIFT MT to ISO 20022 MX Translator Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `translate_swift_mt_to_iso20022_mx`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Translates legacy SWIFT MT103/MT202 messages into CBPR+ compliant ISO 20022 pacs.008.001.08 XML, validating UETR, structured postal addresses, and charge bearer codes.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (Cross-Border Banking & SWIFT)`

## MCP Tool Specification
### `translate_swift_mt_to_iso20022_mx`
Parameters:
- `sender_bic` (str): Originating Bank Identifier Code (8 or 11 chars)
- `receiver_bic` (str): Instructed Bank Identifier Code (8 or 11 chars)
- `uetr_guid` (str): 36-char Unique End-to-end Transaction Reference (UUID)
- `currency` (str): ISO 4217 Currency Code (e.g. 'USD', 'EUR')
- `amount` (float): Interbank settlement amount
- `debtor_name` (str): Ordering customer / Debtor legal entity
- `creditor_iban` (str): Beneficiary IBAN or account number
- `creditor_name` (str): Beneficiary customer legal entity
- `charge_bearer` (str): Charge bearer code: 'DEBT', 'CRED', or 'SHAR'

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-cross-border-cbpr-plus-iso20022-swift-mx-translator-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-cross-border-cbpr-plus-iso20022-swift-mx-translator-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
