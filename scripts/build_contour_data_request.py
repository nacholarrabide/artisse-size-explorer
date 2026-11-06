from pathlib import Path
import tempfile

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "contour_neurovascular_system_data_request.docx"


def build_measurement_diagram():
    width, height = 2200, 420
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    # Liberation Sans Narrow is the installed Arial Narrow-compatible face.
    regular = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf", 30)
    small = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf", 25)
    bold = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf", 28)
    teal = "#0D9488"
    teal_light = "#99D5CF"
    gray = "#6B7280"
    pale = "#E5E7EB"
    black = "#111827"

    def cubic(p0, p1, p2, p3, steps=80):
        points = []
        for i in range(steps + 1):
            t = i / steps
            u = 1 - t
            points.append((
                u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
                u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1],
            ))
        return points

    def arrow_head(point, direction, size=13, color=gray):
        x, y = point
        dx, dy = direction
        length = max((dx*dx + dy*dy) ** 0.5, 1)
        dx, dy = dx/length, dy/length
        px, py = -dy, dx
        base_x, base_y = x - dx*size, y - dy*size
        draw.polygon([
            (x, y),
            (base_x + px*size*0.52, base_y + py*size*0.52),
            (base_x - px*size*0.52, base_y - py*size*0.52),
        ], fill=color)

    def double_arrow(p1, p2, color=gray, line_width=3, head=13):
        draw.line([p1, p2], fill=color, width=line_width)
        arrow_head(p1, (p1[0]-p2[0], p1[1]-p2[1]), head, color)
        arrow_head(p2, (p2[0]-p1[0], p2[1]-p1[1]), head, color)

    # Left panel: cross-section through the device and aneurysm neck.
    draw.text((28, 12), "CROSS-SECTION", font=bold, fill=black)
    neck_y = 292
    for x in range(75, 1510, 30):
        draw.line((x, neck_y, x+16, neck_y), fill=gray, width=3)
    draw.text((82, neck_y+9), "neck plane", font=small, fill=gray)
    draw.text((1320, 16), "SAC", font=small, fill=gray)
    draw.text((1260, 374), "PARENT VESSEL", font=small, fill=gray)

    outer = cubic((260, 102), (380, 235), (610, 310), (765, 318), 45)
    outer += cubic((765, 318), (920, 310), (1150, 235), (1270, 102), 45)[1:]
    inner = cubic((292, 118), (430, 228), (620, 286), (765, 296), 45)
    inner += cubic((765, 296), (910, 286), (1100, 228), (1238, 118), 45)[1:]
    draw.line(outer, fill=teal, width=9, joint="curve")
    draw.line(inner, fill=teal_light, width=7, joint="curve")
    draw.ellipse((751, 304, 779, 332), fill=teal, outline=black, width=2)

    double_arrow((260, 64), (1270, 64), color=black, head=15)
    label = "maximum deployed diameter"
    bbox = draw.textbbox((0, 0), label, font=regular)
    draw.text(((1530-(bbox[2]-bbox[0]))/2, 18), label, font=regular, fill=black)

    double_arrow((690, 102), (690, 318), color=gray, head=12)
    draw.text((480, 185), "cup depth", font=regular, fill=black)

    double_arrow((1350, 102), (1350, neck_y), color=gray, head=12)
    draw.text((1375, 150), "distal", font=regular, fill=black)
    draw.text((1375, 182), "penetration", font=regular, fill=black)

    double_arrow((1435, neck_y), (1435, 326), color=gray, head=9)
    draw.text((1365, 312), "proximal", font=small, fill=black)
    draw.text((1365, 340), "protrusion", font=small, fill=black)

    double_arrow((405, 180), (428, 198), color=gray, head=7)
    draw.line((405, 190, 215, 230), fill=gray, width=2)
    draw.text((28, 224), "residual layer", font=small, fill=black)
    draw.text((28, 252), "separation", font=small, fill=black)

    # Right panel: projection onto the aneurysm ostium.
    draw.line((1570, 24, 1570, 392), fill=pale, width=3)
    draw.text((1600, 12), "NECK-PLANE VIEW", font=bold, fill=black)
    neck_box = (1650, 86, 2140, 348)
    footprint_box = (1730, 112, 2075, 330)
    draw.ellipse(neck_box, outline=gray, width=4)
    draw.ellipse(footprint_box, fill="#D8F0ED", outline=teal, width=7)
    neck_center = (1895, 217)
    # Exaggerate the offset marker for legibility while keeping the footprint position faithful.
    device_center = (1960, 226)
    draw.ellipse((neck_center[0]-7, neck_center[1]-7, neck_center[0]+7, neck_center[1]+7), fill=gray)
    draw.ellipse((device_center[0]-8, device_center[1]-8, device_center[0]+8, device_center[1]+8), fill=teal)
    double_arrow(neck_center, device_center, color=black, head=8)
    draw.text((1848, 250), "eccentricity", font=small, fill=black)
    draw.line((2070, 145, 2150, 105), fill=teal, width=3)
    draw.text((1810, 54), "neck-plane footprint", font=regular, fill=black)

    out = Path(tempfile.gettempdir()) / "contour_measurement_diagram.png"
    image.save(out, dpi=(300, 300))
    return out


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


def add_group(document, number, title, purpose, items, diagram_path=None, diagram_note=None):
    p = document.add_paragraph(style="Group Heading")
    r = p.add_run(f"{number}  {title}")
    set_font(r, size=10.5, bold=True)

    if purpose:
        p = document.add_paragraph(style="Compact Body")
        r = p.add_run(purpose)
        set_font(r, size=9.0, color="404040")

    if diagram_path is not None:
        p = document.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.keep_with_next = True
        inline = p.add_run().add_picture(str(diagram_path), width=Inches(7.02))
        inline._inline.docPr.set("descr", "Contour measurement definitions in cross-section and neck-plane views")
        if diagram_note:
            p = document.add_paragraph(style="Compact Body")
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run("Definitions  ")
            set_font(r, size=8.25, bold=True)
            r = p.add_run(diagram_note)
            set_font(r, size=8.25, color="404040")

    for item in items:
        add_bullet(document, item)


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    diagram_path = build_measurement_diagram()
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
        "We are developing a continuous sizing model for Contour and request the minimum non-proprietary information "
        "needed to represent device geometry, deployment performance, and clinical size selection."
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
    add_bullet(doc, "Please confirm whether the current 0.021 inch 5-9 mm implants are geometrically and mechanically equivalent to the earlier 0.027 inch versions, and identify relevant design revisions.")
    add_bullet(doc, "Please confirm that the published sizing ranges are current and provide the applicable IFU or sizing-chart revision.")

    add_group(
        doc,
        "1",
        "Geometry and deformation",
        None,
        [
            "For each SKU, provide the measured free-state outer diameter, cup height or depth, radial profile, marker position, manufacturing tolerances, and measurement conditions.",
            "Provide a lookup table or validated function for deployment across the recommended range of maximum equatorial width and major and minor neck diameters, using the dimensional definitions shown above.",
            "Please include sample number and variability. CAD is welcome, but a CSV of radial profiles and deployed measurements would be sufficient."
        ],
        diagram_path=diagram_path,
        diagram_note=(
            "Maximum deployed diameter is the widest outer span after release; cup depth is the rim-to-deepest-point distance; "
            "neck-plane footprint is the outline and area projected over the ostium; distal penetration and proximal protrusion "
            "are measured from the neck plane into the sac and parent vessel; eccentricity is the offset between device and neck "
            "centers; residual layer separation is the maximum final gap between mesh layers."
        ),
    )

    add_group(
        doc,
        "2",
        "Expected deployment performance",
        None,
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
        None,
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
        "Current IFU and sizing algorithm plus tabular data with units, test conditions, sample number, variability, and tolerances. Normalized or categorical data are acceptable where detailed design data are confidential."
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
