"""
Canonical guided procedures under the Telangana Cooperative Societies Act, 1964.
Provides structured workflows, statutory steps, timelines, and mandatory document checklists.
"""

from typing import Any, Dict, List, Optional


PROCEDURES_CATALOG: Dict[str, Dict[str, Any]] = {
    "registration": {
        "id": "registration",
        "title": "Registration of a New Cooperative Society",
        "act_reference": "Telangana Cooperative Societies Act, 1964 — Sections 6, 7 & 8",
        "authority": "Registrar / Deputy Registrar of Cooperative Societies of the District",
        "estimated_days": "60 to 90 days from submission",
        "summary": "Step-by-step procedure to promote, formulate bye-laws, deposit share capital, and officially register a primary cooperative society.",
        "eligibility": [
            "At least 10 eligible individuals from different families residing in the area of operation (or representative societies for federal bodies).",
            "Promoters must not be disqualified under Section 21 of the Act.",
            "Common economic or social objective adhering to cooperative principles with proven economic viability."
        ],
        "steps": [
            {
                "step_number": 1,
                "title": "Promoters Meeting & Chief Promoter Selection",
                "description": "Convene a preliminary meeting of at least 10 prospective members. Elect a Chief Promoter to sign applications, collect initial share capital, and liaise with the department.",
                "tips": "Record minutes of the preliminary meeting and have all founding members sign the attendance sheet."
            },
            {
                "step_number": 2,
                "title": "Drafting Model Bye-Laws & Economic Viability Scheme",
                "description": "Prepare proposed bye-laws specifying society name, registered address, objectives, share value, membership criteria, and governance structure in conformity with the Act.",
                "tips": "Ensure bye-laws do not conflict with the Act and include a realistic 3-year viability report."
            },
            {
                "step_number": 3,
                "title": "Opening Bank Account & Capital Deposit",
                "description": "Open a temporary share capital account in the District Cooperative Central Bank (DCCB) under the Chief Promoter's name and deposit initial share subscriptions and entrance fees.",
                "tips": "Obtain a formal bank certificate confirming deposit of share capital."
            },
            {
                "step_number": 4,
                "title": "Formal Application Submission to Registrar",
                "description": "Submit Form 'A' application in triplicate to the Deputy Registrar along with 4 copies of proposed bye-laws, bank certificate, promoters' ID/address proofs, and prescribed fee.",
                "tips": "The Registrar must dispose of the application or communicate objections within 90 days."
            }
        ],
        "required_documents": [
            "Application in Form 'A' signed by at least 10 promoters",
            "Four certified copies of proposed Bye-Laws signed by promoters",
            "Minutes of the Promoters Meeting appointing the Chief Promoter",
            "Bank balance certificate from DCCB showing share capital deposit",
            "Scheme showing economic soundness and viability of the society",
            "KYC documents (Aadhaar/Voter ID) and address proofs of all promoters",
            "Challan / Receipt of registration fee payment"
        ],
        "applicable_forms": ["Form 'A' (Application for Registration)", "Form 'B' (Certificate of Registration)"]
    },
    "agm": {
        "id": "agm",
        "title": "Convening Annual General Body Meeting (AGM) & Passing Accounts",
        "act_reference": "Telangana Cooperative Societies Act, 1964 — Section 30",
        "authority": "Managing Committee of the Society / Registrar",
        "estimated_days": "Within 6 months from close of cooperative financial year (by September 30)",
        "summary": "Statutory rules and procedures for convening the mandatory Annual General Meeting of members, presenting audit reports, and declaring dividends.",
        "eligibility": [
            "Conducted at least once every cooperative year.",
            "All active, non-defaulting members with voting rights are entitled to attend.",
            "Notice must be served to all members within statutory notice period."
        ],
        "steps": [
            {
                "step_number": 1,
                "title": "Managing Committee Resolution & Agenda Setting",
                "description": "The committee meets to fix the AGM date, time, and venue, and drafts the agenda covering annual report, audited accounts, budget, and dividend allocation.",
                "tips": "Pass committee resolution at least 25-30 days before the scheduled AGM date."
            },
            {
                "step_number": 2,
                "title": "Serving Statutory AGM Notice",
                "description": "Issue clear notice (typically 15 to 21 days as specified in society bye-laws) to every member via post, hand delivery with acknowledgement, and display on the notice board.",
                "tips": "Publish notice in local news circulation if membership exceeds 500."
            },
            {
                "step_number": 3,
                "title": "Verification of Quorum & Proceedings",
                "description": "Verify minimum quorum as required by bye-laws at meeting commencement. If quorum is not met within 30 minutes, adjourn as per statutory procedure.",
                "tips": "Maintain a strict signature register at the entrance to verify attendance and quorum."
            },
            {
                "step_number": 4,
                "title": "Adoption of Accounts & Filing with Registrar",
                "description": "Present annual accounts, statutory audit report, and committee report for approval. Record all resolutions and file a certified copy with the Registrar within 30 days.",
                "tips": "Failure to hold AGM within statutory time allows the Registrar to convene the meeting or take penal action under Section 30."
            }
        ],
        "required_documents": [
            "Notice of AGM with complete agenda and explanatory notes",
            "Member delivery proof / dispatch register / postal receipts",
            "Audited balance sheet and profit & loss statement for the preceding year",
            "Statutory auditor's report and compliance notes",
            "Annual administrative report of the managing committee",
            "Attendance register with member signatures",
            "Signed minutes of the General Body Meeting"
        ],
        "applicable_forms": ["Form of AGM Notice", "Annual Returns Filing Format"]
    },
    "elections": {
        "id": "elections",
        "title": "Conducting Managing Committee & Office Bearer Elections",
        "act_reference": "Telangana Cooperative Societies Act, 1964 — Section 31 & Election Rules",
        "authority": "State Cooperative Election Authority / Designated Election Officer",
        "estimated_days": "60 days process prior to committee term expiry",
        "summary": "Statutory election cycle for electing president, directors, and committee members under democratic supervision.",
        "eligibility": [
            "Members who have completed requisite qualifying period and are not in loan default.",
            "Candidates must satisfy eligibility criteria and reservations (SC/ST/BC/Women) under Section 31(1)."
        ],
        "steps": [
            {
                "step_number": 1,
                "title": "Appointment of Election Officer & Voter List Preparation",
                "description": "The Election Authority appoints an independent Election Officer. The committee prepares and submits the provisional electoral roll of eligible members.",
                "tips": "Provisional roll must exclude members disqualified under Section 21."
            },
            {
                "step_number": 2,
                "title": "Publication of Draft Voter Roll & Objections",
                "description": "Publish draft voter list on the society notice board. Allow statutory window (typically 7-10 days) for members to file claims and objections.",
                "tips": "The Election Officer must personally hear objections and publish the final voter roll."
            },
            {
                "step_number": 3,
                "title": "Election Notification & Nominations",
                "description": "Election Officer publishes calendar of events: nomination filing dates, scrutiny of nominations, withdrawal deadline, and final list of contesting candidates.",
                "tips": "Ensure valid proposer and seconder from eligible voters for each nomination paper."
            },
            {
                "step_number": 4,
                "title": "Polling, Counting & Declaration of Results",
                "description": "Conduct secret ballot polling on scheduled date. Count votes immediately following polling in presence of candidates/agents, declare results, and issue Election Certificates.",
                "tips": "Election disputes cannot stop polling; disputes must be filed post-election under Section 61."
            }
        ],
        "required_documents": [
            "Certified final electoral roll / voter list",
            "Election notification published by Election Officer",
            "Nomination forms with proposer/seconder declarations",
            "Affidavit of non-disqualification and asset disclosure",
            "Caste/Category certificates for reserved seats",
            "No-due certificates confirming absence of loan default",
            "Official certificate of election results issued by Election Officer"
        ],
        "applicable_forms": ["Nomination Paper Form", "Declaration of Election Result Form"]
    },
    "dispute_filing": {
        "id": "dispute_filing",
        "title": "Filing a Dispute before Registrar / Cooperative Tribunal",
        "act_reference": "Telangana Cooperative Societies Act, 1964 — Section 61",
        "authority": "Registrar of Cooperative Societies / Telangana Cooperative Tribunal",
        "estimated_days": "Notice within 15-30 days; adjudication within 6-12 months",
        "summary": "Statutory legal remedy for disputes touching the constitution, management, elections, or business of a cooperative society.",
        "eligibility": [
            "Any member, past member, person claiming through member, or society.",
            "Dispute must fall within Section 61 jurisdiction (ousting civil courts).",
            "Filed within the statutory period of limitation specified under Section 61(2)."
        ],
        "steps": [
            {
                "step_number": 1,
                "title": "Legal Representation & Demand for Justice",
                "description": "Serve a formal written grievance / legal representation to the society committee or registrar setting out facts, violations, and requested relief.",
                "tips": "Send via Registered Post with Acknowledgement Due (RPAD) and preserve the postal receipt and delivery proof."
            },
            {
                "step_number": 2,
                "title": "Drafting Formal Dispute Petition under Section 61",
                "description": "Draft petition stating facts, grounds of illegality, specific statutory violations of the Act/bye-laws, and explicit prayers/reliefs sought.",
                "tips": "Attach verified affidavit and pay the requisite court fee / challan."
            },
            {
                "step_number": 3,
                "title": "Filing with Registrar / Tribunal & Interim Relief",
                "description": "File the petition in required duplicate sets with the competent authority. If urgent (e.g. stopping illegal election or illegal expulsion), file an interim stay application.",
                "tips": "The Registrar may adjudicate directly or refer the dispute to a designated Arbitrator."
            },
            {
                "step_number": 4,
                "title": "Notice to Opponents, Evidence & Award",
                "description": "Official notices are issued to opposite parties to file counter-affidavits. Evidence is presented, arguments are heard, and a binding Award / Order is pronounced.",
                "tips": "An appeal against the Registrar's order lies to the Cooperative Tribunal under Section 76."
            }
        ],
        "required_documents": [
            "Dispute Petition in prescribed format with supporting affidavit",
            "Copy of society bye-laws and registration details",
            "Proof of membership (share certificate, passbook, receipt)",
            "Impugned resolution, notice, or order being challenged",
            "Copy of prior representation submitted and postal acknowledgement",
            "Court fee challan / payment receipt"
        ],
        "applicable_forms": ["Dispute Application Form under Section 61", "Interim Stay Petition Format"]
    },
    "membership": {
        "id": "membership",
        "title": "Membership Admission, Transfer & Rejection Appeal",
        "act_reference": "Telangana Cooperative Societies Act, 1964 — Section 19",
        "authority": "Society Managing Committee / Registrar (Appellate Authority)",
        "estimated_days": "60 days for committee decision; 60 days for appeal",
        "summary": "Procedure to apply for membership, statutory open membership doctrine, and appeal process if membership is illegally refused.",
        "eligibility": [
            "Individual competent to contract, residing or owning property in society area of operation.",
            "Fulfills eligibility criteria in bye-laws and does not run a conflicting competitive business."
        ],
        "steps": [
            {
                "step_number": 1,
                "title": "Submission of Membership Application",
                "description": "Submit Form 'I' membership application to the society secretary with entrance fee, prescribed share capital subscription, and identity proofs.",
                "tips": "Always obtain a signed acknowledgement receipt with date and seal."
            },
            {
                "step_number": 2,
                "title": "Statutory 60-Day Society Consideration Window",
                "description": "The managing committee must consider the application within 60 days from receipt and communicate its decision. If not communicated within 60 days, deeming provisions may apply.",
                "tips": "A society cannot refuse membership without recording cogent, valid reasons under Section 19."
            },
            {
                "step_number": 3,
                "title": "Communication of Rejection with Reasons",
                "description": "If rejected, the society must communicate the rejection order in writing along with explicit reasons within 15 days of the decision.",
                "tips": "Verify whether the reason violates the open membership principle of the Act."
            },
            {
                "step_number": 4,
                "title": "Statutory Appeal to the Registrar",
                "description": "If membership is rejected or ignored, file an appeal under Section 19(3) to the Deputy Registrar within 60 days of communication or expiry of the initial window.",
                "tips": "The Registrar has statutory authority to direct the society to admit the applicant."
            }
        ],
        "required_documents": [
            "Duly filled and signed Membership Application Form",
            "Receipt or proof of payment for entrance fee and share capital",
            "KYC documents (Aadhaar, Voter ID, PAN)",
            "Proof of residence or land ownership in the society operational jurisdiction",
            "Official acknowledgement slip from society",
            "Copy of rejection order (if appeal is being filed)"
        ],
        "applicable_forms": ["Membership Application Form 'I'", "Statutory Appeal Memo under Section 19(3)"]
    },
    "bylaw_amendment": {
        "id": "bylaw_amendment",
        "title": "Amendment of Society Bye-Laws & Official Registration",
        "act_reference": "Telangana Cooperative Societies Act, 1964 — Section 16",
        "authority": "General Body of the Society & Registrar of Cooperative Societies",
        "estimated_days": "60 days for Registrar approval",
        "summary": "Procedure for modifying, adding, or deleting bye-laws of an existing cooperative society and registering changes with the Registrar.",
        "eligibility": [
            "Proposed amendment must not violate the Telangana Cooperative Societies Act or Rules.",
            "Requires special General Body resolution passed with statutory 2/3rd majority of members present and voting."
        ],
        "steps": [
            {
                "step_number": 1,
                "title": "Drafting Amendment & Managing Committee Resolution",
                "description": "Managing committee formulates proposed amendments with reasons and justification table showing existing vs proposed bye-law clauses.",
                "tips": "Issue special General Body meeting notice giving at least 15 clear days notice."
            },
            {
                "step_number": 2,
                "title": "Passing Resolution in General Body Meeting",
                "description": "Convene General Body meeting with requisite quorum. Pass the amendment resolution with at least 2/3rd majority of members present and voting.",
                "tips": "Record exact voting numbers and verbatim amendment text in the minutes book."
            },
            {
                "step_number": 3,
                "title": "Application Filing with Registrar",
                "description": "Submit application to the Registrar within 30 days of the meeting along with 4 copies of the amendment signed by committee officers, notice copy, and minutes.",
                "tips": "Attach certificate confirming compliance with bye-law amendment rules."
            },
            {
                "step_number": 4,
                "title": "Registration & Certificate by Registrar",
                "description": "Registrar scrutinizes the amendment. If satisfied, registers the amendment and issues a Certificate of Registration of Amendment within 60 days.",
                "tips": "An amendment takes legal effect only upon official registration by the Registrar."
            }
        ],
        "required_documents": [
            "Application for registration of amendment in prescribed Form",
            "Four copies of the amendment resolution with existing vs proposed comparative table",
            "Notice convening the General Body meeting with dispatch proofs",
            "Certified copy of General Body minutes with voting breakdown",
            "Challan / Receipt of statutory amendment fee"
        ],
        "applicable_forms": ["Form 'C' (Application for Amendment of Bye-Laws)", "Certificate of Amendment Registration"]
    },
    "audit_inspection": {
        "id": "audit_inspection",
        "title": "Statutory Audit, Inspection of Books & Special Inquiry",
        "act_reference": "Telangana Cooperative Societies Act, 1964 — Sections 50, 51, 52 & 60",
        "authority": "Director of Cooperative Audit / Registrar / Surcharge Officer",
        "estimated_days": "Annual cycle (within 6 months from close of cooperative year)",
        "summary": "Statutory audit procedure, rights of members to demand special inspection of books, and surcharge proceedings against defaulting officers.",
        "eligibility": [
            "Mandatory for all registered cooperative societies annually.",
            "Special inquiry can be ordered on application of 1/3rd committee members or 1/5th total members."
        ],
        "steps": [
            {
                "step_number": 1,
                "title": "Closing Accounts & Audit Preparation",
                "description": "Society secretary closes annual accounts by April 30 and prepares balance sheet, profit & loss statement, and schedules for audit.",
                "tips": "Submit completed books to the Departmental Auditor / Chartered Accountant panel."
            },
            {
                "step_number": 2,
                "title": "Statutory Audit Examination & Report",
                "description": "The appointed auditor examines cash books, vouchers, securities, loans, and assets, prepares the audit report, and assigns audit classification (A/B/C/D).",
                "tips": "Auditor must complete audit and submit report within statutory timeline."
            },
            {
                "step_number": 3,
                "title": "Audit Rectification Report",
                "description": "The managing committee must prepare a detailed Audit Rectification Report remedying any defects/objections within 3 months and submit to Registrar.",
                "tips": "Place audit report and rectification notes before the next AGM."
            },
            {
                "step_number": 4,
                "title": "Special Inquiry & Surcharge (if irregularities found)",
                "description": "If severe embezzlement or losses are discovered, Registrar orders inquiry under Section 51 and institutes surcharge recovery under Section 60 against responsible officers.",
                "tips": "Surcharge orders are enforceable as civil court decrees."
            }
        ],
        "required_documents": [
            "Complete cash books, day books, and general ledgers",
            "Loan registers, mortgage deeds, and security bonds",
            "Bank reconciliation statements and DCCB balance confirmations",
            "Vouchers, payment receipts, and procurement invoices",
            "Minutes of managing committee and General Body meetings",
            "Audit Rectification Compliance Report"
        ],
        "applicable_forms": ["Annual Audit Schedule Form", "Audit Rectification Report Form"]
    }
}


def get_all_procedures() -> List[Dict[str, Any]]:
    """Return list of all 7 canonical procedure summary cards."""
    return [
        {
            "id": p["id"],
            "title": p["title"],
            "act_reference": p["act_reference"],
            "authority": p["authority"],
            "estimated_days": p["estimated_days"],
            "summary": p["summary"],
            "step_count": len(p["steps"]),
            "document_count": len(p["required_documents"]),
        }
        for p in PROCEDURES_CATALOG.values()
    ]


def get_procedure_by_id(proc_id: str) -> Optional[Dict[str, Any]]:
    """Return full procedure details by ID."""
    if not proc_id:
        return None
    return PROCEDURES_CATALOG.get(proc_id.strip().lower())


def match_procedure_by_query(query: str) -> Optional[Dict[str, Any]]:
    """Heuristically match a user's question to a guided procedure."""
    q = query.lower()
    if any(k in q for k in ["register", "registration", "new society", "form a society", "start a society", "form a coop"]):
        return PROCEDURES_CATALOG["registration"]
    if any(k in q for k in ["election", "vote", "voter list", "ballot", "nominat", "electoral roll", "contest"]):
        return PROCEDURES_CATALOG["elections"]
    if any(k in q for k in ["agm", "general body", "annual meeting", "general meeting", "annual general"]):
        return PROCEDURES_CATALOG["agm"]
    if any(k in q for k in ["dispute", "tribunal", "section 61", "arbitrat", "file a case", "file dispute"]):
        return PROCEDURES_CATALOG["dispute_filing"]
    if any(k in q for k in ["membership", "become a member", "join", "admit", "rejected membership", "form i"]):
        return PROCEDURES_CATALOG["membership"]
    if any(k in q for k in ["amend bye-law", "amendment", "modify bye-laws", "byelaw change", "form c"]):
        return PROCEDURES_CATALOG["bylaw_amendment"]
    if any(k in q for k in ["audit", "inspection", "surcharge", "section 50", "section 51", "section 60"]):
        return PROCEDURES_CATALOG["audit_inspection"]
    return None


if __name__ == "__main__":
    print(f"Loaded {len(PROCEDURES_CATALOG)} canonical procedures.")
    for p in get_all_procedures():
        print(f" - [{p['id']}] {p['title']}")
