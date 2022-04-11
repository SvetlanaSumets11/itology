import os.path
import uuid

from PIL import Image, ImageDraw, ImageFont
import qrcode

from itology.config import DOWNLOAD_FILE_LINK, REDIRECT_DOWNLOAD_FILE_LINK
from itology.models import Advert, Certificate


class CertificatesGenerator:
    FONT = 'itology/certificates/times-new-roman.ttf'
    CERTIFICATE_TEMPLATE = 'itology/certificates/pattern.png'
    TEXT_Y_POSITION = 350
    QR_CODE_Y_POSITION = 800

    @classmethod
    def generate_certificates(cls, advert: Advert):
        participants = advert.get_members()
        for participant in participants:
            print(participant, participant.first_name, participant.last_name)
            participant_name = f'{participant.first_name} {participant.last_name}'
            pattern = Image.open(cls.CERTIFICATE_TEMPLATE, mode='r')
            drawing = ImageDraw.Draw(pattern)
            font = ImageFont.truetype(cls.FONT, 75)
            text_width, _ = drawing.textsize(participant_name, font=font)
            drawing.text(
                xy=((pattern.width - text_width) / 2 + 75, cls.TEXT_Y_POSITION),
                text=participant_name.upper(),
                fill=(52, 51, 133),
                font=font,
            )

            certificate_uuid = str(uuid.uuid4())
            Certificate.objects.create(uuid=certificate_uuid, nominee=participant, advert=advert)
            qr_code = qrcode.make(os.path.join(REDIRECT_DOWNLOAD_FILE_LINK, certificate_uuid))
            x, y = qr_code.size
            pattern.paste(qr_code, (1360, 930, x + 1360, y + 930))
            cls._convert_to_pdf(pattern, certificate_uuid)

    @classmethod
    def _convert_to_pdf(cls, file: Image, name: str):
        img = Image.new('RGB', file.size, (255, 255, 255))
        img.paste(file, mask=file.split()[3])
        img.save(os.path.join(DOWNLOAD_FILE_LINK, f'{name}.pdf'))
