# Gamificación Clínica, Sistemas de Recompensas y Reglas del Tablero

Este documento detalla el diseño de mecánicas lúdicas, sistemas de recompensas iconográficas y el respeto estricto a las restricciones clínicas en el ecosistema de Lúa.

---

## 🎯 1. Principio de Transformación Terapéutica

La terapia del lenguaje y la rehabilitación auditivo-verbal (TAV) requieren repeticiones sistemáticas de pares mínimos, fonemas y discriminación de sonidos. La gamificación transforma estas tareas clínicas en retos lúdicos gratificantes mediante:

1. **Narrativa Cooperativa (Compañera de Aventura)**:
   - Lúa no es un juez que evalúa al niño: es una gata exploradora que necesita que el niño le enseñe "palabras mágicas" o "claves sonoras" para abrir cofres, encender constelaciones o explorar islas.
2. **Ciclo de Feedback Inmediato y No Punitivo**:
   - Cada intento genera una respuesta instantánea y comprensible sin necesidad de leer texto.
   - El refuerzo positivo es variable y progresivo: pequeños aciertos dan destellos suaves; hitos acumulados desbloquean insignias con animaciones especiales.

---

## 🚫 2. Reglas del Tablero (Clinical Constraints)

### A. Regla de Cero Texto
- **Constraint**: Queda terminantemente prohibido mostrar palabras ("BIEN", "NIVEL 1", "PUNTOS: 100", "REPETIR").
- **Solución Visual**:
  - Estado de ánimo → Expresión facial directa de Lúa.
  - Progreso de nivel → 12 segmentos luminosos en el anillo circular perimetral (`LEVEL 1-12`).
  - Tipo de ejercicio → Pictograma central de $24 \times 24$ px con silueta universal.
  - Recompensa → Insignia glífica animada con destellos dorados.

### B. Regla de Silencio Clínico y Timing Estricto
- **Constraint**: La atención auditiva del paciente pediátrico con hipoacusia o implante coclear es sumamente frágil. La sobrecarga visual en el momento de la audición destruye la discriminación fonológica.
- **Protocolo de Timing**:
  1. **Emisión de Estímulo Sonoro (0.0s – 1.5s)**: Pantalla en calma absoluta (`kExprAttentive`), Lúa mirando de frente, respiración sutil de 1 px. Cero partículas, cero destellos en el anillo.
  2. **Ventana de Respuesta del Paciente (1.5s – 4.0s)**: Lúa pasa a `kExprEncouraging` (ojos abiertos y orejas alertas).
  3. **Refuerzo / Celebración (4.0s – 5.5s)**:
     - Si es acierto breve: Animación de 1.2s (`kExprYes`), 3 destellos verdes en el anillo y retorno inmediato a `kExprAttentive`.
     - Si es subida de nivel / insignia: Animación de 2.5s (`kExprEpiphany` / `kExprSuccess`) con rotación suave del anillo de 12 segmentos.

---

## 🏆 3. Sistema de Recompensas: Insignias Glíficas y Anillo de 12 Niveles

### A. Anillo Perimetral de 12 Segmentos (`LEVEL 1-12`)
El borde de la pantalla circular de 240×240 px se divide en 12 arcos de 30° cada uno:
- Cada segmento encendido representa una sesión o bloque superado.
- Al completar los 12 segmentos, el anillo gira en un ciclo de arcoíris y se desbloquea una insignia de rango superior.

### B. Matriz de Insignias Glíficas (24×24 px)

| Categoría | Glifo Base (24×24) | Rango Bronce (Nivel 1) | Rango Plata (Nivel 2) | Rango Oro (Nivel 3) |
| :--- | :--- | :--- | :--- | :--- |
| **Fonación** | Campana mágica | Campana con borde cobre | Campana plateada con onda | Campana dorada con destellos |
| **Discriminación** | Oído estelar | Orejita de gato bronce | Orejita con destello azul | Orejita dorada con constelación |
| **Constancia** | Sol sonriente | Sol ámbar | Sol amarillo brillante | Sol radiante con corona |
| **Exploración** | Huella cósmica | Huella de gato marrón | Huella azul eléctrico | Huella dorada con partículas |

---

## 🎲 4. Mecánicas de Juego de Mesa y Entornos Espaciales

1. **Tablero Circular de Aventura**:
   - La pantalla de Lúa actúa como una brújula o mapa estelar donde cada punto cardinal representa un mundo o bloque fonético.
2. **Mecánica de Co-regulación y Calma**:
   - Antes de iniciar un bloque complejo, Lúa activa la mecánica del "Farol Tranquilo": el anillo se ilumina en azul suave mientras Lúa inhala durante 4 segundos y exhala en 4 segundos, invitando al niño a sincronizar su respiración antes de hablar.
