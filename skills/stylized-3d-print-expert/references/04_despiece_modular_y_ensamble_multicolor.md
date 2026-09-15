# 04 · Despiece Modular y Ensamble Multicolor para Impresoras Monomaterial

## 1. Por Qué Imprimir un Personaje en una Sola Pieza es un Error

Intentar imprimir un personaje orgánico completo (cabeza, torso, extremidades y accesorios) de una sola vez en una impresora FDM monomaterial (como la Creality Ender-3 S1 Pro) genera 3 problemas críticos:

1. **Cicatrices de Soporte en Zonas Visibles**:
   - La barbilla, las axilas y los voladizos inferiores quedan cubiertos de estructuras de soporte. Al retirarlos, dejan una superficie rugosa, picada y blanquecina imposible de disimular en la piel del muñeco.
2. **Monocromatismo Forzado**:
   - Todo el muñeco sale de un único color de filamento. Para que parezca un producto comercial, exige pintar a mano con imprimación y acrílicos, perdiendo la limpieza del acabado plástico inyectado.
3. **Riesgo Catastrófico de Fallo en Máquina**:
   - Si una impresión de 15 horas falla en la hora 14 (por un despegue en una oreja o atasco puntual), se pierde todo el muñeco y cientos de gramos de filamento.

---

## 2. La Filosofía del Despiece Profesional de Juguetes (Toy-Art Modular)

La técnica estándar en la industria de figuras de colección (Pop Mart, Good Smile Company, Kidrobot) consiste en **descomponer el modelo tridimensional por sus líneas de costura o ensambles naturales**:

```
               [ Oreja Izq ]       [ Oreja Der ]
                    \                 /
                     [ CABEZA FRENTE ]
                     [  (Visor/Cara) ]
                            │
                       [ COLLAR ]
                            │
                    [ TORSO / CUERPO ] ── [ Mochila Trasera ]
                    /                \
          [ Brazo Izq ]            [ Brazo Der ]
                │                        │
         [ Pierna Izq ]            [ Pierna Der ]
```

### Ventajas Radicales del Despiece Modular:
- **Impresión Multicolor Sin Cambios de Filamento en Caliente**:
  - Imprimes todas las piezas blancas juntas en una tanda (cabeza, cuerpo, brazos).
  - Imprimes las piezas turquesa en otra tanda (collar, orejas, mochila, emblemas).
  - Imprimes el marco del visor en filamento oscuro.
- **Cero o Mínimos Soportes**:
  - Cada pieza se orienta sobre su cara de corte plana apoyada contra la cama de impresión. Los voladizos desaparecen o se reducen a menos del 15%.
- **Recuperabilidad Inmediata**:
  - Si una pierna o un botón falla al imprimir, solo se repite esa pequeña pieza de 15 minutos, sin comprometer el cuerpo de 4 horas.

---

## 3. Clavijas de Registro Macho-Hembra (Registration Keys)

Para que el usuario o ensamblador no tenga que adivinar la posición de las piezas ni correr el riesgo de que la cabeza quede torcida respecto al cuerpo, las uniones deben incorporar **clavijas geométricas de autocentrado**:

### Tipos de Encaje:
1. **Espiga Cilíndrica Única con Chaflán (Single Pin)**:
   - Adecuada para piezas simétricas o donde la orientación angular no es crítica (ej. botones redondos).
   - Diámetro recomendado: Ø6 a Ø8 mm. Altura: 6 a 8 mm. Chaflán superior: 45° de 1 mm para inserción asistida.
2. **Doble Espiga Anti-Rotación (Dual Pins / Keyed)**:
   - **Obligatoria en cabezas, torsos y extremidades**. Dos clavijas separadas impiden que la pieza rote sobre su eje Z durante el pegado.
   - El script `generate_keyed_split.py --dual-pins` genera automáticamente esta configuración.
3. **Uniones en Cola de Milano o Chaveteros Poligonales**:
   - Secciones hexagonales o cuadradas que obligan mecánicamente a una orientación angular única (poka-yoke).

---

## 4. Flujo de Trabajo para Dividir un Modelo Generado por IA

Cuando se obtiene la malla estanca del personaje (`personaje_estanco.stl`):

```bash
# 1. Separar la cabeza del cuerpo a la altura del cuello (ej. Z = 75 mm)
/Applications/Blender.app/Contents/MacOS/Blender -b --python \
    "/Users/frankalbertobetancesreinoso/Documentos locales/Proyecto Lua/.agents/skills/stylized-3d-print-expert/scripts/generate_keyed_split.py" -- \
    --input "personaje_estanco.stl" \
    --cut-z 75.0 \
    --output-top "cabeza_con_cajas.stl" \
    --output-bottom "cuerpo_con_espigas.stl" \
    --pin-diameter 7.0 \
    --pin-height 8.0 \
    --tolerance 0.25 \
    --dual-pins \
    --pin-spacing 18.0 \
    --pin-axis x \
    --place-on-bed

# 2. Las dos piezas resultantes están 100% cerradas (watertight),
# sus pines están autocentrados respecto a la sección real de corte
# y ambas bases quedan asentadas en Z=0 listas para Cura/PrusaSlicer.
```

---

## 5. Protocolo de Ensamble y Adhesión Química

1. **Prueba en Seco (Dry-Fit)**:
   - Presentar la espiga macho en el alojamiento hembra antes de aplicar adhesivo. Debe deslizarse hasta el fondo con suave presión de dedos. Si entra apretada por sobreextrusión puntual de la impresora, una pasada suave de lija grano 240 en la espiga es suficiente.
2. **Adhesivo Recomendado**:
   - **Cianoacrilato de viscosidad media o en gel** (ej. Loctite 401 o Super Glue Gel).
   - *Técnica*: Depositar 1 o 2 gotas en el fondo del hueco hembra, jamás en la superficie exterior, para evitar que el adhesivo rebose hacia la línea visible de la costura.
   - Presionar firmemente durante 15 segundos. La unión queda estructuralmente indivisible.
