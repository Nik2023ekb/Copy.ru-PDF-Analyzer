"""PDF analysis utilities using PyMuPDF (fitz).

Provides functions to compute page sizes, detect color pages, and summarize a PDF.
"""


from typing import Dict, List, Tuple
import fitz  # PyMuPDF

MM_PER_PT = 25.4 / 72  # 1 pt = 0.3527778 mm
SIZE_TOL_MM = 2.0  # Погрешность для группировки
STD_SIZES_MM = {
    "A0": (841, 1189),
    "A1": (594, 841),
    "A2": (420, 594),
    "A3": (297, 420),
    "A4": (210, 297),
}

def pt_to_mm(size: Tuple[float, float]) -> Tuple[float, float]:
    return (round(size[0] * MM_PER_PT, 1), round(size[1] * MM_PER_PT, 1))

def match_std_size(w_mm: float, h_mm: float) -> str:
    for name, (w, h) in STD_SIZES_MM.items():
        if (
            abs(w_mm - w) <= SIZE_TOL_MM and abs(h_mm - h) <= SIZE_TOL_MM
        ) or (
            abs(w_mm - h) <= SIZE_TOL_MM and abs(h_mm - w) <= SIZE_TOL_MM
        ):
            return name
    return "Другие размеры"

def analyze_pdf(path: str) -> Dict:
    doc = fitz.open(path)
    num_pages = len(doc)
    color_pages: List[Dict] = []
    bw_pages: List[Dict] = []
    for i in range(num_pages):
        page = doc.load_page(i)
        rect = page.rect
        size_pt = (rect.width, rect.height)
        size_mm = pt_to_mm(size_pt)
        is_color = _page_is_color(page)
        rec = {'page': i + 1, 'size_mm': size_mm}
        if is_color:
            color_pages.append(rec)
        else:
            bw_pages.append(rec)

    def classify(pages: List[Dict]) -> Dict[str, Dict]:
        result = {k: {'count': 0, 'pages': []} for k in list(STD_SIZES_MM.keys()) + ['Другие размеры']}
        for info in pages:
            w_mm, h_mm = info['size_mm']
            fmt = match_std_size(w_mm, h_mm)
            result[fmt]['count'] += 1
            result[fmt]['pages'].append(info['page'])
        return result

    color_stat = classify(color_pages)
    bw_stat = classify(bw_pages)

    return {
        'num_pages': num_pages,
        'color_stat': color_stat,
        'bw_stat': bw_stat,
    }

def _page_is_color(page: fitz.Page) -> bool:
    try:
        mat = fitz.Matrix(1, 1)
        pix = page.get_pixmap(matrix=mat, alpha=False)
    except Exception:
        return True
    samples = pix.samples
    n = len(samples)
    if pix.n < 3:
        return False
    for idx in range(0, n, pix.n):
        r = samples[idx]
        g = samples[idx + 1]
        b = samples[idx + 2]
        if r != g or g != b:
            return True
    return False
