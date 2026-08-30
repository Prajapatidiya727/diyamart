import os
import re
import time
import requests

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from products.models import Category


# Load .env from the Django project root
load_dotenv()


PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

PEXELS_URL = "https://api.pexels.com/v1/search"


# Better search phrases for categories
SEARCH_TERMS = {

    # Electronics
    "Mobiles": "smartphone mobile phone",
    "Laptops": "laptop computer",
    "Headphones": "headphones",
    "Smart Watches": "smartwatch",
    "Accessories": "mobile phone accessories",
    "Tablets": "tablet computer",
    "Earphones": "wired earphones",
    "Earbuds": "wireless earbuds",
    "Smart Bands": "fitness smart band",
    "Mobile Accessories": "mobile phone accessories",
    "Laptop Accessories": "laptop accessories",
    "Computer Accessories": "computer accessories",
    "Keyboards": "computer keyboard",
    "Mice": "computer mouse",
    "Webcams": "webcam",
    "Monitors": "computer monitor",
    "Printers": "printer",
    "Scanners": "document scanner",
    "Projectors": "projector",
    "Televisions": "smart television",
    "Home Theater": "home theater system",
    "Speakers": "bluetooth speaker",
    "Soundbars": "soundbar",
    "Cameras": "digital camera",
    "DSLR Cameras": "DSLR camera",
    "Mirrorless Cameras": "mirrorless camera",
    "Action Cameras": "action camera",
    "Camera Accessories": "camera accessories",
    "Gaming Consoles": "gaming console",
    "Gaming Accessories": "gaming accessories",

    # Clothing
    "Men's Clothing": "men fashion clothing",
    "Women's Clothing": "women fashion clothing",
    "Kids' Clothing": "children clothing",
    "T-Shirts": "t shirt clothing",
    "Shirts": "men shirt",
    "Jeans": "jeans clothing",
    "Trousers": "trousers pants",
    "Shorts": "shorts clothing",
    "Jackets": "jacket clothing",
    "Sweaters": "sweater clothing",
    "Hoodies": "hoodie clothing",
    "Sarees": "Indian saree",
    "Kurtis": "Indian kurti",
    "Lehengas": "Indian lehenga",
    "Ethnic Wear": "Indian ethnic clothing",
    "Western Wear": "western fashion clothing",
    "Innerwear": "clothing",
    "Sleepwear": "sleepwear pajamas",
    "Sportswear": "sports clothing",
    "Formal Wear": "formal clothing",

    # Shoes
    "Shoes": "shoes footwear",
    "Running Shoes": "running shoes",
    "Sports Shoes": "sports shoes",
    "Sneakers": "sneakers shoes",
    "Casual Shoes": "casual shoes",
    "Formal Shoes": "formal shoes",
    "Boots": "boots footwear",
    "Sandals": "sandals footwear",
    "Slippers": "slippers footwear",
    "Heels": "women high heels",
    "Flats": "women flats shoes",

    # Beauty
    "Beauty": "beauty products",
    "Makeup": "makeup cosmetics",
    "Skincare": "skincare products",
    "Hair Care": "hair care products",
    "Hair Styling": "hair styling",
    "Bath & Body": "bath body care",
    "Fragrances": "perfume fragrance",
    "Perfumes": "perfume bottle",
    "Deodorants": "deodorant",
    "Lip Care": "lip balm",
    "Face Care": "face skincare",
    "Body Care": "body care",
    "Nail Care": "nail polish",

    # Jewellery
    "Jewellery": "jewelry",
    "Gold Jewellery": "gold jewelry",
    "Silver Jewellery": "silver jewelry",
    "Artificial Jewellery": "fashion jewelry",
    "Earrings": "earrings jewelry",
    "Necklaces": "necklace jewelry",
    "Bracelets": "bracelet jewelry",
    "Rings": "rings jewelry",
    "Bangles": "Indian bangles",
    "Watches": "wrist watch",

    # Home
    "Furniture": "home furniture",
    "Home Decor": "home decor",
    "Living Room": "living room furniture",
    "Bedroom": "bedroom furniture",
    "Kitchen": "modern kitchen",
    "Dining": "dining table",
    "Storage & Organization": "home storage",
    "Lighting": "home lighting lamp",
    "Curtains": "window curtains",
    "Cushions": "decorative cushions",
    "Bedsheets": "bedsheets",
    "Blankets": "blanket",
    "Pillows": "pillows",
    "Mattresses": "mattress",
    "Carpets": "carpet rug",
    "Wall Decor": "wall decor",
    "Clocks": "wall clock",
    "Mirrors": "wall mirror",

    # Kitchen
    "Kitchen Appliances": "kitchen appliances",
    "Cookware": "cookware pots pans",
    "Bakeware": "baking cookware",
    "Kitchen Tools": "kitchen utensils",
    "Dinner Sets": "dinner plates set",
    "Glassware": "drinking glasses",
    "Water Bottles": "water bottle",
    "Lunch Boxes": "lunch box",
    "Coffee Makers": "coffee maker",
    "Electric Kettles": "electric kettle",
    "Mixer Grinders": "mixer grinder",
    "Air Fryers": "air fryer",
    "Microwave Ovens": "microwave oven",

    # Grocery
    "Grocery": "grocery shopping",
    "Rice": "rice grains",
    "Atta & Flour": "wheat flour",
    "Pulses": "lentils pulses",
    "Cooking Oil": "cooking oil",
    "Spices": "Indian spices",
    "Dry Fruits": "almonds cashews dry fruits",
    "Snacks": "snacks food",
    "Biscuits": "biscuits cookies",
    "Chocolates": "chocolate",
    "Beverages": "drinks beverages",
    "Tea": "tea cup",
    "Coffee": "coffee beans",
    "Breakfast Foods": "breakfast food",

    # Sports
    "Sports": "sports equipment",
    "Cricket": "cricket bat ball",
    "Football": "football soccer",
    "Basketball": "basketball",
    "Badminton": "badminton racket",
    "Tennis": "tennis racket",
    "Table Tennis": "table tennis",
    "Volleyball": "volleyball",
    "Cycling": "bicycle cycling",
    "Fitness": "fitness equipment",
    "Gym Equipment": "gym equipment",
    "Yoga": "yoga mat",
    "Running": "running shoes",
    "Sports Accessories": "sports accessories",

    # Toys
    "Toys": "children toys",
    "Educational Toys": "educational toys",
    "Remote Control Toys": "remote control toy car",
    "Board Games": "board games",
    "Puzzles": "jigsaw puzzle",
    "Action Figures": "action figure",
    "Dolls": "doll toy",
    "Building Blocks": "building blocks",
    "Outdoor Toys": "outdoor toys",
    "Baby Toys": "baby toys",

    # Books
    "Books": "books",
    "Fiction Books": "fiction novels",
    "Non-Fiction Books": "non fiction books",
    "Academic Books": "academic textbooks",
    "Competitive Exam Books": "exam preparation books",
    "Children's Books": "children books",
    "Comics": "comic books",
    "Self Help Books": "self help books",
    "Business Books": "business books",
    "Technology Books": "technology programming books",

    # Automotive
    "Automotive": "automotive car",
    "Car Accessories": "car accessories",
    "Bike Accessories": "motorcycle accessories",
    "Car Electronics": "car electronics",
    "Car Care": "car cleaning",
    "Bike Care": "motorcycle care",
    "Helmets": "motorcycle helmet",
    "Car Covers": "car cover",
    "Bike Covers": "motorcycle cover",
    "Vehicle Lighting": "car headlights",

    # Travel
    "Travel": "travel luggage",
    "Luggage": "travel suitcase",
    "Trolley Bags": "trolley suitcase",
    "Backpacks": "backpack",
    "Travel Bags": "travel bag",
    "Travel Accessories": "travel accessories",
    "Travel Organizers": "travel organizer",
    "Passport Holders": "passport holder",

    # Pets
    "Pet Supplies": "pet supplies",
    "Dog Supplies": "dog supplies",
    "Cat Supplies": "cat supplies",
    "Pet Food": "pet food",
    "Pet Toys": "pet toys",
    "Pet Accessories": "pet accessories",

    # Office
    "Office Supplies": "office supplies",
    "Stationery": "stationery",
    "Pens": "pens",
    "Notebooks": "notebook",
    "Diaries": "diary",
    "Art Supplies": "art supplies",
    "School Supplies": "school supplies",
    "Office Furniture": "office desk furniture",

    # Baby
    "Baby Products": "baby products",
    "Baby Clothing": "baby clothes",
    "Baby Care": "baby care",
    "Baby Food": "baby food",
    "Diapers": "baby diapers",
    "Baby Accessories": "baby accessories",
}


def safe_filename(name):
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


class Command(BaseCommand):

    help = "Download real category photos from Pexels"

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

        categories = Category.objects.all()

        self.stdout.write(
            self.style.SUCCESS(
                f"Found {categories.count()} categories."
            )
        )

        success = 0
        failed = 0

        for category in categories:

            search_term = SEARCH_TERMS.get(
                category.name,
                category.name + " product"
            )

            self.stdout.write(
                f"\nDownloading real photo for: {category.name}"
            )

            try:

                params = {
                    "query": search_term,
                    "per_page": 10,
                    "orientation": "landscape"
                }

                response = requests.get(
                    PEXELS_URL,
                    headers=headers,
                    params=params,
                    timeout=30
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
                        timeout=30
                    )

                if response.status_code != 200:

                    self.stdout.write(
                        self.style.ERROR(
                            f"  ✗ Pexels API error: "
                            f"{response.status_code}"
                        )
                    )

                    failed += 1
                    continue

                data = response.json()

                photos = data.get("photos", [])

                if not photos:

                    self.stdout.write(
                        self.style.ERROR(
                            "  ✗ No suitable photo found"
                        )
                    )

                    failed += 1
                    continue

                # Use the first suitable photo
                photo = photos[0]

                image_url = (
                    photo.get("src", {})
                    .get("large2x")
                    or
                    photo.get("src", {})
                    .get("large")
                )

                if not image_url:

                    self.stdout.write(
                        self.style.ERROR(
                            "  ✗ Photo URL not available"
                        )
                    )

                    failed += 1
                    continue

                image_response = requests.get(
                    image_url,
                    timeout=30
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
                    f"{safe_filename(category.name)}.jpg"
                )

                # Delete old image
                if category.image:

                    try:

                        old_path = category.image.path

                        if os.path.exists(old_path):
                            os.remove(old_path)

                    except Exception:
                        pass

                # Save real photo locally
                category.image.save(
                    filename,
                    ContentFile(image_response.content),
                    save=True
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"  ✓ {category.name}"
                    )
                )

                success += 1

                # Small delay to avoid API rate limits
                time.sleep(1)

            except Exception as e:

                self.stdout.write(
                    self.style.ERROR(
                        f"  ✗ {category.name}: {e}"
                    )
                )

                failed += 1

        self.stdout.write("\n")
        self.stdout.write("=" * 45)

        self.stdout.write(
            self.style.SUCCESS(
                f"Completed: {success}"
            )
        )

        self.stdout.write(
            self.style.ERROR(
                f"Failed: {failed}"
            )
        )

        self.stdout.write("=" * 45)

        self.stdout.write(
            self.style.SUCCESS(
                "\nReal category photos are stored locally in:"
            )
        )

        self.stdout.write(
            "media/categories/"
        )