import os
import re
import time
import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from products.models import Category


load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_URL = "https://api.pexels.com/v1/search"


RETRY_CATEGORIES = {
    "Mobiles": "smartphone mobile phone",
    "Casual Shoes": "casual shoes",
    "Formal Shoes": "formal shoes",
    "Boots": "boots footwear",
    "Sandals": "sandals footwear",
    "Slippers": "slippers footwear",
    "Makeup": "makeup cosmetics",
    "Artificial Jewellery": "fashion jewelry",
    "Carpets": "carpet rug",
    "Kitchen Appliances": "kitchen appliances",
    "Spices": "Indian spices",
    "Dry Fruits": "almonds cashews dry fruits",
    "Snacks": "snacks food",
    "Tennis": "tennis racket",
    "Board Games": "board games",
}


def safe_filename(name):
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


class Command(BaseCommand):

    help = "Retry only the previously failed category images"

    def handle(self, *args, **options):

        if not PEXELS_API_KEY:
            self.stdout.write(
                self.style.ERROR(
                    "PEXELS_API_KEY not found in .env"
                )
            )
            return

        headers = {
            "Authorization": PEXELS_API_KEY
        }

        success = 0
        failed = 0

        self.stdout.write(
            self.style.WARNING(
                f"\nRetrying only {len(RETRY_CATEGORIES)} failed categories..."
            )
        )

        for category_name, search_term in RETRY_CATEGORIES.items():

            self.stdout.write(
                f"\nDownloading: {category_name}"
            )

            try:

                category = Category.objects.get(
                    name=category_name
                )

                params = {
                    "query": search_term,
                    "per_page": 5,
                    "orientation": "landscape"
                }

                response = requests.get(
                    PEXELS_URL,
                    headers=headers,
                    params=params,
                    timeout=15
                )

                if response.status_code == 429:

                    self.stdout.write(
                        self.style.WARNING(
                            "  Rate limit reached. Waiting 10 seconds..."
                        )
                    )

                    time.sleep(10)

                    response = requests.get(
                        PEXELS_URL,
                        headers=headers,
                        params=params,
                        timeout=15
                    )

                if response.status_code != 200:

                    self.stdout.write(
                        self.style.ERROR(
                            f"  ✗ API error: {response.status_code}"
                        )
                    )

                    failed += 1
                    continue

                data = response.json()

                photos = data.get("photos", [])

                if not photos:

                    self.stdout.write(
                        self.style.ERROR(
                            "  ✗ No photo found"
                        )
                    )

                    failed += 1
                    continue

                photo = photos[0]

                image_url = (
                    photo.get("src", {}).get("large2x")
                    or
                    photo.get("src", {}).get("large")
                )

                if not image_url:

                    self.stdout.write(
                        self.style.ERROR(
                            "  ✗ Image URL not found"
                        )
                    )

                    failed += 1
                    continue

                image_response = requests.get(
                    image_url,
                    timeout=15
                )

                if image_response.status_code != 200:

                    self.stdout.write(
                        self.style.ERROR(
                            f"  ✗ Image download failed: "
                            f"{image_response.status_code}"
                        )
                    )

                    failed += 1
                    continue

                filename = (
                    f"{safe_filename(category_name)}.jpg"
                )

                category.image.save(
                    filename,
                    ContentFile(image_response.content),
                    save=True
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"  ✓ {category_name}"
                    )
                )

                success += 1

                time.sleep(0.5)

            except Category.DoesNotExist:

                self.stdout.write(
                    self.style.ERROR(
                        f"  ✗ Category not found: {category_name}"
                    )
                )

                failed += 1

            except Exception as e:

                self.stdout.write(
                    self.style.ERROR(
                        f"  ✗ {category_name}: {e}"
                    )
                )

                failed += 1

        self.stdout.write("\n")
        self.stdout.write("=" * 45)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully downloaded: {success}"
            )
        )

        self.stdout.write(
            self.style.ERROR(
                f"Still failed: {failed}"
            )
        )

        self.stdout.write("=" * 45)