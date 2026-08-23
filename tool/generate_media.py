from pathlib import Path
import math
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont
import qrcode
from qrcode.constants import ERROR_CORRECT_H


ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "website" / "assets"
FRAMES = ROOT / "website" / ".frames"
LOGO = ASSETS / "logo.png"
DOWNLOAD_URL = "https://finance.equitick.top/api/app/download"
WIDTH, HEIGHT, FPS = 960, 720, 24
GREEN = "#018B8D"
DEEP = "#12372d"
INK = "#17211e"
MUTED = "#66716d"
PAPER = "#f7faf8"


def font(size: int, bold: bool = False):
    name = "msyhbd.ttc" if bold else "msyh.ttc"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def rounded(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def paste_rounded(image, source, position, radius):
    mask = Image.new("L", source.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, source.width - 1, source.height - 1),
        radius=radius,
        fill=255,
    )
    image.paste(source, position, mask)


def make_qr():
    qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H, box_size=14, border=3)
    qr.add_data(DOWNLOAD_URL)
    qr.make(fit=True)
    image = qr.make_image(fill_color=DEEP, back_color="white").convert("RGBA")
    logo = Image.open(LOGO).convert("RGBA").resize((112, 112), Image.Resampling.LANCZOS)
    x = (image.width - logo.width) // 2
    y = (image.height - logo.height) // 2
    background = Image.new("RGBA", (132, 132), "white")
    image.alpha_composite(background, (x - 10, y - 10))
    image.alpha_composite(logo, (x, y))
    image.save(ASSETS / "download-qr.png", optimize=True)


SCENES = [
    ("一眼看清财务", "资产、收支和预算集中呈现", ["净资产  ¥ 126,580", "本月结余  +¥ 3,860", "预算执行  68%"]),
    ("AI 智能记账", "一句话或一张账单，快速生成记录", ["午餐  ¥ 32", "已识别：餐饮", "确认后安全入账"]),
    ("预算与消费洞察", "提前发现风险，而不是月底才后悔", ["餐饮预算  76%", "交通支出下降 12%", "本月可节省 ¥ 420"]),
    ("家庭共享账本", "共同管理，也保留各自的隐私边界", ["家庭账本  3 位成员", "共同预算  ¥ 8,000", "敏感备注端到端加密"]),
    ("预测未来现金流", "让今天的每一笔，都服务于明天", ["月末预测  +¥ 6,240", "未来扣款  4 笔", "财务健康分  86"]),
]


def draw_frame(scene_index: int, phase: float):
    image = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(image)
    for radius, alpha in [(430, 28), (320, 22), (220, 18)]:
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.ellipse((-160 - radius / 3, -190, radius, radius + 160), fill=(67, 185, 173, alpha))
        image = Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(image)
    title, subtitle, cards = SCENES[scene_index]
    eased = 1 - (1 - min(phase * 1.8, 1)) ** 3
    offset = int((1 - eased) * 34)

    logo = Image.open(LOGO).convert("RGBA").resize((64, 64), Image.Resampling.LANCZOS)
    paste_rounded(image, logo, (56, 46), 12)
    draw.text((134, 58), "司库", font=font(28, True), fill=DEEP)
    draw.text((56, 164 + offset), title, font=font(48, True), fill=DEEP)
    draw.text((58, 232 + offset), subtitle, font=font(23), fill=MUTED)

    phone = (540, 52, 890, 670)
    rounded(draw, phone, 48, GREEN)
    rounded(draw, (546, 58, 884, 664), 42, "#f9fbfa")
    rounded(draw, (665, 76, 765, 86), 6, "#d8e1dd")
    draw.text((582, 122), title, font=font(28, True), fill=INK)
    draw.text((582, 164), "智能财务管家", font=font(17), fill=MUTED)
    for i, line in enumerate(cards):
        y = 232 + i * 112
        delay = max(0, min(1, phase * 2.1 - i * 0.18))
        x = 582 + int((1 - delay) * 30)
        rounded(draw, (x, y, 848, y + 88), 20, "white", "#dfe8e4", 2)
        rounded(draw, (x + 16, y + 18, x + 54, y + 56), 12, "#e2f6f2")
        draw.ellipse((x + 27, y + 29, x + 43, y + 45), fill=GREEN)
        draw.text((x + 68, y + 24), line, font=font(18, i == 0), fill=DEEP if i == 0 else INK)
    draw.text((58, 628), "SIKU · AI FINANCE", font=font(18, True), fill=GREEN)
    return image


def make_video():
    shutil.rmtree(FRAMES, ignore_errors=True)
    FRAMES.mkdir(parents=True)
    seconds_per_scene = 2.4
    total_frames = int(len(SCENES) * seconds_per_scene * FPS)
    for frame_index in range(total_frames):
        scene_float = frame_index / (seconds_per_scene * FPS)
        scene_index = min(int(scene_float), len(SCENES) - 1)
        phase = scene_float - scene_index
        frame = draw_frame(scene_index, phase)
        if phase > 0.82 and scene_index < len(SCENES) - 1:
            next_frame = draw_frame(scene_index + 1, 0)
            blend = (phase - 0.82) / 0.18
            frame = Image.blend(frame, next_frame, blend)
        frame.save(FRAMES / f"frame-{frame_index:04d}.png", optimize=True)
    draw_frame(0, 1).save(ASSETS / "siku-demo-poster.jpg", quality=90, optimize=True)
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(FRAMES / "frame-%04d.png"),
        "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", str(ASSETS / "siku-demo.mp4")
    ], check=True)
    shutil.rmtree(FRAMES)


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    make_qr()
    make_video()
