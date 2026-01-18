import qrcode
from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Questionnaire

@receiver(post_save, sender=Questionnaire)
def generate_qr_code_for_questionnaire(sender, instance, created, **kwargs):
    """
    Automatically generate a QR code pointing to the questionnaire
    access endpoint when a questionnaire is created.
    """
    if not created:
        return

    # 🔹 Build access URL (used by Flutter app / web)
    base_url = getattr(settings, "QUESTIONNAIRE_ACCESS_BASE_URL", None)

    if not base_url:
        # Fallback (avoid crashing in case setting is missing)
        base_url = "https://api.example.com/forms/access"

    access_url = f"{base_url}/{instance.id}/"

    # 🔹 Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(access_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    # 🔹 Save to model without retriggering signal
    instance.qr_code.save(
        f"questionnaire_{instance.id}.png",
        ContentFile(buffer.getvalue()),
        save=False
    )
    instance.link = access_url

    instance.save(update_fields=["qr_code", "link"])