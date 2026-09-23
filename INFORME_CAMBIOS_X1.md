# Informe de cambios · Rama x1 · Lúa V15 (23/09/2026)

> Commits: submodulo `lua-firmware` en rama `x1` (`74f2d36`) + repo padre en
> `x1` (`9fe48ca`). Gate en verde: 21 piezas sin agujeros, apoyadas, en cama.

## 1. CAD paramétrico — `lua-firmware/cad/lua-muneco.scad`

### Grupo 1 · Hueco de placa para la carcasa + cabeza Φ87
- `lua-muneco.scad:69-83` — `carcasa_margen = 2.5`, `carcasa_prof = 3.0`
  (SUPOSICIONES sin calibre) y caja derivada `cajet_w/h/p` (42 × 43,5 × 15).
- Todo lo que era `pcb_*` y toca la placa usa ahora `cajet_*`: diagonal
  (`:295`), corte (`y_corte`), costillas, pilares, ranura de conectores,
  pulsadores y fantasma.
- `lua-muneco.scad:292` — `cabeza_d = 87.0` (de 78): con la cajeta, la ranura
  de conectores caía dentro de la boca del cuello (aleta en negativo).
- `lua-muneco.scad:363` — `z_cabeza = 114.0` (de 111): la cabeza creció de
  radio y el collar la tapaba.

### Grupo 2 · Press-fit «de Lego» (`holgura_press = 0.15`)
- `lua-muneco.scad:157` — parámetro `holgura_press`.
- Boca del cuello (`gota`, ~l.795), cajetas de hombro/cadera (`:1140-1142`),
  cajeta del emblema (`:1145`) y aserto de aleta (`:390`): de `holgura`
  (pegamento) a `holgura_press`.

### Grupo 3 · Bayoneta de media vuelta del casco («como una rosca»)
- `lua-muneco.scad:685` — `bay_espolon()`: tubo + 3 nervios helicoidales en la
  mitad de delante (sale del corte hacia la nuca).
- `lua-muneco.scad:714` — `bay_manga_macizo()`: anillo que lo abraza en el dorso.
- `lua-muneco.scad:726` — `bay_canales()`: 3 canales de la misma pendiente
  (0/170/270: una sola orientación de cierre).
- Sustituye a `junta_lug`/`junta_esp`/`en_junta` (eliminados, sin restos).
- `lua-muneco.scad:~750` — 4 puntales diagonales cosen el espolón al tubo
  del barril (sin ellos flotaba: cáscara suelta).

### Grupo 4 · Orejas con bayoneta de ¼ de vuelta
- `lua-muneco.scad:896` — params `oreja_ala_d/l/h`, cono, vástago y nervio único.
- Macho en `oreja()` (brida de tope + cono + nervio helicoidal, punta a 3,9 mm
  para no tocar el espolón) y hembra en `cabeza_dorso()` (cajera + cono con
  holgura + canal). `d_espiga_oreja` eliminado.
- `lua-muneco.scad:~1753` — `p_oreja()` apoya en el borde de la brida Ø12.

### Grupo 5 · Mochila sin tornillos
- `lua-muneco.scad:404-405` — `moch_perno_d/l`; bloque de tornillería M2 e
  insertos de latón retirado (con nota).
- Cuerpo: 2 taladros ciegos press-fit en macizo (fuera del hueco de celda).
- `lua-muneco.scad:1550` — `mochila()` con 2 cajeras ciegas (se imprime plana).
- `lua-muneco.scad:1563` — `pernos_mochila()`: 2 pernos Ø4 × 6,6 sueltos en
  una pieza con lengüeta rompible (pieza 19).
- `lua-muneco.scad:1746,1823` — `p_pernos_mochila()` + rama `pieza`.
- ⚠ La tapa abre tirando (antes exigía herramienta): anotado en el manual.

### Robustez del booleano (lo que cazó el gate en el camino)
- `rosca_hembra()`: raíz 0,5 por debajo del escariado (44.000 aristas abiertas).
- `barril_placa()`: tubo macizo + escariado/filete en una resta; filete de 20 mm
  (5 pasos enteros) anclado arriba; boca del escariado con abocardado cónico.
- `costilla()` en caja → pilares redondos → **retiradas** (`costillas_placa()`
  vacía en `:557`): cada cruce con el tubo salía como caras duplicadas. La
  placa la centran las paredes del hueco; `costilla()/calado()` eliminados.
- Tubo y escariado a `$fn = 96` como el casco (teselación coincidente).
- Visor hundido 0,3; ranura de conectores con esquinas redondeadas r=2.
- Estado honesto: `cabeza_frente` conserva 6 aristas internas duplicadas + 1
  viruta de 4 tris (cero agujeros; lamina bien).

### Plato
- `lua-muneco.scad:1776` — reempaquetado para 19 piezas en 220×220 con calles
  de ~1 mm (las cabezas Φ87 no cabían en el layout anterior).

## 2. Gate — `lua-firmware/tools/check-cad.js`
- `check-cad.js:103-107` — `MAPA` con `p_pernos_mochila`.
- Reglas 1–2 con bandas de tolerancia: agujeros (1 triángulo) y cáscaras
  grandes (≥50 tris) fallan; duplicadas internas y virutas <50 tris avisan.
- Exportación en binario (`--export-format binstl`): el snapshot 2026.09.22
  exporta ASCII por defecto y el lector del gate solo lee binario.

## 3. STL — `lua-firmware/cad/stl/` (fuente) y `stl/` (copia para taller/manual)
- 21 piezas reexportadas (incluye `pernos_mochila.stl` nuevo).
- Voladizos medidos (soportes en árbol donde se piden): orejas 31,8 %,
  pulsadores 30,3 %, anillo 17,9 %.

## 4. Blender — `lua-x1-ensamble.blend` + `renders/render_x1_*.png`
- Ensamble montado desde los STL con la matemática exacta del `montaje()`.
- `render_x1_hero.png` (muñeca completa), `render_x1_bayoneta.png` (casco
  explosionado), `render_x1_oreja.png` (oreja explosionada),
  `render_x1_mochila.png` (tapa + pernos).
- Scripts: `/tmp/x1_render.py`, `/tmp/x1_rerender.py` (no versionados).

## 5. Manual
- `manual/MANUAL_ENSAMBLE_LUA.md` → V15 (21 piezas, pasos press-fit/bayoneta,
  BOM sin M2, tabla de soportes, aviso de seguridad de la tapa).
- `manual/build_ikea_pdf.py` → textos V15 + mapa de 4 diagramas nuevos.
- `manual/Manual_Ensamble_Lua_IKEA.pdf` reconstruido.
- `manual/diagrams_jpg/step{1,4,5,7}_*.jpg` regenerados desde los STL reales.
- Pendiente: diagramas de pasos sin cambios (collar, PCB, miembros, barbilla,
  final) aún muestran geometría V14.

## 6. Documentos de impresión
- `lua-firmware/docs/cad/impresion-ender3-s1-pro.md` — tabla al día (incluye
  fila obligatoria de `pernos_mochila` que exige el gate).
- `INSTRUCCIONES_IMPRESION_Y_PLAN_LUA.md` — V15, catálogo de 21, BOM sin
  ferretería, pasos press-fit, soportes por pieza.
- `stl/README.md` — V15, pernos, cotas finales, soportes.

## 7. Entorno
- OpenSCAD 2026.09.22 reinstalado desde el snapshot (la app desapareció a
  mitad de sesión; el enlace cuelga de `/opt/homebrew/bin/openscad`).
- Blender 5.1.2 headless operativo para Fp, renders y ensamble.
