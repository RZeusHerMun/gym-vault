---
tipo: MOC
tags: [gym, MOC]
---
# Gym IA — Inicio

Vault del proyecto de hipertrofia ("volumen limpio"). Aquí vive lo **investigado**, lo **implementado** y **cómo medimos** el progreso.

## Estado actual (23-nov-2026)
- Programa activo: [[Rutina v3 - Constancia Nov26]]: **Mar `TORSO A` · Mié `PIERNA` · Vie `TORSO B`** (+ fin de semana opcional)
- Última revisión: [[2026-11-23 Revision formal]] (v2 archivada)
- Prioridades: constancia de 3 sesiones por semana · sesiones ≤85 min · **sueño ≥6.5 h, luz apagada a las 23:15** · calorías congeladas
- Tobillo derecho ~90 %, ya no limita → [[Registro tobillo]]
- Tablero visual (desactualizado, es de la v2): [[Tablero y tiempos de sesion]] → https://claude.ai/artifact/6u8F6WdYW1G27cwU638Yux
- Próximas revisiones: **21-dic** (intermedia) · **18-ene** (formal)

## Mapa
| Carpeta         | Qué hay                                                                                                                |
| --------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `01 Programa`   | [[Rutina v3 - Constancia Nov26]] · [[Rutina v2 - Regreso Sep26]] · [[Tablero y tiempos de sesion]] · [[Rutina v1 - Torso-Posterior 4x (Abr-Jul26)]]                                         |
| `02 Analisis`   | [[2026-11-23 Revision formal]] · [[2026-09-16 Analisis Abr-Sep26]] (+ `adjuntos/` con gráficas)                                                         |
| `03 Metricas`   | [[Sistema de medicion]] · [[Baselines de rendimiento]] · [[Registro corporal]] · [[Registro tobillo]] · CSVs derivados |
| `04 Principios` | [[Principios de entrenamiento]]                                                                                        |
| `05 Plantillas` | [[Plantilla revision de programa]]                                                                                     |
| `99 Bitacora`   | [[Bitacora de decisiones]]                                                                                             |
| `workouts`      | Export de Hevy **CSV acumulado** (`workouts.csv`, reemplazar en cada export). `sleepdata.csv` (raíz) = app de sueño                                                                    |
| `scripts`       | `analisis_hevy.py` — regenera métricas desde un export                                                                 |

## Flujo de trabajo
1. Exportar Hevy en **CSV** → reemplazar `workouts/workouts.csv`. Exportar la app de sueño → reemplazar `sleepdata.csv`.
2. Correr `python scripts/analisis_hevy.py workouts/<archivo>` dentro de `03 Metricas` (o pedírselo a Claude).
3. Nueva nota en `02 Analisis` con fecha `AAAA-MM-DD`, usando la plantilla.
4. Toda decisión de cambio → una línea en [[Bitacora de decisiones]].
5. Si cambia el programa → nueva versión en `01 Programa` (no se edita la anterior; se marca `estado: archivado`).
