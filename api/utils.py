from django.core.handlers.wsgi import WSGIRequest
from docx import Document
from cm_site.models import Tracks
from cm_site.models import SignContracts
from www.settings import REPLACE_PATTERN_CONTRACTS
from datetime import datetime
import uuid

def generate_unique_sequence():
    unique_id = uuid.uuid4()
    return unique_id.hex.upper()

def has_duplicate_dicts(lst):
    seen = set()
    for d in lst:
        if tuple(d.items()) in seen:
            return True
        seen.add(tuple(d.items()))
    return False


def replace_text_in_docx(input_docx: str, output_docx: str, pattern: dict) -> None:
    doc = Document(input_docx)
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            for key in pattern.keys():
                if pattern.get(key).get('old') in run.text:
                    run.text = run.text.replace(pattern.get(key).get('old'), pattern.get(key).get('new'))
    doc.save(output_docx)
    return output_docx


def createContract(request: WSGIRequest, track: Tracks, license_type: str):
    user = request.user 
    if license_type == 'wav':
        pattern = REPLACE_PATTERN_CONTRACTS.get('wav')
        contract_path = SignContracts.objects.all().first().wav_license
        pattern_data = [
            datetime.now().strftime("%a, %d %b %Y"),
            datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
            track.track_name,
            f'{user.first_name} {user.last_name}' if user.first_name and user.last_name else user.artist_name if user.artist_name else user.username
        ]
        keys = ['date', 'date_full', 'track_name', 'lic']
        for key in keys:
            pattern[key]['new'] = pattern_data[keys.index(key)]
        
        return replace_text_in_docx(contract_path, f'media//uploads//contracts//DEL//intermediate_{generate_unique_sequence()}.docx', pattern)

    elif license_type == "unlimited":
        pattern = REPLACE_PATTERN_CONTRACTS.get('unlimited')
        contract_path = SignContracts.objects.all().first().unlimited_license
        pattern_data = [
            datetime.now().strftime("%a, %d %b %Y"),
            datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
            track.track_name,
            f'{user.first_name} {user.last_name}' if user.first_name and user.last_name else user.artist_name if user.artist_name else user.username
        ]
        keys = ['date', 'date_full', 'track_name', 'lic']
        for key in keys:
            pattern[key]['new'] = pattern_data[keys.index(key)]
        
        return replace_text_in_docx(contract_path, f'media//uploads//contracts//DEL//intermediate_{generate_unique_sequence()}.docx', pattern)
    elif license_type == "exclusive":
        pattern = REPLACE_PATTERN_CONTRACTS.get('exclusive')
        contract_path = SignContracts.objects.all().first().exclusive_license
        pattern_data = [
            datetime.now().strftime("%a, %d %b %Y"),
            user.artist_name if user.artist_name else user.username,
            track.track_name,
            f'{user.first_name} {user.last_name}' if user.first_name and user.last_name else user.artist_name if user.artist_name else user.username
        ]
        keys = ['date', 'customer_alias', 'track_name', 'customer_name']
        for key in keys:
            pattern[key]['new'] = pattern_data[keys.index(key)]
        
        return replace_text_in_docx(contract_path, f'media//uploads//contracts//DEL//intermediate_{generate_unique_sequence()}.docx', pattern)
        