---
tipo: analisis
fecha: 2026-11-23
periodo: 2026-09-16 → 2026-11-20
fuente: workouts/workouts.csv · sleepdata.csv
tags: [gym, analisis, revision]
---
# Revisión formal 2026-11-23 (Rutina v2)

Vuelve a [[00 - Inicio]] · Programa revisado: [[Rutina v2 - Regreso Sep26]] · Resultado: [[Rutina v3 - Constancia Nov26]]

> La revisión estaba prevista para el 8-nov y se hizo el 23-nov. La intermedia del 11-oct no se hizo.

## 0. Contexto del periodo
- **Tobillo derecho:** no hubo cita con el fisio. Mejoró por su cuenta y está al ~90 %. La progresión de pierna fue por tolerancia, adelantada respecto a las fases del plan.
- **Semana 26-oct → 1-nov:** cero sesiones por trabajo, estrés y gripe. Se trata como excepción.
- **13-nov:** entrenó en otro gym, así que esa sesión queda fuera de la comparación de KPI.
- **Estrés alto** sostenido. La nutrición se intentó mantener constante "pero ha sido difícil"; no hay kcal registradas.
- **Horario:** almuerza hasta las ~16:00, así que entrena tarde (empieza a las ~20:00).

## 1. Proceso
| Métrica | Objetivo | Real |
|---|---|---|
| Sesiones/sem | ≥3.5 | **2.3** (22 en 9.6 semanas) |
| Duración media | 75–90 min | **99.5 min** (rango 67–140) |
| % series efectivas | ≥75 % | **48 %** |
| % series al fallo/drop | ≤15 % | **19 %** (F2: 22 %) |
| Fallo en compuestos | 0 | **12** (la mayoría en jalones) |
| Rotación seguida | 100 % | 35 % (TORSO A 7 · POSTERIOR I 7 · TORSO B 4 · POSTERIOR II 3) |

Por qué: máquinas ocupadas, no recordar qué tocaba (elegía según las ganas) y fallo "según cómo me sienta". Las pirámides siguen igual. El "Warm Up" es movilidad dinámica de pies a cabeza, que está bien.

## 2. Volumen por músculo (series/sem, total fraccional)
| Músculo | Plan v2 | Real | Jun–Jul |
|---|---|---|---|
| Pecho | ~9 | 5.7 | 7.1 |
| Espalda | ~11 | 5.9 | 7.5 |
| Delt. lateral | 7 | 3.3 | 8.2 |
| Cuádriceps | ~9 | 6.0 | 8.8 |
| Isquios | 6–8 | **3.8** | 9.7 |
| Glúteo | ~6 | 4.4 | 5.2 |

Todo baja frente a Jun–Jul. Isquios cae más que nada porque POSTERIOR II casi desapareció.

## 3. KPIs de rendimiento (e1RM, kg)
**Corrección de unidades:** el export xlsx de septiembre registraba las mancuernas en **libras** etiquetadas como kg (factor 2.205). Lo confirmó el usuario: el Incline del 15-sep fue de 20 lb, que son 9.07 kg. El CSV es correcto y [[Baselines de rendimiento]] se recalculó desde él.

| Ejercicio | Media últimas 3 pre-pausa | Últimas 3 (nov) | % |
|---|---|---|---|
| Incline DB Press | 12.7 | 12.2 | −4 % |
| Iso-Lateral Chest Press | 34.6 | 26.8 | −23 % |
| Chest Fly | 94.0 | 88.2 | −6 % |
| Lat Pulldown | 79.6 | 72.3 | −9 % |
| Lat Pulldown Close Grip | 78.4 | 70.6 | −10 % |
| Single Arm Cable Row | 102.6 | 93.1 | −9 % |
| Shoulder Press (placas) | 35.0 | 21.5 | −39 % |
| Lateral Raise Machine | 45.1 | 24.6 | −45 % |
| Preacher Curl | 44.6 | 35.0 | −21 % |
| Leg Extension | 76.9 | 63.9 | −17 % |
| Leg Press | 136.4 | 114.9 | −16 % |
| Hip Thrust | 146.0 | 128.4 | −12 % |
| Pendulum Squat | 42.3 | 48.2 | **+14 %** |
| Cross Body Hammer Curl | 10.6 | 11.9 | **+12 %** |

Cumplen el objetivo "volver a la media pre-pausa antes del 8-nov": **no**. La mayoría quedan entre −5 y −25 %. Shoulder Press y Lateral Raise pueden estar afectados por cambios de máquina o por cómo se registra el peso por lado. Triceps: el KPI "Rope Pushdown" ya no se usa y ahora se registra "Pressdown", así que no son comparables.

## 4. Resultado corporal → [[Registro corporal]]
- **Peso:** 68.9 (22-sep) → 71.4 (18-nov y 23-nov). Son **+2.5 kg en 2 meses**, unos 1.3 kg/mes, frente al objetivo de ~0.2–0.35 kg/mes.
- **Medidas, línea base del 23-nov:** cintura 77 · cadera 96 · pecho 94 · hombro 116/124 · brazo 31/36 · muslo 57. Faltan fotos y pantorrillas.
- **Lectura:** la cintura está baja para el peso, así que la subida no parece "sucia". Aun así, el ritmo triplica lo planeado. Se congelan las calorías y se vigila la cintura.

## 5. Sueño (nuevo; `sleepdata.csv`, app tipo Sleep Cycle)
| | May–Jul | Programa (sep–nov) | Últimas 2 sem |
|---|---|---|---|
| Tiempo dormido (media) | 6.0 h | **5.9 h** | **5.3 h** |
| Noches <6 h | 38 % | 60 % | 91 % |
| Acostarse (media ± sd) | 00:14 ± 49 min | 23:44 ± 80 min | 00:06 |
| Levantarse | 07:07 | 06:46 | 06:33 (fijo) |

- **La hora de acostarse lo explica casi todo** (r = −0.84). Acostarse antes de las 23:30 da 6.6 h y calidad de 75 %. Después de las 00:30 da 4.8 h y calidad de 59 %.
- **Entrenar a las ≥18 h** se asocia con acostarse ~35 min más tarde y dormir **5.2 h**, frente a 6.4 h cuando entrena antes de las 18 h (n = 6, es una señal).
- La semana sin gym (26-oct) fue la de peor sueño (dos noches de 3.3 h): el problema fue el estrés y la gripe, no la carga.
- Datos incompletos: no hay noches del 16-sep al 9-oct y falta el 21 % desde el 10-oct.

## 6. Tobillo / salud → [[Registro tobillo]]
~90 %. No duele al hacer ejercicio, solo una leve molestia en la dorsiflexión cerrada y con el frío. Inflamación tras pierna: 2–3/10. Aguanta 30 s en una pierna. Usa tobillera en los días de pierna. **Ya no limita el programa.**

## 7. Aciertos · Errores · Ajustes
- **Aciertos:** volvió a entrenar con constancia razonable después de una pausa de 2 meses. El tobillo se recuperó sin recaídas. Pendulum y curl martillo superan lo que hacía antes de la pausa. La cintura está controlada.
- **Errores:** la rotación continua no funcionó en la práctica, siguieron el fallo en compuestos y las pirámides, las sesiones fueron largas y nocturnas, no hubo registros (tobillo, cuerpo, revisiones) y hubo poco sueño.
- **Ajustes:** días fijos, tope de 75+10 min, regla de fallo sin excepciones, plan B escrito, objetivo de sueño, calorías congeladas y proteína mínima.

## 8. Decisiones (copiadas a [[Bitacora de decisiones]])
1. Archivar la v2 y pasar a [[Rutina v3 - Constancia Nov26]] (días fijos Mar/Mié/Vie más un opcional en fin de semana).
2. Recalcular las líneas base desde el CSV en kg; el xlsx de septiembre queda descartado para pesos de mancuerna.
3. Báscula de referencia: la del gym. La de casa marca +1.1 kg.
4. Añadir la capa de sueño al [[Sistema de medicion]], con objetivo de 6.5 h y luego 7 h, y apagar la luz a las 23:15.
5. Congelar las calorías; proteína ≥120 g. Recortar si el peso sube >0.5 kg/mes o la cintura pasa de 78.
6. Tobillo dado de alta funcional sin fisio; se retoma la consulta si vuelven el dolor o la inestabilidad.

## 9. Pendientes
- [ ] Fotos frente, lado y espalda, y pantorrilla D/I.
- [ ] 3 pesajes en ayunas esta semana (báscula del gym, o la de casa restando 1.1).
- [ ] Crear en Hevy las 4 rutinas de la v3 con los nombres exactos.
- [ ] Adaptar `analisis_hevy.py` (periodo por parámetro, unidades) y arreglar el `.gitignore` (UTF-16).
- [ ] Actualizar el tablero visual a la v3.
