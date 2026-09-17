"""Analisis de export de Hevy. Uso: python analisis_hevy.py ruta/al/export.xlsx|csv
Genera: volumen semanal por musculo (CSV), baselines e1RM (CSV) y resumen por bloques en consola.
Series fraccionales: musculo primario=1, secundario=0.5. Se excluyen calentamientos.
Serie efectiva = peso >= 85% del peso tope del ejercicio en esa sesion, o marcada fallo/dropset."""
import sys
import pandas as pd,re
f=sys.argv[1]
d=pd.read_csv(f) if f.endswith('.csv') else pd.read_excel(f)
M={'ene':1,'feb':2,'mar':3,'abr':4,'may':5,'jun':6,'jul':7,'ago':8,'sept':9,'sep':9,'oct':10,'nov':11,'dic':12}
def p(s):
    m=re.match(r'(\d+) (\w+)\.? (\d+), (\d+):(\d+)',s)
    return pd.Timestamp(int(m[3]),M[m[2].strip('.')],int(m[1]),int(m[4]),int(m[5]))
d['st']=d.start_time.map(p);d['en']=d.end_time.map(p);d['date']=d.st.dt.date
# direct sets (primary=1, secondary=0.5)
P={'Lateral Raise':{'DeltLat':1},'Leg Curl':{'Isquios':1},'Triceps':{'Triceps':1},'Skullcrusher':{'Triceps':1},
'Chest Press':{'Pecho':1,'Triceps':.5,'DeltAnt':.5},'Bench Press':{'Pecho':1,'Triceps':.5,'DeltAnt':.5},'Chest Fly':{'Pecho':1},'Dip':{'Pecho':1,'Triceps':.5},
'Leg Extension':{'Cuadri':1},'Single Leg Extensions':{'Cuadri':1},'Curl':{'Biceps':1},
'Lat Pulldown':{'Espalda':1,'Biceps':.5},'Row':{'Espalda':1,'Biceps':.5,'DeltPost':.5},'Straight Arm':{'Espalda':1},
'Shoulder Press':{'DeltAnt':1,'Triceps':.5,'DeltLat':.5},'Front Raise':{'DeltAnt':1},
'Calf':{'Pantorrilla':1},'Crunch':{'Abs':1},'Knee Raise':{'Abs':1},
'Leg Press':{'Cuadri':1,'Gluteo':.5},'Squat':{'Cuadri':1,'Gluteo':.5},'Hip Thrust':{'Gluteo':1,'Isquios':.5},
'Rear Delt':{'DeltPost':1},'Face Pull':{'DeltPost':1},'Hip Adduction':{'Aductor':1},'Hip Abduction':{'Gluteo':1},
'Romanian':{'Isquios':1,'Gluteo':.5},'Deadlift':{'Isquios':1,'Gluteo':.5,'Espalda':.5},'Back Extension':{'Isquios':.5,'Gluteo':.5}}
order=['Leg Curl','Hammer Curl','Curl','Triceps','Skullcrusher','Straight Arm','Lat Pulldown','Romanian','Deadlift']
def mm(e):
    for k in order+list(P):
        if k in e:
            if k in('Hammer Curl',): return {'Biceps':1}
            return P[k]
    return {}
r=d[(d.set_type!='warmup')&d.reps.notna()&(d.reps>0)].copy()
rows=[]
for _,x in r.iterrows():
    for m,v in mm(x.exercise_title).items(): rows.append((x.st,m,v,x.set_type))
s=pd.DataFrame(rows,columns=['st','m','v','t'])
def blk(a,b,name):
    q=s[(s.st>=a)&(s.st<b)];wk=(pd.Timestamp(b)-pd.Timestamp(a)).days/7
    ns=d[(d.st>=a)&(d.st<b)].st.nunique()
    print(name,'semanas',round(wk,1),'sesiones',ns,'ses/sem',round(ns/wk,2))
    return (q.groupby('m').v.sum()/wk).round(1).rename(name)
t=pd.concat([blk('2026-01-05','2026-04-13','Ene-Abr12'),blk('2026-04-13','2026-06-01','Abr13-May'),blk('2026-06-01','2026-07-25','Jun-Jul24'),blk('2026-09-07','2026-09-16','Sep(regreso)')],axis=1)
print(t.to_string())
fs=r[(r.st>='2026-04-13')&(r.st<'2026-07-25')]
print('fallo+drop % sets',(fs.set_type.isin(['failure','dropset'])).mean().round(2))
w=d.drop_duplicates('st');w=w[(w.st>='2026-04-13')&(w.st<'2026-07-25')]
print('dur media',((w.en-w.st).dt.total_seconds()/60).mean().round())
print(w.groupby(w.st.dt.isocalendar().week).size().to_string())
print('---- progresion e1RM top set (media primeras 3 vs ultimas 3 sesiones, Abr13-Jul24) y regreso')
b=r[(r.st>='2026-04-13')&(r.weight_kg>0)].copy();b['e']=b.weight_kg*(1+b.reps/30)
g=b.groupby(['exercise_title','st']).e.max().reset_index()
out=[]
for e,x in g.groupby('exercise_title'):
    pre=x[x.st<'2026-07-25'];post=x[x.st>='2026-09-01']
    if len(pre)>=5:
        a=pre.e.head(3).mean();z=pre.e.tail(3).mean()
        out.append((e,len(pre),round(a,1),round(z,1),round((z/a-1)*100),round(post.e.max(),1) if len(post) else None, round((post.e.max()/z-1)*100) if len(post) else None))
print(pd.DataFrame(out,columns=['ej','n','ini','fin','%','sep','%vsJul']).sort_values('%').to_string())
# effective sets
b2=r[(r.st>='2026-04-13')&(r.st<'2026-07-25')].copy()
b2['top']=b2.groupby(['st','exercise_title']).weight_kg.transform('max')
b2['eff']=(b2.weight_kg>=.85*b2.top)|b2.set_type.isin(['failure','dropset'])
print('sets efectivos %',b2.eff.mean().round(2), 'sets/sesion',round(len(b2)/b2.st.nunique(),1),'ejercicios/sesion',round(b2.groupby('st').exercise_title.nunique().mean(),1))

# --- salidas a CSV
s['semana']=s.st.dt.to_period('W').dt.start_time
s[s.st>='2026-01-01'].pivot_table(index='semana',columns='m',values='v',aggfunc='sum').fillna(0).to_csv('volumen_semanal.csv')
g.assign(e=g.e.round(1)).rename(columns={'e':'e1RM_top'}).to_csv('e1rm_por_sesion.csv',index=False)
