---
tipo: MOC
tags: [gym, MOC]
---
# Gym IA — Inicio

Vault del proyecto de hipertrofia ("volumen limpio"). Aquí vive lo **investigado**, lo **implementado** y **cómo medimos** el progreso.

## Estado actual (16-sep-2026)
- Tablero visual (celular/gym): [[Tablero y tiempos de sesion]] → https://claude.ai/artifact/6u8F6WdYW1G27cwU638Yux
- Programa activo: [[Rutina v2 - Regreso Sep26]] — **Fase 0 · Re-entrada** (hasta 27-sep)
- Limitante: esguince de tobillo (~75 %), fisio esta semana → [[Registro tobillo]]
- Próxima sesión con Claude: actualización de medidas + indicaciones del fisio
- Próxima revisión: **11-oct** (intermedia) · **8-nov** (formal) con [[Plantilla revision de programa]]

## Mapa
| Carpeta         | Qué hay                                                                                                                |
| --------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `01 Programa`   | [[Rutina v2 - Regreso Sep26]] · [[Tablero y tiempos de sesion]] · [[Rutina v1 - Torso-Posterior 4x (Abr-Jul26)]]                                         |
| `02 Analisis`   | [[2026-09-16 Analisis Abr-Sep26]] (+ `adjuntos/` con gráficas)                                                         |
| `03 Metricas`   | [[Sistema de medicion]] · [[Baselines de rendimiento]] · [[Registro corporal]] · [[Registro tobillo]] · CSVs derivados |
| `04 Principios` | [[Principios de entrenamiento]]                                                                                        |
| `05 Plantillas` | [[Plantilla revision de programa]]                                                                                     |
| `99 Bitacora`   | [[Bitacora de decisiones]]                                                                                             |
| `workouts`      | Exports crudos de Hevy (`workouts_<mes><año>.xlsx`)                                                                    |
| `scripts`       | `analisis_hevy.py` — regenera métricas desde un export                                                                 |

## Flujo de trabajo
1. Exportar Hevy → guardar en `workouts/`.
2. Correr `python scripts/analisis_hevy.py workouts/<archivo>` dentro de `03 Metricas` (o pedírselo a Claude).
3. Nueva nota en `02 Analisis` con fecha `AAAA-MM-DD`, usando la plantilla.
4. Toda decisión de cambio → una línea en [[Bitacora de decisiones]].
5. Si cambia el programa → nueva versión en `01 Programa` (no se edita la anterior; se marca `estado: archivado`).
