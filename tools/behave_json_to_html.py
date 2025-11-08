#!/usr/bin/env python3
"""Convertidor simple de JSON (salida de behave --format=json) a HTML.

Uso:
    python tools/behave_json_to_html.py input.json output.html

Genera un HTML estático con resumen y lista de features/escenarios/steps.
"""
import json
import sys
import html
from pathlib import Path


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def safe_get_step_status(step):
    # behave json may store step result in 'result' with 'status'
    r = step.get('result') if isinstance(step, dict) else None
    if r and 'status' in r:
        return r['status']
    # fallback
    return 'unknown'


def summarize(features):
    summary = {'features': 0, 'scenarios': 0, 'passed': 0, 'failed': 0}
    for f in features:
        summary['features'] += 1
        for e in f.get('elements', []) or f.get('scenarios', []):
            # element type may be 'scenario' or 'background'. Skip backgrounds
            if e.get('keyword', '').lower() == 'background':
                continue
            summary['scenarios'] += 1
            # decide scenario status: failed if any step failed
            steps = e.get('steps', [])
            statuses = [safe_get_step_status(s) for s in steps]
            if any(s == 'failed' for s in statuses):
                summary['failed'] += 1
            else:
                summary['passed'] += 1
    return summary


def render_html(features, summary):
    title = 'Behave BDD Report'
    css = '''
    body{font-family:Arial,Helvetica,sans-serif;padding:20px}
    .summary{margin-bottom:20px}
    .feature{border:1px solid #ddd;padding:12px;margin-bottom:12px}
    .feature h2{margin:0 0 8px}
    .scenario{padding:8px;border-top:1px dashed #eee}
    .step{font-size:90%;margin-left:12px}
    .passed{color:green}
    .failed{color:red}
    '''

    parts = []
    parts.append(f'<!doctype html>')
    parts.append('<html><head><meta charset="utf-8"><title>' + html.escape(title) + '</title>')
    parts.append('<style>' + css + '</style>')
    parts.append('</head><body>')
    parts.append(f'<h1>{html.escape(title)}</h1>')
    parts.append('<div class="summary">')
    parts.append(f'<b>Features:</b> {summary["features"]} &nbsp;')
    parts.append(f'<b>Scenarios:</b> {summary["scenarios"]} &nbsp;')
    parts.append(f'<b>Passed:</b> <span class="passed">{summary["passed"]}</span> &nbsp;')
    parts.append(f'<b>Failed:</b> <span class="failed">{summary["failed"]}</span>')
    parts.append('</div>')

    for f in features:
        fname = f.get('name') or f.get('uri') or 'Unnamed feature'
        parts.append('<div class="feature">')
        parts.append(f'<h2>{html.escape(str(fname))}</h2>')
        desc = f.get('description') or ''
        # behave may provide description as a list of lines; normalizar a string
        if isinstance(desc, list):
            desc = "\n".join(str(x) for x in desc)
        if desc:
            parts.append(f'<div class="desc">{html.escape(str(desc)).replace("\n","<br>")}</div>')

        for e in f.get('elements', []) or f.get('scenarios', []):
            # skip backgrounds
            if e.get('keyword', '').lower() == 'background':
                continue
            ename = e.get('name') or 'Unnamed scenario'
            parts.append('<div class="scenario">')
            parts.append(f'<b>Scenario:</b> {html.escape(str(ename))}')
            parts.append('<div>')
            for s in e.get('steps', []):
                st_text = s.get('name') or s.get('keyword', '') + ' ' + (s.get('name') or '')
                status = safe_get_step_status(s)
                cls = 'passed' if status == 'passed' else ('failed' if status == 'failed' else '')
                parts.append(f'<div class="step {cls}">{html.escape(st_text)} - <i>{html.escape(status)}</i></div>')
            parts.append('</div>')
            parts.append('</div>')

        parts.append('</div>')

    parts.append('</body></html>')
    return '\n'.join(parts)


def main(argv):
    if len(argv) < 3:
        print('Uso: behave_json_to_html.py input.json output.html')
        sys.exit(2)
    in_path = Path(argv[1])
    out_path = Path(argv[2])
    if not in_path.exists():
        print('Input file no encontrado:', in_path)
        sys.exit(1)
    try:
        data = load_json(in_path)
    except Exception as e:
        print('Error leyendo JSON:', e)
        sys.exit(1)

    # behave json is often a list of features
    features = data if isinstance(data, list) else data.get('features', [])
    summary = summarize(features)
    html_text = render_html(features, summary)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html_text, encoding='utf-8')
    print('Generado reporte HTML en', out_path)


if __name__ == '__main__':
    main(sys.argv)
