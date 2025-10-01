"""Минимальный тест для pdf_analyzer."""
import fitz
from src.pdf_analyzer import analyze_pdf

def test_analyze_minimal_pdf(tmp_path):
    doc = fitz.open()
    doc.new_page(width=200, height=300)
    p = tmp_path / "t.pdf"
    doc.save(str(p))
    doc.close()
    rep = analyze_pdf(str(p))
    assert rep['num_pages'] == 1
    assert len(rep['sizes']) == 1
    sizes = list(rep['sizes'].values())
    assert 1 in sizes[0]['pages']
    assert isinstance(rep['color_pages'], list)
    assert isinstance(rep['bw_pages'], list)
