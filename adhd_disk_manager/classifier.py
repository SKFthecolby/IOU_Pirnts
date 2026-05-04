from __future__ import annotations
from pathlib import Path

DEFAULT_MAP = {
    'CAD': {'.step','.stp','.iges','.igs','.sldprt','.sldasm','.slddrw','.f3d','.f3z','.dwg','.dxf','.ipt','.iam','.idw','.catpart','.catproduct','.x_t','.x_b'},
    'CAM': {'.cam','.cl','.apt'},
    'CNC': {'.nc','.tap','.gcode','.cnc','.ngc','.sbp'},
    '3D_Printing': {'.stl','.3mf','.obj','.amf'},
    'Code': {'.py','.js','.ts','.tsx','.jsx','.c','.cpp','.h','.hpp','.cs','.java','.go','.rs','.php','.rb','.html','.css','.json','.yaml','.yml','.toml','.xml','.sql','.bat','.cmd','.ps1','.sh'},
    'Documents': {'.pdf','.doc','.docx','.txt','.rtf','.md','.odt'},
    'Spreadsheets': {'.xls','.xlsx','.csv','.ods'},
    'Archives': {'.zip','.7z','.rar','.tar','.gz','.bz2','.xz'},
    'Installers': {'.exe','.msi','.iso','.dmg','.appx'},
    'Firmware': {'.bin','.hex','.uf2','.elf'},
}


def classify(path: Path, rules: dict, in_project: bool=False) -> tuple[str,str]:
    ext = path.suffix.lower()
    name = path.name.lower()
    p = str(path).lower()
    if ext in (rules.get('extension_rules') or {}):
        return 'RuleBased', f'extension:{ext}'
    for r in rules.get('file_name_rules', []):
        if r.get('contains','').lower() in name:
            return 'RuleBased', f"file:{r['contains']}"
    for r in rules.get('folder_name_rules', []):
        if r.get('contains','').lower() in p:
            return 'RuleBased', f"folder:{r['contains']}"
    if in_project:
        return 'Git_Repo', 'project_detector'
    for c, exts in DEFAULT_MAP.items():
        if ext in exts:
            return c, 'category_map'
    return 'Unknown', 'fallback'
