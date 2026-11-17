"""Copy slides between .pptx files of the same size (python-pptx has no slide copy): shapes, pictures, native charts
(with their embedded workbook) and speaker notes. Used by make_deck_17nov_all.py. Layout: the target's blank layout."""
import copy
from io import BytesIO
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.opc.packuri import PackURI
from pptx.parts.chart import ChartPart
from pptx.parts.embeddedpackage import EmbeddedXlsxPart

R_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def _copy_chart(src_part, dst_prs):
    pkg = dst_prs.part.package
    chart = ChartPart.load(pkg.next_partname(ChartPart.partname_template), src_part.content_type, pkg, src_part.blob)
    for rid, rel in src_part.rels.items():
        if rel.is_external:
            continue
        t = rel.target_part
        xl = EmbeddedXlsxPart.load(pkg.next_partname("/ppt/embeddings/Microsoft_Excel_Sheet%d.xlsx"), t.content_type, pkg, t.blob)
        new = chart.relate_to(xl, rel.reltype)
        for el in chart._element.iter():
            if el.get(R_NS + "id") == rid:
                el.set(R_NS + "id", new)
    return chart


def copy_slide(src, dst_prs):
    s = dst_prs.slides.add_slide(dst_prs.slide_layouts[6])
    bg = src._element.cSld.bg
    if bg is not None:
        s._element.cSld.insert(0, copy.deepcopy(bg))
    for sh in src.shapes:
        s.shapes._spTree.insert_element_before(copy.deepcopy(sh._element), "p:extLst")
    remap = {}
    for rid, rel in src.part.rels.items():
        if rel.reltype in (RT.SLIDE_LAYOUT, RT.NOTES_SLIDE):
            continue
        if rel.is_external:
            remap[rid] = s.part.relate_to(rel.target_ref, rel.reltype, is_external=True)
        elif rel.reltype == RT.IMAGE:
            _, remap[rid] = s.part.get_or_add_image_part(BytesIO(rel.target_part.blob))
        elif rel.reltype == RT.CHART:
            remap[rid] = s.part.relate_to(_copy_chart(rel.target_part, dst_prs), RT.CHART)
    for el in s.shapes._spTree.iter():
        for attr in ("embed", "link", "id"):
            v = el.get(R_NS + attr)
            if v in remap:
                el.set(R_NS + attr, remap[v])
    if src.has_notes_slide:
        s.notes_slide.notes_text_frame.text = src.notes_slide.notes_text_frame.text
    return s
