"""
Generador de video corporativo en MP4 para LYRAPOINT.
Crea un video profesional en 1280x720 HD con el logo, fondo y todas las caracteristicas solicitadas.
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio

# Configuracion General
WIDTH, HEIGHT = 1280, 720
FPS = 24
OUTPUT_FILE = "lyrapoint-video.mp4"

# Cargar recursos
BG_PATH = "FONDO.jpg"
LOGO_PATH = "Lyrapoint-transparent.png"

bg_img_raw = Image.open(BG_PATH).convert("RGBA")
# Ajustar fondo a tamano un poco mayor para efecto sutil de movimiento
BG_SCALED_W = int(WIDTH * 1.15)
BG_SCALED_H = int(HEIGHT * 1.15)
bg_img_scaled = bg_img_raw.resize((BG_SCALED_W, BG_SCALED_H), Image.Resampling.LANCZOS)

logo_raw = Image.open(LOGO_PATH).convert("RGBA")

# Fuentes
WINDIR = os.environ.get("WINDIR", "C:/Windows")
FONTS_DIR = os.path.join(WINDIR, "Fonts")

def get_font(name, size):
    path = os.path.join(FONTS_DIR, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

font_title_huge = get_font("segoeuib.ttf", 68)
font_title_large = get_font("segoeuib.ttf", 44)
font_title_medium = get_font("segoeuib.ttf", 34)
font_subtitle = get_font("segoeui.ttf", 26)
font_badge = get_font("segoeuib.ttf", 20)
font_body_bold = get_font("segoeuib.ttf", 24)
font_body = get_font("segoeui.ttf", 20)
font_small = get_font("segoeui.ttf", 16)

# Paleta de colores (RGBA)
COLOR_WHITE = (255, 255, 255, 255)
COLOR_CYAN = (0, 210, 255, 255)
COLOR_BLUE = (37, 99, 235, 255)
COLOR_MUTED = (160, 185, 215, 255)
COLOR_CARD_BG = (9, 18, 38, 225)
COLOR_CARD_BORDER = (0, 210, 255, 120)
COLOR_CHECK = (16, 185, 129, 255)

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def create_top_bar(canvas, draw):
    # Barra superior con mini logo y marca
    logo_mini = logo_raw.resize((48, 44), Image.Resampling.LANCZOS)
    canvas.paste(logo_mini, (50, 30), logo_mini)
    draw.text((110, 32), "LYRAPOINT", font=font_title_medium, fill=COLOR_CYAN)
    draw.text((110, 68), "Soluciones para controlar tu negocio digitalmente", font=font_small, fill=COLOR_MUTED)

# Definicion de Escenas
scenes = [
    {
        "type": "intro",
        "duration": 3.8,  # segundos
        "title": "LYRAPOINT",
        "tagline": "Soluciones para controlar tu negocio digitalmente",
        "badge": "SISTEMA INTEGRAL DE GESTIÓN COMERCIAL"
    },
    {
        "type": "features_cards",
        "duration": 4.5,
        "badge": "ALTO RENDIMIENTO Y EFICIENCIA",
        "title": "Control Rápido, Seguro y Simultáneo",
        "items": [
            ("Multiusuario", "Todo tu personal conectado y trabajando en simultáneo sin límites ni trabas."),
            ("Tiempo de Respuesta Inmediato", "Operaciones ultra rápidas al registrar productos, ventas y consultas."),
            ("Confiable y Estable", "Máxima seguridad y solidez en los momentos de mayor flujo comercial.")
        ]
    },
    {
        "type": "highlight_card",
        "duration": 4.0,
        "badge": "EXPERIENCIA DE USUARIO",
        "title": "Fácil Manejo e Implementación Ágil",
        "subtitle": "Capacitación en pocas horas",
        "desc": "El sistema está diseñado para que cualquier persona del equipo aprenda a usarlo de forma natural y rápida. Olvídate de manuales interminables o semanas de adiestramiento.",
        "highlights": ["✓ Interfaz intuitiva y visual", "✓ Curva de aprendizaje inmediata", "✓ Puesta en marcha rápida"]
    },
    {
        "type": "features_cards",
        "duration": 4.5,
        "badge": "FACTURACIÓN Y COBRANZAS",
        "title": "Flexibilidad Total en Ventas",
        "items": [
            ("Ventas en Moneda Dual", "Manejo ágil y simultáneo en múltiples divisas con conversión automática."),
            ("Múltiples Formas de Pago", "Acepta tarjetas, transferencias, efectivo, pago móvil y combinaciones."),
            ("Rapidez en el Punto de Venta", "Atiende a tus clientes en segundos y evita colas en caja.")
        ]
    },
    {
        "type": "highlight_card",
        "duration": 4.8,
        "badge": "IMPRESIÓN Y FACTURACIÓN FISCAL",
        "title": "Documentos Impresos y Digitales",
        "subtitle": "Alianza Tecnológica con The Factory HKA",
        "desc": "Manejo de documentos a través de impresoras fiscales homologadas e impresión digital en alianza oficial con The Factory TFHKA. Cumple con todas las normas fiscales sin enredos.",
        "highlights": [
            "✓ Integración con Impresoras Fiscales",
            "✓ Impresión Digital certificada TFHKA",
            "✓ Emisión rápida de facturas y notas"
        ]
    },
    {
        "type": "features_cards",
        "duration": 4.5,
        "badge": "DISTRIBUCIÓN Y REPORTES",
        "title": "Comunicación y Reportes Inteligentes",
        "items": [
            ("Envío de Copia de Documentos", "Envío instantáneo de comprobantes y facturas vía Correo y WhatsApp."),
            ("Reportes en PDF y Excel", "Exportación completa de inventario, ventas y cierres con un solo clic."),
            ("Toma de Decisiones Informada", "Información clara y transparente para hacer crecer tu negocio.")
        ]
    },
    {
        "type": "outro",
        "duration": 4.2,
        "title": "LYRAPOINT",
        "subtitle": "Toma el control de tu negocio hoy mismo",
        "cta": "Visítanos en: lyrapoint-web.vercel.app",
        "badge": "SOLICITA TU DEMOSTRACIÓN"
    }
]

def render_frame(scene, progress, global_time):
    # progress va de 0.0 a 1.0 dentro de la escena
    # Crear fondo con efecto sutil de paneo / zoom
    dx = int(math.sin(global_time * 0.3) * 30 + 30)
    dy = int(math.cos(global_time * 0.25) * 20 + 20)
    
    # Crop del fondo
    bg_cropped = bg_img_scaled.crop((dx, dy, dx + WIDTH, dy + HEIGHT))
    
    # Overlay oscuro para nitidez
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (7, 12, 24, 185))
    frame = Image.alpha_composite(bg_cropped, overlay)
    
    # Fade in / Fade out de la escena
    alpha = 1.0
    FADE_IN_TIME = 0.4 / scene["duration"]
    FADE_OUT_TIME = 0.4 / scene["duration"]
    if progress < FADE_IN_TIME:
        alpha = progress / FADE_IN_TIME
    elif progress > (1.0 - FADE_OUT_TIME):
        alpha = (1.0 - progress) / FADE_OUT_TIME
    alpha = max(0.0, min(1.0, alpha))
    
    # Capa de dibujo de contenido
    content = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(content)
    
    stype = scene["type"]
    
    if stype == "intro":
        # Logo central animado
        logo_size = int(180 + math.sin(progress * math.pi) * 8)
        logo_resized = logo_raw.resize((logo_size, int(logo_size * 0.9)), Image.Resampling.LANCZOS)
        logo_x = (WIDTH - logo_resized.width) // 2
        logo_y = 130
        content.paste(logo_resized, (logo_x, logo_y), logo_resized)
        
        # Badge
        badge_text = scene["badge"]
        draw_rounded_rect(draw, (360, 320, WIDTH - 360, 360), radius=16, fill=(0, 210, 255, 30), outline=(0, 210, 255, 140))
        draw.text((WIDTH // 2, 340), badge_text, font=font_badge, fill=COLOR_CYAN, anchor="mm")
        
        # Titulo Principal
        draw.text((WIDTH // 2, 420), scene["title"], font=font_title_huge, fill=COLOR_WHITE, anchor="mm")
        
        # Subtitulo
        draw.text((WIDTH // 2, 480), scene["tagline"], font=font_subtitle, fill=COLOR_MUTED, anchor="mm")
        
        # Puntos clave inferiores
        bullets = "Control de Inventario  •  Facturación Fácil  •  Aprendizaje Rápido"
        draw.text((WIDTH // 2, 570), bullets, font=font_badge, fill=COLOR_CYAN, anchor="mm")
        
    elif stype == "features_cards":
        create_top_bar(content, draw)
        
        # Badge de categoria
        badge_text = scene["badge"]
        draw_rounded_rect(draw, (50, 110, 500, 145), radius=12, fill=(0, 210, 255, 25), outline=(0, 210, 255, 120))
        draw.text((70, 127), badge_text, font=font_badge, fill=COLOR_CYAN, anchor="lm")
        
        # Titulo de seccion
        draw.text((50, 185), scene["title"], font=font_title_large, fill=COLOR_WHITE, anchor="lm")
        
        # 3 Tarjetas de caracteristicas
        items = scene["items"]
        card_w = (WIDTH - 100 - (len(items) - 1) * 24) // len(items)
        card_h = 410
        card_y = 230
        
        for i, (title, desc) in enumerate(items):
            cx = 50 + i * (card_w + 24)
            # Dibujar tarjeta con borde cyan
            draw_rounded_rect(draw, (cx, card_y, cx + card_w, card_y + card_h), radius=18, 
                              fill=COLOR_CARD_BG, outline=COLOR_CARD_BORDER, width=2)
            
            # Icono / Circulo con numero
            draw.ellipse((cx + 25, card_y + 30, cx + 75, card_y + 80), fill=(0, 210, 255, 35), outline=COLOR_CYAN, width=2)
            draw.text((cx + 50, card_y + 55), str(i + 1), font=font_title_medium, fill=COLOR_CYAN, anchor="mm")
            
            # Titulo de la tarjeta
            # Ajustar texto largo
            words = title.split()
            lines = []
            cur = ""
            for w in words:
                if len(cur + " " + w) > 22:
                    lines.append(cur)
                    cur = w
                else:
                    cur = (cur + " " + w).strip()
            if cur:
                lines.append(cur)
            
            ty = card_y + 115
            for line in lines:
                draw.text((cx + 25, ty), line, font=font_body_bold, fill=COLOR_WHITE)
                ty += 32
                
            # Linea decorativa
            draw.line((cx + 25, ty + 10, cx + 120, ty + 10), fill=COLOR_CYAN, width=3)
            
            # Descripcion
            desc_words = desc.split()
            d_lines = []
            d_cur = ""
            for w in desc_words:
                if len(d_cur + " " + w) > 26:
                    d_lines.append(d_cur)
                    d_cur = w
                else:
                    d_cur = (d_cur + " " + w).strip()
            if d_cur:
                d_lines.append(d_cur)
                
            dy_pos = ty + 30
            for dl in d_lines:
                draw.text((cx + 25, dy_pos), dl, font=font_body, fill=COLOR_MUTED)
                dy_pos += 28

    elif stype == "highlight_card":
        create_top_bar(content, draw)
        
        # Badge
        badge_text = scene["badge"]
        draw_rounded_rect(draw, (50, 110, 480, 145), radius=12, fill=(0, 210, 255, 25), outline=(0, 210, 255, 120))
        draw.text((70, 127), badge_text, font=font_badge, fill=COLOR_CYAN, anchor="lm")
        
        # Gran tarjeta contenedora
        draw_rounded_rect(draw, (50, 180, WIDTH - 50, 660), radius=22, fill=COLOR_CARD_BG, outline=COLOR_CARD_BORDER, width=2)
        
        # Titulo y Subtitulo
        draw.text((90, 230), scene["title"], font=font_title_large, fill=COLOR_WHITE)
        draw.text((90, 280), scene["subtitle"], font=font_subtitle, fill=COLOR_CYAN)
        
        # Linea divisoria
        draw.line((90, 325, 450, 325), fill=COLOR_CYAN, width=3)
        
        # Descripcion en parrafos
        desc_words = scene["desc"].split()
        lines = []
        cur = ""
        for w in desc_words:
            if len(cur + " " + w) > 65:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        if cur:
            lines.append(cur)
            
        py = 355
        for l in lines:
            draw.text((90, py), l, font=font_subtitle, fill=COLOR_MUTED)
            py += 38
            
        # Puntos destacados
        hy = py + 30
        for h in scene["highlights"]:
            draw_rounded_rect(draw, (90, hy, 850, hy + 48), radius=10, fill=(0, 210, 255, 18), outline=(0, 210, 255, 80))
            draw.text((115, hy + 24), h, font=font_body_bold, fill=COLOR_WHITE, anchor="lm")
            hy += 60

    elif stype == "outro":
        # Outro con llamado a la accion
        logo_out = logo_raw.resize((150, 135), Image.Resampling.LANCZOS)
        logo_x = (WIDTH - logo_out.width) // 2
        content.paste(logo_out, (logo_x, 110), logo_out)
        
        draw.text((WIDTH // 2, 285), scene["title"], font=font_title_huge, fill=COLOR_WHITE, anchor="mm")
        draw.text((WIDTH // 2, 350), scene["subtitle"], font=font_subtitle, fill=COLOR_CYAN, anchor="mm")
        
        # Tarjeta CTA
        draw_rounded_rect(draw, (300, 410, WIDTH - 300, 560), radius=20, fill=(0, 210, 255, 25), outline=COLOR_CYAN, width=2)
        draw.text((WIDTH // 2, 455), scene["badge"], font=font_badge, fill=COLOR_CYAN, anchor="mm")
        draw.text((WIDTH // 2, 510), scene["cta"], font=font_title_medium, fill=COLOR_WHITE, anchor="mm")
        
        # Mensaje de contacto
        draw.text((WIDTH // 2, 620), "Disponible para PyMEs y Comercios en Crecimiento", font=font_body, fill=COLOR_MUTED, anchor="mm")

    # Aplicar transparencia alpha (Fade In / Fade Out)
    if alpha < 0.999:
        # Multiplicar canal alpha del contenido
        r, g, b, a = content.split()
        a = a.point(lambda p: int(p * alpha))
        content.putalpha(a)
        
    final_frame = Image.alpha_composite(frame, content)
    return np.array(final_frame.convert("RGB"))

def generate():
    print("Iniciando renderizado del video corporativo de LYRAPOINT...")
    total_duration = sum(s["duration"] for s in scenes)
    total_frames = int(total_duration * FPS)
    print(f"Duracion total: {total_duration:.1f} segundos ({total_frames} fotogramas a {FPS} FPS)")
    
    writer = imageio.get_writer(
        OUTPUT_FILE, 
        fps=FPS, 
        codec="libx264", 
        quality=8, 
        pixelformat="yuv420p",
        macro_block_size=16
    )
    
    frame_idx = 0
    global_time = 0.0
    dt = 1.0 / FPS
    
    for s_idx, scene in enumerate(scenes):
        s_frames = int(scene["duration"] * FPS)
        print(f"Renderizando Escena {s_idx + 1}/{len(scenes)} ({scene['type']})...")
        for f in range(s_frames):
            prog = f / max(1, s_frames - 1)
            frame_arr = render_frame(scene, prog, global_time)
            writer.append_data(frame_arr)
            frame_idx += 1
            global_time += dt
            
    writer.close()
    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"Video generado con exito: {OUTPUT_FILE} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    generate()
