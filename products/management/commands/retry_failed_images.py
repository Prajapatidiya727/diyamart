import os
import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from products.models import Category


load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_URL = "https://api.pexels.com/v1/search"


class Command(BaseCommand):

    help = "Retry only Casual Shoes category image"

    def handle(self, *args, **options):

        category_name = "Casual Shoes"
        search_term = "casual shoes footwear"

        if not PEXELS_API_KEY:
            self.stdout.write(
                self.style.ERROR(
                    "PEXELS_API_KEY not found in .env"
                )
            )
            return

        self.stdout.write(
            "\nRetrying ONLY: Casual Shoes\n"
        )

        try:

            category = Category.objects.get(
                name=category_name
            )

            headers = {
                "Authorization": PEXELS_API_KEY
            }

            params = {
                "query": search_term,
                "per_page": 10,
                "orientation": "landscape"
            }

            self.stdout.write(
                "Searching Pexels..."
            )

            response = requests.get(
                PEXELS_URL,
                headers=headers,
                params=params,
                timeout=20
            )

            if response.status_code != 200:
                self.stdout.write(
                    self.style.ERROR(
                        f"✗ Pexels API error: "
                        f"{response.status_code}"
                    )
                )
                return

            photos = response.json().get(
                "photos", []
            )

            if not photos:
                self.stdout.write(
                    self.style.ERROR(
                        "✗ No photo found"
                    )
                )
                return

            photo = photos[0]

            # Use medium image instead of large2x
            image_url = (
                photo.get("src", {}).get("medium")
                or photo.get("src", {}).get("large")
            )

            if not image_url:
                self.stdout.write(
                    self.style.ERROR(
                        "✗ Image URL not found"
                    )
                )
                return

            self.stdout.write(
                "Downloading image..."
            )

            image_response = requests.get(
                image_url,
                timeout=20,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            if image_response.status_code != 200:
                self.stdout.write(
                    self.style.ERROR(
                        f"✗ Image download failed: "
                        f"{image_response.status_code}"
                    )
                )
                return

            filename = "casual_shoes.jpg"

            category.image.save(
                filename,
                ContentFile(image_response.content),
                save=True
            )

            self.stdout.write(
                self.style.SUCCESS(
                    "\n✓ Casual Shoes image downloaded successfully!"
                )
            )

            self.stdout.write(
                "Saved to: media/categories/"
            )

        except Exception as e:

            self.stdout.write(
                self.style.ERROR(
                    f"\n✗ Casual Shoes failed: {e}"
                )
            )