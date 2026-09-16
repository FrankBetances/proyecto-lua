#!/usr/bin/env python3
"""
Official IKEA Manual PDF Builder for Lúa Mascot (Valeria+ / VIA+ · V14)
Builds an authentic, 8-page, publication-grade IKEA assembly manual
using pure Python standard library and real line-art CAD diagrams.
"""

import os
import sys
import struct
import zlib

BASE_DIR = os.path.abspath('.')
DIAGRAMS_DIR = os.path.join(BASE_DIR, 'manual/diagrams_jpg')
PROJECT_PDF = os.path.join(BASE_DIR, 'manual/Manual_Ensamble_Lua_IKEA.pdf')
DOWNLOAD_PDF = '/Users/frankalbertobetancesreinoso/Downloads/Manual_Ensamble_Lua_IKEA.pdf'

PAGE_W = 595.28  # A4 width in points
PAGE_H = 841.89  # A4 height in points

def clean_latin1(text):
    replacements = {
        '\u26d4': '[!]',
        '\u26a0': '[!]',
        '\ufe0f': '',
        '\u21bb': '->',
        '\u2728': '*',
        '\ud83d\udd29': '[M2]',
        '\ud83d\udca7': '[Adhesivo]',
        '\u26a1': '[USB]',
        '\u2013': '-',
        '\u2014': '--',
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return ''.join(c if ord(c) < 256 else '?' for c in text)

class PdfWriter:
    def __init__(self):
        self.objects = []
        self.pages = []
        self.images = {}  # name -> obj_id
        self.image_dims = {}

    def add_object(self, content):
        self.objects.append(content)
        return len(self.objects)

    def load_image(self, name, filepath):
        with open(filepath, 'rb') as f:
            data = f.read()

        w, h = 1400, 1100
        idx = 2
        while idx < len(data) - 9:
            if data[idx] == 0xFF:
                marker = data[idx+1]
                if marker in [0xC0, 0xC1, 0xC2]:
                    h, w = struct.unpack('>HH', data[idx+5:idx+9])
                    break
                length = struct.unpack('>H', data[idx+2:idx+4])[0]
                idx += 2 + length
            else:
                idx += 1

        obj_id = self.add_object(None)
        stream_dict = (
            f"<< /Type /XObject /Subtype /Image /Width {w} /Height {h} "
            f"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode "
            f"/Length {len(data)} >>\nstream\n"
        ).encode('latin1') + data + b"\nendstream"
        
        self.objects[obj_id - 1] = stream_dict
        self.images[name] = obj_id
        self.image_dims[name] = (w, h)
        return obj_id

    def add_page(self, stream_ops):
        clean_ops = clean_latin1(stream_ops)
        raw_stream = clean_ops.encode('latin1')
        compressed = zlib.compress(raw_stream)
        stream_id = self.add_object(
            f"<< /Length {len(compressed)} /Filter /FlateDecode >>\nstream\n".encode('latin1')
            + compressed
            + b"\nendstream"
        )
        self.pages.append(stream_id)

    def save(self, filepath):
        f_reg = self.add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>".encode('latin1'))
        f_bold = self.add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>".encode('latin1'))
        f_oblique = self.add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Oblique >>".encode('latin1'))

        xobj_dict_str = "<< " + " ".join(f"/Img_{name} {obj_id} 0 R" for name, obj_id in self.images.items()) + " >>"

        res_id = self.add_object(
            f"<< /Font << /F1 {f_reg} 0 R /F2 {f_bold} 0 R /F3 {f_oblique} 0 R >> "
            f"/XObject {xobj_dict_str} >>".encode('latin1')
        )

        pages_id = self.add_object(None)

        page_obj_ids = []
        for stream_id in self.pages:
            p_id = self.add_object(
                f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {PAGE_W:.2f} {PAGE_H:.2f}] "
                f"/Contents {stream_id} 0 R /Resources {res_id} 0 R >>".encode('latin1')
            )
            page_obj_ids.append(p_id)

        kids_str = " ".join(f"{pid} 0 R" for pid in page_obj_ids)
        self.objects[pages_id - 1] = f"<< /Type /Pages /Kids [{kids_str}] /Count {len(page_obj_ids)} >>".encode('latin1')

        cat_id = self.add_object(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode('latin1'))

        with open(filepath, 'wb') as f:
            f.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
            offsets = []
            for i, obj in enumerate(self.objects):
                offsets.append(f.tell())
                f.write(f"{i+1} 0 obj\n".encode('latin1'))
                f.write(obj)
                f.write(b"\nendobj\n")

            xref_pos = f.tell()
            f.write(f"xref\n0 {len(self.objects)+1}\n".encode('latin1'))
            f.write(b"0000000000 65535 f \n")
            for off in offsets:
                f.write(f"{off:010d} 00000 n \n".encode('latin1'))

            f.write(
                f"trailer\n<< /Size {len(self.objects)+1} /Root {cat_id} 0 R >>\n"
                f"startxref\n{xref_pos}\n%%EOF\n".encode('latin1')
            )
        print(f"Generated PDF: {filepath} ({os.path.getsize(filepath)} bytes)")

class PageCanvas:
    def __init__(self, page_num, total_pages=8, is_cover=False):
        self.page_num = page_num
        self.total_pages = total_pages
        self.is_cover = is_cover
        self.ops = []
        if not is_cover:
            self.draw_ikea_header()
            self.draw_ikea_footer()

    def add(self, s):
        self.ops.append(s)

    def draw_ikea_header(self):
        self.add("q\n")
        self.add("0.0 0.318 0.729 RG 2.5 w\n")
        self.add(f"36 {PAGE_H - 42:.2f} m {PAGE_W - 36:.2f} {PAGE_H - 42:.2f} l S\n")
        self.add("BT\n")
        self.add("/F2 16 Tf 0.05 0.05 0.08 rg\n")
        self.add(f"36 {PAGE_H - 36:.2f} Td (L\xdaA) Tj\n")
        self.add("/F1 9 Tf 0.35 0.35 0.38 rg\n")
        self.add("50 0 Td (Mascota Rob\xf3tica \xb7 Valeria+ / VIA+ \xb7 V14) Tj\n")
        self.add("ET\n")
        self.add("BT\n")
        self.add(f"/F2 9 Tf 0.2 0.2 0.2 rg\n")
        self.add(f"{PAGE_W - 95:.2f} {PAGE_H - 36:.2f} Td (P\xe1g. {self.page_num} de {self.total_pages}) Tj\n")
        self.add("ET\n")
        self.add("Q\n")

    def draw_ikea_footer(self):
        self.add("q\n")
        self.add("0.8 0.8 0.82 RG 0.75 w\n")
        self.add(f"36 32 m {PAGE_W - 36:.2f} 32 l S\n")
        self.add("BT\n")
        self.add("/F1 8 Tf 0.45 0.45 0.48 rg\n")
        self.add("36 20 Td (Manual de ensamble oficial \xb7 Proyecto L\xfaa V14 \xb7 USC / ACOPROS 2023-2027) Tj\n")
        self.add(f"{PAGE_W - 170:.2f} 20 Td (Frank Betances \xb7 Ender-3 S1 Pro) Tj\n")
        self.add("ET\n")
        self.add("Q\n")

    def draw_rect(self, x, y, w, h, fill_rgb=None, stroke_rgb=(0,0,0), stroke_w=1, rx=0):
        self.add("q\n")
        if fill_rgb:
            self.add(f"{fill_rgb[0]} {fill_rgb[1]} {fill_rgb[2]} rg\n")
        if stroke_rgb:
            self.add(f"{stroke_rgb[0]} {stroke_rgb[1]} {stroke_rgb[2]} RG {stroke_w} w\n")
        
        self.add(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re\n")
        if fill_rgb and stroke_rgb:
            self.add("B\n")
        elif fill_rgb:
            self.add("f\n")
        else:
            self.add("S\n")
        self.add("Q\n")

    def draw_circle(self, cx, cy, r, fill_rgb=None, stroke_rgb=(0,0,0), stroke_w=1):
        self.add("q\n")
        if fill_rgb:
            self.add(f"{fill_rgb[0]} {fill_rgb[1]} {fill_rgb[2]} rg\n")
        if stroke_rgb:
            self.add(f"{stroke_rgb[0]} {stroke_rgb[1]} {stroke_rgb[2]} RG {stroke_w} w\n")
        
        k = 0.5522847498 * r
        self.add(f"{cx + r:.2f} {cy:.2f} m\n")
        self.add(f"{cx + r:.2f} {cy + k:.2f} {cx + k:.2f} {cy + r:.2f} {cx:.2f} {cy + r:.2f} c\n")
        self.add(f"{cx - k:.2f} {cy + r:.2f} {cx - r:.2f} {cy + k:.2f} {cx - r:.2f} {cy:.2f} c\n")
        self.add(f"{cx - r:.2f} {cy - k:.2f} {cx - k:.2f} {cy - r:.2f} {cx:.2f} {cy - r:.2f} c\n")
        self.add(f"{cx + k:.2f} {cy - r:.2f} {cx + r:.2f} {cy - k:.2f} {cx + r:.2f} {cy:.2f} c\n")
        if fill_rgb and stroke_rgb:
            self.add("B\n")
        elif fill_rgb:
            self.add("f\n")
        else:
            self.add("S\n")
        self.add("Q\n")

    def draw_step_badge(self, step_num, x, y, r=16):
        self.draw_circle(x, y, r, fill_rgb=(0.08, 0.08, 0.10), stroke_rgb=None)
        self.add("q\nBT\n")
        self.add(f"/F2 {r*1.15:.1f} Tf 1 1 1 rg\n")
        tx = x - (4.5 if step_num < 10 else 8.5)
        ty = y - (r * 0.38)
        self.add(f"{tx:.2f} {ty:.2f} Td ({step_num}) Tj\n")
        self.add("ET\nQ\n")

    def draw_part_badge(self, letter, count_str, x, y, r=12):
        self.draw_circle(x, y, r, fill_rgb=(1, 1, 1), stroke_rgb=(0.08, 0.08, 0.1), stroke_w=1.8)
        self.add("q\nBT\n")
        self.add(f"/F2 {r*1.1:.1f} Tf 0.08 0.08 0.1 rg\n")
        self.add(f"{x - 4:.2f} {y - 4:.2f} Td ({letter}) Tj\n")
        if count_str:
            self.add(f"/F2 10 Tf 0.25 0.25 0.3 rg\n")
            self.add(f"16 0 Td ({count_str}) Tj\n")
        self.add("ET\nQ\n")

    def draw_image(self, img_name, x, y, w, h):
        self.add("q\n")
        self.add(f"{w:.2f} 0 0 {h:.2f} {x:.2f} {y:.2f} cm\n")
        self.add(f"/Img_{img_name} Do\n")
        self.add("Q\n")

    def draw_dashed_arrow(self, x1, y1, x2, y2, stroke_w=2):
        self.add("q\n")
        self.add("0.08 0.08 0.1 RG [4 3] 0 d\n")
        self.add(f"{stroke_w} w\n")
        self.add(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S\n")
        dx = x2 - x1
        dy = y2 - y1
        length = (dx*dx + dy*dy)**0.5
        if length > 0.1:
            ux, uy = dx/length, dy/length
            px, py = -uy, ux
            size = 6
            p1x, p1y = x2 - ux*size + px*(size*0.5), y2 - uy*size + py*(size*0.5)
            p2x, p2y = x2 - ux*size - px*(size*0.5), y2 - uy*size - py*(size*0.5)
            self.add("0.08 0.08 0.1 rg [] 0 d\n")
            self.add(f"{x2:.2f} {y2:.2f} m {p1x:.2f} {p1y:.2f} l {p2x:.2f} {p2y:.2f} l f\n")
        self.add("Q\n")

    def draw_text(self, text, x, y, font='/F1', size=10, rgb=(0,0,0)):
        self.add("q\nBT\n")
        self.add(f"{font} {size} Tf {rgb[0]} {rgb[1]} {rgb[2]} rg\n")
        clean = clean_latin1(text).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        self.add(f"{x:.2f} {y:.2f} Td ({clean}) Tj\n")
        self.add("ET\nQ\n")

    def draw_alert_box(self, x, y, w, h, title, lines, color_rgb=(0.95, 0.45, 0.15)):
        self.draw_rect(x, y, w, h, fill_rgb=(0.98, 0.98, 0.99), stroke_rgb=(0.85, 0.85, 0.88), stroke_w=1)
        self.draw_rect(x, y, 6, h, fill_rgb=color_rgb, stroke_rgb=None)
        self.draw_text(title, x + 14, y + h - 16, font='/F2', size=9.5, rgb=color_rgb)
        cur_y = y + h - 28
        for line in lines:
            self.draw_text(line, x + 14, cur_y, font='/F1', size=8, rgb=(0.25, 0.25, 0.28))
            cur_y -= 11

    def get_stream(self):
        return "".join(self.ops)

def build_manual():
    pdf = PdfWriter()
    
    diagram_files = {
        'cover': 'mascot_full_cover.jpg',
        'overview': 'parts_overview_plate.jpg',
        'step1': 'step1_inserts.jpg',
        'step2': 'step2_collar.jpg',
        'step3': 'step3_pcb_thread.jpg',
        'step4': 'step4_head_halves.jpg',
        'step5': 'step5_head_accessories.jpg',
        'step6': 'step6_chest_emblem.jpg',
        'step7': 'step7_battery_backpack.jpg',
        'step8': 'step8_limbs.jpg',
        'step9': 'step9_chin_port.jpg',
        'step10': 'step10_final_assembly.jpg',
    }
    for name, filename in diagram_files.items():
        path = os.path.join(DIAGRAMS_DIR, filename)
        pdf.load_image(name, path)

    # PÁGINA 1: PORTADA OFICIAL IKEA
    p1 = PageCanvas(1, 8, is_cover=True)
    p1.draw_rect(36, PAGE_H - 95, 140, 48, fill_rgb=(0.0, 0.318, 0.729))
    p1.draw_text("IKEA", 48, PAGE_H - 82, font='/F2', size=34, rgb=(1.0, 0.855, 0.102))
    p1.draw_text("DESIGN & ASSEMBLY", 188, PAGE_H - 66, font='/F2', size=11, rgb=(0.1, 0.1, 0.1))
    p1.draw_text("Technical Robotics Collection \xb7 Fase 3 USC", 188, PAGE_H - 80, font='/F1', size=9, rgb=(0.4, 0.4, 0.4))

    p1.draw_text("L\xdaA", 36, PAGE_H - 165, font='/F2', size=58, rgb=(0.05, 0.05, 0.08))
    p1.draw_text("Manual de Ensamble F\xedsico Oficial \xb7 20 Piezas STL", 36, PAGE_H - 186, font='/F2', size=14, rgb=(0.0, 0.318, 0.729))
    p1.draw_text("Ender-3 S1 Pro \xb7 Boquilla 0.4 mm \xb7 Maqueta Cl\xednica Pedi\xe1trica Valeria+ / VIA+", 36, PAGE_H - 202, font='/F1', size=10, rgb=(0.35, 0.35, 0.38))

    p1.draw_rect(36, 215, PAGE_W - 72, 405, fill_rgb=(0.99, 0.99, 1.0), stroke_rgb=(0.88, 0.88, 0.9), stroke_w=1)
    p1.draw_image('cover', 46, 220, PAGE_W - 92, 395)

    p1.draw_rect(36, 42, 250, 155, fill_rgb=(0.97, 0.98, 0.99), stroke_rgb=(0.82, 0.85, 0.88), stroke_w=1)
    p1.draw_rect(36, 172, 250, 25, fill_rgb=(0.0, 0.318, 0.729))
    p1.draw_text("HERRAMIENTAS REQUERIDAS", 46, 180, font='/F2', size=9.5, rgb=(1, 1, 1))
    p1.draw_text("[OK] Soldador fino regulado a 200 \xb0C (insertos)", 46, 154, font='/F1', size=8.5, rgb=(0.15, 0.15, 0.15))
    p1.draw_text("[OK] Destornillador Phillips / Plano M2", 46, 137, font='/F1', size=8.5, rgb=(0.15, 0.15, 0.15))
    p1.draw_text("[OK] Cianoacrilato de viscosidad media", 46, 120, font='/F1', size=8.5, rgb=(0.15, 0.15, 0.15))
    p1.draw_text("[OK] Cinta de espuma doble cara (bater\xeda)", 46, 103, font='/F1', size=8.5, rgb=(0.15, 0.15, 0.15))
    p1.draw_text("[NO] Martillos, alicates o llaves inglesas", 46, 75, font='/F2', size=8.5, rgb=(0.75, 0.1, 0.1))
    p1.draw_text("El modelo est\xe1 dise\xf1ado para tolerancias finas FDM.", 46, 58, font='/F1', size=7.5, rgb=(0.4, 0.4, 0.4))

    p1.draw_rect(300, 42, PAGE_W - 336, 155, fill_rgb=(0.97, 0.98, 0.99), stroke_rgb=(0.82, 0.85, 0.88), stroke_w=1)
    p1.draw_rect(300, 172, PAGE_W - 336, 25, fill_rgb=(0.08, 0.08, 0.1))
    p1.draw_text("REGLAS CLAVE DE MONTAJE", 310, 180, font='/F2', size=9.5, rgb=(1, 1, 1))
    p1.draw_text("1. Ensayo en seco: Comprueba todas las uniones", 310, 154, font='/F1', size=8.5, rgb=(0.15, 0.15, 0.15))
    p1.draw_text("   antes de aplicar cianoacrilato definitivo.", 310, 142, font='/F1', size=8.5, rgb=(0.15, 0.15, 0.15))
    p1.draw_text("2. Cuello m\xf3vil: El collar y la cabeza NO van pegados", 310, 126, font='/F1', size=8.5, rgb=(0.15, 0.15, 0.15))
    p1.draw_text("   al cuerpo para permitir giro y servicio t\xe9cnico.", 310, 114, font='/F1', size=8.5, rgb=(0.15, 0.15, 0.15))
    p1.draw_text("3. Retenci\xf3n positiva: La rosca M55 aprieta a mano.", 310, 98, font='/F1', size=8.5, rgb=(0.15, 0.15, 0.15))
    p1.draw_text("Soporte: github.com/FrankBetances/proyecto-lua", 310, 68, font='/F2', size=8, rgb=(0.0, 0.318, 0.729))
    p1.draw_text("Iteraci\xf3n V14 \xb7 Septiembre 2026 \xb7 Santiago de Compostela", 310, 55, font='/F1', size=7.5, rgb=(0.4, 0.4, 0.4))

    pdf.add_page(p1.get_stream())

    # PÁGINA 2: INVENTARIO DE PIEZAS
    p2 = PageCanvas(2, 8)
    p2.draw_text("INVENTARIO OFICIAL DE COMPONENTES", 36, PAGE_H - 65, font='/F2', size=16, rgb=(0.05, 0.05, 0.08))
    p2.draw_text("Comprueba que tienes las 20 piezas impresas y la torniller\xeda antes de iniciar el montaje:", 36, PAGE_H - 80, font='/F1', size=9.5, rgb=(0.35, 0.35, 0.38))

    p2.draw_rect(36, PAGE_H - 330, PAGE_W - 72, 235, fill_rgb=(0.99, 0.99, 1.0), stroke_rgb=(0.85, 0.85, 0.88), stroke_w=1)
    p2.draw_image('overview', 44, PAGE_H - 325, PAGE_W - 88, 225)

    parts_col1 = [
        ("A", "cuerpo.stl", "Tronco principal (alojamiento bater\xeda)", "1x", "Blanco"),
        ("B", "cabeza_frente.stl", "Cara frontal y rosca M55", "1x", "Blanco"),
        ("C", "cabeza_dorso.stl", "C\xfapula con 2 espigas centrado", "1x", "Blanco"),
        ("D", "brazo_izq.stl", "Brazo izquierdo (pu\xf1o turquesa)", "1x", "Bicolor"),
        ("E", "brazo_der.stl", "Brazo derecho (pu\xf1o turquesa)", "1x", "Bicolor"),
        ("F", "pierna_izq.stl", "Pierna izquierda (bota turquesa)", "1x", "Bicolor"),
        ("G", "pierna_der.stl", "Pierna derecha (bota turquesa)", "1x", "Bicolor"),
        ("H", "oreja_izq.stl", "Oreja izquierda con espiga", "1x", "Turquesa"),
        ("I", "oreja_der.stl", "Oreja derecha con espiga", "1x", "Turquesa"),
        ("J", "collar.stl", "Anillo de cuello con muesca USB-C", "1x", "Turquesa"),
    ]
    parts_col2 = [
        ("K", "mochila.stl", "Tapa trasera con 2 taladros M2", "1x", "Turquesa"),
        ("L", "boton.stl", "Dial est\xe9tico sien derecha", "1x", "Turquesa"),
        ("M", "emblema.stl", "Aro de escudo en el pecho (\xd822 mm)", "1x", "Turquesa"),
        ("N", "logo.stl", "Silueta relieve L\xfaa (blanco)", "1x", "Blanco"),
        ("O", "aro_visor.stl", "Marco frontal protector de pantalla", "1x", "Negro"),
        ("P", "anillo_placa.stl", "Tuerca M55 de retenci\xf3n PCB", "1x", "Blanco"),
        ("Q", "cartucho.stl", "Cuna deslizante celda litio", "1x", "Blanco"),
        ("R", "pulsadores.stl", "Embellecedor botones bajo barbilla", "1x", "Negro"),
        ("S", "Insertos lat\xf3n M2", "Insertos roscados termofusibles", "2x", "Lat\xf3n"),
        ("T", "Tornillos M2\xd78 mm", "Tornillos cabeza avellanada/cil\xedndrica", "2x", "Acero"),
    ]

    def draw_parts_table(col_parts, x_start, y_start):
        y = y_start
        for letter, fname, desc, qty, col in col_parts:
            p2.draw_part_badge(letter, "", x_start + 12, y + 8, r=9)
            p2.draw_text(qty, x_start + 28, y + 5, font='/F2', size=9, rgb=(0.0, 0.318, 0.729))
            p2.draw_text(fname, x_start + 50, y + 8, font='/F2', size=8.5, rgb=(0.1, 0.1, 0.1))
            p2.draw_text(f"{desc} \xb7 {col}", x_start + 50, y - 1, font='/F1', size=7.2, rgb=(0.4, 0.4, 0.45))
            p2.add(f"q 0.9 0.9 0.92 RG 0.5 w {x_start} {y - 5:.2f} m {x_start + 245} {y - 5:.2f} l S Q\n")
            y -= 25

    table_y = PAGE_H - 365
    draw_parts_table(parts_col1, 36, table_y)
    draw_parts_table(parts_col2, 305, table_y)

    p2.draw_alert_box(36, 48, PAGE_W - 72, 58,
                      "PROBETAS PREVIAS DE CALIBRACION (No van en el muneco montado)",
                      ["\xb7 testigo_placa.stl: Comprueba contorno de pantalla y ranura USB-C antes de imprimir la cabeza.",
                       "\xb7 testigo_rosca.stl: Barril de 12 mm para validar ajuste suave del anillo_placa M55."],
                      color_rgb=(0.0, 0.45, 0.75))

    pdf.add_page(p2.get_stream())

    # PÁGINA 3: PASOS 1 & 2
    p3 = PageCanvas(3, 8)
    p3.draw_step_badge(1, 55, PAGE_H - 75)
    p3.draw_text("INSERTOS TERMICOS M2 EN LA ESPALDA", 82, PAGE_H - 72, font='/F2', size=13, rgb=(0.05, 0.05, 0.08))
    p3.draw_part_badge("A", "1x", 360, PAGE_H - 72)
    p3.draw_part_badge("S", "2x", 425, PAGE_H - 72)

    p3.draw_rect(36, PAGE_H - 425, 335, 330, fill_rgb=(0.99, 0.99, 1.0), stroke_rgb=(0.88, 0.88, 0.9), stroke_w=1)
    p3.draw_image('step1', 40, PAGE_H - 420, 327, 320)
    p3.draw_dashed_arrow(182, PAGE_H - 225, 142, PAGE_H - 248)
    p3.draw_dashed_arrow(238, PAGE_H - 245, 198, PAGE_H - 268)

    p3.draw_text("1. Apoya el tronco cuerpo.stl boca abajo sobre la mesa.", 385, PAGE_H - 110, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p3.draw_text("2. Coloca un casquillo de laton M2 sobre cada uno de los", 385, PAGE_H - 124, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p3.draw_text("   dos orificios a los lados de la bahia dorsal.", 385, PAGE_H - 136, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p3.draw_text("3. Aplica calor con la punta fina del soldador (~200 \xb0C).", 385, PAGE_H - 150, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p3.draw_text("4. El inserto debe descender por peso propio, NUNCA a golpes.", 385, PAGE_H - 164, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p3.draw_text("5. Dejar enfriar 2 minutos enrasado a nivel de la pared.", 385, PAGE_H - 178, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p3.draw_alert_box(385, PAGE_H - 265, 175, 78, "TEMPERATURA ~200 \xb0C",
                      ["\xb7 No calentar en exceso el PLA.",
                       "\xb7 Debe quedar al ras de la cara.",
                       "\xb7 No obstruir la rosca interior."],
                      color_rgb=(0.85, 0.35, 0.1))

    p3.add(f"q 0.85 0.85 0.88 RG 1 w 36 {PAGE_H - 440:.2f} m {PAGE_W - 36:.2f} {PAGE_H - 440:.2f} l S Q\n")

    p3.draw_step_badge(2, 55, PAGE_H - 475)
    p3.draw_text("DESLIZAR EL COLLAR AL CUELLO", 82, PAGE_H - 472, font='/F2', size=13, rgb=(0.05, 0.05, 0.08))
    p3.draw_part_badge("A", "1x", 360, PAGE_H - 472)
    p3.draw_part_badge("J", "1x", 425, PAGE_H - 472)

    p3.draw_rect(36, 45, 335, 370, fill_rgb=(0.99, 0.99, 1.0), stroke_rgb=(0.88, 0.88, 0.9), stroke_w=1)
    p3.draw_image('step2', 40, 50, 327, 360)
    p3.draw_dashed_arrow(202, 345, 202, 275, stroke_w=2.5)

    p3.draw_text("1. Toma el collar turquesa collar.stl.", 385, PAGE_H - 505, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p3.draw_text("2. Orienta la MUESCA PASANTE hacia el FRENTE", 385, PAGE_H - 519, font='/F2', size=8.5, rgb=(0.0, 0.318, 0.729))
    p3.draw_text("   (coincidiendo con la ranura USB-C del pecho).", 385, PAGE_H - 531, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p3.draw_text("3. Deslizalo suavemente por la espiga del cuello.", 385, PAGE_H - 545, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p3.draw_text("4. NO USAR PEGAMENTO: el collar debe rotar libre.", 385, PAGE_H - 559, font='/F2', size=8.5, rgb=(0.8, 0.1, 0.1))

    p3.draw_alert_box(385, PAGE_H - 680, 175, 105, "[!] REGLA CRITICA DE MONTAJE",
                      ["\xb7 Colocar el collar ANTES de montar",
                       "  o encolar la cabeza.",
                       "\xb7 Si se monta la cabeza primero,",
                       "  el collar NO podra introducirse.",
                       "\xb7 Muesca al frente para cable USB-C."],
                      color_rgb=(0.75, 0.1, 0.1))

    pdf.add_page(p3.get_stream())

    # PÁGINA 4: PASOS 3 & 4
    p4 = PageCanvas(4, 8)
    p4.draw_step_badge(3, 55, PAGE_H - 75)
    p4.draw_text("ELECTRONICA Y RETENCION POR ROSCA M55", 82, PAGE_H - 72, font='/F2', size=13, rgb=(0.05, 0.05, 0.08))
    p4.draw_part_badge("B", "1x", 370, PAGE_H - 72)
    p4.draw_part_badge("P", "1x", 425, PAGE_H - 72)

    p4.draw_rect(36, PAGE_H - 425, 335, 330, fill_rgb=(0.99, 0.99, 1.0), stroke_rgb=(0.88, 0.88, 0.9), stroke_w=1)
    p4.draw_image('step3', 40, PAGE_H - 420, 327, 320)
    p4.draw_dashed_arrow(202, PAGE_H - 185, 202, PAGE_H - 235)

    p4.draw_text("1. Introduce la placa ESP32-S3 por detras de cabeza_frente.", 385, PAGE_H - 110, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p4.draw_text("2. Apoya la pantalla IPS entre las 4 costillas interiores.", 385, PAGE_H - 124, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p4.draw_text("3. Conectores USB-C orientados hacia la barbilla (abajo).", 385, PAGE_H - 138, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p4.draw_text("4. Enrosca el anillo_placa.stl en el barril M55 en sentido", 385, PAGE_H - 152, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p4.draw_text("   horario unicamente a mano con dos dedos.", 385, PAGE_H - 164, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p4.draw_alert_box(385, PAGE_H - 265, 175, 88, "-> APRIETE MANUAL SUAVE",
                      ["\xb7 Absorbe holguras entre 8 y 16 mm.",
                       "\xb7 NO usar herramientas ni alicates.",
                       "\xb7 Deja el centro libre para cable bateria.",
                       "\xb7 Si roza, repasar hilos con cepillo."],
                      color_rgb=(0.0, 0.45, 0.75))

    p4.add(f"q 0.85 0.85 0.88 RG 1 w 36 {PAGE_H - 440:.2f} m {PAGE_W - 36:.2f} {PAGE_H - 440:.2f} l S Q\n")

    p4.draw_step_badge(4, 55, PAGE_H - 475)
    p4.draw_text("CIERRE Y SELLADO DEL CASCO", 82, PAGE_H - 472, font='/F2', size=13, rgb=(0.05, 0.05, 0.08))
    p4.draw_part_badge("B", "1x", 360, PAGE_H - 472)
    p4.draw_part_badge("C", "1x", 425, PAGE_H - 472)

    p4.draw_rect(36, 45, 335, 370, fill_rgb=(0.99, 0.99, 1.0), stroke_rgb=(0.88, 0.88, 0.9), stroke_w=1)
    p4.draw_image('step4', 40, 50, 327, 360)
    p4.draw_dashed_arrow(202, 335, 202, 230)

    p4.draw_text("1. Ensayo en seco: Comprueba que las 2 espigas de centrado", 385, PAGE_H - 505, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p4.draw_text("   de cabeza_dorso calzan sin resistencia en cabeza_frente.", 385, PAGE_H - 517, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p4.draw_text("2. Aplica un cordon fino de cianoacrilato en el rebaje perimetral.", 385, PAGE_H - 533, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p4.draw_text("3. Presiona firmemente ambas mitades durante 45-60 segundos.", 385, PAGE_H - 547, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p4.draw_text("4. Dejar reposar 5 minutos para curado completo.", 385, PAGE_H - 561, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))

    p4.draw_alert_box(385, PAGE_H - 680, 175, 105, "[!] ALINEACION OBLIGATORIA",
                      ["\xb7 Las 2 espigas impiden que el casco",
                       "  quede girado al encolar.",
                       "\xb7 Comprobar que el cable de bateria",
                       "  asoma por la boca del cuello.",
                       "\xb7 Una vez pegado no debe reabrirse."],
                      color_rgb=(0.85, 0.35, 0.1))

    pdf.add_page(p4.get_stream())

    # PÁGINA 5: PASOS 5 & 6
    p5 = PageCanvas(5, 8)
    p5.draw_step_badge(5, 55, PAGE_H - 75)
    p5.draw_text("ACCESORIOS DEL CASCO (VISOR, OREJAS, BOTON)", 82, PAGE_H - 72, font='/F2', size=13, rgb=(0.05, 0.05, 0.08))
    p5.draw_part_badge("O", "1x", 370, PAGE_H - 72)
    p5.draw_part_badge("H,I", "2x", 420, PAGE_H - 72)
    p5.draw_part_badge("L", "1x", 480, PAGE_H - 72)

    p5.draw_rect(36, PAGE_H - 425, 335, 330, fill_rgb=(0.99, 0.99, 1.0), stroke_rgb=(0.88, 0.88, 0.9), stroke_w=1)
    p5.draw_image('step5', 40, PAGE_H - 420, 327, 320)
    p5.draw_dashed_arrow(145, PAGE_H - 230, 175, PAGE_H - 260)
    p5.draw_dashed_arrow(170, PAGE_H - 120, 170, PAGE_H - 150)
    p5.draw_dashed_arrow(235, PAGE_H - 120, 235, PAGE_H - 150)

    p5.draw_text("1. Marco del Visor aro_visor.stl (Negro): Gota minima de", 385, PAGE_H - 110, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p5.draw_text("   adhesivo en el reverso y pegar enmarcando la pantalla.", 385, PAGE_H - 122, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p5.draw_text("2. Orejas oreja_izq / oreja_der.stl (Turquesa): Adhesivo en", 385, PAGE_H - 138, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p5.draw_text("   las espigas e insertar en las ranuras superiores.", 385, PAGE_H - 150, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p5.draw_text("3. Boton de Sien boton.stl (Turquesa): Pegar el dial de 3", 385, PAGE_H - 166, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p5.draw_text("   surcos concentricos en el rebaje de la sien derecha.", 385, PAGE_H - 178, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p5.draw_alert_box(385, PAGE_H - 265, 175, 75, "DETALLE ESTETICO",
                      ["\xb7 El boton de sien es un dial estetico.",
                       "\xb7 Las orejas encajan con espiga mecanica.",
                       "\xb7 El aro oculta la junta del cristal."],
                      color_rgb=(0.0, 0.45, 0.75))

    p5.add(f"q 0.85 0.85 0.88 RG 1 w 36 {PAGE_H - 440:.2f} m {PAGE_W - 36:.2f} {PAGE_H - 440:.2f} l S Q\n")

    p5.draw_step_badge(6, 55, PAGE_H - 475)
    p5.draw_text("EMBLEMA Y SILUETA DEL LOGO EN EL PECHO", 82, PAGE_H - 472, font='/F2', size=13, rgb=(0.05, 0.05, 0.08))
    p5.draw_part_badge("M", "1x", 370, PAGE_H - 472)
    p5.draw_part_badge("N", "1x", 425, PAGE_H - 472)
    p5.draw_part_badge("A", "1x", 480, PAGE_H - 472)

    p5.draw_rect(36, 45, 335, 370, fill_rgb=(0.99, 0.99, 1.0), stroke_rgb=(0.88, 0.88, 0.9), stroke_w=1)
    p5.draw_image('step6', 40, 50, 327, 360)
    p5.draw_dashed_arrow(140, 230, 185, 230)

    p5.draw_text("1. Subensamble del Logo: Aplica una microgota de", 385, PAGE_H - 505, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p5.draw_text("   cianoacrilato en el rebaje interior de emblema.stl.", 385, PAGE_H - 517, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p5.draw_text("2. Encaja la pastilla logo.stl (silueta blanca en relieve).", 385, PAGE_H - 533, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p5.draw_text("3. Fijacion al Torso: Pega el conjunto en el asiento esferico", 385, PAGE_H - 549, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p5.draw_text("   del pecho de cuerpo.stl, exactamente centrado a x = 0.", 385, PAGE_H - 561, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))

    p5.draw_alert_box(385, PAGE_H - 680, 175, 105, "* CENTRADO V14 (x = 0)",
                      ["\xb7 El modelo V14 adelanta el asiento",
                       "  +1,9 mm y lo centra a x = 0.",
                       "\xb7 Asienta al ras de la curva del pecho.",
                       "\xb7 Asegurar que la silueta de la gata",
                       "  apunta erguida hacia arriba."],
                      color_rgb=(0.15, 0.65, 0.35))

    pdf.add_page(p5.get_stream())

    # PÁGINA 6: PASOS 7 & 8
    p6 = PageCanvas(6, 8)
    p6.draw_step_badge(7, 55, PAGE_H - 75)
    p6.draw_text("BATERIA DE LITIO Y FIJACION DE MOCHILA", 82, PAGE_H - 72, font='/F2', size=13, rgb=(0.05, 0.05, 0.08))
    p6.draw_part_badge("Q", "1x", 370, PAGE_H - 72)
    p6.draw_part_badge("K", "1x", 420, PAGE_H - 72)
    p6.draw_part_badge("T", "2x", 475, PAGE_H - 72)

    p6.draw_rect(36, PAGE_H - 425, 335, 330, fill_rgb=(0.99, 0.99, 1.0), stroke_rgb=(0.88, 0.88, 0.9), stroke_w=1)
    p6.draw_image('step7', 40, PAGE_H - 420, 327, 320)
    p6.draw_dashed_arrow(120, PAGE_H - 240, 160, PAGE_H - 240)
    p6.draw_dashed_arrow(160, PAGE_H - 265, 205, PAGE_H - 265)

    p6.draw_text("1. Fija la celda de litio con cinta doble cara en cartucho.stl.", 385, PAGE_H - 110, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p6.draw_text("2. Desliza el cartucho dentro de la bahia dorsal del cuerpo.", 385, PAGE_H - 124, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p6.draw_text("3. Conecta el cable MX1.25 a la placa a traves del cuello.", 385, PAGE_H - 138, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p6.draw_text("4. Coloca mochila.stl y atornilla los 2 tornillos M2x8 mm en", 385, PAGE_H - 152, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p6.draw_text("   los insertos de laton fijados en el Paso 1.", 385, PAGE_H - 164, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p6.draw_alert_box(385, PAGE_H - 265, 175, 88, "[M2] DOBLE TORNILLO M2",
                      ["\xb7 El doble tornillo impide el pivoteo.",
                       "\xb7 Protege la bateria frente a ninos.",
                       "\xb7 No apretar en exceso: el laton",
                       "  ofrece retencion mecanica firme."],
                      color_rgb=(0.0, 0.45, 0.75))

    p6.add(f"q 0.85 0.85 0.88 RG 1 w 36 {PAGE_H - 440:.2f} m {PAGE_W - 36:.2f} {PAGE_H - 440:.2f} l S Q\n")

    p6.draw_step_badge(8, 55, PAGE_H - 475)
    p6.draw_text("EXTREMIDADES BICOLOR (BRAZOS Y PIERNAS)", 82, PAGE_H - 472, font='/F2', size=13, rgb=(0.05, 0.05, 0.08))
    p6.draw_part_badge("D,E", "2x", 360, PAGE_H - 472)
    p6.draw_part_badge("F,G", "2x", 425, PAGE_H - 472)

    p6.draw_rect(36, 45, 335, 370, fill_rgb=(0.99, 0.99, 1.0), stroke_rgb=(0.88, 0.88, 0.9), stroke_w=1)
    p6.draw_image('step8', 40, 50, 327, 360)
    p6.draw_dashed_arrow(105, 275, 155, 240)
    p6.draw_dashed_arrow(295, 275, 245, 240)
    p6.draw_dashed_arrow(115, 130, 160, 155)
    p6.draw_dashed_arrow(285, 130, 240, 155)

    p6.draw_text("1. Orientacion: Punos y botas turquesas miran hacia ABAJO.", 385, PAGE_H - 505, font='/F2', size=8.5, rgb=(0.0, 0.318, 0.729))
    p6.draw_text("2. Brazos: Aplica cianoacrilato en la espiga y cara plana de", 385, PAGE_H - 521, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p6.draw_text("   brazo_izq / brazo_der e inserta en cajera de hombro.", 385, PAGE_H - 533, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p6.draw_text("3. Piernas: Aplica cianoacrilato e inserta pierna_izq / der", 385, PAGE_H - 549, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p6.draw_text("   en las cajeras inferiores. Presiona cada miembro 20 s.", 385, PAGE_H - 561, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p6.draw_text("4. Dejar reposar tumbado boca arriba 10 minutos.", 385, PAGE_H - 575, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))

    p6.draw_alert_box(385, PAGE_H - 680, 175, 95, "[Adhesivo] FIJACION CON ADHESIVO",
                      ["\xb7 Las cajeras llevan holgura +0,15 mm",
                       "  calculada para cianoacrilato.",
                       "\xb7 No dejar sueltas: son criticas",
                       "  para la estabilidad de la figura.",
                       "\xb7 Curado quimico completo: 10 min."],
                      color_rgb=(0.85, 0.35, 0.1))

    pdf.add_page(p6.get_stream())

    # PÁGINA 7: PASOS 9 & 10
    p7 = PageCanvas(7, 8)
    p7.draw_step_badge(9, 55, PAGE_H - 75)
    p7.draw_text("RANURA DE CARGA USB-C Y PULSADORES", 82, PAGE_H - 72, font='/F2', size=13, rgb=(0.05, 0.05, 0.08))
    p7.draw_part_badge("R", "1x", 370, PAGE_H - 72)

    p7.draw_rect(36, PAGE_H - 425, 335, 330, fill_rgb=(0.99, 0.99, 1.0), stroke_rgb=(0.88, 0.88, 0.9), stroke_w=1)
    p7.draw_image('step9', 40, PAGE_H - 420, 327, 320)
    p7.draw_dashed_arrow(180, PAGE_H - 180, 205, PAGE_H - 230)

    p7.draw_text("1. Acceso de Carga: La ranura bajo la barbilla y la muesca", 385, PAGE_H - 110, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p7.draw_text("   del collar permiten conectar directamente un cable USB-C.", 385, PAGE_H - 122, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p7.draw_text("2. Pieza pulsadores.stl (opcional segun placa): Se coloca", 385, PAGE_H - 138, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p7.draw_text("   bajo barbilla para guiar el conector y proteger REST y BOOT.", 385, PAGE_H - 150, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p7.draw_alert_box(385, PAGE_H - 265, 175, 85, "[USB] CARGA SIN DESMONTAR",
                      ["\xb7 Ranura de 16 mm 100% despejada.",
                       "\xb7 No requiere abrir el casco.",
                       "\xb7 Agujero para boton reset con aguja.",
                       "\xb7 Tecla activa BOOT para interaccion."],
                      color_rgb=(0.0, 0.45, 0.75))

    p7.add(f"q 0.85 0.85 0.88 RG 1 w 36 {PAGE_H - 440:.2f} m {PAGE_W - 36:.2f} {PAGE_H - 440:.2f} l S Q\n")

    p7.draw_step_badge(10, 55, PAGE_H - 475)
    p7.draw_text("ACOPLE FINAL DEL CASCO (GRAVEDAD / GIRO)", 82, PAGE_H - 472, font='/F2', size=13, rgb=(0.05, 0.05, 0.08))

    p7.draw_rect(36, 45, 335, 370, fill_rgb=(0.99, 0.99, 1.0), stroke_rgb=(0.88, 0.88, 0.9), stroke_w=1)
    p7.draw_image('step10', 40, 50, 327, 360)
    p7.draw_dashed_arrow(202, 335, 202, 240, stroke_w=2.5)

    p7.draw_text("1. El casco NO SE PEGA al cuerpo.", 385, PAGE_H - 505, font='/F2', size=9, rgb=(0.8, 0.1, 0.1))
    p7.draw_text("2. Desciende el casco montado sobre la espiga del cuello.", 385, PAGE_H - 521, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p7.draw_text("3. Encaje por gravedad y friccion: la cabeza gira 360\xb0 para", 385, PAGE_H - 535, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p7.draw_text("   orientar la mirada hacia el paciente pediatrico.", 385, PAGE_H - 547, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p7.draw_text("4. Permite retirar el casco tirando hacia arriba en cualquier", 385, PAGE_H - 561, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))
    p7.draw_text("   momento para inspeccionar la electronica sin romper nada.", 385, PAGE_H - 573, font='/F1', size=8.5, rgb=(0.2, 0.2, 0.2))

    p7.draw_alert_box(385, PAGE_H - 680, 175, 95, "* LUA TERMINADA!",
                      ["\xb7 El centro de gravedad en la base",
                       "  garantiza pose sentada estable.",
                       "\xb7 Cabeza articulada y orientable.",
                       "\xb7 Modelo listo para evaluacion clinica."],
                      color_rgb=(0.15, 0.65, 0.35))

    pdf.add_page(p7.get_stream())

    # PÁGINA 8: DIRECTRICES TÉCNICAS Y SEGURIDAD
    p8 = PageCanvas(8, 8)
    p8.draw_text("GUIA TECNICA DE TOLERANCIAS Y SEGURIDAD PEDIATRICA", 36, PAGE_H - 65, font='/F2', size=15, rgb=(0.05, 0.05, 0.08))
    p8.draw_text("Valeria+ / VIA+ \xb7 Dispositivo Medico Software (SaMD Clase IIa / MDR 2017/745)", 36, PAGE_H - 80, font='/F1', size=9, rgb=(0.35, 0.35, 0.38))

    p8.draw_rect(36, PAGE_H - 325, PAGE_W - 72, 230, fill_rgb=(0.99, 0.99, 1.0), stroke_rgb=(0.85, 0.85, 0.88), stroke_w=1)
    p8.draw_rect(36, PAGE_H - 120, PAGE_W - 72, 25, fill_rgb=(0.0, 0.318, 0.729))
    p8.draw_text("ZONA MECANICA", 48, PAGE_H - 105, font='/F2', size=8.5, rgb=(1, 1, 1))
    p8.draw_text("TOLERANCIA CAD", 175, PAGE_H - 105, font='/F2', size=8.5, rgb=(1, 1, 1))
    p8.draw_text("REGLA Y RECOMENDACION DE TALLER", 280, PAGE_H - 105, font='/F2', size=8.5, rgb=(1, 1, 1))

    tol_rows = [
        ("Rosca M55 (anillo_placa)", "\xb1 0.30 mm", "Roscado a mano con alas de apriete. Repasar hilos con cepillo."),
        ("Espigas centrado casco", "\xd8 2.4 mm", "Alineacion forzosa. Si roza, pasar lija fina al 400 por la espiga."),
        ("Cajeras de extremidades", "+ 0.15 mm", "Calculada para cianoacrilato. No dejar sin encolar (riesgo caida)."),
        ("Insertos de laton M2", "\xd8 3.2 mm", "Insercion termica a ~200 \xb0C. Prohibido insertar en frio a golpes."),
        ("Tornillos mochila trasera", "M2 \xd7 8 mm", "Doble tornillo fijado a insertos. Evita giro y protege celda de litio."),
        ("Ranura de conectores", "16.0 \xd7 8.0 mm", "Despejada bajo barbilla. Permite carga USB-C sin abrir el casco."),
        ("Cuello y collarin", "\xd8 22.0 mm", "Encaje deslizante holgado. NO aplicar pegamento."),
    ]
    cur_y = PAGE_H - 145
    for area, tol, rec in tol_rows:
        p8.draw_text(area, 48, cur_y + 3, font='/F2', size=8, rgb=(0.1, 0.1, 0.1))
        p8.draw_text(tol, 175, cur_y + 3, font='/F2', size=8, rgb=(0.0, 0.318, 0.729))
        p8.draw_text(rec, 280, cur_y + 3, font='/F1', size=7.5, rgb=(0.25, 0.25, 0.28))
        p8.add(f"q 0.9 0.9 0.92 RG 0.5 w 36 {cur_y - 4:.2f} m {PAGE_W - 36:.2f} {cur_y - 4:.2f} l S Q\n")
        cur_y -= 25

    p8.draw_alert_box(36, PAGE_H - 510, PAGE_W - 72, 165,
                      "PROTOCOLO DE SEGURIDAD PEDIATRICA (MDR 2017/745 / EVALUACION CLINICA)",
                      ["\xb7 1. Proteccion de Bateria: La celda de litio esta confinada en el cartucho interior con doble tornillo M2.",
                       "     Ningun nino puede acceder a la bateria sin herramienta especifica.",
                       "\xb7 2. Cero Piezas Sueltas: Todas las extremidades, orejas y accesorios deben fijarse con cianoacrilato",
                       "     de grado profesional para evitar riesgo de atragantamiento.",
                       "\xb7 3. Bordes Redondeados: Todos los radios del modelo (R > 2 mm) eliminan aristas vivas en el contacto.",
                       "\xb7 4. Biocompatibilidad del PLA: Emplear filamento PLA virgen certificado sin aditivos toxicos.",
                       "\xb7 5. Limpieza y Desinfeccion: Limpiar con toallitas con alcohol isopropilico al 70% entre sesiones clinicas."],
                      color_rgb=(0.85, 0.35, 0.1))

    p8.draw_rect(36, 45, PAGE_W - 72, 85, fill_rgb=(0.97, 0.98, 0.99), stroke_rgb=(0.85, 0.85, 0.88), stroke_w=1)
    p8.draw_text("PROYECTO LUA \xb7 VALERIA+ / VIA+ \xb7 TESIS DOCTORAL USC 2023-2027", 48, 112, font='/F2', size=9, rgb=(0.0, 0.318, 0.729))
    p8.draw_text("Investigador Principal: Dr. Frank Alberto Betances Reinoso \xb7 ACOPROS / USC", 48, 98, font='/F1', size=8, rgb=(0.2, 0.2, 0.2))
    p8.draw_text("Repositorio GitHub: https://github.com/FrankBetances/proyecto-lua (Rama 'manual')", 48, 84, font='/F1', size=8, rgb=(0.2, 0.2, 0.2))
    p8.draw_text("Fecha de publicacion: Septiembre 2026 \xb7 Santiago de Compostela, Galicia, Espana", 48, 70, font='/F1', size=8, rgb=(0.4, 0.4, 0.4))
    p8.draw_text("Documento oficial para replicacion en taller y comites eticos de evaluacion clinica.", 48, 56, font='/F2', size=7.5, rgb=(0.1, 0.1, 0.1))

    pdf.add_page(p8.get_stream())

    # Save to project
    pdf.save(PROJECT_PDF)
    print("Project PDF built successfully!")

if __name__ == '__main__':
    build_manual()
