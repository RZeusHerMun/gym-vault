"""Análisis del export de Hevy (CSV o xlsx).

Uso (desde la raíz del vault):
    python scripts/analisis_hevy.py workouts/workouts.csv --desde 2026-11-24 --hasta 2026-12-21
    python scripts/analisis_hevy.py workouts/workouts.csv --desde 2026-09-16 --hasta 2026-11-20 \
        --base-desde 2026-04-13 --base-hasta 2026-07-24 --excluir 2026-11-13

Imprime para el periodo [desde, hasta]:
  1. Proceso: sesiones/sem, duración, % series efectivas, % fallo/dropset y fallo en compuestos.
  2. Volumen semanal por músculo (series fraccionales: primario=1, secundario=0.5), totales y efectivas.
  3. KPI de e1RM: media de las últimas 3 sesiones del periodo vs la base (por defecto, las 3 previas a --desde).
  4. Avisos de calidad: posibles pesos en libras, nombres de sesión fuera de la rutina.
Escribe en --out (por defecto "03 Metricas"): volumen_semanal.csv y e1rm_por_sesion.csv (historial completo).

Definiciones (ver 03 Metricas/Sistema de medicion.md):
  - Se excluyen las series marcadas como warmup.
  - Serie efectiva: peso >= 85 % del peso tope del ejercicio en esa sesión, o marcada fallo/dropset.
  - e1RM = peso * (1 + reps/30).
"""
import argparse
import re
from pathlib import Path

import pandas as pd

VAULT = Path(__file__).resolve().parent.parent
MESES = {'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'ago': 8,
         'sept': 9, 'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12}

# Rutina v3: KPI y nombres de sesión válidos
KPI = ['Incline Bench Press (Dumbbell)', 'Lat Pulldown (Cable)', 'Pendulum Squat (Machine)',
       'Hip Thrust (Barbell)', 'Single Arm Cable Row', 'Shoulder Press (Machine Plates)']
SESIONES = {'TORSO A', 'PIERNA', 'TORSO B', 'POSTERIOR + BRAZO',
            # v2 (histórico)
            'POSTERIOR I', 'POSTERIOR II'}
COMPUESTOS = ['Press', 'Pulldown', 'Row', 'Squat', 'Leg Press', 'Hip Thrust', 'Deadlift', 'Romanian', 'Dip']

# patrón en el nombre del ejercicio -> músculos (primario=1, secundario=0.5). Se evalúa en orden.
MUSCULOS = [
    ('Leg Curl', {'Isquios': 1}), ('Hammer Curl', {'Biceps': 1}), ('Curl', {'Biceps': 1}),
    ('Tricep', {'Triceps': 1}), ('Skullcrusher', {'Triceps': 1}), ('Straight Arm', {'Espalda': 1}),
    ('Lat Pulldown', {'Espalda': 1, 'Biceps': .5}), ('Romanian', {'Isquios': 1, 'Gluteo': .5}),
    ('Deadlift', {'Isquios': 1, 'Gluteo': .5, 'Espalda': .5}), ('Lateral Raise', {'DeltLat': 1}),
    ('Chest Press', {'Pecho': 1, 'Triceps': .5, 'DeltAnt': .5}),
    ('Bench Press', {'Pecho': 1, 'Triceps': .5, 'DeltAnt': .5}), ('Chest Fly', {'Pecho': 1}),
    ('Dip', {'Pecho': 1, 'Triceps': .5}), ('Leg Extension', {'Cuadri': 1}),
    ('Single Leg Extensions', {'Cuadri': 1}), ('Row', {'Espalda': 1, 'Biceps': .5, 'DeltPost': .5}),
    ('Shoulder Press', {'DeltAnt': 1, 'Triceps': .5, 'DeltLat': .5}), ('Front Raise', {'DeltAnt': 1}),
    ('Calf', {'Pantorrilla': 1}), ('Crunch', {'Abs': 1}), ('Knee Raise', {'Abs': 1}),
    ('Leg Press', {'Cuadri': 1, 'Gluteo': .5}), ('Squat', {'Cuadri': 1, 'Gluteo': .5}),
    ('Hip Thrust', {'Gluteo': 1, 'Isquios': .5}), ('Rear Delt', {'DeltPost': 1}),
    ('Face Pull', {'DeltPost': 1}), ('Hip Adduction', {'Aductor': 1}), ('Hip Abduction', {'Gluteo': 1}),
    ('Back Extension', {'Isquios': .5, 'Gluteo': .5}),
]


def fecha(s):
    m = re.match(r'(\d+) (\w+)\.? (\d+), (\d+):(\d+)', str(s))
    return pd.Timestamp(int(m[3]), MESES[m[2].strip('.')], int(m[1]), int(m[4]), int(m[5]))


def musculos(ej):
    for patron, m in MUSCULOS:
        if patron in ej:
            return m
    return {}


def cargar(ruta):
    d = pd.read_csv(ruta) if str(ruta).endswith('.csv') else pd.read_excel(ruta)
    d['st'] = d.start_time.map(fecha)
    d['en'] = d.end_time.map(fecha)
    return d


def parece_libras(w):
    """True si el peso en kg corresponde a un número 'redondo' de libras y no a uno de kg."""
    if pd.isna(w) or w <= 0:
        return False
    lb = w * 2.20462
    redondo_lb = abs(lb - round(lb * 2) / 2) < 0.03          # múltiplo de 0.5 lb
    redondo_kg = abs(w * 4 - round(w * 4)) < 0.01             # múltiplo de 0.25 kg
    return redondo_lb and not redondo_kg


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('archivo')
    ap.add_argument('--desde', required=True, help='AAAA-MM-DD, inicio del periodo a analizar')
    ap.add_argument('--hasta', default=None, help='AAAA-MM-DD inclusive (por defecto: última sesión)')
    ap.add_argument('--base-desde', default=None, help='inicio del periodo base para comparar KPI')
    ap.add_argument('--base-hasta', default=None, help='fin del periodo base (por defecto: día antes de --desde)')
    ap.add_argument('--excluir', nargs='*', default=[], help='fechas AAAA-MM-DD a excluir (otro gym, enfermedad)')
    ap.add_argument('--out', default=str(VAULT / '03 Metricas'), help='carpeta de salida de los CSV')
    a = ap.parse_args()

    d = cargar(a.archivo)
    excl = {pd.Timestamp(x).date() for x in a.excluir}
    d = d[~d.st.dt.date.isin(excl)]
    ini = pd.Timestamp(a.desde)
    fin = pd.Timestamp(a.hasta) + pd.Timedelta(days=1) if a.hasta else d.st.max() + pd.Timedelta(minutes=1)
    trabajo = d[(d.set_type != 'warmup') & d.reps.notna() & (d.reps > 0)].copy()
    trabajo['top'] = trabajo.groupby(['st', 'exercise_title']).weight_kg.transform('max')
    trabajo['efectiva'] = (trabajo.weight_kg.fillna(0) >= .85 * trabajo.top.fillna(0)) | \
        trabajo.set_type.isin(['failure', 'dropset'])

    per = trabajo[(trabajo.st >= ini) & (trabajo.st < fin)]
    ses = d[(d.st >= ini) & (d.st < fin)].drop_duplicates('st')
    semanas = max((min(fin, d.st.max()) - ini).days / 7, 1 / 7)
    print(f'=== Periodo {ini.date()} → {(fin - pd.Timedelta(days=1)).date()} · {semanas:.1f} semanas'
          + (f' · excluidas: {", ".join(a.excluir)}' if a.excluir else ''))

    # 1. Proceso
    dur = (ses.en - ses.st).dt.total_seconds() / 60
    fallo = per.set_type.isin(['failure', 'dropset'])
    comp = per.exercise_title.apply(lambda e: any(c in e for c in COMPUESTOS)) & \
        ~per.exercise_title.str.contains('Leg Curl|Leg Extension|Calf|Raise|Fly|Curl|Tricep', regex=True)
    print('\n1. Proceso')
    print(f'   sesiones: {len(ses)} ({len(ses) / semanas:.1f}/sem) · duración media {dur.mean():.0f} min '
          f'(mediana {dur.median():.0f}, rango {dur.min():.0f}–{dur.max():.0f})')
    print(f'   series de trabajo: {len(per)} ({len(per) / max(len(ses), 1):.1f}/sesión) · efectivas '
          f'{per.efectiva.mean() * 100:.0f} % · fallo+drop {fallo.mean() * 100:.0f} % · '
          f'fallo/drop en compuestos: {int((fallo & comp).sum())}')
    print('   por sesión:', ses.title.value_counts().to_dict())
    semana_iso = ses.st.dt.strftime('%G-W%V').value_counts().sort_index()
    print('   por semana ISO:', semana_iso.to_dict())

    # 2. Volumen por músculo
    filas = [(x.st, m, v, x.efectiva) for x in per.itertuples() for m, v in musculos(x.exercise_title).items()]
    vol = pd.DataFrame(filas, columns=['st', 'm', 'v', 'ef'])
    if len(vol):
        t = pd.DataFrame({'total/sem': vol.groupby('m').v.sum() / semanas,
                          'efectivas/sem': vol[vol.ef].groupby('m').v.sum() / semanas}).fillna(0).round(1)
        print('\n2. Volumen semanal por músculo (series fraccionales)')
        print(t.sort_values('total/sem', ascending=False).to_string())

    # 3. KPI e1RM
    trabajo['e1rm'] = trabajo.weight_kg * (1 + trabajo.reps / 30)
    g = trabajo[trabajo.weight_kg > 0].groupby(['exercise_title', 'st']).e1rm.max().reset_index()
    bini = pd.Timestamp(a.base_desde) if a.base_desde else None
    bfin = pd.Timestamp(a.base_hasta) + pd.Timedelta(days=1) if a.base_hasta else ini
    print('\n3. KPI e1RM (media de 3 sesiones: últimas de la base vs últimas del periodo)')
    filas = []
    for ej in KPI:
        x = g[g.exercise_title == ej]
        base = x[(x.st < bfin) & ((x.st >= bini) if bini is not None else True)].sort_values('st').e1rm.tail(3)
        ahora = x[(x.st >= ini) & (x.st < fin)].sort_values('st').e1rm
        b, p = base.mean(), ahora.tail(3).mean()
        filas.append((ej, round(b, 1), len(ahora), round(p, 1),
                      f'{(p / b - 1) * 100:+.0f} %' if len(ahora) and len(base) else '—'))
    print(pd.DataFrame(filas, columns=['ejercicio', 'base', 'n periodo', 'periodo', 'Δ']).to_string(index=False))

    # 4. Avisos
    # las mancuernas del gym están en libras: que salgan "convertidas" es lo esperado
    mancuerna = per.exercise_title.str.contains('Dumbbell|Hammer Curl|DB', regex=True)
    lb = per[per.weight_kg.apply(parece_libras) & ~mancuerna]
    print('\n4. Avisos')
    if len(lb):
        print(f'   {len(lb)} series de máquina/barra con peso que parece convertido de libras (¿otro gym?):')
        print('   ', lb.groupby([lb.st.dt.date, 'exercise_title']).size().to_string().replace('\n', '\n    '))
    otros = sorted(set(ses.title) - SESIONES)
    if otros:
        print('   nombres de sesión fuera de la rutina:', otros)
    if not len(lb) and not otros:
        print('   sin avisos')

    # salidas (historial completo)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    todo = [(x.st, m, v) for x in trabajo.itertuples() for m, v in musculos(x.exercise_title).items()]
    s = pd.DataFrame(todo, columns=['st', 'm', 'v'])
    s['semana'] = s.st.dt.to_period('W').dt.start_time
    s[s.st >= '2026-01-01'].pivot_table(index='semana', columns='m', values='v', aggfunc='sum') \
        .fillna(0).to_csv(out / 'volumen_semanal.csv')
    g.assign(e1rm=g.e1rm.round(1)).rename(columns={'e1rm': 'e1RM_top'}).to_csv(out / 'e1rm_por_sesion.csv', index=False)
    print(f'\nCSV escritos en {out}')


if __name__ == '__main__':
    main()
