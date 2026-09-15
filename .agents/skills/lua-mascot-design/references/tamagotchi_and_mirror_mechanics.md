# Mecánicas de Doble Modo: Espejo de App vs. Mascota Independiente (Tamagotchi Pediátrico)

Este documento define la arquitectura de comportamiento, interacción y regulación emocional de Lúa operando en sus dos modos funcionales: sincronizada con la app de terapia (**Modo Espejo**) y autónoma (**Modo Mascota Tamagotchi**).

---

## 🔄 1. Arquitectura de Doble Modo

```
                      ┌────────────────────────────────────────┐
                      │            DISPOSITIVO LÚA             │
                      └──────────────────┬─────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
    ┌──────────────────────────┐                   ┌──────────────────────────┐
    │       MODO ESPEJO        │                   │    MODO INDEPENDIENTE    │
    │  (Sincronizado vía BLE)  │                   │       (Tamagotchi)       │
    ├──────────────────────────┤                   ├──────────────────────────┤
    │ • Recibe opcodes de app  │                   │ • Autónomo sin BLE       │
    │ • Refuerzo de ejercicios │                   │ • Respuestas a caricias  │
    │ • Pictogramas / Niveles  │                   │ • Estados afectivos 0-7  │
    │ • Sigue el ritmo clínico │                   │ • Cero relojes de hambre │
    └──────────────────────────┘                   └──────────────────────────┘
```

---

## 🪞 2. Modo Espejo (App Mirror)

En este modo, Lúa actúa como el reflejo físico y periférico de la sesión clínica en Valeria+ o VIA+. El paciente dirige su atención al muñeco/pantalla física, reduciendo la fijación en la pantalla de la tableta.

### Comportamientos y Sincronización:
1. **Fase de Escucha (`PHASE 0`)**: Lúa mira al frente con atención serena (`kExprAttentive`). Cero movimiento brusco mientras el niño escucha el audio modelo.
2. **Fase de Repetición (`PHASE 1`)**: Lúa abre los ojos con entusiasmo sutil (`kExprEncouraging`), invitando al niño a hablar.
3. **Veredicto Articulado**:
   - `VERDICT 1` (**Impulso / Casi**): Mirada cálida de aliento. No hay penalización.
   - `VERDICT 2` (**Acierto / Calma**): Parpadeo alegre, rubor y destello verde esmeralda.
   - `VERDICT 0` (**Desvío**): Retorno silencioso y neutro a `kExprAttentive`. **Lúa no castiga ni muestra tristeza**.
4. **Despliegue de Ficha (`PICTO`) e Insignia (`AWARD`)**: La pantalla sustituye temporalmente la cara de la gata por la ficha iconográfica de 24×24 escalada con su marco circular.

---

## 🐱 3. Modo Independiente (Tamagotchi Pediátrico Seguro)

Lúa funciona fuera de las sesiones de terapia como una mascota digital viva, cálida y de compañía, diseñada bajo principios de **no adicción** y **cero ansiedad pediátrica**.

### Principios Fundamentales:
1. **Sin Relojes de Hambre ni Decaimiento Autónomo**:
   - Lúa **NO** se "muere", no se "enferma" ni se pone "hambrienta" si el niño no la usa durante días.
   - La experiencia es 100% positiva: el estado de Lúa refleja bienestar continuo y reposo pacífico.
2. **Interacciones Táctiles Deliberadas**:
   - **Caricia en la cabeza (Touch Sensor 1)**: Lúa cierra los ojos lentamente con forma de medialuna, emite un rubor rosa suave y entra en estado `kExprLove` o `kExprGratitude`.
   - **Toque en las orejas (Touch Sensors 2/3)**: Guiño travieso y micro-animación de orejas atentas (`kExprAmusement`).
   - **Abrazo / Toque prolongado en el pecho (Touch Sensor 4)**: Respiración rítmica y pulsación de luz suave en el anillo (`kExprTranquility`), ideal para co-regulación emocional antes de dormir.

---

## 💖 4. Catálogo de los 8 Estados Afectivos Puros (`AFFECT 0-7`)

Estos estados pueden ser activados manualmente por la familia/terapeuta desde la app o disparados por secuencias lúdicas autónomas:

| Código | Estado | Animación Facial | Patrón de Anillo / Partículas | Intención Clínica / Emocional |
| :---: | :--- | :--- | :--- | :--- |
| `0` | **Alegría** | Ojos chispeantes, boca abierta sonriente | Destellos dorados giratorios | Celebrar momentos cotidianos |
| `1` | **Amor** | Ojos de arco cerrado, rubor intenso | Pulso suave magenta/rosa | Fomentar el apego seguro |
| `2` | **Gratitud** | Inclinación de cabeza, ojos semicerrados | Halo verde menta calmante | Cierre de momentos compartidos |
| `3` | **Tranquilidad** | Respiración pautada 4s inhalar / 4s exhalar | Onda azul cielo expansiva lenta | Regulación de ansiedad / Calma |
| `4` | **Esperanza** | Mirada orientada al cielo, pupilas dilatadas | Destellos ascendentes cian | Motivación antes de una sesión |
| `5` | **Orgullo** | Pecho erguido, sonrisa de satisfacción | Corona púrpura fija | Reconocimiento del esfuerzo |
| `6` | **Inspiración** | Ojos grandes con brillo estelar blanco | Chispas doradas aleatorias | Estímulo de creatividad y juego |
| `7` | **Diversión** | Guiño asimétrico, leve balanceo | Rebote dinámico multicolor | Dinamismo y risa espontánea |

---

## 🌙 5. Transición a Reposo y Seguridad

- **Inactividad (> 60 segundos sin interacción)**: Lúa bosteza sutilmente, sus ojos se cierran despacio y pasa a `kExprAsleep` (respiración suave a 12 respiraciones por minuto con brillo tenue del panel al 10%).
- **Cero Alarmas Nocturnas**: La mascota permanece en reposo absoluto sin emitir luces fuertes ni sonidos en ausencia de toque deliberado.
