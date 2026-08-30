import os
import time
import hashlib
import requests

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile

from products.models import Product


PEXELS_URL = "https://api.pexels.com/v1/search"


# Better search terms for generic category names
CATEGORY_SEARCH_TERMS = {
    "Mobiles": "smartphone mobile phone",
    "Laptops": "laptop computer",
    "Headphones": "headphones audio",
    "Smart Watches": "smart watch",
    "Accessories": "mobile accessories",
    "Tablets": "tablet device",
    "Earphones": "wired earphones",
    "Earbuds": "wireless earbuds",
    "Smart Bands": "fitness smart band",
    "Mobile Accessories": "phone accessories",
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
    "Home Theater": "home theater",
    "Speakers": "bluetooth speaker",
    "Soundbars": "soundbar",
    "Cameras": "digital camera",
    "DSLR Cameras": "DSLR camera",
    "Mirrorless Cameras": "mirrorless camera",
    "Action Cameras": "action camera",
    "Camera Accessories": "camera accessories",
    "Gaming Consoles": "gaming console",
    "Gaming Accessories": "gaming accessories",

    "Men's Clothing": "men clothing fashion",
    "Women's Clothing": "women clothing fashion",
    "Kids' Clothing": "kids clothing",
    "T-Shirts": "t shirt clothing",
    "Shirts": "shirt clothing",
    "Jeans": "jeans",
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

    "Shoes": "shoes footwear",
    "Running Shoes": "running shoes",
    "Sports Shoes": "sports shoes",
    "Sneakers": "sneakers",
    "Casual Shoes": "casual shoes",
    "Formal Shoes": "formal shoes",
    "Boots": "boots footwear",
    "Sandals": "sandals footwear",
    "Slippers": "slippers footwear",
    "Heels": "women heels shoes",
    "Flats": "women flats shoes",

    "Beauty": "beauty products",
    "Makeup": "makeup cosmetics",
    "Skincare": "skincare cosmetics",
    "Hair Care": "hair care products",
    "Hair Styling": "hair styling",
    "Bath & Body": "bath body products",
    "Fragrances": "fragrance perfume",
    "Perfumes": "perfume bottle",
    "Deodorants": "deodorant",
    "Lip Care": "lip balm",
    "Face Care": "face skincare",
    "Body Care": "body care",
    "Nail Care": "nail care manicure",

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

    "Furniture": "modern furniture",
    "Home Decor": "home decor",
    "Living Room": "living room furniture",
    "Bedroom": "bedroom furniture",
    "Kitchen": "kitchen",
    "Dining": "dining table",
    "Storage & Organization": "home storage organization",
    "Lighting": "home lighting lamp",
    "Curtains": "curtains",
    "Cushions": "cushions",
    "Bedsheets": "bedsheet",
    "Blankets": "blanket",
    "Pillows": "pillow",
    "Mattresses": "mattress",
    "Carpets": "carpet rug",
    "Wall Decor": "wall decor",
    "Clocks": "wall clock",
    "Mirrors": "home mirror",

    "Kitchen Appliances": "kitchen appliances",
    "Cookware": "cookware",
    "Bakeware": "bakeware",
    "Kitchen Tools": "kitchen utensils",
    "Dinner Sets": "dinner set",
    "Glassware": "glassware",
    "Water Bottles": "water bottle",
    "Lunch Boxes": "lunch box",
    "Coffee Makers": "coffee maker",
    "Electric Kettles": "electric kettle",
    "Mixer Grinders": "mixer grinder",
    "Air Fryers": "air fryer",
    "Microwave Ovens": "microwave oven",

    "Grocery": "grocery food",
    "Rice": "rice bag food",
    "Atta & Flour": "flour wheat atta",
    "Pulses": "lentils pulses",
    "Cooking Oil": "cooking oil bottle",
    "Spices": "Indian spices",
    "Dry Fruits": "almonds cashews dry fruits",
    "Snacks": "snacks food",
    "Biscuits": "biscuits cookies",
    "Chocolates": "chocolate",
    "Beverages": "beverages drinks",
    "Tea": "tea",
    "Coffee": "coffee",

    "Breakfast Foods": "breakfast food",

    "Sports": "sports equipment",
    "Cricket": "cricket equipment",
    "Football": "football soccer",
    "Basketball": "basketball",
    "Badminton": "badminton racket",
    "Tennis": "tennis racket",
    "Table Tennis": "table tennis",
    "Volleyball": "volleyball",
    "Cycling": "cycling bicycle",
    "Fitness": "fitness equipment",
    "Gym Equipment": "gym equipment",
    "Yoga": "yoga equipment",
    "Running": "running fitness",
    "Sports Accessories": "sports accessories",

    "Toys": "children toys",
    "Educational Toys": "educational toys",
    "Remote Control Toys": "remote control toy",
    "Board Games": "board games",
    "Puzzles": "jigsaw puzzle",
    "Action Figures": "action figures toys",
    "Dolls": "dolls toys",
    "Building Blocks": "building blocks toys",
    "Outdoor Toys": "outdoor toys",
    "Baby Toys": "baby toys",

    "Books": "books",
    "Fiction Books": "fiction books",
    "Non-Fiction Books": "books reading",
    "Academic Books": "academic textbooks",
    "Competitive Exam Books": "competitive exam books",
    "Children's Books": "children books",
    "Comics": "comic books",
    "Self Help Books": "self help books",
    "Business Books": "business books",
    "Technology Books": "technology books",

    "Automotive": "automotive car",
    "Car Accessories": "car accessories",
    "Bike Accessories": "motorcycle accessories",
    "Car Electronics": "car electronics",
    "Car Care": "car cleaning",
    "Bike Care": "motorcycle cleaning",
    "Helmets": "motorcycle helmet",
    "Car Covers": "car cover",
    "Bike Covers": "motorcycle cover",
    "Vehicle Lighting": "car vehicle lights",

    "Travel": "travel accessories",
    "Luggage": "travel luggage",
    "Trolley Bags": "trolley luggage",
    "Backpacks": "backpack",
    "Travel Bags": "travel bag",
    "Travel Accessories": "travel accessories",
    "Travel Organizers": "travel organizer",
    "Passport Holders": "passport holder",

    "Pet Supplies": "pet supplies",
    "Dog Supplies": "dog supplies",
    "Cat Supplies": "cat supplies",
    "Pet Food": "pet food",
    "Pet Toys": "pet toys",
    "Pet Accessories": "pet accessories",

    "Office Supplies": "office supplies",
    "Stationery": "stationery",
    "Pens": "pens",
    "Notebooks": "notebook",
    "Diaries": "diary notebook",
    "Art Supplies": "art supplies",
    "School Supplies": "school supplies",
    "Office Furniture": "office furniture",

    "Baby Products": "baby products",
    "Baby Clothing": "baby clothing",
    "Baby Care": "baby care",
    "Baby Food": "baby food",
    "Diapers": "baby diapers",
    "Baby Accessories": "baby accessories",
}


class Command(BaseCommand):

    help = "Replace all product images with unique Pexels images"

    def handle(self, *args, **kwargs):

        api_key = os.getenv("PEXELS_API_KEY")

        if not api_key:
            self.stdout.write(
                self.style.ERROR(
                    "PEXELS_API_KEY not found in .env"
                )
            )
            return

        headers = {
            "Authorization": api_key
        }

        products_dir = os.path.join(
            settings.MEDIA_ROOT,
            "products"
        )

        os.makedirs(
            products_dir,
            exist_ok=True
        )

        products = list(
            Product.objects
            .select_related("category")
            .order_by("id")
        )

        total = len(products)

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "   DIYAMART UNIQUE PRODUCT IMAGE FIX"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )
        self.stdout.write(
            f"Total products: {total}"
        )
        self.stdout.write("")

        # ------------------------------------------------------------
        # Group products by category
        # ------------------------------------------------------------

        products_by_category = {}

        for product in products:

            category_name = product.category.name

            products_by_category.setdefault(
                category_name,
                []
            ).append(product)

        downloaded = 0
        failed = 0
        duplicate_count = 0

        # Stores hashes of images already used
        used_hashes = set()

        # ------------------------------------------------------------
        # Download different images for every category
        # ------------------------------------------------------------

        for category_name, category_products in products_by_category.items():

            search_term = CATEGORY_SEARCH_TERMS.get(
                category_name,
                category_name
            )

            self.stdout.write("")
            self.stdout.write(
                self.style.WARNING(
                    f"Category: {category_name}"
                )
            )

            self.stdout.write(
                f"Search: {search_term}"
            )

            # --------------------------------------------------------
            # Get many different photos at once
            # --------------------------------------------------------

            try:

                response = requests.get(
                    PEXELS_URL,
                    headers=headers,
                    params={
                        "query": search_term,
                        "per_page": 80,
                        "orientation": "square",
                    },
                    timeout=30
                )

                if response.status_code == 429:

                    self.stdout.write(
                        self.style.WARNING(
                            "Pexels rate limit reached. Waiting 20 seconds..."
                        )
                    )

                    time.sleep(20)

                    response = requests.get(
                        PEXELS_URL,
                        headers=headers,
                        params={
                            "query": search_term,
                            "per_page": 80,
                            "orientation": "square",
                        },
                        timeout=30
                    )

                if response.status_code != 200:

                    self.stdout.write(
                        self.style.ERROR(
                            f"API error: {response.status_code}"
                        )
                    )

                    failed += len(category_products)

                    continue

                data = response.json()

                photos = data.get(
                    "photos",
                    []
                )

                if not photos:

                    self.stdout.write(
                        self.style.ERROR(
                            "No photos found."
                        )
                    )

                    failed += len(category_products)

                    continue

                # ----------------------------------------------------
                # Make sure we have unique photo URLs
                # ----------------------------------------------------

                image_urls = []

                for photo in photos:

                    src = photo.get(
                        "src",
                        {}
                    )

                    image_url = (
                        src.get("large2x")
                        or src.get("large")
                        or src.get("medium")
                    )

                    if image_url and image_url not in image_urls:

                        image_urls.append(
                            image_url
                        )

                # ----------------------------------------------------
                # Download products
                # ----------------------------------------------------

                photo_index = 0

                for product in category_products:

                    if not image_urls:

                        self.stdout.write(
                            self.style.ERROR(
                                f"✗ No unique image available: "
                                f"{product.name}"
                            )
                        )

                        failed += 1

                        continue

                    success_for_product = False

                    # Try multiple photos if one is duplicate
                    for attempt in range(len(image_urls)):

                        image_url = image_urls[
                            (photo_index + attempt)
                            % len(image_urls)
                        ]

                        try:

                            image_response = requests.get(
                                image_url,
                                timeout=30,
                                headers={
                                    "User-Agent":
                                    "DiyaMart Product Image Downloader"
                                }
                            )

                            if image_response.status_code != 200:

                                continue

                            image_data = (
                                image_response.content
                            )

                            if len(image_data) < 5000:

                                continue

                            # ----------------------------------------
                            # Check actual image content
                            # ----------------------------------------

                            image_hash = hashlib.sha256(
                                image_data
                            ).hexdigest()

                            if image_hash in used_hashes:

                                duplicate_count += 1

                                continue

                            # ----------------------------------------
                            # Save physical image
                            # ----------------------------------------

                            filename = (
                                f"product_{product.id}.jpg"
                            )

                            file_path = os.path.join(
                                products_dir,
                                filename
                            )

                            with open(
                                file_path,
                                "wb"
                            ) as image_file:

                                image_file.write(
                                    image_data
                                )

                            # ----------------------------------------
                            # Update Django Product
                            # ----------------------------------------

                            product.image = (
                                f"products/{filename}"
                            )

                            product.save(
                                update_fields=["image"]
                            )

                            used_hashes.add(
                                image_hash
                            )

                            downloaded += 1

                            success_for_product = True

                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"✓ [{product.id}] "
                                    f"{product.name}"
                                )
                            )

                            photo_index += 1

                            break

                        except Exception as e:

                            self.stdout.write(
                                self.style.WARNING(
                                    f"  Image attempt failed: {e}"
                                )
                            )

                    if not success_for_product:

                        failed += 1

                        self.stdout.write(
                            self.style.ERROR(
                                f"✗ Failed: {product.name}"
                            )
                        )

                    # Small delay
                    time.sleep(0.15)

            except Exception as e:

                self.stdout.write(
                    self.style.ERROR(
                        f"Category failed: {category_name}"
                    )
                )

                self.stdout.write(
                    f"Error: {e}"
                )

                failed += len(category_products)

        # ------------------------------------------------------------
        # FINAL REPORT
        # ------------------------------------------------------------

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "       IMAGE FIX COMPLETE"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )

        self.stdout.write(
            f"Total products : {total}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Images replaced: {downloaded}"
            )
        )

        self.stdout.write(
            self.style.WARNING(
                f"Duplicates skipped: {duplicate_count}"
            )
        )

        self.stdout.write(
            self.style.ERROR(
                f"Failed: {failed}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )

        self.stdout.write("")
        self.stdout.write(
            "Images stored in:"
        )
        self.stdout.write(
            products_dir
        )