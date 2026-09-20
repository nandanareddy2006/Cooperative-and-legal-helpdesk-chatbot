"""
ReportLab PDF Generation Engine for Sahakaar Saathi.
Generates print-ready, legally formatted documents:
1. Statutory Grievance & Representation Petitions
2. Step-by-Step Guided Procedure Manuals & Checklists
3. Legal Advice & Advisory Reports
"""

import io
from datetime import datetime
from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page numbers and official footer."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))

        # Footer Line
        self.setStrokeColor(colors.HexColor("#004c43"))
        self.setLineWidth(0.75)
        self.line(40, 42, 555, 42)

        # Footer Text
        footer_text = "Sahakaar Saathi — Telangana Cooperative Legal & Governance Helpdesk"
        self.drawString(40, 30, footer_text)

        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 30, page_str)

        self.restoreState()


def get_custom_styles():
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#004c43"),
        alignment=1, # Center
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#2a524a"),
        alignment=1,
        spaceAfter=10
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#004c43"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#222222"),
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        "DocBodyBold",
        parent=body_style,
        fontName="Helvetica-Bold"
    )

    legal_clause = ParagraphStyle(
        "LegalClause",
        parent=body_style,
        fontSize=9,
        leading=13,
        leftIndent=14,
        spaceAfter=5
    )

    meta_label = ParagraphStyle(
        "MetaLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#004c43")
    )

    meta_val = ParagraphStyle(
        "MetaVal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#333333")
    )

    return {
        "title": title_style,
        "subtitle": subtitle_style,
        "h2": h2_style,
        "body": body_style,
        "body_bold": body_bold,
        "clause": legal_clause,
        "meta_label": meta_label,
        "meta_val": meta_val
    }


def generate_grievance_pdf(
    draft_response_data: Dict[str, Any],
    request_data: Dict[str, Any]
) -> bytes:
    """
    Generate an official, statutory grievance petition PDF under Telangana Cooperative Societies Act, 1964.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=55
    )

    styles = get_custom_styles()
    story = []

    # 1. Header Banner
    header_data = [
        [
            Paragraph("<b>GOVERNMENT OF TELANGANA — DEPARTMENT OF COOPERATION</b>", styles["title"]),
        ],
        [
            Paragraph("STATUTORY REPRESENTATION & DISPUTE PETITION", styles["subtitle"])
        ]
    ]
    header_table = Table(header_data, colWidths=[515])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0f8f5")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#004c43")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    # 2. Key Metadata Summary Table
    complainant_name = request_data.get("complainant_name", "N/A")
    society_name = request_data.get("society_name", "N/A")
    cat_title = draft_response_data.get("category_title", "Cooperative Grievance")
    citations = ", ".join(draft_response_data.get("act_citations", ["Telangana Cooperative Societies Act, 1964"]))
    authority = draft_response_data.get("addressed_to", "Competent Cooperative Authority")
    date_str = datetime.now().strftime("%d-%B-%Y")

    meta_table_data = [
        [
            Paragraph("<b>Filing Date:</b>", styles["meta_label"]),
            Paragraph(date_str, styles["meta_val"]),
            Paragraph("<b>Jurisdiction:</b>", styles["meta_label"]),
            Paragraph("State of Telangana", styles["meta_val"])
        ],
        [
            Paragraph("<b>Complainant:</b>", styles["meta_label"]),
            Paragraph(complainant_name, styles["meta_val"]),
            Paragraph("<b>Membership ID:</b>", styles["meta_label"]),
            Paragraph(request_data.get("complainant_membership_no") or "Aggrieved Member/Applicant", styles["meta_val"])
        ],
        [
            Paragraph("<b>Respondent Society:</b>", styles["meta_label"]),
            Paragraph(society_name, styles["meta_val"]),
            Paragraph("<b>Reg. No:</b>", styles["meta_label"]),
            Paragraph(request_data.get("society_reg_no") or "Registered Primary Society", styles["meta_val"])
        ],
        [
            Paragraph("<b>Authority:</b>", styles["meta_label"]),
            Paragraph(authority, styles["meta_val"]),
            Paragraph("<b>Statute:</b>", styles["meta_label"]),
            Paragraph(citations, styles["meta_val"])
        ]
    ]

    meta_table = Table(meta_table_data, colWidths=[95, 160, 95, 165])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fafdfb")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cde3db")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # 3. Formal Addressee Block
    addressee_text = f"""<b>BEFORE THE COMPETENT STATUTORY AUTHORITY:</b><br/>
{authority}<br/>
Department of Cooperation, Government of Telangana"""
    story.append(Paragraph(addressee_text, styles["body"]))
    story.append(Spacer(1, 6))

    # 4. Subject Line
    subject_text = f"<b>SUBJECT:</b> {draft_response_data.get('subject_line', 'Formal representation regarding cooperative grievance.')}"
    sub_table = Table([[Paragraph(subject_text, styles["body_bold"])]], colWidths=[515])
    sub_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#e8f4ef")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#004c43")),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(sub_table)
    story.append(Spacer(1, 10))

    # 5. Salutation & Body
    story.append(Paragraph("<b>RESPECTED SIR / MADAM,</b>", styles["body_bold"]))
    story.append(Paragraph(
        f"I, <b>{complainant_name}</b>, residing at {request_data.get('complainant_address', 'Telangana')}, "
        f"most respectfully submit this formal statutory representation and petition for your urgent intervention:",
        styles["body"]
    ))
    story.append(Spacer(1, 6))

    # Section 1: Standing
    story.append(Paragraph("<b>1. JURISDICTION & LOCUS STANDI:</b>", styles["h2"]))
    story.append(Paragraph(
        f"The Respondent Society, namely <b>{society_name}</b>, is registered under the provisions of the "
        f"Telangana Cooperative Societies Act, 1964 and functions within your territorial and statutory jurisdiction. "
        f"The undersigned is directly aggrieved by the unlawful actions/omissions of the society management.",
        styles["clause"]
    ))

    # Section 2: Statutory Provisions
    story.append(Paragraph("<b>2. STATUTORY GROUNDS & VIOLATIONS:</b>", styles["h2"]))
    story.append(Paragraph(
        f"The subject matter of this grievance concerns <b>{cat_title}</b> and directly attracts remedies under "
        f"<b>{citations}</b> of the Telangana Cooperative Societies Act, 1964 and the statutory Rules framed thereunder.",
        styles["clause"]
    ))

    # Section 3: Statement of Facts
    story.append(Paragraph("<b>3. STATEMENT OF FACTS & INCIDENTS:</b>", styles["h2"]))
    facts = request_data.get("statement_of_facts", "Facts not provided.")
    for para in facts.split("\n"):
        if para.strip():
            story.append(Paragraph(para.strip(), styles["clause"]))

    # Section 4: Inaction & Illegality
    story.append(Paragraph("<b>4. ILLEGALITY & VIOLATION OF NATURAL JUSTICE:</b>", styles["h2"]))
    story.append(Paragraph(
        "The aforesaid conduct of the managing committee / office bearers is arbitrary, ultra vires the registered "
        "bye-laws, and in violation of democratic cooperative principles. Formal requests to rectify have been disregarded.",
        styles["clause"]
    ))

    # Section 5: Prayer / Relief Sought
    story.append(Paragraph("<b>5. PRAYER / SPECIFIC RELIEF SOUGHT:</b>", styles["h2"]))
    relief = request_data.get("relief_sought") or "Initiate statutory inquiry and issue binding directions."
    prayer_items = [
        f"a) Take immediate official cognizance of this representation under the Telangana Cooperative Societies Act, 1964;",
        f"b) <b>{relief}</b>;",
        f"c) Direct the respondent society to produce all related records, minutes, and audited accounts for statutory inspection;",
        f"d) Pass such further interim or final orders as deemed fit and proper to secure the ends of justice."
    ]
    for p in prayer_items:
        story.append(Paragraph(p, styles["clause"]))

    story.append(Spacer(1, 8))

    # Verification Block
    verif_text = f"""<b>VERIFICATION:</b><br/>
I, <b>{complainant_name}</b>, do hereby declare that the facts stated in paragraphs 1 to 5 above are true and correct to the best of my knowledge, information, and belief."""
    story.append(Paragraph(verif_text, styles["body"]))
    story.append(Spacer(1, 14))

    # Signature Block
    sig_data = [
        [
            Paragraph(f"<b>Date:</b> {date_str}<br/><b>Place:</b> Telangana", styles["body"]),
            Paragraph(f"<b>Signature of Complainant:</b><br/><br/><br/>( <b>{complainant_name}</b> )<br/>Phone: {request_data.get('complainant_phone', 'N/A')}", styles["body"])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[240, 275])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 10))

    # Enclosures Checklist Table
    enclosures = draft_response_data.get("required_enclosures", [
        "Photocopy of Complainant ID Proof (Aadhaar / Voter ID)",
        "Proof of Membership / Share Certificate / Payment Receipt",
        "Copies of correspondence / rejection letter / notice"
    ])
    enc_rows = [[Paragraph("<b>#</b>", styles["meta_label"]), Paragraph("<b>MANDATORY ENCLOSURES & EVIDENTIARY EXHIBITS</b>", styles["meta_label"]), Paragraph("<b>ATTACHED</b>", styles["meta_label"])]]
    for idx, enc in enumerate(enclosures, start=1):
        enc_rows.append([
            Paragraph(str(idx), styles["meta_val"]),
            Paragraph(enc, styles["meta_val"]),
            Paragraph("[  ] Verified", styles["meta_val"])
        ])

    enc_table = Table(enc_rows, colWidths=[25, 410, 80])
    enc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e8f4ef")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cde3db")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(KeepTogether([
        Paragraph("<b>LIST OF STATUTORY ENCLOSURES:</b>", styles["h2"]),
        enc_table
    ]))

    doc.build(story, canvasmaker=NumberedCanvas)
    return buffer.getvalue()


def generate_procedure_pdf(procedure: Dict[str, Any]) -> bytes:
    """
    Generate a comprehensive Canonical Procedure Guide & Checklist PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=55
    )

    styles = get_custom_styles()
    story = []

    # 1. Header Banner
    header_data = [
        [
            Paragraph("<b>SAHAKAAR SAATHI — CANONICAL GUIDED PROCEDURE MANUAL</b>", styles["title"]),
        ],
        [
            Paragraph(f"Official Compliance Manual: {procedure.get('title', 'Cooperative Procedure')}", styles["subtitle"])
        ]
    ]
    header_table = Table(header_data, colWidths=[515])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0f8f5")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#004c43")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    # 2. Metadata Overview Table
    meta_table_data = [
        [
            Paragraph("<b>Statutory Reference:</b>", styles["meta_label"]),
            Paragraph(procedure.get("act_reference", "Telangana Cooperative Societies Act, 1964"), styles["meta_val"]),
            Paragraph("<b>Statutory Timeline:</b>", styles["meta_label"]),
            Paragraph(procedure.get("estimated_days", "Prescribed by Act"), styles["meta_val"])
        ],
        [
            Paragraph("<b>Competent Authority:</b>", styles["meta_label"]),
            Paragraph(procedure.get("authority", "Registrar of Cooperative Societies"), styles["meta_val"]),
            Paragraph("<b>Applicable Forms:</b>", styles["meta_label"]),
            Paragraph(", ".join(procedure.get("applicable_forms", ["Prescribed Formats"])), styles["meta_val"])
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[110, 160, 100, 145])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fafdfb")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cde3db")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # 3. Summary & Eligibility
    story.append(Paragraph("<b>1. EXECUTIVE SUMMARY & SCOPE</b>", styles["h2"]))
    story.append(Paragraph(procedure.get("summary", ""), styles["body"]))
    story.append(Spacer(1, 4))

    if procedure.get("eligibility"):
        story.append(Paragraph("<b>Eligibility & Pre-requisites:</b>", styles["body_bold"]))
        for elig in procedure["eligibility"]:
            story.append(Paragraph(f"• {elig}", styles["clause"]))
        story.append(Spacer(1, 6))

    # 4. Step-by-Step Procedural Workflow
    story.append(Paragraph("<b>2. STEP-BY-STEP STATUTORY WORKFLOW</b>", styles["h2"]))
    steps = procedure.get("steps", [])
    for step in steps:
        step_num = step.get("step_number", 1)
        step_title = step.get("title", "")
        step_desc = step.get("description", "")
        step_tips = step.get("tips", "")

        step_card = [
            [
                Paragraph(f"<b>Step {step_num}: {step_title}</b>", styles["body_bold"])
            ],
            [
                Paragraph(step_desc, styles["body"])
            ]
        ]
        if step_tips:
            step_card.append([
                Paragraph(f"💡 <b>Compliance Guidance:</b> {step_tips}", styles["clause"])
            ])

        step_table = Table(step_card, colWidths=[515])
        step_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f9fbfb")),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#004c43")),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e8f4ef")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(step_table)
        story.append(Spacer(1, 6))

    # 5. Required Documents Checklist Table
    docs = procedure.get("required_documents", [])
    if docs:
        story.append(Spacer(1, 6))
        doc_rows = [[
            Paragraph("<b>#</b>", styles["meta_label"]),
            Paragraph("<b>MANDATORY DOCUMENT CHECKLIST & FILINGS</b>", styles["meta_label"]),
            Paragraph("<b>STATUS</b>", styles["meta_label"])
        ]]
        for idx, doc_name in enumerate(docs, start=1):
            doc_rows.append([
                Paragraph(str(idx), styles["meta_val"]),
                Paragraph(doc_name, styles["meta_val"]),
                Paragraph("[  ] Ready", styles["meta_val"])
            ])

        doc_table = Table(doc_rows, colWidths=[25, 410, 80])
        doc_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e8f4ef")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cde3db")),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(KeepTogether([
            Paragraph("<b>3. STATUTORY DOCUMENTATION & FILINGS CHECKLIST</b>", styles["h2"]),
            doc_table
        ]))

    doc.build(story, canvasmaker=NumberedCanvas)
    return buffer.getvalue()


if __name__ == "__main__":
    test_proc = {
        "title": "Registration of a New Cooperative Society",
        "act_reference": "Telangana Cooperative Societies Act, 1964 — Sections 6, 7 & 8",
        "authority": "Deputy Registrar of Cooperative Societies",
        "estimated_days": "60 to 90 days",
        "summary": "Full procedure to form and register a cooperative society.",
        "eligibility": ["At least 10 eligible individuals residing in the operational area."],
        "steps": [
            {
                "step_number": 1,
                "title": "Promoters Meeting",
                "description": "Elect a Chief Promoter and pass initial resolutions.",
                "tips": "Maintain strict minutes."
            }
        ],
        "required_documents": [
            "Application in Form 'A'",
            "Four certified copies of proposed Bye-Laws",
            "Bank balance certificate"
        ],
        "applicable_forms": ["Form 'A'", "Form 'B'"]
    }
    pdf_bytes = generate_procedure_pdf(test_proc)
    print(f"Test Procedure PDF generated: {len(pdf_bytes)} bytes")
