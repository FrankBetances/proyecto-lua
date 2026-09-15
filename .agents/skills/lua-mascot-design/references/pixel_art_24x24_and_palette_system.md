# Sistema de Pixel Art 24×24 y Paleta Estricta de 21 Colores para Lúa

Este documento establece las especificaciones técnicas y artísticas para la creación de sprites, iconos de recompensas, estados emocionales y minijuegos en la pantalla circular de Lúa (panel IPS GC9A01 de 240×240 píxeles).

---

## 🔲 1. Cuadrícula Canónica de 24×24 Píxeles

### Geometría y Escalado
- **Resolución Lógica Base**: $24 \times 24$ píxeles.
- **Factor de Escala Entero**: $8\times$ o $9\times$ sobre el panel físico de 240×240.
  - A escala $8\times$, un sprite de $24\times24$ ocupa $192\times192$ píxeles físicos, dejando un margen perimetral seguro de 24 px en cada eje, perfecto para no ser recortado por el bisel circular del panel.
  - A escala $9\times$, ocupa $216\times216$ píxeles físicos con margen perimetral de 12 px.
- **Mapeo en Memoria**:
  Cada sprite de 24×24 se representa como un array de cadenas de 24 caracteres (`const char* const sprite[24]`), donde cada carácter mapea a un índice de color de la paleta.

---

## 🎨 2. Paleta Canónica Estricta de 21 Colores

La paleta se organiza en familias tonales jerárquicas con triple nivel de valor (Luz / Base / Sombra) para lograr volumen y contraste sobre fondo negro (#0A0C10) o fondo claro de ficha (#F4F6F8).

| Índice | Código Hex | RGB565 | Carácter Clave | Nombre / Uso Semántico |
| :---: | :---: | :---: | :---: | :--- |
| **00** | `#000000` | `0x0000` | `.` | Transparente / Fondo nulo |
| **01** | `#0B0E14` | `0x0862` | `K` | Fondo Profundo / Sombra extrema |
| **02** | `#1C2230` | `0x1926` | `o` | Contorno Gata / Sombra pelaje |
| **03** | `#2D3748` | `0x29E9` | `b` | Pelaje Base (Tuxedo Negro Suave) |
| **04** | `#4A5568` | `0x4AAD` | `B` | Brillo Pelaje / Reflejo sutil |
| **05** | `#CBD5E1` | `0xCE79` | `s` | Blanco Sombra (Pechera/Hocico) |
| **06** | `#FFFFFF` | `0xFFFF` | `w` | Blanco Puro (Brillo ojos, pechera) |
| **07** | `#991B1B` | `0x98C3` | `r` | Rojo Sombra (Boca, corazón) |
| **08** | `#EF4444` | `0xEE88` | `R` | Rojo Vivo (Amor, alerta suave) |
| **09** | `#FCA5A5` | `0xFD54` | `p` | Rosa Oreja / Rubor Suave (`c`) |
| **10** | `#92400E` | `0x9201` | `d` | Dorado Sombra / Bronce Insignia |
| **11** | `#F59E0B` | `0xF4E1` | `Y` | Amarillo Oro (Ojos Lúa, Estrellas) |
| **12** | `#FEF08A` | `0xFF31` | `y` | Amarillo Brillo (Destellos, chispas) |
| **13** | `#065F46` | `0x0308` | `g` | Verde Sombra / Éxito fondo |
| **14** | `#10B981` | `0x15D0` | `G` | Verde Esmeralda (Acierto, Esperanza) |
| **15** | `#A7F3D0` | `0xAF7A` | `e` | Verde Menta Brillo (Partículas acierto) |
| **16** | `#1E40AF` | `0x1A15` | `u` | Azul Ojo / Modo Vínculo Sombra |
| **17** | `#3B82F6` | `0x3C1E` | `U` | Azul Eléctrico (Conectado, Tranquilidad) |
| **18** | `#93C5FD` | `0x963F` | `a` | Azul Cielo Brillo (Aura mágica) |
| **19** | `#6B21A8` | `0x6915` | `m` | Violeta Sombra (Orgullo, Misterio) |
| **20** | `#A855F7` | `0xAA3E` | `M` | Púrpura Vibrante (Epifanía, Magia) |

---

## 🖌️ 3. Reglas de Volumetría y Shading en 24×24

1. **Jerarquía 3-Tono**:
   - Cada masa visual (ej. cara de Lúa, estrella de recompensa, corazón) debe estructurarse con:
     - $60\%$ Color Base (`Midtone`)
     - $25\%$ Sombra Propia (`Shadow`) orientada abajo/derecha
     - $15\%$ Brillo Especular (`Highlight`) orientado arriba/izquierda
2. **Cero Ruido (Clustering Obligatorio)**:
   - No colocar píxeles aislados tipo ajedrez (*checkerboard dithering*).
   - Agrupar píxeles de brillo o sombra en islas continuas de al menos $2 \times 1$ o $2 \times 2$ px para garantizar lectura a distancia en el dispositivo.
3. **Contornos Inteligentes (*Selective Outlining*)**:
   - En fondos oscuros (#0B0E14), el contorno `o` (`#1C2230`) separa el cuerpo negro de la gata del fondo sin quemar la silueta.
   - En insignias brillantes, no utilizar contorno negro puro; emplear la sombra propia del tono (ej. dorado sombra `#92400E` para delimitar el oro `#F59E0B`).

---

## 🧪 4. Plantilla de Representación de Sprite (24×24)

```c
// Ejemplo: Insignia "Estrella de Articulación" (AWARD_STAR) en 24x24
const char* const kSpriteAwardStar[24] = {
  "........................",
  "...........yy...........",
  "...........YY...........",
  "..........yYYy..........",
  "..........YYYY..........",
  ".........yYYYYy.........",
  ".........YYYYYY.........",
  "..yyyyyyyYYYYYYyyyyyyy..",
  "...YYYYYYYYYYYYYYYYYY...",
  "....dYYYYYYYYYYYYYYd....",
  "......dYYYYYYYYYYd......",
  ".......dYYYYYYYYd.......",
  "......yYYYYYYYYYYy......",
  ".....yYYYYd..dYYYYy.....",
  "....yYYYd......dYYYy....",
  "...yYYd..........dYYy...",
  "..yYd..............dYy..",
  "..dd................dd..",
  "........................",
  "........................",
  "........................",
  "........................",
  "........................",
  "........................",
};
```

---

## 🔍 5. Verificación de Contraste y Calibración en Pantalla Circular

1. **Máscara Circular**: Todo elemento clave debe quedar inscrito dentro del radio $R \le 108\text{ px}$ desde el centro $(120, 120)$.
2. **Prueba de Iluminación**: Los colores amarillos y verdes deben mantener legibilidad con la retroiluminación IPS al 40% y al 100%.
