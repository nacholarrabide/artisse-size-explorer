from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "contour_neurovascular_system_data_request.docx"


def set_cell_margins(cell, top=70, start=90, bottom=70, end=90):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for edge, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        tag = "w:" + edge
        element = tc_mar.find(qn(tag))
        if element is None:
            element = OxmlElement(tag)
            tc_mar.append(element)
        element.set(qn("w:w"), str(value))
        element.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def set_table_borders(table, color="D9D9D9", size="5"):
    tbl_pr = table._tbl.tblPr
    borders = tbl_pr.first_child_found_in("w:tblBorders")
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tbl_pr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), size)
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), color)
        borders.append(node)


def shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.first_child_found_in("w:shd")
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_font(run, size=9.25, bold=False, color="000000"):
    run.font.name = "Aptos"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor.from_string(color)


def remove_paragraph_borders(element):
    p_pr = element.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is not None:
        p_pr.remove(p_bdr)


def add_bullet(document, text, bold_lead=None):
    p = document.add_paragraph(style="Compact Bullet")
    bullet = p.add_run("•  ")
    set_font(bullet)
    if bold_lead and text.startswith(bold_lead):
        lead = p.add_run(bold_lead)
        set_font(lead, bold=True)
        rest = p.add_run(text[len(bold_lead):])
        set_font(rest)
    else:
        run = p.add_run(text)
        set_font(run)
    return p


def add_group(document, number, title, purpose, items):
    p = document.add_paragraph(style="Group Heading")
    r = p.add_run(f"{number}  {title}")
    set_font(r, size=10.5, bold=True)

    p = document.add_paragraph(style="Compact Body")
    r = p.add_run(purpose)
    set_font(r, size=9.0, color="404040")

    for item in items:
        add_bullet(document, item)


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.48)
    section.bottom_margin = Inches(0.48)
    section.left_margin = Inches(0.62)
    section.right_margin = Inches(0.62)
    section.header_distance = Inches(0.2)
    section.footer_distance = Inches(0.2)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(9.25)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.space_after = Pt(2)
    normal.paragraph_format.line_spacing = 1.03

    title = styles["Title"]
    title.font.name = "Aptos Display"
    title.font.size = Pt(17)
    title.font.bold = True
    title.font.color.rgb = RGBColor(0, 0, 0)
    title.paragraph_format.space_after = Pt(3)
    title.paragraph_format.keep_with_next = True
    remove_paragraph_borders(title.element)

    compact_body = styles.add_style("Compact Body", WD_STYLE_TYPE.PARAGRAPH)
    compact_body.font.name = "Aptos"
    compact_body.font.size = Pt(9.25)
    compact_body.font.color.rgb = RGBColor(0, 0, 0)
    compact_body.paragraph_format.space_after = Pt(2)
    compact_body.paragraph_format.line_spacing = 1.03

    compact_bullet = styles.add_style("Compact Bullet", WD_STYLE_TYPE.PARAGRAPH)
    compact_bullet.font.name = "Aptos"
    compact_bullet.font.size = Pt(9.15)
    compact_bullet.font.color.rgb = RGBColor(0, 0, 0)
    compact_bullet.paragraph_format.left_indent = Inches(0.18)
    compact_bullet.paragraph_format.first_line_indent = Inches(-0.12)
    compact_bullet.paragraph_format.space_after = Pt(1.2)
    compact_bullet.paragraph_format.line_spacing = 1.01
    compact_bullet.paragraph_format.keep_together = True
    compact_bullet.paragraph_format.keep_with_next = False

    group_heading = styles.add_style("Group Heading", WD_STYLE_TYPE.PARAGRAPH)
    group_heading.font.name = "Aptos"
    group_heading.font.size = Pt(10.5)
    group_heading.font.bold = True
    group_heading.font.color.rgb = RGBColor(0, 0, 0)
    group_heading.paragraph_format.space_before = Pt(4)
    group_heading.paragraph_format.space_after = Pt(1)
    group_heading.paragraph_format.keep_with_next = True

    p = doc.add_paragraph(style="Title")
    remove_paragraph_borders(p._p)
    p.add_run("Contour Neurovascular System Data Request")

    p = doc.add_paragraph(style="Compact Body")
    r = p.add_run(
        "We are developing a continuous sizing model for the Contour Neurovascular System. "
        "The request below focuses on the minimum information needed to represent device geometry, "
        "expected deployment performance, and clinical size selection without requiring proprietary manufacturing details."
    )
    set_font(r, size=9.35)

    p = doc.add_paragraph(style="Group Heading")
    r = p.add_run("Please confirm our current understanding")
    set_font(r, size=10.5, bold=True)

    p = doc.add_paragraph(style="Compact Body")
    r = p.add_run(
        "Public Stryker information and clinical literature describe Contour as a circular, dual-layer construct with "
        "72 wires per layer, radiopaque DFT wire technology, and one proximal marker. The current range comprises "
        "5, 7, 9, 11, and 14 mm devices; the 5–9 mm devices use a 0.021 inch microcatheter and the 11–14 mm devices a 0.027 inch microcatheter."
    )
    set_font(r)

    add_bullet(doc, "Please confirm that these specifications remain correct for every current SKU and correct any inaccuracies.")
    add_bullet(doc, "Please identify differences in wire count, wire diameter, braid pattern, materials, mesh density, or free shape between device sizes.")
    add_bullet(doc, "Please clarify whether the current 0.021 inch versions of the 5, 7, and 9 mm devices have the same implant geometry and mechanical behavior as the earlier 0.027 inch versions, and list any relevant design generations or revisions.")
    add_bullet(doc, "Please confirm that the sizing ranges currently published by Stryker are the latest approved recommendations and provide the applicable IFU or sizing-chart revision date.")

    add_group(
        doc,
        "1",
        "Geometry and deformation",
        "Priority is a usable mapping from nominal size and aneurysm dimensions to the deployed device shape.",
        [
            "For each SKU, provide the measured free-state outer diameter, cup height or depth, radial profile, marker position, manufacturing tolerances, and measurement conditions.",
            "Provide a lookup table or validated function for deployment across the recommended range of maximum equatorial width and major and minor neck diameters. Desired outputs are deployed diameter, cup depth, neck-plane footprint, distal penetration, proximal protrusion, eccentricity, and residual separation between layers.",
            "Please include sample number and variability. CAD is welcome, but a CSV of radial profiles and deployed measurements would be sufficient."
        ],
    )

    add_group(
        doc,
        "2",
        "Expected deployment performance",
        "For the same test conditions, we would like to distinguish an appropriate deployment from under- or oversizing.",
        [
            "Report neck area covered, percentage coverage, maximum uncovered peripheral gap, apposition, and protrusion into the parent vessel.",
            "Provide the expected or acceptable ranges for opening and contact force, migration resistance, and layer separation. If numerical force data cannot be shared, a recommended, acceptable, borderline, or unacceptable classification for each size–anatomy combination would be useful.",
            "Define the quantitative or visual signs of inadequate opening, instability, undersizing, and excessive oversizing, including the persistent teardrop or double-layer configuration."
        ],
    )

    add_group(
        doc,
        "3",
        "Clinical sizing and acceptance rules",
        "Priority is the decision logic taught to operators, especially where published size ranges overlap.",
        [
            "Define how maximum equatorial width and neck dimensions should be measured, including imaging modality, projections, irregular or elliptical necks, rounding, and measurement uncertainty.",
            "Explain which variable takes precedence and the target and maximum acceptable oversizing. Please include boundary examples such as width/neck 5.0/4.5 mm, 7.0/5.5 mm, and 8.0/7.0 mm, where two sizes appear eligible.",
            "State how aneurysm height, angulation, branches arising from the neck, lobulation, or partial thrombosis modify selection or exclude treatment.",
            "Provide pre-detachment criteria for adequate coverage, apposition, protrusion, marker position, layer separation, stability, branch patency, and contrast stasis, together with rules for redeploying, upsizing, downsizing, or abandoning Contour."
        ],
    )

    p = doc.add_paragraph(style="Compact Body")
    p.paragraph_format.space_before = Pt(3)
    r = p.add_run("Preferred delivery format  ")
    set_font(r, size=8.7, bold=True)
    r = p.add_run(
        "Current IFU and sizing algorithm plus CSV or equivalent tabular data with units, test conditions, sample number, mean, variability, and tolerances. Normalized or categorical data would still be valuable where detailed design data are confidential."
    )
    set_font(r, size=8.7, color="404040")

    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    rr = fp.add_run("Technical discussion draft  |  6 November 2026")
    set_font(rr, size=7.5, color="707070")

    core = doc.core_properties
    core.title = "Contour Neurovascular System Data Request"
    core.subject = "Priority engineering and clinical sizing data requested from Stryker"
    core.author = "Prof. André Kemmling"
    core.keywords = "Contour, Stryker, neurovascular, sizing, device geometry"

    doc.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    build()
