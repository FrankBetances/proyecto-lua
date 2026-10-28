# 🐈‍⬛ Lúa · mascota STEAM de bloques

### Cabeza versión 4 con placa V1 circular · cuerpo de bloques que monta el niño · sets de Construye con Lúa · Realidad Aumentada local · bloque háptico Ronroneo

![C++17](https://img.shields.io/badge/C%2B%2B-17-00599C?style=flat-square&logo=cplusplus&logoColor=white)
![V1 oficial](https://img.shields.io/badge/placa%20oficial-V1%20·%20ESP32--C3%20·%20GC9A01%20redondo-0a7d54?style=flat-square&logo=espressif&logoColor=white)
![STEAM](https://img.shields.io/badge/eje%20vertebrador-STEAM-00c4be?style=flat-square)
![Versión de prueba](https://img.shields.io/badge/versión%20de%20prueba-V5%20bloques%20(en%20diseño)-f0a500?style=flat-square)
![Versión robot descartada](https://img.shields.io/badge/versión%20robot-descartada%20(oct%202026)-8a8a8a?style=flat-square)
![Sin altavoz](https://img.shields.io/badge/altavoz-no%20existe-b3261e?style=flat-square)
![Sin micrófono](https://img.shields.io/badge/micrófono-no%20existe-b3261e?style=flat-square)
![Zero PHI](https://img.shields.io/badge/Zero--PHI-estructural-0a7d54?style=flat-square)

---

**Lúa** es la gata negra en píxel art de [Valeria+](https://github.com/FrankBetances/Valeria) y de **Descubre con Lúa**, y también un juguete físico que el niño **construye con sus manos**.

Desde octubre de 2026 el proyecto se ordena alrededor de una sola idea: **Lúa es un juguete STEAM de bloques**. La cabeza es la única pieza electrónica de la mascota; el resto del cuerpo, los escenarios y los seis mundos de Construye con Lúa se montan con bloques. Valeria+ (familias y sesión) y Descubre con Lúa (escuela 0–6) son las dos puertas de entrada al mismo sistema de bloques.

> **La app decide. Lúa reacciona. Los bloques los mueve el niño. El adulto media siempre.**

## Qué es y qué no es

Lúa **muestra** expresiones, pictogramas, insignias y niveles en una pantalla circular de 240×240 px. **No** mide, **no** puntúa, **no** guarda, **no** escucha, **no** habla y **no** se mueve. No tiene altavoz ni micrófono en ninguna versión: el Silencio Clínico es una garantía física, no una configuración.

Lúa es un periférico de interacción. No es una fuente de datos clínicos ni un sistema de decisión. Valeria+ es una aplicación educativa y Descubre con Lúa es un recurso escolar; ninguno de los dos diagnostica ni trata.

## Decisiones de diseño vigentes (octubre 2026)

| Decisión | Estado |
|---|---|
| Versión robótica motorizada | **Descartada** definitivamente |
| Otras placas | **Descartadas**. Solo placa V1 circular |
| Cabeza del muñeco versión 4 (PLA, masque3d, Orense) | **Se conserva** |
| Cuerpo del muñeco versión 4 | **Se sustituye** por un cuerpo de bloques armable por el niño |
| Vibración como canal de interacción | **Propuesta**: solo en un bloque externo independiente (Ronroneo), nunca en la cabeza. Pendiente de aprobación en la puerta clínica |
| Luces como canal de interacción | **Adoptado como propuesta V5**: anillo de cuatro luces direccionales en el bloque-cuello sellado, una por lado. Nunca en los bloques del cuerpo |
| Impresión e integración electrónica de la V5 | **masque3d (Orense)** imprime la nueva versión e incorpora la electrónica. El niño y el equipo no hacen ninguna intervención de hardware |
| STEAM como eje vertebrador | **Adoptado**: cada set se diseña primero como experiencia STEAM y después se le asignan objetivos de lenguaje |

## Arquitectura física · V5 de prueba

```
                    UNIDAD ELECTRÓNICA SELLADA DE LÚA (la monta el fabricante, no el niño)
        ┌──────────────────────────────────────────────────────────────────────────┐
        │  Cabeza versión 4 (PLA) + placa V1 (ESP32-C3 · GC9A01 Ø32,4 mm · 27 fps) │
        │  + bloque-cuello impreso que aloja la batería (propuesta, ver B1)        │
        │  + anillo de luz: 4 luces direccionales (delante/detrás/izq./dcha.)      │
        │  Impresión e integración: masque3d (Orense)                              │
        │  Sin altavoz · sin micrófono · sin motores · BLE GATT · Zero-PHI         │
        │  Debajo del cuello: anti-espigas estándar de bloque grande               │
        └──────────────────────────────────┬───────────────────────────────────────┘
                                           │ encaja en
        ┌──────────────────────────────────┴───────────────────────────────────────┐
        │  CUERPO DE BLOQUES (lo arma el niño)                                     │
        │  Tronco, patas y cola de Lúa con bloques pasivos, sin electrónica,       │
        │  sin tornillos, sin pegamento, sin imanes. Una sola forma correcta de    │
        │  encajar la cabeza (orientación forzada)                                 │
        └──────────────────────────────────┬───────────────────────────────────────┘
                                           │ mismo módulo de encaje
        ┌──────────────────────────────────┴───────────────────────────────────────┐
        │  SETS DE CONSTRUYE CON LÚA · 6 mundos STEAM                               │
        │  Valeria+ (hogar / sesión)  ◄── 100 % compatibles ──►  Descubre con Lúa   │
        │                                                        (escuela 0-6)     │
        │  Opcional, ≥ 3 años: bloque háptico RONRONEO (batería propia, BLE)        │
        └──────────────────────────────────────────────────────────────────────────┘

        TABLETA DEL ADULTO: decide, narra, guía y actúa como sensor ciego local de RA
        (ARCore + MediaPipe + Google Filament, mallas < 100 KB). Cero vídeo, cero red.
```

**Topología BLE en estrella.** La app es el único central. Lúa y Ronroneo son periféricos independientes que no se hablan entre sí. Ninguno toma decisiones: ambos ejecutan índices de catálogos flasheados.

### Por qué la electrónica vive solo en la cabeza

El niño debe poder montar, desmontar, morder, mojar y tirar el cuerpo sin riesgo. Concentrar la electrónica en una unidad sellada (cabeza + cuello) deja todo lo que el niño manipula libremente como piezas pasivas, lavables y sustituibles. La batería del muñeco versión 4 estaba en un cartucho dorsal del cuerpo; al desaparecer ese cuerpo, la batería se traslada a la unidad sellada (decisión bloqueante B1).

## STEAM como columna vertebral

Cada set se diseña empezando por un fenómeno científico o técnico que el niño provoca con las manos. Después se le asignan objetivos de lenguaje, de inglés L2 mediante TPR y, cuando corresponde, de práctica de rehabilitación en Valeria+. El orden importa: **el fenómeno manda y el lenguaje lo nombra**.

El adulto narra y amplía; la app le sugiere palabras espaciales y de proceso adecuadas al momento (dimensiones, formas, posición y dirección, orientación y transformación, cantidad, deícticos, propiedades espaciales y patrón). Este enfoque de juego guiado con mediación parental se apoya en trabajos como BrickSmart (Liu, Zha *et al.*, CHI 2025), que observó más uso de lenguaje espacial en juego de bloques guiado con apoyo al adulto.

| Set | Ciencia (S) | Tecnología (T) | Ingeniería (E) | Arte (A) | Matemáticas (M) |
|---|---|---|---|---|---|
| 1 · El Camino de Lúa | Orientación espacial | Algoritmos tangibles desconectados | Circuito modular | Secuencia narrativa del recorrido | Secuencias, giros de 90° |
| 2 · Estación de Sonido y Eco | El sonido es vibración | Resonadores de pared variable | Cajas de resonancia | Ritmo silábico | Grave/agudo, fuerte/débil |
| 3 · Laboratorio de Rampas y Gravedad | Gravedad y fricción | Tramos intercambiables | Planos inclinados 15° / 30° | Prosodia ascendente/descendente | Comparar velocidades y alturas |
| 4 · Máquina de Soplo y Viento | Flujo de aire | Rotor de baja fricción | Compuertas ligera y pesada | Vocabulario del tiempo | Más fuerte / más suave |
| 5 · Puente de Equilibrio y Fuerza | Centro de gravedad | Fulcro y palanca | Distribución de cargas | Simetría | Masas 20 / 40 / 60 g |
| 6 · Jardín del Sol, la Sombra y la Semilla | Crecimiento vegetal, óptica | Prismas translúcidos | Tallos extensibles con rosca | Siluetas y sombras | Ciclos y secuencias temporales |

## Los 6 mundos de Construye con Lúa

Cada set activa al menos dos de los tres ejes: lenguaje, inglés L2 mediante TPR y STEAM. El adulto opera la aplicación; el niño manipula los bloques y mira a Lúa.

### SET 1 · El Camino de Lúa (*Lúa's Stepping Trail*)
Circuito de senderos táctiles, encrucijadas y orientación espacial. Propiocepción y desensibilización palmar, secuenciación motriz, algoritmos tangibles y verbos de movimiento TPR (*Step forward*, *Turn left*, *Stop*). Baldosas rectas lisas y rugosas con ranura de 12 mm, curvas de 90°, intersecciones en T, fichas cilíndricas de comando, zócalos de inicio y meta. Lúa mira atenta al inicio, da pulsos de ánimo al avanzar y celebra en la meta; si el camino se interrumpe, espera serena.

### SET 2 · La Estación de Sonido y Eco (*Sound & Echo Station*)
Resonancia, ritmo y discriminación fonológica. Discriminación grave/agudo y fuerte/débil, ritmo silábico, pares mínimos, autorregulación ante hiperreactividad acústica. Resonadores huecos (paredes 5,0 / 3,2 / 1,5 mm), martillo balancín, raspadores estriados, plataforma de escucha. Silencio clínico al acoplar; metrónomo visual en el borde del visor. Con Ronroneo: el niño **siente** el pulso que antes ha oído, en una fase separada de la escucha (ver reglas hápticas).

### SET 3 · El Laboratorio de Rampas y Gravedad (*Motion & Gravity Lab*)
Rastreo visual, control inhibitorio, prosodia y cinemática (15° frente a 30°, fricción). Rampas, pilares de elevación 1–6, esferas lisa y rugosa (Ø 38 mm), tramo de fricción intercambiable, zócalo receptor. Espera expectante; celebración o expresión «slow» según el resultado. Sin penalización si la esfera se detiene.

### SET 4 · La Máquina de Soplo y Viento (*Wind & Breath Engine*)
Protrusión labial, cierre velar, dosificación del soplo, vocabulario meteorológico (*Blow*, *Gentle*, *Storm*). Canales de soplo con embocadura anatómica, codo de 90°, rotor de baja fricción, compuertas ligera y pesada. Animación de inhalación, remolino al girar el rotor, espejo de mofletes si el soplo se dispersa, insignia al abatir la compuerta pesada.

### SET 5 · El Puente de Equilibrio y Fuerza (*Bridge & Balance Studio*)
Tono postural, percepción háptica del peso, pinza digital, comparativos y condicionales, estática. Fulcro y viga balancín, masas calibradas de 20, 40 y 60 g, pasadores de anclaje, zócalo de nivel. Sorpresa atenta al inclinarse; alivio e insignia de constructora al recuperar el equilibrio.

### SET 6 · El Jardín del Sol, la Sombra y la Semilla (*Sun, Shadow & Growth Garden*)
Secuenciación narrativa, ampliación morfosintáctica, praxia rotatoria de muñeca, biología vegetal y óptica. Base de tierra, semilla, tallos extensibles con rosca, coronas florales y frutales, prismas translúcidos, pantallas opacas de silueta. Ternura al sembrar, esperanza al brotar, celebración al florecer, modo descanso al proyectar la sombra de la Luna.

### Interoperabilidad
Los seis sets comparten el mismo módulo de encaje y la misma lógica de respuesta de Lúa, y pueden combinarse en un macro-escenario continuo: un soplo impulsa una esfera que golpea un resonador; Lúa cruza el puente nivelado y llega al jardín por el camino táctil.

## Anillo de luz direccional · propuesta V5

El cuerpo de Lúa, montado con bloques, es cuadrado visto desde arriba. Para que cada lado tenga una luz sin meter electrónica en los bloques que monta el niño, las cuatro luces viven en el **bloque-cuello sellado**, una mirando a cada lado: delante, detrás, izquierda y derecha. Las alimenta la batería de la cabeza y las gobierna la placa V1. No añaden batería, dispositivo BLE ni contactos expuestos. masque3d las integra en fábrica.

La referencia de partida es el sistema de luces de InsideOut ReMind (Harshini *et al.*, *Alzheimer's & Dementia* 2025), que usa un LED RGB WS2812B por cubo para dar respuesta visual suave. En Lúa se adopta el tipo de luz, pero no su disparo por tacto: la acción la detecta la RA de la tableta, la app decide y Lúa enciende la luz. No se añaden sensores táctiles al cuerpo.

**Las luces significan dirección, no decoran.** El significado lo lleva la posición de la luz, no su color, para que funcione también con alteraciones de la percepción del color.

| Set | Uso de las cuatro luces |
|---|---|
| 1 · El Camino de Lúa | La luz del lado del giro acompaña *Turn left* / *Turn right*; la luz delantera, *Step forward* |
| 3 · Rampas y Gravedad | La luz del lado de la rampa se enciende mientras la esfera baja |
| 5 · Puente de Equilibrio | La luz del lado que baja indica hacia dónde se inclina la viga; todas tenues al recuperar el equilibrio |
| 6 · Jardín del Sol y la Sombra | La luz del lado iluminado marca de dónde viene el «sol»; la sombra queda en el lado contrario |
| Todos · `RELAX` | Las cuatro a brillo mínimo, cambio muy lento o apagadas |

**Protocolo.** Nuevo opcode `LIGHT(patrón)` con índice a un catálogo flasheado (por ejemplo `DIR_IZQ`, `DIR_DCHA`, `DIR_DELANTE`, `DIR_ATRAS`, `CALMA`, `APAGADO`). Sin colores ni tiempos libres. Bit `CAP_LIGHT` en la máscara de `GRANT`, desactivado por defecto. Si se pierde BLE, el anillo se apaga junto con el paso de Lúa a estado seguro.

## Reglas de luz (de obligado cumplimiento)

1. Brillo bajo y limitado por firmware; cambios fijos o lentos.
2. Nunca más de tres destellos por segundo.
3. Nunca como señal de error.
4. Apagadas durante la escucha, la captura de voz y el turno de respuesta del niño.
5. Apagadas en todo VIA+: VIA+ no concede `CAP_LIGHT`.
6. El adulto puede apagarlas en cualquier momento desde la app.

## Bloque háptico Ronroneo · propuesta V5

Ronroneo es un bloque independiente, con batería recargable propia, que convierte el ronroneo de Lúa en algo que el niño siente en la mano. **No forma parte de la cabeza** y **no se incluye en el kit de VIA+**. Así, el Silencio Clínico en VIA+ sigue siendo una garantía física: la cabeza no puede vibrar y el bloque que vibra no está presente.

**Para qué sirve.** Corregulación (vibración lenta y suave sincronizada con el estado `RELAX` de Lúa). Metrónomo táctil para el ritmo silábico, con especial interés en niños con hipoacusia o implante coclear (hipótesis por validar, no un beneficio demostrado). Fenómeno STEAM del Set 2: el sonido es vibración. Celebración breve y opcional al completar un objetivo motor.

**Qué no hace nunca.** No vibra ante un error ni como aviso o castigo (error neutro). No vibra durante el turno de respuesta del niño ni durante la escucha. No vibra en VIA+. No tiene sensores, micrófono, altavoz, cámara ni LED de estado. No guarda nada. No se comunica con Lúa directamente.

**Arquitectura propuesta (pendiente de diseño electrónico por un proveedor):**

| Elemento | Propuesta | Motivo |
|---|---|---|
| Envolvente | Bloque de 2×4 módulos, altura doble, cantos redondeados, paredes ≥ 3,2 mm, cierre que solo se abre con herramienta | Volumen suficiente para la electrónica; batería inaccesible para el niño |
| Microcontrolador | ESP32-C3, misma familia que la placa V1 | Un solo toolchain, un solo protocolo, menos superficie de error |
| Actuador | Motor lineal resonante (LRA) con driver háptico dedicado (por ejemplo, DRV2605L) | Más silencioso y controlable que un motor de masa excéntrica; amplitud limitable por hardware y firmware |
| Batería | LiPo con circuito de protección, cargador con protección térmica, capacidad por dimensionar con consumo medido | Autonomía de una jornada de sesiones sin depender de la cabeza |
| Carga | USB-C empotrado bajo tapón de silicona; la realiza solo el adulto | Evita contactos eléctricos expuestos en una pieza que el niño manipula |
| Encendido | Interruptor empotrado de almacenamiento/transporte, accionable por el adulto | Corte total de energía fuera de uso |
| Edad | ≥ 3 años | Pieza con batería; se excluye del material 0–3 de Descubre con Lúa |

**Firmware y protocolo.** La app envía `HAPTIC(patrón, nivel)`, donde *patrón* es un índice a un catálogo flasheado (por ejemplo `RONRONEO`, `LATIDO`, `METRONOMO_LENTO`, `CELEBRA_CORTO`) y *nivel* va de 0 a 3. No existen patrones libres: el artículo TactCube (Battistoni *et al.*, *Sensors* 2022) transmitía secuencias arbitrarias de milisegundos; aquí se descarta para que ningún mensaje pueda producir una vibración fuera de límites. El permiso háptico es un bit de la máscara de capacidades de `GRANT`, desactivado por defecto. El firmware impone duración máxima por pulso, ciclo de trabajo máximo, tiempo acumulado máximo por minuto y corte térmico. Si se pierde BLE o falta el latido de la app, la vibración se detiene de inmediato y el bloque queda inerte. El bloque solo devuelve nivel de batería, versión de firmware y códigos de fallo.

## Reglas hápticas (de obligado cumplimiento)

1. La vibración es siempre opcional, la activa el adulto y empieza en el nivel mínimo.
2. Nunca durante la escucha, la captura de voz o el turno de respuesta del niño.
3. Nunca como señal de error.
4. Nunca en VIA+: el bloque no forma parte de ese kit y VIA+ no concede el bit háptico.
5. El adulto la detiene con un gesto en la app; detenerla nunca resta ni penaliza.
6. Ante signos de malestar sensorial del niño, se desactiva para el resto de la sesión.

## Principios rectores

- **Agencia compartida.** El niño es el motor del mundo de juguete: desplaza a Lúa, sopla, aprieta, equilibra, riega. La pantalla circular es el espejo afectivo inmediato.
- **Lúa permanece muda.** La voz está solo en el dispositivo del adulto, para no enmascarar estímulos ni competir con audífonos o implantes.
- **Error neutro.** Desacople, inclinación insuficiente o soplo débil producen su consecuencia física natural. Lúa permanece serena, atenta o de aliento.
- **Higiene sensorial y silencio clínico.** Durante el turno de respuesta del niño todo está quieto. Metrónomos visuales por defecto; táctil solo con Ronroneo y bajo las reglas hápticas. Descanso visual 20-20-20 (`RELAX`).
- **El adulto media siempre.** La tecnología contextualiza; no sustituye la interacción humana ni el andamiaje.
- **Montaje infantil sin fricción.** Una sola forma correcta de encajar cada pieza clave, piezas grandes, sin tornillos, sin pegamento y sin imanes en las piezas que monta el niño.
- **Zero-PHI / Zero-Network.** La cámara de la tableta es un sensor ciego local. Solo se usan magnitudes físicas (grados, latencias en ms, ratios 0,0–1,0). Cero vídeo, cero transmisión.

## Seguridad física · lo que está afirmado y lo que está por verificar

Las piezas de bloque se diseñan con dimensiones mayores que el cilindro de piezas pequeñas de EN 71-1 y con paredes estructurales ≥ 3,2 mm. Ninguna conformidad normativa se declara hasta disponer de ensayo de laboratorio. Pendiente de verificar, como mínimo: EN 71-1/2/3 (seguridad de juguetes), EN 62115 (juguetes eléctricos) para la unidad de cabeza y para Ronroneo, la Directiva de equipos radioeléctricos por BLE y sus actos delegados de ciberseguridad y privacidad, el calendario del nuevo Reglamento europeo de seguridad de juguetes y los requisitos de extraibilidad de baterías del Reglamento (UE) 2023/1542, que pueden chocar con una batería sellada.

## Firmware

- Catálogo de expresiones (neutra, atenta, celebración, pictograma, insignia, nivel, ronroneo…) y partículas. Arte 24×24 copiado de Valeria+ con gate de paridad de sprite.
- Máquina de estados completa con concesión (`GRANT` y máscara de capacidades), silencio clínico, ancla visual (`RELAX`) y modos sensoriales. Más de 57 000 comprobaciones.
- Emulador de escritorio C++17 sin dependencias: `make run` (placa V1 circular).
- Protocolo sin campo de texto: índices a catálogos flasheados y estado de 8 bytes fijo. Cero líneas de audio en el firmware.
- Opcodes de Lúa: `PHASE`, `VERDICT`, `CELEBRATE`, `AWARD`, `PICTO`, `MOOD`, `ACCESSORY`, `RELAX`… El firmware no sabe qué palabra se trabaja.
- Propuesto para V5: opcode `LIGHT` y bit `CAP_LIGHT` para el anillo de luz de la cabeza; opcode `HAPTIC` y bit `CAP_HAPTIC`, exclusivos del firmware de Ronroneo. Cualquier nuevo opcode pasa por la puerta de aprobación clínica (`docs/pendiente-en-valeria.md`) antes de fusionarse.

## Estado (octubre 2026)

| Componente | Estado |
|---|---|
| Placa V1 circular | Compila, flashea, arranca y pinta a 27 fps. Ocho unidades encargadas. Cristal capacitivo leído |
| Cabeza versión 4 | Diseñada en Blender (`bpy`). Entregada para impresión en masque3d (Orense). **Se conserva** |
| Cuerpo versión 4 | **Retirado**. Sustituido por cuerpo de bloques (V5, en diseño) |
| Bloque-cuello con batería y anillo de luz | **Propuesta**. Depende de B1 y B5. Impresión e integración: masque3d |
| Ronroneo | **Propuesta**. Impresión e integración: masque3d. Pendiente de B3 |
| Construye con Lúa | Pipeline procedural Blender + JSON + CustomPainter operativo. RA (AR-1/2/3) en integración |
| Valeria+ | Premiada como mejor iniciativa innovadora en Maker Faire Galicia 2026 |

## Decisiones bloqueantes

- **B1 · Dónde va la batería de Lúa.** ¿Cabe en la cabeza versión 4 o necesita el bloque-cuello sellado? Requiere medir el volumen interior de la cabeza impresa, ya con el consumo del anillo de luz incluido.
- **B2 · Integración electrónica.** Resuelta en parte: masque3d imprime e integra. Queda por confirmar con masque3d si también aportan o diseñan la placa de Ronroneo, o si debe llegarles montada de otro proveedor.
- **B3 · Aprobación clínica** de la vibración y la luz como canales nuevos y de los opcodes `HAPTIC` y `LIGHT`.
- **B4 · Denominación pública de los bloques.** Evitar marcas de terceros en nombre, insignias y material comercial; describirlos por su módulo de encaje.
- **B5 · Pin libre en la placa V1** para gobernar el anillo de luz. Lo comprueba masque3d sobre la placa real antes de imprimir el cuello.

## Hoja de ruta

El plan detallado de la versión de prueba V5 está en [`docs/PLAN-PRUEBA-V5.md`](docs/PLAN-PRUEBA-V5.md).

---

*Todo el apoyo digital es offline. No hay red ni datos de los niños.*
