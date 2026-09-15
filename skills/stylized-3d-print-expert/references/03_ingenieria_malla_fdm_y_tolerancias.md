# 03 · Ingeniería de Malla FDM, Estanqueidad y Tolerancias Mecánicas

## 1. La Regla de Oro: Malla 2-Manifold y Estanqueidad Absoluta

Un laminador 3D (Cura, PrusaSlicer, Bambu Studio) funciona calculando planos de intersección $Z$ a través de un volumen cerrado. Si la malla contiene aristas abiertas, huecos o caras que se intersectan a sí mismas, el laminador sufre fallos de cálculo que provocan:
- Rellenos sólidos donde debería haber huecos.
- Capas omitidas en el código G (`G-code gaps`).
- Extrusión en el aire y colapso de la pieza.

### Requisitos Geométricos Estrictos:
1. **Aristas no-manifold = 0**: Cada arista de la malla debe ser compartida por **exactamente dos caras**. Si una arista pertenece a 3 o más caras (unión interna de dos conchas), es no-manifold.
2. **Aristas de frontera (Boundary edges) = 0**: No puede haber ninguna arista abierta. La pieza debe ser un volumen hermético "sumergible en agua" (*Watertight*).
3. **Normales coherentes hacia el exterior**: Todas las normales de las caras deben apuntar hacia afuera. Las caras invertidas confunden el cálculo del "interior vs exterior".
4. **Caras de área cero = 0**: Deben eliminarse los triángulos degenerados donde dos vértices coinciden en el mismo punto del espacio.

El script `clean_and_watertight.py` garantiza el cumplimiento de estos 4 requisitos mediante su algoritmo de **Voxel Remesh**, que regenera la piel completa como un campo de distancia con signo (SDF).

---

## 2. Parámetros del Voxel Remesh para Figuras Infantiles

Al ejecutar `clean_and_watertight.py`, la elección del tamaño de vóxel (`--voxel-size`) determina el equilibrio entre detalle de la figura y tiempo de procesamiento:

| Tamaño de Vóxel | Detalle Obtenido | Tamaño de Triángulos | Caso de Uso Recomendado |
| :--- | :--- | :--- | :--- |
| **0.50 mm** | Medio (suprime micro-detalles) | ~30.000 - 50.000 | Prototipos rápidos, piezas internas |
| **0.30 mm** (Recomendado) | **Alto y óptimo** | ~100.000 - 150.000 | **Cuerpos, cabezas y piezas principales de juguetes** |
| **0.20 mm** | Ultra-fino (captura texturas mínimas) | ~250.000 - 500.000 | Expresiones faciales diminutas, ojos, medallas |
| **< 0.15 mm** | Excesivo | > 1.000.000 | Innecesario para boquillas FDM de 0.4 mm |

---

## 3. Matriz de Tolerancias Mecánicas para FDM (Ender-3 S1 Pro)

Las impresoras 3D FDM depositan filamento termoplástico fundido que sufre una pequeña expansión lateral al salir de la boquilla (*die swell*) y contracción térmica al enfriarse. Por ello, dos piezas modeladas con la misma cota nominal **jamás encajarán físicamente**.

Para ensambles por encaje o clavijas (pines macho-hembra), se debe aplicar la siguiente tabla de holgura radial $\Delta$:

```
   Pieza Macho (Espiga)             Pieza Hembra (Alojamiento)
        ┌──────┐                       ┌──────────────┐
        │  ØD  │                       │ Ø(D + 2Δ)    │
        │      │                       │   ┌──────┐   │
        │      │                       │   │      │   │
        └──────┘                       └───┴──────┴───┘
```

| Tipo de Ajuste | Holgura Radial ($\Delta$) | Comportamiento Físico en PLA / PETG | Aplicación Típica |
| :--- | :---: | :--- | :--- |
| **Prensa Fija (Press-fit)** | **0.15 mm** | Entra a presión dura con mazo de goma; no se sale sin herramientas. | Espigas permanentes sin pegamento |
| **Deslizamiento Suave (Slip-fit)** | **0.25 mm** | **Entra con la mano suavemente; ideal para unir con 1 gota de cianoacrilato.** | **Clavijas de cabeza, brazos y mochilas (RECOMENDADO)** |
| **Holgado / Desmontable** | **0.35 mm** | Entra y sale sin fricción con juego mínimo perceptible. | Tapas de baterías, trampillas de inspección |
| **Articulación Móvil** | **0.50 mm** | Permite rotación o bisagra libre sin agarrotamiento por hilos de filamento. | Ruedas, articulaciones giratorias |

> **Mandato del Skill**: El script `generate_keyed_split.py` aplica por defecto **$\Delta = 0.25\text{ mm}$**, garantizando que las piezas impresas en la Ender-3 S1 Pro encajen a la primera sin necesidad de limar o lijar.

---

## 4. Grosor de Pared y Solidez Pediátrica

En figuras destinadas a niñas y niños (donde existe riesgo de caídas, golpes o manipulación energética), las paredes del modelo deben resistir impactos mecánicos:

- **Grosor mínimo de pared exterior**: $1.6\text{ mm}$ a $2.0\text{ mm}$ (equivalente a 4 o 5 pasadas de perímetro con boquilla de 0.4 mm).
- **Evitar efecto "radiografía" del relleno**: Menos de 3 perímetros permite que el patrón de relleno interior (rejilla o giroide) se transparente en la superficie lisa exterior, arruinando el acabado estético.
- **Relleno interior (Infill)**:
  - Para figuras decorativas de exposición: 10% - 15% (Giroide).
  - Para muñecos interactivos pediátricos o maquetas de peso: 20% - 25% (Giroide o Cúbico adaptativo).
