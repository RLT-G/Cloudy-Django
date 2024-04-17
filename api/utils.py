from django.core.handlers.wsgi import WSGIRequest
from docx import Document
from cm_site.models import Tracks
from www.settings import REPLACE_PATTERN_CONTRACTS


def has_duplicate_dicts(lst):
    seen = set()
    for d in lst:
        if tuple(d.items()) in seen:
            return True
        seen.add(tuple(d.items()))
    return False


def replace_text_in_docx(input_docx: str, output_docx: str, search_text: str, replace_text: str) -> None:
    """
        input_docx - path to docx file
        output_docx - path to output docx file
        search_text - old text
        replace_text - new text
    """
    doc = Document(input_docx)
    for paragraph in doc.paragraphs:
        if search_text in paragraph.text:
            paragraph.text = paragraph.text.replace(search_text, replace_text)
    doc.save(output_docx)


def createContract(request: WSGIRequest, track: Tracks, license_type: str):
    user = request.user
    if license_type == 'wav':
        pattern = REPLACE_PATTERN_CONTRACTS.get('wav')
    elif license_type == "unlimited":
        pattern = REPLACE_PATTERN_CONTRACTS.get('unlimited')
    elif license_type == "exclusive":
        pattern = REPLACE_PATTERN_CONTRACTS.get('exclusive')
        