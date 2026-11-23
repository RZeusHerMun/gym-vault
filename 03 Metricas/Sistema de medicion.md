---
tipo: metodo
tags: [gym, metricas]
---
# Sistema de medición del progreso

Vuelve a [[00 - Inicio]]

Hipertrofia no se mide directo; se triangula con cuatro capas. Ninguna sola decide.

| Capa | Métrica | Fuente | Cadencia | Señal de que vamos bien |
|---|---|---|---|---|
| 1. Proceso | Sesiones/semana · duración · % series efectivas · % series al fallo | Hevy → `analisis_hevy.py` | Cada export (mensual) | ≥3 ses/sem (3 fijas de la v3) · ≤85 min · ≥75 % efectivas · fallo ≤15 % y 0 en compuestos |
| 2. Dosis | Series efectivas semanales por músculo | `volumen_semanal.csv` | Mensual | Pecho/espalda/cuádriceps ≥9–10; ningún músculo prioritario cae 2 semanas seguidas |
| 3. Rendimiento | e1RM del top set en ejercicios KPI | `e1rm_por_sesion.csv` → [[Baselines de rendimiento]] | Mensual | Tendencia positiva en ≥70 % de los KPI; ninguno plano >6 semanas |
| 4. Resultado | Peso corporal, perímetros, fotos | [[Registro corporal]] | Peso 3×/sem en ayunas, **báscula del gym** (la de casa −1.1 kg), media semanal · perímetros y fotos cada 2 semanas | +0.25–0.5 % peso/mes con cintura estable; brazo/muslo/pecho al alza |
| 0. Recuperación | Sueño: tiempo dormido medio semanal · noches <6 h · hora media de acostarse | App de sueño → `sleepdata.csv` | Semanal (export semanal o mensual) | ≥6.5 h → ≥7 h · luz apagada ≤23:15 al menos 5/7 noches |
| Contexto | Proteína/comidas · estrés · semanas excepcionales (enfermedad, viaje, otro gym) | Check-in semanal | Semanal | Proteína ≥120 g la mayoría de los días |
| Salud | Tobillo: dolor, inflamación, función | [[Registro tobillo]] | Cada sesión de pierna + mañana siguiente | Inflamación a la baja; desbloqueo de fases |

## Definiciones
- **Serie efectiva:** peso ≥85 % del peso tope del ejercicio en esa sesión, o marcada fallo/dropset. Calentamientos excluidos.
- **Series fraccionales:** músculo primario = 1, secundario = 0.5 (p. ej. jalón: espalda 1, bíceps 0.5).
- **e1RM:** peso × (1 + reps/30). Solo comparable dentro del mismo ejercicio y máquina.
- **KPI:** los 6 ejercicios en negrita de [[Rutina v3 - Constancia Nov26]].
- **Unidades:** todo en kg. Las mancuernas del gym están en libras: hay que registrarlas en Hevy en kg (o confirmar que Hevy convierte). El xlsx de septiembre tenía libras etiquetadas como kg; usar siempre el CSV.
- **Semana excepcional:** enfermedad, viaje u otro gym. No cuenta para tendencias de KPI ni de peso.

## Reglas de decisión
- **Si la media de sueño de la semana es de 6 h o menos, esa semana no cuenta para juzgar estancamiento.** No se toca el volumen; primero se arregla el sueño.
- KPI plano 3 sesiones seguidas con RIR real ≤2 → revisar orden, descanso y sueño antes de tocar volumen.
- KPI plano 6 semanas → cambiar a la opción B del slot o variar rango de reps.
- Peso corporal plano 3 semanas + KPIs planos (con sueño ≥6.5 h) → +150 kcal/día.
- Peso medio sube >0.5 kg/mes **o** cintura >78 cm → −150 kcal/día.
- Todo cambio se anota en [[Bitacora de decisiones]].
