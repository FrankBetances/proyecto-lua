# Archivos STL Oficiales · Muñeco Lúa (Ender-3 S1 Pro)

> **Iteración:** V15 / Fase 3 USC (Actualizado al 23/09/2026)  
> **Total de piezas:** 21 archivos STL (19 componentes del muñeco + 2 probetas de verificación previa).  
> **Novedad x1:** sin pegamento estructural, sin tornillos M2 ni insertos. Todo encaja a presión (0,15 mm) o con bayoneta de 1/4 de vuelta.
> **Documentación técnica completa y plan de impresión:** Ver [`../INSTRUCCIONES_IMPRESION_Y_PLAN_LUA.md`](../INSTRUCCIONES_IMPRESION_Y_PLAN_LUA.md) y [`../lua-firmware/docs/cad/impresion-ender3-s1-pro.md`](../lua-firmware/docs/cad/impresion-ender3-s1-pro.md).

---

## 📋 Catálogo de Piezas, Colores y Dimensiones Exactas

| Archivo STL | Cant. | Color sugerido | Huella X × Y × Z (mm) | Volumen | Observaciones técnicas y montaje |
| :--- | :---: | :--- | :---: | :---: | :--- |
| **`testigo_placa.stl`** | 1 | Cualquier color | 63.2 × 59.7 × 2.4 | 2.2 cm³ | **Probeta 1 (Imprimir primero):** Comprueba ajuste de carcasa Ø50 y ranura USB-C. |
| **`testigo_rosca.stl`** | 1 | Cualquier color | 58.8 × 58.8 × 12.0 | 5.1 cm³ | **Probeta 2 (Imprimir con balsa/raft):** Comprueba rosca M55 con `anillo_placa`. |
| **`anillo_placa.stl`** | 1 | Blanco / Libre | 55.0 × 55.0 × 9.0 | 1.7 cm³ | **Retención de PCB:** Asiento cónico a 45° (recoge 5 a 18 mm). Con soportes de árbol. |
| **`cabeza_frente.stl`** | 1 | Blanco | 75.7 × 75.3 × 24.9 | 24.3 cm³ | Visor circular, labio Ø50 y rosca M55. Espolón con 3 llaves rectas asimétricas. |
| **`cabeza_dorso.stl`** | 1 | Blanco | 78.0 × 76.3 × 48.1 | 30.7 cm³ | Cúpula con respiraderos, manga 3 canales y banda de refuerzo. Brim 5 mm. |
| **`cuerpo.stl`** | 1 | Blanco | 75.4 × 65.5 × 80.0 | 162.3 cm³ | Tronco principal. Aloja batería, cuello, cajetas miembros Lego y cajeta pecho. |
| **`brazo_izq.stl`** | 1 | Blanco + Turquesa | 20.0 × 18.2 × 42.1 | 6.0 cm³ | Espiga macho Ø8 mm Lego. Recorte curvo que abraza la barriga sin colisiones. |
| **`brazo_der.stl`** | 1 | Blanco + Turquesa | 20.0 × 18.2 × 42.1 | 6.0 cm³ | Espiga macho Ø8 mm Lego. Recorte curvo que abraza la barriga sin colisiones. |
| **`pierna_izq.stl`** | 1 | Blanco + Turquesa | 28.3 × 23.7 × 40.9 | 11.9 cm³ | Espiga macho Ø9 mm Lego con nervios de aplastamiento. |
| **`pierna_der.stl`** | 1 | Blanco + Turquesa | 28.3 × 23.7 × 40.9 | 11.9 cm³ | Espiga macho Ø9 mm Lego con nervios de aplastamiento. |
| **`oreja_izq.stl`** | 1 | Turquesa | 30.0 × 26.7 × 8.2 | 2.6 cm³ | Espiga en D Ø8 anti-rotación (impresa tumbada). Sin pegamento. |
| **`oreja_der.stl`** | 1 | Turquesa | 30.0 × 26.7 × 8.2 | 2.6 cm³ | Espiga en D Ø8 anti-rotación (impresa tumbada). Sin pegamento. |
| **`collar.stl`** | 1 | Turquesa | 34.4 × 36.6 × 8.5 | 4.0 cm³ | Deslizar al cuello antes de montar la cabeza. Muesca al frente. |
| **`mochila.stl`** | 1 | Turquesa | 48.0 × 36.0 × 10.4 | 14.6 cm³ | Tapa trasera a presión sobre 2 pernos sueltos (sin tornillos; abre tirando). |
| **`pernos_mochila.stl`** | 1 | Blanco / Libre | 20.6 × 4.0 × 4.0 | 0.2 cm³ | Los 2 pernos Ø4 en una pieza con lengüeta rompible. |
| **`boton.stl`** | 1 | Turquesa | 15.0 × 15.0 × 3.4 | 0.5 cm³ | Detalle estético dial pegado en la sien derecha. |
| **`emblema.stl`** | 1 | Turquesa | 22.6 × 22.0 × 5.2 | 1.7 cm³ | Tetón macho stud tipo Lego con nervios. Entra a presión en el pecho. |
| **`logo.stl`** | 1 | Blanco | 14.9 × 14.9 × 1.6 | 0.3 cm³ | Silueta icónica de Lúa. Se encaja y pega dentro del emblema. |
| **`pulsadores.stl`** | 1 | Oscuro / Negro | 28.3 × 10.8 × 9.8 | 0.6 cm³ | Guía de botones bajo barbilla (con soportes de árbol). |
| **`cartucho.stl`** | 1 | Blanco / Libre | 33.2 × 9.2 × 23.2 | 2.5 cm³ | Cuna interior para sujetar la celda de litio con cinta doble cara. |
| **`aro_visor.stl`** | 1 | Oscuro (Gris/Negro)| 44.0 × 44.0 × 1.6 | 0.9 cm³ | Marco circular del visor. Oculta la junta del cristal de la pantalla. |

---

## ⚙️ Parámetros Clave de Laminación (Creality Ender-3 S1 Pro)

- **Boquilla (Nozzle):** 0,40 mm
- **Altura de capa:** 0,20 mm (0,12 mm - 0,16 mm opcional para `logo.stl`, `emblema.stl` y `boton.stl` para mayor definición)
- **Perímetros (Paredes):** 3 a 4 líneas (1,2 a 1,6 mm)
- **Capas superior / inferior:** 4 a 5 capas sólidas
- **Relleno:** 12% - 15% Giroide (*Gyroid*)
- **Soportes:** en árbol solo donde el gate los pide: `oreja_izq`/`oreja_der` (31,8 %), `pulsadores` (30,3 %) y `anillo_placa` (17,9 %). El resto sale sin soportes.
- **Adherencia a cama:** 
  - *Brim* de 5 mm en `cabeza_dorso.stl` y piezas pequeñas.
  - *Balsa (Raft)* obligatoria en `testigo_rosca.stl` (pared fina de tubo vertical).
- **Alisado (Ironing):** Recomendado en capas superiores planas (`emblema.stl`, `logo.stl`, `aro_visor.stl`).
