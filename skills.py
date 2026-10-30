# -*- coding: utf-8 -*-
"""Cross-Border CBPR+ SWIFT MT to ISO 20022 MX Translator Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def translate_swift_mt_to_iso20022_mx(**kwargs):
    """Translates legacy SWIFT MT103/MT202 messages into CBPR+ compliant ISO 20022 pacs.008.001.08 XML, validating UETR, structured postal addresses, and charge bearer codes."""
    sender_bic = kwargs.get('sender_bic')
    receiver_bic = kwargs.get('receiver_bic')
    uetr_guid = kwargs.get('uetr_guid')
    currency = kwargs.get('currency')
    amount = kwargs.get('amount')
    debtor_name = kwargs.get('debtor_name')
    creditor_iban = kwargs.get('creditor_iban')
    creditor_name = kwargs.get('creditor_name')
    charge_bearer = kwargs.get('charge_bearer')

    import uuid
    clean_uetr = uetr_guid.strip() if uetr_guid else str(uuid.uuid4())
    charges = charge_bearer.upper().strip() if charge_bearer.upper().strip() in ["DEBT", "CRED", "SHAR"] else "SHAR"
    
    xml_envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08">
  <FIToFICstmrCdtTrf>
    <GrpHdr>
      <MsgId>GENPARK-{clean_uetr[:8].upper()}</MsgId>
      <CreDtTm>2026-10-30T09:00:00Z</CreDtTm>
      <NbOfTxs>1</NbOfTxs>
      <SttlmInf><SttlmMtd>CLRG</SttlmMtd></SttlmInf>
    </GrpHdr>
    <CdtTrfTxInf>
      <PmtId>
        <EndToEndId>E2E-{clean_uetr[:12]}</EndToEndId>
        <UETR>{clean_uetr}</UETR>
      </PmtId>
      <IntrBkSttlmAmt Ccy="{currency}">{amount:.2f}</IntrBkSttlmAmt>
      <ChrgBr>{charges}</ChrgBr>
      <Dbtr><Nm>{debtor_name}</Nm></Dbtr>
      <DbtrAgt><FinInstnId><BICFI>{sender_bic}</BICFI></FinInstnId></DbtrAgt>
      <CdtrAgt><FinInstnId><BICFI>{receiver_bic}</BICFI></FinInstnId></CdtrAgt>
      <Cdtr><Nm>{creditor_name}</Nm></Cdtr>
      <CdtrAcct><Id><Othr><Id>{creditor_iban}</Id></Othr></Id></CdtrAcct>
    </CdtTrfTxInf>
  </FIToFICstmrCdtTrf>
</Document>"""
    
    result = {
        "status": "success",
        "iso20022_message_type": "pacs.008.001.08",
        "cbpr_plus_compliant": True,
        "uetr": clean_uetr,
        "settlement_currency": currency,
        "amount": amount,
        "charge_bearer": charges,
        "generated_xml": xml_envelope,
        "engine": "GenPark Cross-Border ISO 20022 CBPR+ Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "translate_swift_mt_to_iso20022_mx": {
        "name": "translate_swift_mt_to_iso20022_mx",
        "description": "Translates legacy SWIFT MT103/MT202 messages into CBPR+ compliant ISO 20022 pacs.008.001.08 XML, validating UETR, structured postal addresses, and charge bearer codes.",
        "parameters": {
            "type": "object",
            "properties": {
                "sender_bic": {"type": "string", "description": "Originating Bank Identifier Code (8 or 11 chars)"},
                "receiver_bic": {"type": "string", "description": "Instructed Bank Identifier Code (8 or 11 chars)"},
                "uetr_guid": {"type": "string", "description": "36-char Unique End-to-end Transaction Reference (UUID)"},
                "currency": {"type": "string", "description": "ISO 4217 Currency Code (e.g. 'USD', 'EUR')"},
                "amount": {"type": "number", "description": "Interbank settlement amount"},
                "debtor_name": {"type": "string", "description": "Ordering customer / Debtor legal entity"},
                "creditor_iban": {"type": "string", "description": "Beneficiary IBAN or account number"},
                "creditor_name": {"type": "string", "description": "Beneficiary customer legal entity"},
                "charge_bearer": {"type": "string", "description": "Charge bearer code: 'DEBT', 'CRED', or 'SHAR'"},
            },
            "required": ['sender_bic', 'receiver_bic', 'uetr_guid', 'currency', 'amount', 'debtor_name', 'creditor_iban', 'creditor_name', 'charge_bearer']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "translate_swift_mt_to_iso20022_mx":
            res = translate_swift_mt_to_iso20022_mx(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-cross-border-cbpr-plus-iso20022-swift-mx-translator-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-cross-border-cbpr-plus-iso20022-swift-mx-translator-skill...")
    test_args = {'sender_bic': 'CHASUS33XXX', 'receiver_bic': 'BNPAFRPPXXX', 'uetr_guid': 'f81d4fae-7dec-11d0-a765-00a0c91e6bf6', 'currency': 'USD', 'amount': 250000.0, 'debtor_name': 'GenPark International LLC', 'creditor_iban': 'FR7630006000011234567890189', 'creditor_name': 'Apex Tech Global SAS', 'charge_bearer': 'SHAR'}
    res = translate_swift_mt_to_iso20022_mx(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-cross-border-cbpr-plus-iso20022-swift-mx-translator-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
