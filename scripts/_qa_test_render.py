import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from utils.quotation_utils import render_quotation_html
from utils.settings import load_settings
from datetime import datetime

ctx = {
    'company_name': load_settings().get('company_name', 'Newton Smart Home'),
    'quotation_number': 'QT-TEST-001',
    'quotation_date': datetime.today().strftime('%Y-%m-%d'),
    'client_name': 'Test Client',
    'client_address': 'Somewhere',
    'items': [],
    'subtotal': 0,
    'Installation': 0,
    'total_amount': 0,
    'sig_name': '',
    'sig_role': ''
}

try:
    html = render_quotation_html(ctx, template_name='newton_quotation_A4.html')
    print('RENDER_OK')
    print(html[:200].replace('\n',' '))
except Exception as e:
    print('RENDER_ERROR', repr(e))
