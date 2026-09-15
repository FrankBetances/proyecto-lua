# Guía de Impresión 3D y Plan de Trabajo · Muñeco Lúa (Ender-3 S1 Pro)

> **Fecha:** 13/09/2026 · **Iteración:** V14 / Fase 3 USC (Oficial · 20 piezas)  
> **Impresora objetivo:** Creality Ender-3 S1 Pro (Cama 220 × 220 × 270 mm, boquilla 0,40 mm, monomaterial)  
> **Archivos STL locales:** [`stl/`](./stl/) (20 archivos STL verificados 100% estancos y cerrados)  
> **Paquete comprimido para taller / servicio:** [`LUA_STL.zip`](./LUA_STL.zip)  
> **Fuente CAD paramétrica:** [`lua-firmware/cad/lua-muneco.scad`](./lua-firmware/cad/lua-muneco.scad)  
> **Renders de referencia:** [`lua-firmware/docs/cad/`](./lua-firmware/docs/cad/)

---

## 1. Novedades y Evolución del Modelo (Septiembre 2026)

El modelo actual representa la **maqueta oficial de la Fase 3 del plan de la USC** para evaluación pediátrica y validación clínica:
1. **Emblema Centrado en el Pecho (`emblema.stl`)**:
   - Originalmente situado en $x = -11\text{ mm}$, ahora se encuentra perfectamente alineado en el eje central ($x = 0$). El asiento en la curva esférica del pecho se adelantó $+1,9\text{ mm}$ para asegurar un asentamiento al ras sin hundimientos.
2. **Pastilla Icónica del Logo (`logo.stl` [NUEVO])**:
   - Resuelve el hueco interior del emblema con la silueta estilizada de Lúa en relieve blanco de alta definición (14,9 × 14,9 × 1,6 mm).
3. **Pulsadores bajo Barbilla (`pulsadores.stl` [NUEVO])**:
   - Embellecedor oscuro que protege e interactúa con los pulsadores físicos del canto de la placa de desarrollo (`REST` y `BOOT`) a través de la ranura de carga. *Nota: se imprime una vez contrastadas las cotas con calibre*.
4. **Sujeción de PCB por Rosca Positiva (`anillo_placa.stl`)**:
   - Rosca trapecial Ø55 mm M55 integrada en `cabeza_frente.stl`. Sujeta firmemente la pantalla y placa absorbiendo espesores entre 8,0 mm y 16,0 mm sin requerir espuma adhesiva.
5. **Alineación Forzosa del Casco (`cabeza_dorso.stl`)**:
   - 2 espigas de centrado impiden que las dos mitades de la cabeza queden giradas al pegar con cianoacrilato.
6. **Túnel de Carga USB-C Despejado**:
   - Ranura de 16 mm bajo la barbilla y muesca pasante en `collar.stl` para conectar el cable de carga USB-C sin desmontar la figura.
7. **Probetas de Verificación Rápida (`testigo_placa.stl` y `testigo_rosca.stl`)**:
   - Dos piezas breves (~35 min de impresión combinada) que resuelven las tolerancias de PCB y rosca antes de lanzar las piezas de 4 horas.

---

## 2. Catálogo Oficial de los 20 Archivos STL

Todos los archivos han sido verificados matemáticamente mediante el gate [`tools/check-cad.js`](./lua-firmware/tools/check-cad.js): **0 aristas sueltas, 1 sola cáscara estanca (manifold), apoyo en Z = 0 y dentro de la cama 220 × 220 mm con 5 mm de margen**.

| Archivo STL | Cant. | Color sugerido | Huella X × Y × Z (mm) | Vol. Macizo | Función y Rol en el Ensamble |
| :--- | :---: | :--- | :---: | :---: | :--- |
| **`testigo_placa.stl`** | 1 | Cualquier color | 49.5 × 51.0 × 8.0 | 3.0 cm³ | **Probeta 1 (Calibración):** Valida contorno de PCB y ranura USB-C. |
| **`testigo_rosca.stl`** | 1 | Cualquier color | 61.0 × 61.0 × 12.0 | 5.3 cm³ | **Probeta 2 (Calibración):** Barril roscado M55 (*imprimir con balsa*). |
| **`anillo_placa.stl`** | 1 | Blanco / Libre | 57.2 × 57.2 × 11.0 | 5.4 cm³ | **Retención de PCB:** Se enrosca tras la placa dentro de la cabeza. |
| **`cuerpo.stl`** | 1 | Blanco | 75.4 × 65.5 × 80.0 | 164.3 cm³ | Tronco principal. Compartimento para batería y encajes de miembros. |
| **`cabeza_frente.stl`** | 1 | Blanco | 75.1 × 75.1 × 20.9 | 20.1 cm³ | Cara frontal, visor circular, 4 costillas interiores y rosca M55. |
| **`cabeza_dorso.stl`** | 1 | Blanco | 78.0 × 76.3 × 49.5 | 26.0 cm³ | Cúpula con respiraderos y 2 espigas de alineación (*brim 5 mm*). |
| **`brazo_izq.stl`** | 1 | Blanco + Turquesa | 20.0 × 19.0 × 39.4 | 7.1 cm³ | Brazo izquierdo vertical. Puño turquesa hasta Z=16.5 mm. |
| **`brazo_der.stl`** | 1 | Blanco + Turquesa | 20.0 × 19.0 × 39.4 | 7.1 cm³ | Brazo derecho vertical. Puño turquesa hasta Z=16.5 mm. |
| **`pierna_izq.stl`** | 1 | Blanco + Turquesa | 28.3 × 23.7 × 34.5 | 11.4 cm³ | Pierna izquierda vertical. Bota turquesa hasta Z=14.0 mm. |
| **`pierna_der.stl`** | 1 | Blanco + Turquesa | 28.3 × 23.7 × 34.5 | 11.4 cm³ | Pierna derecha vertical. Bota turquesa hasta Z=14.0 mm. |
| **`oreja_izq.stl`** | 1 | Turquesa | 30.0 × 29.9 × 8.2 | 2.5 cm³ | Oreja izquierda pegada con espiga en la cúpula. |
| **`oreja_der.stl`** | 1 | Turquesa | 30.0 × 29.9 × 8.2 | 2.5 cm³ | Oreja derecha pegada con espiga en la cúpula. |
| **`collar.stl`** | 1 | Turquesa | 34.4 × 36.6 × 8.5 | 3.8 cm³ | Anillo del cuello con muesca para USB-C hacia el frente. |
| **`mochila.stl`** | 1 | Turquesa | 48.0 × 36.0 × 10.4 | 14.7 cm³ | Tapa trasera asegurada con 2 tornillos métrica M2 × 8 mm. |
| **`boton.stl`** | 1 | Turquesa | 15.0 × 15.0 × 3.4 | 0.5 cm³ | Detalle estético pegado en la sien derecha. |
| **`emblema.stl`** | 1 | Turquesa | 22.0 × 22.0 × 2.4 | 0.6 cm³ | Aro exterior del escudo centrado en el pecho. Aloja `logo.stl`. |
| **`logo.stl`** | 1 | Blanco | 14.9 × 14.9 × 1.6 | 0.3 cm³ | **[NUEVO]** Silueta de Lúa pegada dentro del emblema. |
| **`cartucho.stl`** | 1 | Blanco / Libre | 33.2 × 9.2 × 23.2 | 2.5 cm³ | Cuna interior para sujetar la celda de litio con cinta doble cara. |
| **`aro_visor.stl`** | 1 | Oscuro / Negro | 44.0 × 44.0 × 1.6 | 0.9 cm³ | Marco circular del visor que enmarca la pantalla IPS. |
| **`pulsadores.stl`** | 1 | Oscuro / Negro | 28.3 × 11.3 × 16.3 | 0.7 cm³ | **[NUEVO]** Guía de botones bajo barbilla (*medir placa antes*). |

---

## 3. Plan de Impresión por Tandas Inteligentes

Diseñado para optimizar cambios de filamento y garantizar el éxito mecánico sin desperdiciar tiempo ni material:

```mermaid
graph TD
    T0["TANDA 0: Probetas de Validación<br>(testigo_placa + testigo_rosca + anillo_placa)<br>~40 min · Cualquier color"]
    T0 --> CHECK{"¿PCB entra en costillas?<br>¿Ranura USB-C centrada?<br>¿Anillo enrosca suave?"}
    
    CHECK -- SÍ (Veredicto APROBADO) --> T1["TANDA 1: Pieza Estructural<br>(cuerpo.stl)<br>~3.5 - 4 h · Blanco"]
    CHECK -- NO (Ajuste) --> SCAD["Ajustar holgura_placa o rosca_juego<br>en lua-muneco.scad"]
    
    T1 --> T2["TANDA 2: Accesorios Turquesa<br>(orejas, collar, mochila, botón, emblema)<br>~1.5 h · Turquesa"]
    T2 --> T3["TANDA 3: Miembros Bicolor<br>(brazos y piernas con pausa a Z fija)<br>~1.5 h · Turquesa a Blanco"]
    T3 --> T4["TANDA 4: Piezas Blancas de Precisión<br>(logo.stl + cartucho.stl)<br>~20 min · Blanco"]
    T4 --> T5["TANDA 5: Elementos de Contraste Oscuros<br>(aro_visor.stl + pulsadores.stl)<br>~15 min · Negro / Grafito"]
    T5 --> T6["TANDA 6: Casco Definitivo<br>(cabeza_frente + cabeza_dorso)<br>~3.5 h · Blanco"]
    T6 --> ENSAMBLE["ENSAMBLE FINAL"]
```

### Detalle Operativo de Cada Tanda:

1. **Tanda 0 · Calibración previa (~40 min · Cualquier filamento)**:
   - Piezas: `testigo_placa.stl`, `testigo_rosca.stl` y `anillo_placa.stl`.
   - **Regla crítica:** `testigo_rosca` debe laminarse obligatoriamente con **balsa (raft)** de 2 capas para asegurar estabilidad.
   - Presentar la placa electrónica en `testigo_placa` y enroscar el anillo en el barril para verificar ajuste suave.
2. **Tanda 1 · Tronco Principal (~3 h 50 min · Blanco PLA)**:
   - Pieza: `cuerpo.stl`.
   - No depende de la placa. Puede imprimirse mientras se revisa la electrónica.
3. **Tanda 2 · Accesorios Turquesa (~1 h 30 min · Turquesa PLA)**:
   - Piezas: `oreja_izq.stl`, `oreja_der.stl`, `collar.stl`, `mochila.stl`, `boton.stl`, `emblema.stl`.
   - Orientación plana en Z = 0 tal como vienen orientadas.
4. **Tanda 3 · Extremidades Bicolor con Cambio en Z (~1 h 30 min)**:
   - Piezas: `brazo_izq.stl`, `brazo_der.stl`, `pierna_izq.stl`, `pierna_der.stl`.
   - **Brazos:** Iniciar en **Turquesa** $\rightarrow$ Pausa (`M600`) o cambio de filamento a **Blanco** a los **16,5 mm** de altura Z.
   - **Piernas:** Iniciar en **Turquesa** $\rightarrow$ Pausa (`M600`) o cambio de filamento a **Blanco** a los **14,0 mm** de altura Z.
5. **Tanda 4 · Piezas Blancas de Detalle (~20 min · Blanco PLA)**:
   - Piezas: `logo.stl` y `cartucho.stl`.
   - Para `logo.stl` se recomienda altura de capa reducida (0,12 mm - 0,16 mm) o activación de *Ironing* (alisado superficial) para máxima nitidez del relieve.
6. **Tanda 5 · Contraste Oscuro (~15 min · Negro / Gris grafito)**:
   - Piezas: `aro_visor.stl` (y opcionalmente `pulsadores.stl` si la placa física coincide con el plano).
7. **Tanda 6 · Casco Definitivo (~3 h 40 min · Blanco PLA)**:
   - Piezas: `cabeza_frente.stl` y `cabeza_dorso.stl`.
   - `cabeza_dorso` requiere **Brim de 5 mm** para garantizar anclaje a la cama.

---

## 4. Parámetros Maestros de Laminación (Cura / PrusaSlicer)

- **Boquilla:** 0,40 mm
- **Altura de capa estándar:** 0,20 mm
- **Perímetros / Paredes:** 3 (1,2 mm) a 4 líneas (1,6 mm)
- **Capas superiores / inferiores:** 4 / 4
- **Relleno:** 12% a 15% Patrón **Giroide** (*Gyroid*)
- **Soportes:** **DESACTIVADOS (0 soportes)** en todo el modelo (la geometría está calculada para volar con voladizos suaves sin marcas).
- **Temperatura:** 205 °C - 215 °C (Nozzle) / 60 °C (Cama PEI).
- **Costura en Z (Z-Seam):** Alinear en la parte trasera (`Back` / Nuca) para preservar la cara frontal totalmente limpia.

---

## 5. Lista de Materiales y Tornillería (BOM)

1. **Filamentos PLA 1,75 mm:**
   - PLA Blanco: ~280 g.
   - PLA Turquesa / Cyan: ~70 g.
   - PLA Negro / Grafito: ~10 g.
2. **Ferretería:**
   - 2× Tornillos métrica M2 × 8 mm (cabeza avellanada o cilíndrica para sujeción de la mochila).
   - 2× Insertos roscados de latón M2 (longitud 3,0 mm - 4,0 mm, instalados con soldador a calor en la espalda).
3. **Adhesivo:**
   - Cianoacrilato de viscosidad media (tipo Loctite / Super Glue) para unión de las dos mitades del casco y accesorios.
   - Cinta de espuma de doble cara para fijar la celda de litio al `cartucho.stl`.

---

## 6. Procedimiento Paso a Paso de Ensamble

1. **Preparación de la Espalda:**
   - Insertar con la punta caliente del soldador los 2 insertos M2 en las cajeras dorsales del `cuerpo.stl`.
2. **Collarín:**
   - Deslizar `collar.stl` en el cuello del `cuerpo.stl` con la muesca apuntando al frente **antes de pegar la cabeza**.
3. **Montaje de la Electrónica:**
   - Introducir la placa con pantalla circular en `cabeza_frente.stl`.
   - Roscar `anillo_placa.stl` en el barril M55 con los dedos hasta que haga tope firme contra la placa.
4. **Cierre de la Cabeza:**
   - Aplicar cianoacrilato en la pestaña de unión de `cabeza_dorso.stl`.
   - Encajar las dos mitades asegurando que las dos espigas de centrado calzan exactamente en sus orificios.
5. **Accesorios:**
   - Pegar `oreja_izq.stl` y `oreja_der.stl` en los huecos superiores.
   - Pegar `boton.stl` en la sien derecha.
   - Pegar `aro_visor.stl` alrededor de la pantalla.
   - Insertar y pegar `logo.stl` dentro del `emblema.stl`, y luego pegar el conjunto centrado en el pecho.
6. **Batería y Miembros:**
   - Fijar la celda en `cartucho.stl`, pasar los cables MX1.25 y cerrar la mochila con los 2 tornillos M2.
   - Encolar las espigas de brazos y piernas en sus cajeras del tronco.
