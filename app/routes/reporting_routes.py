import csv
from datetime import date
from io import StringIO

from flask import (
    Blueprint,
    Response,
    render_template,
    request,
)

from app.security.decorators import roles_required
from app.security.session_user import get_current_user
from app.services.reporting_service import ReportingService
from datetime import datetime
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

reporting_bp = Blueprint(
    "reporting",
    __name__,
    url_prefix="/supervisor/reports",
)


def get_filtered_reporting_data():
    period = request.args.get("period", "30")

    if period == "custom":
        start_date_value = request.args.get("start_date", "")
        end_date_value = request.args.get("end_date", "")

        if not start_date_value or not end_date_value:
            raise ValueError("Please select both a start date and an end date.")

        start_date = date.fromisoformat(start_date_value)
        end_date = date.fromisoformat(end_date_value)

        return ReportingService.get_reporting_data(
            start_date=start_date,
            end_date=end_date,
            period="custom",
        )

    return ReportingService.get_reporting_data(period=period)


def safe_csv_value(value):
    """Protect spreadsheet users from CSV formula injection."""

    if isinstance(value, str) and value.startswith(("=", "+", "-", "@", "\t", "\r")):
        return "'" + value

    return value


@reporting_bp.route("/")
@roles_required("Supervisor", "Administrator")
def reports():
    current_user = get_current_user()
    error_message = None

    try:
        reporting_data = get_filtered_reporting_data()

    except ValueError as error:
        error_message = str(error)

        reporting_data = ReportingService.get_reporting_data(period="30")

    return render_template(
        "supervisor/reports.html",
        current_user=current_user,
        data=reporting_data,
        error_message=error_message,
    )


@reporting_bp.route("/export/csv")
@roles_required("Supervisor", "Administrator")
def export_csv():

    try:
        data = get_filtered_reporting_data()

    except ValueError as error:
        return Response(
            str(error),
            status=400,
            mimetype="text/plain",
        )

    output = StringIO()
    writer = csv.writer(output)

    # Report information
    writer.writerow(["SUPPORTDESK PRO - REPORT"])
    writer.writerow(["Reporting Period", data["filters"]["period_label"]])
    writer.writerow(["Start Date", data["filters"]["start_date"]])
    writer.writerow(["End Date", data["filters"]["end_date"]])
    writer.writerow([])

    # Summary
    writer.writerow(["INCIDENT SUMMARY"])
    writer.writerow(["Metric", "Value"])
    writer.writerow(
        [
            "Total Incidents (All Time)",
            data["summary"]["total_incidents"],
        ]
    )
    writer.writerow(
        [
            "Incidents in Selected Period",
            data["summary"]["incidents_in_period"],
        ]
    )
    writer.writerow(
        [
            "Average Resolution Time (Hours)",
            data["summary"]["average_resolution_hours"],
        ]
    )
    writer.writerow(
        [
            "Closed Incidents Used for Average",
            data["summary"]["closed_incidents_used_for_average"],
        ]
    )
    writer.writerow([])

    # Incident trends
    writer.writerow(["INCIDENT TRENDS"])
    writer.writerow(["Date", "Incidents Reported"])

    for item in data["incident_trends"]:
        writer.writerow(
            [
                item["date_label"],
                item["count"],
            ]
        )

    writer.writerow([])

    # Category breakdown
    writer.writerow(["INCIDENTS BY CATEGORY"])
    writer.writerow(["Category", "Count", "Percentage"])

    for item in data["category_breakdown"]:
        writer.writerow(
            [
                safe_csv_value(item["category"]),
                item["count"],
                item["percentage"],
            ]
        )

    writer.writerow([])

    # Priority breakdown
    writer.writerow(["INCIDENTS BY PRIORITY"])
    writer.writerow(["Priority", "Count", "Percentage"])

    for item in data["priority_breakdown"]:
        writer.writerow(
            [
                safe_csv_value(item["priority"]),
                item["count"],
                item["percentage"],
            ]
        )

    writer.writerow([])

    # Technician performance
    writer.writerow(["TECHNICIAN PERFORMANCE"])
    writer.writerow(
        [
            "Technician",
            "Account Status",
            "Total Assigned",
            "Closed",
            "Outstanding",
            "Closed Share (%)",
            "Average Resolution Hours",
        ]
    )

    for technician in data["technician_performance"]:
        writer.writerow(
            [
                safe_csv_value(technician["technician"]),
                "Active" if technician["is_active"] else "Inactive",
                technician["total_assigned"],
                technician["closed"],
                technician["outstanding"],
                technician["completion_rate"],
                technician["average_resolution_hours"],
            ]
        )

    writer.writerow([])

    # Resolution performance
    resolution = data["resolution_performance"]

    writer.writerow(["RESOLUTION PERFORMANCE"])
    writer.writerow(["Metric", "Value"])
    writer.writerow(["Total Resolutions", resolution["total"]])
    writer.writerow(["Accepted", resolution["accepted"]])
    writer.writerow(["Rejected", resolution["rejected"]])
    writer.writerow(["Pending", resolution["pending"]])
    writer.writerow(
        [
            "Acceptance Rate (%)",
            resolution["acceptance_rate"],
        ]
    )

    filename = (
        "supportdesk_pro_report_"
        f"{data['filters']['start_date']}_"
        f"{data['filters']['end_date']}.csv"
    )

    return Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": (f'attachment; filename="{filename}"')},
    )


def pdf_safe(value):
    """Safely format values for PDF paragraphs."""
    if value is None:
        return "N/A"

    return escape(str(value))


def build_reporting_pdf(data):
    """Generate a professional SupportDesk Pro PDF report."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=20 * mm,
        bottomMargin=18 * mm,
        title="SupportDesk Pro Management Report",
        author="SupportDesk Pro",
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontSize=22,
            leading=27,
            textColor=colors.HexColor("#172b4d"),
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.HexColor("#546e7a"),
            alignment=TA_CENTER,
            spaceAfter=15,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#172b4d"),
            spaceBefore=12,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallCell",
            parent=styles["Normal"],
            fontSize=8,
            leading=10,
        )
    )

    elements = []

    # --------------------------------------------------
    # Report heading
    # --------------------------------------------------

    elements.append(
        Paragraph(
            "SUPPORTDESK PRO",
            styles["ReportTitle"],
        )
    )

    elements.append(
        Paragraph(
            "Management Reporting &amp; Analytics",
            styles["ReportSubtitle"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>Reporting Period:</b> " f"{pdf_safe(data['filters']['period_label'])}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>From:</b> {pdf_safe(data['filters']['start_date'])}"
            f"&nbsp;&nbsp;&nbsp;"
            f"<b>To:</b> {pdf_safe(data['filters']['end_date'])}",
            styles["Normal"],
        )
    )

    elements.append(
        Paragraph(
            f"<b>Generated:</b> " f"{datetime.now().strftime('%d %B %Y at %H:%M')}",
            styles["Normal"],
        )
    )

    elements.append(Spacer(1, 12))

    # --------------------------------------------------
    # Incident summary
    # --------------------------------------------------

    elements.append(Paragraph("1. Executive Summary", styles["SectionHeading"]))

    summary = data["summary"]
    resolution = data["resolution_performance"]

    summary_table = [
        ["Metric", "Value"],
        [
            "Total Incidents (All Time)",
            str(summary["total_incidents"]),
        ],
        [
            "Incidents in Selected Period",
            str(summary["incidents_in_period"]),
        ],
        [
            "Average Resolution Time",
            (
                f"{summary['average_resolution_hours']} hours"
                if summary["average_resolution_hours"] is not None
                else "N/A"
            ),
        ],
        [
            "Closed Incidents Used for Average",
            str(summary["closed_incidents_used_for_average"]),
        ],
        [
            "Resolution Acceptance Rate",
            f"{resolution['acceptance_rate']}%",
        ],
    ]

    elements.append(
        Table(
            summary_table,
            colWidths=[100 * mm, 75 * mm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172b4d")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d5dce5")),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f4f6f9")),
                    ("PADDING", (0, 0), (-1, -1), 7),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            ),
        )
    )

    # --------------------------------------------------
    # Incident trends
    # --------------------------------------------------

    elements.append(Paragraph("2. Incident Trends", styles["SectionHeading"]))

    trend_table = [["Date", "Incidents Reported"]]

    for item in data["incident_trends"]:
        trend_table.append(
            [
                item["date_label"],
                str(item["count"]),
            ]
        )

    if len(trend_table) == 1:
        trend_table.append(["No data available", "0"])

    elements.append(
        Table(
            trend_table,
            colWidths=[65 * mm, 65 * mm],
            repeatRows=1,
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172b4d")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d5dce5")),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            ),
        )
    )

    # --------------------------------------------------
    # Category breakdown
    # --------------------------------------------------

    elements.append(Paragraph("3. Incidents by Category", styles["SectionHeading"]))

    category_table = [["Category", "Incident Count", "Percentage"]]

    for item in data["category_breakdown"]:
        category_table.append(
            [
                pdf_safe(item["category"]),
                str(item["count"]),
                f"{item['percentage']}%",
            ]
        )

    elements.append(
        Table(
            category_table,
            colWidths=[80 * mm, 55 * mm, 45 * mm],
            repeatRows=1,
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172b4d")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d5dce5")),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            ),
        )
    )

    # --------------------------------------------------
    # Priority breakdown
    # --------------------------------------------------

    elements.append(Paragraph("4. Incidents by Priority", styles["SectionHeading"]))

    priority_table = [["Priority", "Incident Count", "Percentage"]]

    for item in data["priority_breakdown"]:
        priority_table.append(
            [
                pdf_safe(item["priority"]),
                str(item["count"]),
                f"{item['percentage']}%",
            ]
        )

    elements.append(
        Table(
            priority_table,
            colWidths=[80 * mm, 55 * mm, 45 * mm],
            repeatRows=1,
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172b4d")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d5dce5")),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            ),
        )
    )

    # --------------------------------------------------
    # Technician performance
    # --------------------------------------------------

    elements.append(Paragraph("5. Technician Performance", styles["SectionHeading"]))

    technician_table = [
        [
            "Technician",
            "Account",
            "Assigned",
            "Closed",
            "Outstanding",
            "Closed Share",
            "Average Hours",
        ]
    ]

    for technician in data["technician_performance"]:
        technician_table.append(
            [
                Paragraph(
                    pdf_safe(technician["technician"]),
                    styles["SmallCell"],
                ),
                "Active" if technician["is_active"] else "Inactive",
                str(technician["total_assigned"]),
                str(technician["closed"]),
                str(technician["outstanding"]),
                f"{technician['completion_rate']}%",
                (
                    str(technician["average_resolution_hours"])
                    if technician["average_resolution_hours"] is not None
                    else "N/A"
                ),
            ]
        )

    if len(technician_table) == 1:
        technician_table.append(["No technician data", "-", "-", "-", "-", "-", "-"])

    elements.append(
        Table(
            technician_table,
            colWidths=[
                55 * mm,
                23 * mm,
                23 * mm,
                20 * mm,
                28 * mm,
                25 * mm,
                30 * mm,
            ],
            repeatRows=1,
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172b4d")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d5dce5")),
                    ("PADDING", (0, 0), (-1, -1), 6),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            ),
        )
    )

    elements.append(
        Paragraph(
            "Closed share represents the proportion of assigned incidents "
            "that are closed. It does not measure resolution quality.",
            styles["Normal"],
        )
    )

    # --------------------------------------------------
    # Resolution performance
    # --------------------------------------------------

    elements.append(Paragraph("6. Resolution Performance", styles["SectionHeading"]))

    resolution_table = [
        ["Metric", "Value"],
        ["Total Resolutions", str(resolution["total"])],
        ["Accepted", str(resolution["accepted"])],
        ["Rejected", str(resolution["rejected"])],
        ["Pending", str(resolution["pending"])],
        ["Acceptance Rate", f"{resolution['acceptance_rate']}%"],
    ]

    elements.append(
        Table(
            resolution_table,
            colWidths=[85 * mm, 65 * mm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#172b4d")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d5dce5")),
                    ("PADDING", (0, 0), (-1, -1), 7),
                ]
            ),
        )
    )

    # --------------------------------------------------
    # Report footer and page numbers
    # --------------------------------------------------

    def add_page_details(canvas, doc):
        canvas.saveState()

        page_width, page_height = landscape(A4)

        canvas.setStrokeColor(colors.HexColor("#d5dce5"))

        canvas.line(
            15 * mm,
            13 * mm,
            page_width - 15 * mm,
            13 * mm,
        )

        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#607d8b"))

        canvas.drawString(
            15 * mm,
            8 * mm,
            "SupportDesk Pro | Management Report",
        )

        canvas.drawRightString(
            page_width - 15 * mm,
            8 * mm,
            f"Page {doc.page}",
        )

        canvas.restoreState()

    document.build(
        elements,
        onFirstPage=add_page_details,
        onLaterPages=add_page_details,
    )

    buffer.seek(0)

    return buffer


@reporting_bp.route("/export/pdf")
@roles_required("Supervisor", "Administrator")
def export_pdf():

    try:
        data = get_filtered_reporting_data()

    except ValueError as error:
        return Response(
            str(error),
            status=400,
            mimetype="text/plain",
        )

    pdf_buffer = build_reporting_pdf(data)

    filename = (
        "supportdesk_pro_report_"
        f"{data['filters']['start_date']}_"
        f"{data['filters']['end_date']}.pdf"
    )

    return Response(
        pdf_buffer.getvalue(),
        mimetype="application/pdf",
        headers={"Content-Disposition": (f'attachment; filename="{filename}"')},
    )
