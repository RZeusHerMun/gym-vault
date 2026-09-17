---
tipo: metodo
tags: [gym, metricas]
---
# Sistema de medición del progreso

Vuelve a [[00 - Inicio]]

Hipertrofia no se mide directo; se triangula con cuatro capas. Ninguna sola decide.

| Capa | Métrica | Fuente | Cadencia | Señal de que vamos bien |
|---|---|---|---|---|
| 1. Proceso | Sesiones/semana · duración · % series efectivas · % series al fallo | Hevy → `analisis_hevy.py` | Cada export (mensual) | ≥3.5 ses/sem · 75–90 min · ≥75 % efectivas · fallo ≤15 % y 0 en compuestos |
| 2. Dosis | Series efectivas semanales por músculo | `volumen_semanal.csv` | Mensual | Pecho/espalda/cuádriceps ≥9–10; ningún músculo prioritario cae 2 semanas seguidas |
| 3. Rendimiento | e1RM del top set en ejercicios KPI | `e1rm_por_sesion.csv` → [[Baselines de rendimiento]] | Mensual | Tendencia positiva en ≥70 % de los KPI; ninguno plano >6 semanas |
| 4. Resultado | Peso corporal, perímetros, fotos | [[Registro corporal]] | Peso 3×/sem (media semanal) · perímetros y fotos cada 2 semanas | +0.25–0.5 % peso/mes con cintura estable; brazo/muslo/pecho al alza |
| Salud | Tobillo: dolor, inflamación, función | [[Registro tobillo]] | Cada sesión de pierna + mañana siguiente | Inflamación a la baja; desbloqueo de fases |

## Definiciones
- **Serie efectiva:** peso ≥85 % del peso tope del ejercicio en esa sesión, o marcada fallo/dropset. Calentamientos excluidos.
- **Series fraccionales:** músculo primario = 1, secundario = 0.5 (p. ej. jalón: espalda 1, bíceps 0.5).
- **e1RM:** peso × (1 + reps/30). Solo comparable dentro del mismo ejercicio y máquina.
- **KPI por slot:** el ejercicio opción A de cada slot de [[Rutina v2 - Regreso Sep26]].

## Reglas de decisión
- KPI plano 3 sesiones seguidas con RIR real ≤2 → revisar orden, descanso y sueño antes de tocar volumen.
- KPI plano 6 semanas → cambiar a la opción B del slot o variar rango de reps.
- Peso corporal plano 3 semanas + KPIs planos → +150 kcal/día.
- Todo cambio se anota en [[Bitacora de decisiones]].
