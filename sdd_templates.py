"""Offline Aikya adaptations of the nine Spec Coding template categories.

Source pages were reviewed on 2026-10-22. No website text, examples, executable
code or project assumptions are imported. Optional section text is reviewed data.
"""
from __future__ import annotations
from pathlib import Path
from docs_layout import stamp


def _entry(filename, slug, fields):
    return {'filename':filename,'source':'https://spec-coding.dev/templates/'+slug,
            'fields':fields}


CATALOG = {
    'feature':_entry('feature.spec.md','feature-spec',{
        'owner':('Owner','Responsable'),'context':('Context','Contexto'),
        'non_goals':('Excluded scope','Fuera de alcance'),'edge_cases':('Boundary behavior','Casos límite'),
        'deliverables':('Expected deliverables','Entregables previstos'),
        'rollout':('Delivery sequence','Secuencia de entrega'),'rollback':('Recovery approach','Plan de reversión'),
        'evidence_required':('Evidence to collect','Evidencias necesarias')}),
    'api':_entry('api.spec.md','api-spec',{
        'owner':('Owner','Responsable'),'endpoint':('Endpoint contract','Contrato del endpoint'),
        'request':('Request shape','Estructura de petición'),'responses':('Response behavior','Comportamiento de respuestas'),
        'authorization':('Access rules','Reglas de acceso'),'idempotency':('Retry and replay rules','Reintentos e idempotencia'),
        'compatibility':('Consumer compatibility','Compatibilidad con consumidores'),
        'checks':('Contract checks','Comprobaciones del contrato'),'rollback':('Recovery approach','Plan de reversión')}),
    'database':_entry('database.spec.md','db-spec',{
        'owner':('Owner','Responsable'),'tables':('Affected data structures','Estructuras de datos afectadas'),
        'columns':('Field definitions','Definiciones de campos'),'constraints':('Data invariants','Invariantes de datos'),
        'indexes':('Query and index impact','Impacto en consultas e índices'),
        'migration':('Migration sequence','Secuencia de migración'),
        'compatibility':('Read/write compatibility','Compatibilidad de lectura y escritura'),
        'checks':('Data verification','Verificación de datos'),'rollback':('Recovery limits','Límites de reversión')}),
    'spec':_entry('spec.md','sdd-change-proposal',{
        'owner':('Owner','Responsable'),'context':('Problem context','Contexto del problema'),
        'non_goals':('Excluded scope','Fuera de alcance'),'evidence_required':('Evidence to collect','Evidencias necesarias'),
        'rollback':('Recovery approach','Plan de reversión')}),
    'design':_entry('design.md','sdd-design-doc',{
        'owner':('Owner','Responsable'),'context':('Design context','Contexto del diseño'),
        'alternatives':('Alternatives and rationale','Alternativas y justificación'),
        'interfaces':('Affected interfaces','Interfaces afectadas'),'constraints':('Design constraints','Restricciones de diseño'),
        'rollout':('Delivery sequence','Secuencia de entrega'),'rollback':('Recovery approach','Plan de reversión')}),
    'tasks':_entry('tasks.md','sdd-tasks-plan',{
        'owner':('Owner','Responsable'),'allowed_files':('Reviewed file scope','Archivos dentro del alcance'),
        'checks':('Checks to execute','Comprobaciones previstas'),'done_when':('Completion conditions','Condiciones de finalización')}),
    'evidence':_entry('evidence.md','sdd-evidence-log',{
        'owner':('Owner','Responsable'),'release':('Release context','Contexto de publicación'),
        'operational':('Observed operational evidence','Evidencias operativas observadas'),
        'manual_checks':('Recorded manual checks','Comprobaciones manuales registradas'),
        'known_gaps':('Unverified areas','Áreas sin verificar'),'stop_signal':('Stop conditions','Condiciones de parada')}),
    'review':_entry('review.md','ai-coding-review',{
        'reviewer':('Reviewer','Revisor'),'scope':('Observed change scope','Alcance de cambios observado'),
        'spec_alignment':('Requirement coverage','Cobertura de requisitos'),
        'evidence':('Reviewed evidence','Evidencias revisadas'),'decision':('Review conclusion','Conclusión de revisión'),
        'follow_up':('Follow-up work','Trabajo pendiente')}),
    'constitution':_entry('constitution.md','engineering-constitution',{
        'owner':('Owner','Responsable'),'applies_to':('Applicable scope','Ámbito de aplicación'),
        'principles':('Engineering principles','Principios de ingeniería'),
        'gates':('Required reviews','Revisiones necesarias'),'ai_rules':('Agent boundaries','Límites de los agentes'),
        'exceptions':('Reviewed exceptions','Excepciones revisadas'),'review_date':('Review date','Fecha de revisión')})
}
SPEC_TEMPLATES = frozenset(('spec','feature','api','database'))


def catalog() -> dict:
    return {name:{'filename':item['filename'],'source':item['source'],
                  'section_keys':list(item['fields'])} for name,item in CATALOG.items()}


def normalize_sections(name: str, value=None) -> dict[str,str]:
    if name not in CATALOG:raise ValueError('Unknown SDD template: '+str(name))
    if value is None:return {}
    if not isinstance(value,dict) or not set(value).issubset(CATALOG[name]['fields']):
        raise ValueError('Unknown or invalid sections for SDD template '+name)
    result={}
    for key,text in value.items():
        if not isinstance(text,str) or not text.strip() or len(text)>4000 or '\x00' in text:
            raise ValueError('Template sections require nonempty text of at most 4000 characters: '+str(key))
        result[key]=text.strip()
    if sum(map(len,result.values()))>20000:raise ValueError('Template sections exceed the document limit')
    return result


def render_sections(name: str, sections=None, language='en') -> str:
    values=normalize_sections(name,sections)
    return '\n\n'.join('## '+labels[language=='es']+'\n\n'+values[key]
                        for key,labels in CATALOG[name]['fields'].items() if key in values)


def source_note(name: str) -> str:
    return 'Template reference: [Spec Coding]('+CATALOG[name]['source']+'). Aikya adaptation.'


def starter(name: str) -> str:
    if name not in CATALOG:raise ValueError('Unknown SDD template: '+str(name))
    base=Path(__file__).resolve().parent/'sdd-templates'
    target=base/CATALOG[name]['filename']
    if base.is_symlink() or target.is_symlink():raise ValueError('Symlinked template assets are not supported')
    return stamp(target.read_text(encoding='utf8'))
