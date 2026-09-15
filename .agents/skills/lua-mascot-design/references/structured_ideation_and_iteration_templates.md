# Metodología de Trabajo: Ideación Estructurada, Constitución de Honestidad e Iteración Visual

Este documento formaliza las plantillas y protocolos que el especialista debe emplear obligatoriamente al formular propuestas de diseño, evaluar alternativas y documentar cambios iterativos para Lúa.

---

## 🏛️ 1. Constitución de Honestidad y Declaración de Primera Línea

### Regla de la Primera Línea
- **Mandato**: La primera línea de cualquier respuesta o propuesta de diseño debe contener el veredicto directo, la recomendación principal o la alerta técnica crítica.
- **Prohibición**: Cero fórmulas de cortesía introductorias ("¡Hola! Claro que sí...", "Con mucho gusto voy a presentarte...").

### Distinción Rigurosa: Hecho vs. Propuesta
- **Hecho (Limitación Técnica Confirmada)**: Restricciones de hardware comprobadas (ej. "La pantalla circular GC9A01 recorta los 18 px de las esquinas en coordenadas $(x, y) < 18$").
- **Propuesta (Idea Creativa / Hipótesis)**: Sugerencias de diseño que requieren comprobación empírica (ej. "Propuesta: Utilizar un destello de 2 px en color `#FEF08A` para simular el brillo del ojo en reposo; requiere validación de contraste bajo luz solar directa").

---

## 💡 2. Plantilla de Ideación Estructurada (2-3 Enfoques Comparativos)

Cuando se evalúe un nuevo elemento visual o mecánica de juego, se deben presentar exactamente 2 o 3 alternativas contrastantes siguiendo esta estructura:

```markdown
### 🎯 Propuesta Principal Recomendada: [Nombre del Concepto A]
[Descripción concisa del diseño o mecánica principal]

---

### ⚖️ Comparativa Estructurada de Enfoques:

#### Enfoque A: [Nombre de la Opción A - Recomendada]
- **Beneficio**: [Ventaja clínica, visual o de UX directa]
- **Riesgo**: [Posible punto débil o sobrecarga visual]
- **Trade-off**: [Qué se gana vs. qué se cede a nivel de píxeles/memoria/atención]
- **Condición que lo desaconseja**: [En qué escenario clínico o técnico NO debe usarse]

#### Enfoque B: [Nombre de la Opción B - Alternativa Radical]
- **Beneficio**: [Ventaja del enfoque alternativo]
- **Riesgo**: [Riesgo asociado]
- **Trade-off**: [Compromiso técnico o perceptivo]
- **Condición que lo desaconseja**: [Cuándo evitarlo]

#### Enfoque C (Opcional): [Nombre de la Opción C]
- **Beneficio**: [...]
- **Riesgo**: [...]
- **Trade-off**: [...]
- **Condición que lo desaconseja**: [...]

---

### 🏁 Recomendación Explícita:
[Veredicto definitivo y justificación clínica/técnica de por qué se adopta la opción elegida].
```

---

## 🔄 3. Protocolo de Iteración Visual ("Mantengo / Elimino / Cambio")

En cada ronda de refinamiento o respuesta a feedback del usuario, el encabezado del diseño debe resumir obligatoriamente el estado de los elementos:

```markdown
### 📋 Registro de Iteración Visual:

- **Mantengo**:
  - [Elemento Aprobado 1: Ej. Silueta de orejas con tono base `#2D3748` y rosa `#FCA5A5`]
  - [Elemento Aprobado 2: Ej. Timing de 1.2 segundos para la celebración corta]

- **Elimino**:
  - [Elemento Descartado 1: Ej. Destellos en forma de cruz de 4 px (generaban ruido visual en 24x24)]
  - [Elemento Descartado 2: Ej. Expresión con ceño fruncido ante fallos]

- **Cambio**:
  - [Modificación 1: De ojos redondos a ojos en medialuna cerrada para la emoción Amor (`AFFECT 1`)]
  - [Modificación 2: Desplazamiento del hocico 1 px hacia abajo para mejorar el centrado en el círculo]
```

---

## 🧪 4. Checklist de Validación Empírica antes de Confirmar

Antes de dar por finalizado un sprite o animación:
- [ ] ¿Cumple con la matriz de $24 \times 24$ píxeles (o submódulos de cara)?
- [ ] ¿Utiliza exclusivamente los 21 colores de la paleta oficial RGB565?
- [ ] ¿Queda dentro de la máscara circular ($R \le 108\text{ px}$)?
- [ ] ¿Es 100% libre de texto alfanumérico?
- [ ] ¿Respeta el principio de "Lúa no castiga" (sin caras tristes o punitivas)?
- [ ] ¿Ha sido probado visualmente en el emulador local (`make shots` / `make run`)?
