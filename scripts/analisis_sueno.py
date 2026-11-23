"""Análisis del export de la app de sueño (CSV separado por ';', tipo Sleep Cycle).

Uso (desde la raíz del vault):
    python scripts/analisis_sueno.py sleepdata.csv --desde 2026-11-24
    python scripts/analisis_sueno.py sleepdata.csv --desde 2026-09-16 --hasta 2026-11-20 --hevy workouts/workouts.csv

Imprime:
  1. Resumen del periodo: tiempo dormido (no tiempo en cama), % noches <6 h / <7 h, hora de acostarse y
     levantarse, eficiencia, latencia, calidad y cobertura (noches registradas).
  2. Tabla por semana ISO con la fila para el check-in: media, noches >=7 h, noches <6 h, acostarse, registradas.
  3. Duración según la hora de acostarse.
  4. Con --hevy: sueño la noche después de entrenar >=18 h, <18 h o sin entrenar.
Objetivos (Rutina v3): media >= 6.5 h (luego >= 7 h) · luz apagada <= 23:15 al menos 5/7 noches.
"""
import argparse
import re

import numpy as np
import pandas as pd

MESES = {'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'ago': 8,
         'sept': 9, 'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12}
OBJ_ACOSTARSE = 23.25  # 23:15


def hhmm(h):
    h = h % 24
    return f'{int(h):02d}:{int(round((h % 1) * 60)) % 60:02d}'


def noches(ruta):
    d = pd.read_csv(ruta, sep=';', encoding='utf-8-sig', na_values=['—'])
    d['bed'] = pd.to_datetime(d['Went to bed'])
    d['wake'] = pd.to_datetime(d['Woke up'])
    d['cama'] = d['Time in bed (seconds)'] / 3600
    d['dormido'] = d['Time asleep (seconds)'] / 3600
    d['lat'] = d['Asleep after (seconds)'] / 60
    d['q'] = pd.to_numeric(d['Sleep Quality'].astype(str).str.rstrip('%'), errors='coerce')
    d = d[(d.cama <= 16) & (d.dormido > 0)]                       # artefactos y fragmentos vacíos
    d['noche'] = (d.bed - pd.Timedelta(hours=12)).dt.normalize()   # la noche del día en que te acuestas
    n = d.groupby('noche').agg(bed=('bed', 'min'), wake=('wake', 'max'), dormido=('dormido', 'sum'),
                               cama=('cama', 'sum'), lat=('lat', 'first'), q=('q', 'max'),
                               animo=('Mood', 'last')).reset_index()
    n = n[n.dormido >= 3].copy()                                   # noches incompletas
    bh = n.bed.dt.hour + n.bed.dt.minute / 60
    n['bed_h'] = np.where(bh > 12, bh - 24, bh)
    n['wake_h'] = n.wake.dt.hour + n.wake.dt.minute / 60
    n['efic'] = n.dormido / n.cama * 100
    return n


def resumen(x):
    a = x.dormido
    return pd.Series({
        'noches': len(x), 'media_h': a.mean(), 'mediana_h': a.median(),
        '<6h %': (a < 6).mean() * 100, '<7h %': (a < 7).mean() * 100,
        'acostarse': hhmm(x.bed_h.mean()), 'sd_acostarse_min': x.bed_h.std() * 60,
        'levantarse': hhmm(x.wake_h.mean()), 'eficiencia %': x.efic.mean(),
        'latencia_min (mediana)': x.lat.median(), 'calidad %': x.q.mean(),
        'luz <=23:15 %': (x.bed_h <= OBJ_ACOSTARSE - 24).mean() * 100,
        'deuda vs 7h (h/noche)': (7 - a).clip(lower=0).mean()})


def sesiones_hevy(ruta):
    w = pd.read_csv(ruta) if ruta.endswith('.csv') else pd.read_excel(ruta)

    def f(s):
        m = re.match(r'(\d+) (\w+)\.? (\d+), (\d+):(\d+)', str(s))
        return pd.Timestamp(int(m[3]), MESES[m[2].strip('.')], int(m[1]), int(m[4]), int(m[5]))
    return w.drop_duplicates('start_time').start_time.map(f)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('archivo')
    ap.add_argument('--desde', required=True)
    ap.add_argument('--hasta', default=None)
    ap.add_argument('--hevy', default=None, help='export de Hevy para cruzar con entrenamiento')
    a = ap.parse_args()

    n = noches(a.archivo)
    ini = pd.Timestamp(a.desde)
    fin = pd.Timestamp(a.hasta) if a.hasta else n.noche.max()
    p = n[(n.noche >= ini) & (n.noche <= fin)].copy()
    dias = (fin - ini).days + 1
    pd.set_option('display.width', 160)

    print(f'=== Sueño {ini.date()} → {fin.date()} · {len(p)}/{dias} noches registradas '
          f'({len(p) / dias * 100:.0f} %)')
    print('\n1. Resumen')
    print(resumen(p).map(lambda v: round(v, 1) if isinstance(v, float) else v).to_string())

    print('\n2. Por semana (fila para el check-in)')
    p['semana'] = p.noche.dt.strftime('%G-W%V')
    sem = p.groupby('semana').agg(registradas=('dormido', 'size'), media_h=('dormido', 'mean'),
                                  noches_7h=('dormido', lambda s: int((s >= 7).sum())),
                                  noches_menos6h=('dormido', lambda s: int((s < 6).sum())),
                                  acostarse=('bed_h', 'mean'),
                                  luz_2315=('bed_h', lambda s: int((s <= OBJ_ACOSTARSE - 24).sum())))
    sem['acostarse'] = sem.acostarse.map(hhmm)
    sem['estado'] = np.where(sem.media_h <= 6, 'NO cuenta (≤6 h)', np.where(sem.media_h >= 6.5, 'ok', 'justo'))
    print(sem.round(2).to_string())

    print('\n3. Según la hora de acostarse')
    p['franja'] = pd.cut(p.bed_h, [-6, -0.5, 0, 0.5, 6], labels=['<23:30', '23:30–00:00', '00:00–00:30', '>00:30'])
    print(p.groupby('franja', observed=False).agg(n=('dormido', 'size'), dormido_h=('dormido', 'mean'),
                                                  calidad=('q', 'mean')).round(2).to_string())

    if a.hevy:
        st = sesiones_hevy(a.hevy)
        tarde = set(st[st.dt.hour >= 18].dt.normalize())
        temprano = set(st[st.dt.hour < 18].dt.normalize())
        p['tipo'] = np.select([p.noche.isin(tarde), p.noche.isin(temprano)],
                              ['entreno ≥18h', 'entreno <18h'], 'sin entreno')
        print('\n4. Noche después de entrenar')
        t = p.groupby('tipo').agg(n=('dormido', 'size'), dormido_h=('dormido', 'mean'), acostarse=('bed_h', 'mean'))
        t['acostarse'] = t.acostarse.map(hhmm)
        print(t.round(2).to_string())


if __name__ == '__main__':
    main()
