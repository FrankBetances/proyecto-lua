# 05 · Perfiles de Laminación Optimizados para Creality Ender-3 S1 Pro

## 1. Especificaciones Críticas de la Ender-3 S1 Pro

La **Creality Ender-3 S1 Pro** cuenta con ventajas clave que deben aprovecharse al máximo para el acabado de figuras y juguetes infantiles:
- **Extrusor Directo Sprite Dual-Gear**: Tracción directa de alta precisión. Permite retracciones muy cortas ($0.8\text{ mm}$ a $40\text{ mm/s}$), eliminando prácticamente los hilos (*stringing*).
- **Cama Magnética de Acero Flexible PEI**: Excelente adherencia en caliente ($60^\circ\text{C}$) y desprendimiento espontáneo al enfriarse ($<35^\circ\text{C}$).
- **Nivelación Automática CR-Touch**: Asegura una primera capa perfecta en toda el área de $220 \times 220\text{ mm}$.
- **Boquilla de Serie**: Latón / Bimetal de Ø0.40 mm.

---

## 2. Perfiles Recomendados de Altura de Capa para Juguetes Estilizados

| Parámetro | Perfil A: "Detalle Máximo Chibi" (Caras, Orejas, Ojos) | Perfil B: "Cuerpo y Estructura" (Tronco, Mochila, Extremidades) |
| :--- | :--- | :--- |
| **Altura de Capa** | **0.12 mm** | **0.16 mm** |
| **Altura de Primera Capa** | 0.20 mm | 0.20 mm |
| **Líneas de Pared (Perímetros)** | **4 perímetros** (1.60 mm de pared sólida) | **4 perímetros** (1.60 mm de pared sólida) |
| **Capas Superiores / Inferiores** | 6 superiores / 5 inferiores | 5 superiores / 4 inferiores |
| **Patrón de Relleno** | Giroide al 15% | Giroide al 15% - 20% |
| **Velocidad de Impresión Pared Ext.** | 25 mm/s (para máxima suavidad) | 35 mm/s |
| **Velocidad de Relleno** | 50 mm/s | 60 mm/s |
| **Retracción (Extrusor Sprite)** | 0.8 mm a 40 mm/s | 0.8 mm a 40 mm/s |
| **Temperatura Hotend (PLA)** | 200°C - 205°C | 205°C - 210°C |
| **Temperatura Cama** | 60°C | 60°C |
| **Ventilador de Capa** | 100% desde capa 3 | 100% desde capa 3 |

---

## 3. Configuración Magistral de Soportes en Árbol (Tree / Organic Supports)

Los soportes convencionales en celosía o rejilla destruyen la estética de un personaje infantil. Se deben configurar **exclusivamente soportes en árbol (Organic Supports)** con la siguiente calibración:

```
               [ Barbilla del Muñeco ]
                        │
                  ═════════════ ◄── Interfaz densa (3 capas al 100%)
                     ↕ 0.20 mm  ◄── DISTANCIA Z CRÍTICA (Se despega como celofán)
                   /     \
                  ( Rama  )     ◄── Tronco tubular hueco
                 (  Árbol  )
                /           \
           ═══════════════════════ ◄── Cama PEI
```

### Parámetros de Soportes en Árbol (Cura / PrusaSlicer / OrcaSlicer):
- **Estructura de soporte**: En árbol (*Tree* / *Organic*).
- **Ángulo de voladizo límite**: **55°** (la Ender-3 S1 Pro resuelve con ventilación al 100% voladizos de hasta 50° sin soporte alguno).
- **Distancia de contacto Z superior (Top Z-Distance)**: **0.20 mm** (exactamente un salto de capa). Si se configura menor a 0.15mm, el soporte se fusiona con la pieza; si se configura mayor a 0.25mm, el filamento del voladizo cuelga descolgado.
- **Capas de interfaz superior**: 3 capas con patrón concéntrico o líneas al 100%. Esta capa crea una "mesa de apoyo lisa" que impide que la rama de soporte marque la pieza.
- **Diámetro de rama del árbol**: 2.5 mm (con ángulo de apertura de 40°). Ahorra hasta un 70% de material respecto a soportes normales.

---

## 4. Ocultamiento de la Costura en Z (Z-Seam Alignment)

La costura en Z es el punto donde la boquilla inicia y finaliza el perímetro de cada capa. Si se deja en modo aleatorio o automático, aparecen pequeños granitos o marcas visibles en la cara o mejillas del personaje.

- **Alineación de la costura**: Seleccionar **"Definida por el usuario" / "Atrás" (Back)** o pintar manualmente la costura con el pincel del laminador en la nuca o detrás de las orejas.
- **Retracción al cambiar de capa**: Activada.
- **Limpieza de boquilla (Wipe on retract)**: 0.4 mm.
- **Rueda libre (Coasting)**: Opcional (0.06 mm³), útil para evitar sobrepresión en la boquilla justo antes de cerrar la costura.

---

## 5. Acabado Superficial Superior: Alisado (Ironing)

Para piezas planas o de detalle como el escudo del pecho, insignias o la cara superior de la base de exposición:
- **Activar Alisado (Ironing)** en la última capa:
  - Flujo de alisado: 10% - 12%.
  - Velocidad de alisado: 15 mm/s.
  - Espaciado entre pasadas: 0.1 mm.
  - *Resultado*: La boquilla caliente plancha las líneas de extrusión, dejando un acabado espejo completamente liso semejante a una pieza de inyección plástica.
