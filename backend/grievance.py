"""
Statutory Grievance & Dispute Redressal Engine for Sahakaar Saathi.
Anchored to the Telangana Cooperative Societies Act, 1964.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


GRIEVANCE_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "MEMBERSHIP_DENIAL": {
        "id": "MEMBERSHIP_DENIAL",
        "title": "Arbitrary Denial, Delay, or Illegal Refusal of Membership",
        "act_sections": [
            "Section 19 (Right of Admission to Membership & Appeals)",
            "Section 21 (Statutory Disqualifications for Membership)"
        ],
        "authority": "The Deputy Registrar / Divisional Cooperative Officer",
        "limitation_period": "Within 60 days from communication of refusal or expiry of 60-day deeming window",
        "court_fee": "Nominal departmental fee / Challan as prescribed",
        "summary": "Complaint when a cooperative society refuses membership application without communicating valid statutory reasons under open membership principles.",
        "sample_relief": "Issue an order directing the society to immediately admit the complainant as a member with all statutory voting, dividend, and participation rights."
    },
    "ELECTION_MALPRACTICE": {
        "id": "ELECTION_MALPRACTICE",
        "title": "Election Irregularities, Voter List Tampering & Model Code Violations",
        "act_sections": [
            "Section 31 (Constitution of Managing Committee & Conduct of Elections)",
            "Section 61 (Election Disputes to be referred to Registrar/Tribunal)"
        ],
        "authority": "The State Cooperative Election Authority / Cooperative Tribunal",
        "limitation_period": "Within 30 days from declaration of election results",
        "court_fee": "Dispute petition challan under Section 61",
        "summary": "Disputes regarding deliberate omission of eligible members from voter rolls, illegal nomination rejection, or polling irregularities during elections.",
        "sample_relief": "Order stay on declaration of results, direction to include lawful members in the electoral roll, and conduct fresh inquiry into polling malpractices under Section 61."
    },
    "FINANCIAL_IRREGULARITY": {
        "id": "FINANCIAL_IRREGULARITY",
        "title": "Misappropriation of Funds, Embezzlement & Surcharge Recovery",
        "act_sections": [
            "Section 51 (Statutory Inquiry by Registrar)",
            "Section 52 (Inspection of Books and Records)",
            "Section 60 (Surcharge Proceedings to Recover Misappropriated Assets)"
        ],
        "authority": "The Registrar of Cooperative Societies / District Collector",
        "limitation_period": "Within 6 years from the date of the act or discovery of embezzlement",
        "court_fee": "Application under Section 51 / Representation",
        "summary": "Grievance against managing committee or office bearers for fund embezzlement, unauthorized loans, fake procurement bills, or fraudulent expenses.",
        "sample_relief": "Immediate institution of statutory inquiry under Section 51, attachment of assets, and surcharge proceedings under Section 60 to recover misappropriated society funds with interest."
    },
    "RECORDS_DENIAL": {
        "id": "RECORDS_DENIAL",
        "title": "Denial of Right to Inspect Books, Accounts & General Body Minutes",
        "act_sections": [
            "Section 114 (Statutory Right of Members to Inspect Society Records)",
            "Section 115 (Supply of Certified Copies of Documents)"
        ],
        "authority": "The Deputy Registrar / Arbitrator",
        "limitation_period": "Immediate upon refusal (within 14 days of written application)",
        "court_fee": "Copying fees as per bye-laws",
        "summary": "Refusal by President, Secretary, or Managing Committee to furnish copies or allow physical inspection of audited balance sheets, member registers, or meeting minutes.",
        "sample_relief": "Issue summons directing immediate production of society records for inspection and penal action against defaulting officers under the Act."
    },
    "FAILURE_TO_HOLD_AGM": {
        "id": "FAILURE_TO_HOLD_AGM",
        "title": "Failure to Convene Mandatory Annual General Body Meeting (AGM)",
        "act_sections": [
            "Section 30 (General Body Meetings and Statutory Annual Periodicity)",
            "Section 34 (Supersession of Committee for Persistent Default)"
        ],
        "authority": "The Registrar of Cooperative Societies",
        "limitation_period": "Post September 30 (close of statutory 6-month window)",
        "court_fee": "Statutory representation format",
        "summary": "Managing committee failed to conduct the mandatory Annual General Body Meeting within 6 months from close of the cooperative financial year.",
        "sample_relief": "Issue official directive ordering a General Body meeting to be convened under Departmental supervision, or appoint a Special Officer under Section 34."
    },
    "ARBITRARY_EXPULSION": {
        "id": "ARBITRARY_EXPULSION",
        "title": "Unlawful Expulsion or Disqualification of a Member",
        "act_sections": [
            "Section 21A (Expulsion of Members & Mandatory 2/3rd Majority at General Body)",
            "Section 19(3) (Appeal against Cessation of Membership)"
        ],
        "authority": "The Registrar of Cooperative Societies / Cooperative Tribunal",
        "limitation_period": "Within 60 days of the expulsion resolution",
        "court_fee": "Appeal fee under Section 19(3)",
        "summary": "Managing committee arbitrarily expelling a member without general body special resolution, prior show cause notice, or hearing in breach of natural justice.",
        "sample_relief": "Declare the expulsion resolution null and void, restore full membership status, and restrain the society from obstructing member participation."
    },
    "UNLAWFUL_LOAN_RECOVERY": {
        "id": "UNLAWFUL_LOAN_RECOVERY",
        "title": "Illegal Surcharge, Coercive Loan Recovery, or Interest Overcharging",
        "act_sections": [
            "Section 70 (Attachment of Property before Award)",
            "Section 71 (Recovery of Debts under Certificates Issued by Registrar)"
        ],
        "authority": "The Registrar / Sale Officer / Cooperative Tribunal",
        "limitation_period": "Within 30 days of receiving coercive attachment notice",
        "court_fee": "Objection petition fee",
        "summary": "Coercive attachment or auction of agricultural/residential property without following statutory notice procedure, overcharging interest beyond approved bye-laws.",
        "sample_relief": "Stay execution of attachment proceedings, direct re-conciliation of loan ledger accounts, and enforce statutory interest caps."
    },
    "GENERAL_DISPUTE": {
        "id": "GENERAL_DISPUTE",
        "title": "General Dispute Touching Business, Management or Constitution of Society",
        "act_sections": [
            "Section 61 (Disputes to be Referred Exclusively to Registrar)",
            "Section 62 (Adjudication and Award by Arbitrator)"
        ],
        "authority": "The Registrar of Cooperative Societies / Appointed Arbitrator",
        "limitation_period": "Within statutory limitation period under Section 61(2)",
        "court_fee": "Arbitration fee challan",
        "summary": "Any dispute touching the business, assets, employment, or management of a cooperative society that is barred from ordinary civil court jurisdiction.",
        "sample_relief": "Formal referral of dispute to statutory arbitration under Section 62 and pronouncement of binding legal award."
    }
}


class GrievanceDraftRequest(BaseModel):
    complainant_name: str = Field(..., description="Full name of complainant")
    complainant_address: str = Field(..., description="Residential address")
    complainant_phone: Optional[str] = Field(None, description="Contact phone number")
    complainant_membership_no: Optional[str] = Field(None, description="Membership ID / Share Certificate No. if member")
    society_name: str = Field(..., description="Full legal name of the cooperative society")
    society_address: str = Field(..., description="Address of registered society office")
    society_reg_no: Optional[str] = Field(None, description="Registration number of society if known")
    category_id: str = Field(..., description="Category identifier from GRIEVANCE_CATEGORIES")
    statement_of_facts: str = Field(..., description="Detailed narration of incident, dates, and actions")
    relief_sought: Optional[str] = Field(None, description="Specific prayers or demands")
    jurisdiction: str = Field("Telangana", description="State jurisdiction")


class GrievanceDraftResponse(BaseModel):
    category_id: str
    category_title: str
    act_citations: List[str]
    addressed_to: str
    limitation_period: str
    subject_line: str
    formal_letter: str
    required_enclosures: List[str]


def get_grievance_categories() -> List[Dict[str, Any]]:
    """Return list of all 8 statutory grievance categories."""
    return list(GRIEVANCE_CATEGORIES.values())


def generate_grievance_draft(request: GrievanceDraftRequest) -> GrievanceDraftResponse:
    """
    Generate a formal statutory representation under the Telangana Cooperative Societies Act, 1964.
    """
    cat_key = request.category_id.upper().strip()
    category = GRIEVANCE_CATEGORIES.get(cat_key, {
        "id": "GENERAL_DISPUTE",
        "title": "General Cooperative Dispute / Grievance",
        "act_sections": ["Section 61 (Disputes to be referred to Registrar)"],
        "authority": "The Deputy Registrar of Cooperative Societies",
        "limitation_period": "As prescribed under Section 61(2)",
        "sample_relief": "Inquiry and statutory intervention under the provisions of the Act."
    })

    current_date = datetime.now().strftime("%d-%B-%Y")
    membership_line = (
        f"Membership / Share No.: {request.complainant_membership_no}"
        if request.complainant_membership_no
        else "Status: Aggrieved Applicant / Member"
    )
    society_reg_line = (
        f"(Registration No.: {request.society_reg_no})"
        if request.society_reg_no
        else ""
    )

    relief = request.relief_sought or category.get("sample_relief", "Appropriate statutory inquiry and remedial orders.")

    subject_line = (
        f"FORMAL STATUTORY REPRESENTATION & PETITION under {', '.join(category['act_sections'])} "
        f"of the Telangana Cooperative Societies Act, 1964 regarding {category['title'].lower()} "
        f"in respect of '{request.society_name}'."
    )

    letter = f"""BEFORE THE COMPETENT STATUTORY AUTHORITY:
{category['authority']}
Department of Cooperation, Government of Telangana

DATE: {current_date}

FROM:
{request.complainant_name}
{membership_line}
Address: {request.complainant_address}
Phone: {request.complainant_phone or "N/A"}

AGAINST / IN THE MATTER OF:
The Managing Committee / President / Secretary,
{request.society_name} {society_reg_line}
Address: {request.society_address}

SUBJECT:
{subject_line}

RESPECTED SIR/MADAM,

I, the undersigned {request.complainant_name}, state and submit on solemn affirmation as follows:

1. JURISDICTION & STANDING:
   The respondent society, namely '{request.society_name}', is a registered cooperative society functioning within your statutory jurisdiction, governed by the provisions of the Telangana Cooperative Societies Act, 1964, the Rules framed thereunder, and its registered Bye-Laws. I am an aggrieved party having direct locus standi in this matter.

2. NATURE OF GRIEVANCE & STATUTORY CITATIONS:
   The subject matter relates to: {category['title']}.
   This grievance falls squarely under the statutory remedies provided under {", ".join(category['act_sections'])} of the Telangana Cooperative Societies Act, 1964.

3. STATEMENT OF FACTS:
{request.statement_of_facts}

4. INACTION & ILLEGALITY:
   The aforementioned act/omission committed by the management of the society is arbitrary, discriminatory, and in blatant violation of statutory provisions, principles of natural justice, and democratic cooperative governance. Prior informal requests or representations made by me have yielded no remedial action.

5. PRAYER / SPECIFIC RELIEFS SOUGHT:
   In light of the aforesaid facts and legal provisions, it is respectfully prayed that your esteemed office may be pleased to:
   a) Take immediate official cognizance of this representation under the Act;
   b) {relief};
   c) Direct the society management to place on record all relevant registers, minutes, and audited files pertaining to this matter;
   d) Pass such further interim or final order(s) as deemed fit and proper to secure the ends of justice.

VERIFICATION:
I, {request.complainant_name}, do hereby declare that the facts stated in paragraphs 1 to 5 above are true and correct to the best of my knowledge, information, and belief.


Yours faithfully,


({request.complainant_name})
Complainant / Aggrieved Party

Copy submitted for information and necessary action to:
1. The Managing Committee / Secretary, {request.society_name}
2. Office Copy / Records
"""

    enclosures = [
        "Photocopy of Complainant's Identity Proof (Aadhaar / Voter ID / PAN Card)",
        "Proof of Membership or Proof of Membership Application / Payment Receipt",
        "Copy of society receipts, communications, rejection letter, or notices (if applicable)",
        "Postal receipt / Delivery acknowledgement of prior representations (if any)",
        "Affidavit in support of petition (if required by authority)"
    ]

    return GrievanceDraftResponse(
        category_id=category["id"],
        category_title=category["title"],
        act_citations=category["act_sections"],
        addressed_to=category["authority"],
        limitation_period=category.get("limitation_period", "As prescribed"),
        subject_line=subject_line,
        formal_letter=letter,
        required_enclosures=enclosures
    )


if __name__ == "__main__":
    print(f"Loaded {len(GRIEVANCE_CATEGORIES)} grievance categories.")
    for k, v in GRIEVANCE_CATEGORIES.items():
        print(f" - [{k}] {v['title']}")
