import os.path
import uuid

from django.contrib.auth.models import User
from PIL import Image, ImageDraw, ImageFont
import qrcode

from itology.config import CERTIFICATE_PATTERN_PATH, DOWNLOAD_FILE_LINK, REDIRECT_DOWNLOAD_FILE_LINK
from itology.models import Advert, Certificate


class CertificatesGenerator:
    FONT = os.path.join(CERTIFICATE_PATTERN_PATH, 'times-new-roman.ttf')
    CERTIFICATE_TEMPLATE = os.path.join(CERTIFICATE_PATTERN_PATH, 'pattern.png')
    TEXT_Y_POSITION = 350
    QR_CODE_Y_POSITION = 800

    @classmethod
    def generate_certificates(cls, advert: Advert):
        participants = advert.get_members()
        for participant in participants:
            pattern = Image.open(cls.CERTIFICATE_TEMPLATE, mode='r')
            pattern = cls._place_nominee_name(participant, pattern)
            certificate_uuid = str(uuid.uuid4())
            pattern = cls._place_download_file_qrcode(participant, advert, pattern, uuid=certificate_uuid)
            cls._convert_to_pdf(pattern, certificate_uuid)

    @classmethod
    def _place_nominee_name(cls, participant: User, pattern: Image) -> Image:
        participant_name = f'{participant.first_name} {participant.last_name}'
        drawing = ImageDraw.Draw(pattern)
        font = ImageFont.truetype(cls.FONT, 75)
        text_width, _ = drawing.textsize(participant_name, font=font)
        drawing.text(
            xy=((pattern.width - text_width) / 2 + 75, cls.TEXT_Y_POSITION),
            text=participant_name.upper(),
            fill=(52, 51, 133),
            font=font,
        )
        return pattern

    @classmethod
    def _place_download_file_qrcode(cls, participant: User, advert: Advert, pattern: Image, uuid: str) -> Image:
        Certificate.objects.create(uuid=uuid, nominee=participant, advert=advert)
        qr_code = qrcode.make(os.path.join(REDIRECT_DOWNLOAD_FILE_LINK, uuid))
        x, y = qr_code.size
        pattern.paste(qr_code, (1360, 930, x + 1360, y + 930))
        return pattern

    @classmethod
    def _convert_to_pdf(cls, file: Image, name: str):
        img = Image.new('RGB', file.size, (255, 255, 255))
        img.paste(file, mask=file.split()[3])
        img.save(os.path.join(DOWNLOAD_FILE_LINK, f'{name}.pdf'))
