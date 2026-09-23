# Archivos STL Oficiales · Muñeco Lúa (Ender-3 S1 Pro)

> **Iteración:** V15 / Fase 3 USC (Actualizado al 23/09/2026)  
> **Total de piezas:** 21 archivos STL (19 componentes del muñeco + 2 probetas de verificación previa).  
> **Novedad x1:** sin pegamento estructural, sin tornillos M2 ni insertos. Todo encaja a presión (0,15 mm) o con bayoneta de 1/4 de vuelta.
> **Documentación técnica completa y plan de impresión:** Ver [`../INSTRUCCIONES_IMPRESION_Y_PLAN_LUA.md`](../INSTRUCCIONES_IMPRESION_Y_PLAN_LUA.md) y [`../lua-firmware/docs/cad/impresion-ender3-s1-pro.md`](../lua-firmware/docs/cad/impresion-ender3-s1-pro.md).

---

## 📋 Catálogo de Piezas, Colores y Dimensiones Exactas

| Archivo STL | Cant. | Color sugerido | Huella X × Y × Z (mm) | Volumen | Observaciones técnicas y montaje |
| :--- | :---: | :--- | :---: | :---: | :--- |
| **`testigo_placa.stl`** | 1 | Cualquier color | 49.5 × 51.0 × 8.0 | 3.0 cm³ | **Probeta 1 (Imprimir primero):** Comprueba ajuste perimetral de PCB y ranura USB-C. |
| **`testigo_rosca.stl`** | 1 | Cualquier color | 61.0 × 61.0 × 12.0 | 5.3 cm³ | **Probeta 2 (Imprimir con balsa/raft):** Comprueba rosca M55 con `anillo_placa`. |
| **`anillo_placa.stl`** | 1 | Blanco / Libre | 64.3 × 64.3 × 11.0 | 8.3 cm³ | **Retención de PCB:** Se enrosca tras la placa (recorrido para PCB de 8 a 16 mm). Con soportes de árbol. |
| **`cabeza_frente.stl`** | 1 | Blanco | 84.4 × 84.5 × 25.9 | 27.6 cm³ | Visor circular y rosca M55. Con espolón de bayoneta (3 nervios). |
| **`cabeza_dorso.stl`** | 1 | Blanco | 87.0 × 85.5 × 53.8 | 34.9 cm³ | Cúpula con respiraderos y manga de bayoneta. Usar brim 5 mm. |
| **`cuerpo.stl`** | 1 | Blanco | 75.4 × 65.5 × 80.0 | 164.3 cm³ | Tronco principal. Aloja celda de litio, cuello y asiento centrado para emblema. |
| **`brazo_izq.stl`** | 1 | Blanco + Turquesa | 20.0 × 19.0 × 39.4 | 7.1 cm³ | Impresión vertical. Turquesa de 0 a 16,5 mm; Blanco desde 16,5 mm. |
| **`brazo_der.stl`** | 1 | Blanco + Turquesa | 20.0 × 19.0 × 39.4 | 7.1 cm³ | Impresión vertical. Turquesa de 0 a 16,5 mm; Blanco desde 16,5 mm. |
| **`pierna_izq.stl`** | 1 | Blanco + Turquesa | 28.3 × 23.7 × 34.5 | 11.4 cm³ | Impresión vertical. Turquesa de 0 a 14,0 mm; Blanco desde 14,0 mm. |
| **`pierna_der.stl`** | 1 | Blanco + Turquesa | 28.3 × 23.7 × 34.5 | 11.4 cm³ | Impresión vertical. Turquesa de 0 a 14,0 mm; Blanco desde 14,0 mm. |
| **`oreja_izq.stl`** | 1 | Turquesa | 30.0 × 27.3 × 12.0 | 2.7 cm³ | Bayoneta de 1/4 de vuelta (con balsa bajo el vástago). |
| **`oreja_der.stl`** | 1 | Turquesa | 30.0 × 27.3 × 12.0 | 2.7 cm³ | Bayoneta de 1/4 de vuelta (con balsa bajo el vástago). |
| **`collar.stl`** | 1 | Turquesa | 34.4 × 36.6 × 8.4 | 3.0 cm³ | Colocar en el cuello antes de montar la cabeza. Muesca orientada al frente. |
| **`mochila.stl`** | 1 | Turquesa | 48.0 × 36.0 × 10.4 | 14.6 cm³ | Tapa trasera sobre 2 pernos sueltos (sin tornillos; abre tirando). |
| **`pernos_mochila.stl`** | 1 | Blanco / Libre | 20.6 × 4.0 × 4.0 | 0.2 cm³ | Los 2 pernos Ø4 en una pieza con lengüeta rompible. |
| **`boton.stl`** | 1 | Turquesa | 15.0 × 15.0 × 3.4 | 0.5 cm³ | Detalle estético pegado en la sien derecha. |
| **`emblema.stl`** | 1 | Turquesa | 22.0 × 22.0 × 2.4 | 0.6 cm³ | Insignia centrada en el pecho (`x = 0`). Entra a presión; aloja la pastilla del logo. |
| **`logo.stl`** | 1 | Blanco | 14.9 × 14.9 × 1.6 | 0.3 cm³ | **[NUEVO]** Silueta icónica de Lúa. Se encaja y pega dentro del emblema. |
| **`pulsadores.stl`** | 1 | Oscuro / Negro | 28.3 × 14.3 × 18.6 | 0.9 cm³ | Guía de botones bajo barbilla (con soportes de árbol). |
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
