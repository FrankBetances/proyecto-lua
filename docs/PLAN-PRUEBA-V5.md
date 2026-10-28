# Plan de la versión de prueba V5 · Lúa de bloques + Ronroneo

**Objetivo de la V5.** Demostrar, antes de cualquier piloto, que un niño de 3 a 6 años puede montar el cuerpo de Lúa con bloques sin ayuda, que la cabeza versión 4 funciona como unidad sellada, que Ronroneo es seguro, silencioso y aceptable para niños y adultos, y que los seis sets se integran con Valeria+ y Descubre con Lúa sin interferir con la sesión.

**Qué no es la V5.** No es un estudio de eficacia. No genera evidencia clínica ni educativa de resultado. Es una prueba técnica y de usabilidad formativa.

**Convenciones.** Semanas S1… desde el lunes 2 de noviembre de 2026 (supuesto). Los plazos de fabricación son supuestos hasta tener presupuesto firmado de masque3d. Responsables por rol: Dirección de producto (Frank), Fabricante e integrador (masque3d, Orense: impresión e incorporación de la electrónica), Proveedor de placa de Ronroneo (masque3d u otro, por confirmar), Responsable de firmware, Logopeda colaboradora, Puerta de aprobación clínica.

**Principio de fabricación.** Toda intervención de hardware la hace masque3d. Lo que llega al equipo son unidades cerradas, probadas y listas para encender. Ninguna fase de este plan exige soldar, montar ni abrir piezas al equipo de producto.

---

## Fase 0 · Decisiones (S1–S2)

**Entregable.** Registro de decisiones B1–B4 en `docs/decisiones-v5.md` y `docs/pendiente-en-valeria.md`.

B1, ubicación de la batería. El proveedor de impresión mide el volumen interior útil de la cabeza versión 4. Si cabe una LiPo con protección y holgura térmica, la batería va en la cabeza; si no, se diseña el bloque-cuello sellado, unido a la cabeza de forma permanente por el fabricante. En ambos casos el niño ve una sola pieza: «la cabeza de Lúa».

B2, integración electrónica. masque3d imprime e incorpora la electrónica. Queda por confirmar con ellos un único punto: si aportan o diseñan la placa de Ronroneo o si debe llegarles montada de otro proveedor. Si no la aportan, Ronroneo se aplaza y la V5 sigue con cabeza, cuello con luces y cuerpo de bloques.

B3, aprobación clínica. Presentar a la puerta de aprobación las reglas hápticas y de luz, los catálogos de patrones, los opcodes `HAPTIC` y `LIGHT`, los bits `CAP_HAPTIC` y `CAP_LIGHT` y la exclusión de ambos canales en VIA+.

B5, pin libre en la placa V1. masque3d comprueba sobre una placa V1 real que queda un pin disponible para el anillo de luz y que la placa admite el consumo añadido. Si no hay pin, el anillo se aplaza y el cuello se imprime sin alojamiento de luces.

B4, denominación. Sustituir en README, sets y material las referencias a marcas de bloques de terceros por una descripción del módulo de encaje.

**Criterio de salida.** B1, B2, B3 y B5 resueltas por escrito. Sin B3 no se fabrican Ronroneo ni el anillo de luz; el resto de la V5 sigue adelante sin ellos.

## Encargo a masque3d · nueva impresión e integración V5

Este es el paquete que se entrega a masque3d en S2, una vez resueltas B1 y B5. Se piden tres conjuntos.

**Conjunto A · Unidad sellada de Lúa (cabeza + cuello).** Se reutiliza el diseño de la cabeza versión 4. Se diseña e imprime el bloque-cuello con anti-espigas estándar inferiores, orientación forzada, alojamiento de la batería (si B1 lo exige) y cuatro ventanas difusoras, una por lado, para el anillo de luz. masque3d instala la placa V1, la batería con protección, los cuatro LED y su cableado interno, y cierra la unidad de forma que solo se abra con herramienta. La carga USB-C queda accesible para el adulto, empotrada y con tapón.

**Conjunto B · Cuerpo de bloques.** Tres iteraciones del cuerpo de Lúa (objetivo de diseño: entre 4 y 8 piezas), sin electrónica, sin tornillos, sin pegamento y sin imanes. La cara superior del cuerpo replica la planta cuadrada del cuello, para que las cuatro luces queden alineadas con los cuatro lados del cuerpo.

**Conjunto C · Ronroneo (condicionado a B2 y B3).** Envolvente de 2×4 módulos de altura doble con cierre que solo se abre con herramienta. masque3d integra la placa, el motor lineal resonante, la batería con protección, el USB-C empotrado y el interruptor de almacenamiento.

**Cantidades (supuesto).** Dos unidades del conjunto A (una de banco y una de usabilidad), un juego completo del conjunto B por iteración y dos unidades del conjunto C. Las cantidades definitivas dependen del presupuesto.

**Condiciones de entrega que se piden a masque3d.** Unidades encendidas y probadas antes del envío, con el firmware cargado por el responsable de firmware o según sus instrucciones. Fotografía interior de cada unidad antes del cierre, para documentar la integración. Lista de componentes instalados con su referencia. Ninguna pieza que deba montar el equipo de producto.

**Lo que se pide a masque3d como respuesta.** Presupuesto, plazo por conjunto, confirmación de B5 y respuesta a la pregunta abierta de B2.

## Fase 1 · Cuerpo de bloques y adaptador de cuello (S2–S5)

**Diseño.** Cuerpo de Lúa con un número reducido de bloques grandes (objetivo de diseño: entre 4 y 8 piezas), con forma reconocible de gata, cola incluida. Bloque-cuello o adaptador con anti-espigas estándar y orientación forzada: la cabeza solo encaja mirando hacia delante. Sin tornillos, sin pegamento ni imanes en piezas que monta el niño. Colores o relieves que guíen el orden de montaje sin instrucciones escritas.

**Producción.** Tres iteraciones cortas de impresión con masque3d.

**Criterios de aceptación verificables en banco:**

- Ninguna pieza que monta el niño entra completa en el cilindro de piezas pequeñas de EN 71-1 (comprobación con el calibre normalizado).
- Paredes estructurales ≥ 3,2 mm en todas las piezas.
- La cabeza no puede encajarse en una orientación incorrecta.
- Fuerza de encaje y de desencaje medidas con dinamómetro; el umbral aceptable se fija tras la Fase 5 con datos reales de niños de 3 años.
- Caída del muñeco montado desde la altura de una mesa sobre suelo duro: la cabeza no se abre, la pantalla no se desprende y la batería no queda expuesta.
- Ningún canto vivo ni rebaba al tacto tras el acabado.

## Fase 1b · Anillo de luz en banco (S4–S7, condicionada a B3 y B5)

**Integración por masque3d** en el conjunto A, con firmware del catálogo `LIGHT` cargado.

**Criterios de aceptación verificables:**

- Cada patrón del catálogo enciende el lado correcto: delante, detrás, izquierda y derecha, comprobado con la cabeza montada sobre el cuerpo de bloques.
- Ningún patrón produce más de tres destellos por segundo, verificado grabando la luz con la cámara lenta de un teléfono durante la prueba de banco (sin niños).
- El brillo máximo, limitado por firmware, no deslumbra a 30 cm en sala con luz normal. El umbral lo fija la puerta clínica antes de medir.
- Sin `CAP_LIGHT` concedido, el anillo permanece apagado en todos los estados.
- Al perderse BLE, el anillo se apaga en el mismo paso a estado seguro que la pantalla.
- El consumo del anillo, medido por masque3d, se incorpora al cálculo de autonomía de B1; la unidad mantiene una jornada de sesiones con las luces activas según una mezcla de patrones tipo.
- La luz se ve a través de las ventanas difusoras sin puntos calientes y sin que la superficie se caliente.

## Fase 2 · Ronroneo en banco (S3–S8, condicionada a B2 y B3)

**Diseño e integración por masque3d o por el proveedor de placa que se confirme en B2.** ESP32-C3, driver háptico con LRA, LiPo con protección, cargador con protección térmica, USB-C empotrado, interruptor de almacenamiento. Envolvente de 2×4 módulos de altura doble, impresa por masque3d, con cierre que solo se abre con herramienta.

**Criterios de aceptación verificables:**

- Ruido acústico de la vibración medido con sonómetro a 30 cm en sala silenciosa, con cada patrón y nivel. Se recomienda medirlo en la cabina de audiometría del servicio de ORL si está disponible. El umbral máximo lo fija la puerta clínica antes de medir, no después.
- Temperatura de la superficie del bloque durante una hora de uso continuo al nivel máximo y durante la carga, registrada con termómetro de contacto. Corte térmico del firmware verificado provocando el sobrecalentamiento en banco.
- Pérdida de BLE con vibración activa: la vibración se detiene en menos de 1 s (supuesto de diseño, revisable) en 50 de 50 intentos.
- Ningún mensaje fuera del catálogo produce vibración: prueba con mensajes malformados, índices fuera de rango y niveles fuera de 0–3.
- Sin `CAP_HAPTIC` concedido no hay vibración en ningún estado.
- Autonomía medida con la mezcla de patrones de una sesión tipo; objetivo de diseño: una jornada sin recargar.
- Caída del bloque desde la altura de una mesa sobre suelo duro: la envolvente no se abre y el bloque sigue funcionando.

## Fase 3 · Firmware y protocolo (S2–S8, en paralelo)

- Firmware de Ronroneo sobre el mismo núcleo que la placa V1: catálogo flasheado de patrones, límites de pulso, ciclo de trabajo y tiempo acumulado, latido de la app con vigilancia y estado inerte por defecto.
- `HAPTIC` y `CAP_HAPTIC`, `LIGHT` y `CAP_LIGHT` añadidos al protocolo con pruebas automáticas al mismo nivel que el resto de la máquina de estados.
- Límite de frecuencia de destello y de brillo implementado en el firmware de la placa V1, con prueba automática que rechaza cualquier patrón que lo supere.
- Emparejamiento solo con la app autorizada; rechazo de centrales desconocidos.
- Gate automático en VIA+ que verifica que los bits háptico y de luz nunca se conceden.
- Gate automático en Valeria+ que bloquea `HAPTIC` y `LIGHT` en las fases de escucha y de respuesta del niño.
- Emulador de escritorio ampliado para simular Ronroneo y el anillo de luz sin hardware.

**Criterio de salida.** Todas las pruebas en verde en integración continua y revisión del protocolo aprobada por la puerta clínica.

## Fase 4 · Integración con Valeria+ y Descubre con Lúa (S6–S9)

- Valeria+: asignar a cada set su tarjeta STEAM (fenómeno → palabras → consigna del adulto) y sus palabras espaciales sugeridas por fase de montaje. Mantener las sugerencias al adulto breves; en BrickSmart el apoyo guiado aumentó el esfuerzo percibido por los padres.
- Valeria+: interruptor de Ronroneo en el menú del adulto, apagado por defecto, con nivel inicial mínimo.
- Valeria+ y Descubre con Lúa: asignar los patrones del anillo de luz a los Sets 1, 3, 5 y 6, e interruptor del anillo en el menú del adulto.
- Descubre con Lúa: misma tarjeta STEAM en versión docente; Ronroneo excluido del material para menores de 3 años.
- Revisión de redacción: retirar «clínico» de los textos de RA de Valeria+ (por ejemplo, «RA de práctica» en lugar de «AR clínico») para no contradecir su finalidad de aplicación educativa.

**Criterio de salida.** Un adulto completa una sesión simulada de cada set sin consultar documentación externa, y la app nunca queda bloqueada al apagar Lúa o Ronroneo a mitad de sesión.

## Fase 5 · Prueba de usabilidad formativa con familias (S9–S11)

**Antes de empezar.** Consultar si la prueba requiere dictamen de un comité de ética de la investigación. Con menores, consentimiento informado de los padres y asentimiento del niño en todo caso.

**Participantes (supuesto).** Entre 6 y 8 niños de 3 a 6 años, repartidos entre 3–4 y 5–6 años, con su adulto de referencia. Muestra de conveniencia, sin pretensión estadística.

**Tareas.** (1) Montar el cuerpo de Lúa y colocar la cabeza sin ayuda. (2) Jugar el Set 1 guiado por el adulto con el anillo de luz activo, para observar si el niño gira hacia el lado iluminado. (3) Solo si el adulto lo activa: probar Ronroneo en `RELAX` y en el metrónomo táctil.

**Qué se registra, sin datos personales ni vídeo.** Hoja en papel con código anónimo y franja de edad. Montaje completado sin ayuda (sí/no), tiempo hasta completarlo, número de intentos de encaje fallidos y número de ayudas del adulto. Reacción a Ronroneo según una escala observacional de tres valores (se acerca / neutral / se retira) y si el adulto lo apagó. Valoración breve del adulto sobre facilidad, utilidad y esfuerzo.

**Criterios de decisión (supuestos, revisables antes de empezar):**

- Montaje: al menos el 80 % de los niños de 5–6 años y la mayoría de los de 3–4 montan el cuerpo y colocan la cabeza sin ayuda.
- Ronroneo: ningún niño muestra rechazo sostenido ni malestar al nivel mínimo. Si alguno lo muestra, se analiza antes de continuar.
- Anillo de luz: la mayoría de los niños de 5–6 años asocia el lado iluminado con la dirección del giro tras una demostración del adulto. Ningún niño muestra malestar ante las luces.
- Ninguna incidencia de seguridad (pieza a la boca con riesgo, pellizco, calor).

## Fase 6 · Decisión de paso a piloto (S12)

**Go** si se cumplen los criterios de las Fases 1, 2, 4 y 5, no hay incidencias de seguridad y la puerta clínica aprueba. **Go sin Ronroneo** si el cuerpo de bloques funciona pero Ronroneo no supera ruido, temperatura o aceptación. **No-go** si los niños no pueden montar el cuerpo sin ayuda: se rediseña la Fase 1.

## Riesgos principales y mitigación

| Riesgo | Mitigación |
|---|---|
| La batería no cabe en la cabeza versión 4 | Bloque-cuello sellado unido de fábrica (B1) |
| masque3d no puede aportar la placa de Ronroneo | Ronroneo se aplaza; la V5 sigue con cabeza, cuello con luces y cuerpo de bloques |
| No hay pin libre en la placa V1 para las luces | El anillo se aplaza; el cuello se imprime sin alojamiento de luces (B5) |
| Las luces añaden consumo y acortan la autonomía | Brillo limitado por firmware y consumo incluido en el cálculo de B1 |
| Luces como estímulo excesivo o riesgo fotosensible | Límite de tres destellos por segundo, brillo bajo, apagado en escucha y en VIA+ |
| Ruido de la vibración incompatible con la sesión | LRA y amplitud limitada; si aun así falla, Ronroneo queda fuera del uso en sesión y solo se usa en hogar |
| Hiperreactividad táctil | Opcional, nivel mínimo inicial, detención inmediata, exclusión en menores de 3 años |
| Batería sellada frente a requisitos de extraibilidad del Reglamento (UE) 2023/1542 | Consultar con laboratorio de ensayo antes de pasar a piloto |
| Contactos y USB-C expuestos a saliva o líquidos | Carga solo por el adulto, puerto empotrado con tapón, sin contactos en las caras de encaje |
| Uso de marcas de terceros en la comunicación de los bloques | Denominación propia del módulo de encaje (B4) |
| Sobrecarga del adulto con demasiadas sugerencias de la app | Una sugerencia por fase, ampliable a petición |

## Evidencia de referencia y su límite

- **Terapia basada en bloques en TEA.** La revisión sistemática de Narzisi *et al.* (*Brain Sciences*, 2021) incluyó 19 estudios, con un único ensayo aleatorizado y calidad global baja. Sirve como fundamento de diseño, no como prueba de eficacia de Lúa.
- **Juego de bloques guiado con apoyo al adulto.** BrickSmart (Liu, Zha *et al.*, CHI 2025) comparó 12 y 12 parejas de padres e hijos de 6–8 años en una sesión única. Respalda el diseño de sugerencias de lenguaje espacial para el adulto, no resultados a largo plazo.
- **Dispositivo táctil con ESP32, vibración y LiPo.** TactCube (Battistoni *et al.*, *Sensors* 2022) es un precedente técnico de viabilidad en laboratorio con adultos. Se adopta su enfoque de patrones de vibración y se descarta la transmisión de patrones libres.
- **Referencia de luces y contraejemplo de arquitectura.** InsideOut ReMind (Harshini *et al.*, *Alzheimer's & Dementia* 2025) usa LED RGB WS2812B como respuesta visual suave; Lúa adopta ese tipo de luz para el anillo direccional. El mismo trabajo usa audio, actualización remota por Wi-Fi, contenidos personales y disparo por tacto; Lúa descarta deliberadamente esos cuatro elementos.
