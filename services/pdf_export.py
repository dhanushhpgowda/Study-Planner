from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import date


# Color palette
DARK       = colors.HexColor("#0a0a0f")
AMBER      = colors.HexColor("#f5a623")
PURPLE     = colors.HexColor("#8b7cf6")
TEAL       = colors.HexColor("#2dd4bf")
CORAL      = colors.HexColor("#f87171")
GREEN      = colors.HexColor("#4ade80")
LIGHT_GRAY = colors.HexColor("#f0eee8")
MID_GRAY   = colors.HexColor("#9896a0")
SURFACE    = colors.HexColor("#1e1e2e")
WHITE      = colors.white

SESSION_COLORS = {
    "study":     PURPLE,
    "revision":  AMBER,
    "mock_test": CORAL,
}


def build_pdf(plan):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Normal"],
        fontSize=28,
        fontName="Helvetica-Bold",
        textColor=DARK,
        spaceAfter=4,
        alignment=TA_LEFT,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=12,
        fontName="Helvetica",
        textColor=MID_GRAY,
        spaceAfter=2,
        alignment=TA_LEFT,
    )
    day_header_style = ParagraphStyle(
        "DayHeader",
        parent=styles["Normal"],
        fontSize=13,
        fontName="Helvetica-Bold",
        textColor=DARK,
        spaceBefore=10,
        spaceAfter=4,
    )
    session_style = ParagraphStyle(
        "Session",
        parent=styles["Normal"],
        fontSize=9,
        fontName="Helvetica",
        textColor=DARK,
        leading=13,
    )
    tip_style = ParagraphStyle(
        "Tip",
        parent=styles["Normal"],
        fontSize=8,
        fontName="Helvetica-Oblique",
        textColor=MID_GRAY,
        leading=11,
    )

    story = []

    # ── HEADER ──────────────────────────────────────────────────
    story.append(Paragraph(plan.title, title_style))
    story.append(Paragraph(
        f"Student: {plan.user.name}  ·  Exam: {plan.exam_date.strftime('%B %d, %Y')}  ·  Generated: {date.today().strftime('%b %d, %Y')}",
        subtitle_style
    ))
    story.append(Spacer(1, 4 * mm))

    # Summary table
    summary_data = [
        ["Total Days", "Daily Hours", "Total Sessions", "Completed", "Progress"],
        [
            str((plan.exam_date - date.today()).days),
            f"{plan.daily_hours}h",
            str(plan.total_sessions),
            str(plan.completed_sessions),
            f"{plan.progress_percent}%",
        ]
    ]
    summary_table = Table(summary_data, colWidths=[35 * mm] * 5)
    summary_table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  DARK),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  AMBER),
        ("BACKGROUND",  (0, 1), (-1, 1),  LIGHT_GRAY),
        ("TEXTCOLOR",   (0, 1), (-1, 1),  DARK),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTNAME",    (0, 1), (-1, 1),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 9),
        ("ALIGN",       (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [DARK, LIGHT_GRAY]),
        ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
        ("TOPPADDING",  (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROUNDEDCORNERS", [3]),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 6 * mm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e0dedd")))
    story.append(Spacer(1, 4 * mm))

    # ── SCHEDULE ────────────────────────────────────────────────
    from models import StudySession
    all_sessions = (
        StudySession.query
        .filter_by(plan_id=plan.id)
        .order_by(StudySession.day_number, StudySession.id)
        .all()
    )

    days = {}
    for s in all_sessions:
        days.setdefault(s.day_number, []).append(s)

    for day_num, sessions in days.items():
        day_date = sessions[0].date
        is_past = day_date < date.today()

        # Day header
        status = " ✓" if all(s.completed for s in sessions) else ""
        story.append(Paragraph(
            f"Day {day_num} — {day_date.strftime('%A, %B %d')}{status}",
            day_header_style
        ))

        # Sessions table
        table_data = [["Subject", "Topic", "Duration", "Type", "Status"]]
        for s in sessions:
            subj  = s.subject.name if s.subject else "General"
            topic = s.topic
            dur   = f"{s.duration_minutes}m"
            stype = s.session_type.replace("_", " ").title()
            if s.completed:
                status_txt = "Done"
            elif s.missed:
                status_txt = "Skipped"
            else:
                status_txt = "Pending"
            table_data.append([subj, topic, dur, stype, status_txt])

        col_widths = [35 * mm, 65 * mm, 20 * mm, 25 * mm, 20 * mm]
        t = Table(table_data, colWidths=col_widths, repeatRows=1)

        row_styles = [
            ("BACKGROUND",    (0, 0), (-1, 0),  DARK),
            ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
            ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",      (0, 0), (-1, -1), 8),
            ("ALIGN",         (2, 0), (-1, -1), "CENTER"),
            ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
            ("GRID",          (0, 0), (-1, -1), 0.3, colors.HexColor("#e0dedd")),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#f8f7f5")]),
        ]

        # Color status column
        for i, s in enumerate(sessions, start=1):
            if s.completed:
                row_styles.append(("TEXTCOLOR", (4, i), (4, i), colors.HexColor("#16a34a")))
            elif s.missed:
                row_styles.append(("TEXTCOLOR", (4, i), (4, i), colors.HexColor("#dc2626")))

        t.setStyle(TableStyle(row_styles))
        story.append(t)
        story.append(Spacer(1, 4 * mm))

    doc.build(story)
    buffer.seek(0)
    return buffer