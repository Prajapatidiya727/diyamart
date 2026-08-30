from django.core.management.base import BaseCommand
from products.models import Category, Product


class Command(BaseCommand):

    help = "Create products for all DiyaMart categories"

    def handle(self, *args, **kwargs):

        created_count = 0
        existing_count = 0

        # =========================================================
        # PRODUCTS FOR CATEGORIES THAT ALREADY HAVE CUSTOM PRODUCTS
        # =========================================================

        products = {

            # ================= ELECTRONICS =================

            "Mobiles": [
                ("iPhone 16", 79999, 20),
                ("iPhone 16 Pro", 119999, 15),
                ("Samsung Galaxy S25", 74999, 20),
                ("OnePlus 13", 59999, 25),
                ("Google Pixel 9", 69999, 15),
                ("Samsung Galaxy A55", 39999, 30),
                ("Redmi Note 14 Pro", 29999, 35),
                ("Realme GT 6", 39999, 25),
            ],

            "Laptops": [
                ("HP Pavilion 15", 65000, 10),
                ("Dell Inspiron 15", 62000, 12),
                ("Lenovo ThinkPad E14", 65000, 8),
                ("ASUS VivoBook 15", 58000, 15),
                ("Acer Aspire 5", 55000, 12),
                ("MacBook Air M3", 99999, 10),
            ],

            "Tablets": [
                ("Apple iPad 10th Gen", 39999, 15),
                ("Samsung Galaxy Tab S9", 69999, 10),
                ("OnePlus Pad 2", 39999, 20),
                ("Lenovo Tab P12", 29999, 15),
            ],

            "Headphones": [
                ("Sony WH-1000XM5", 29999, 10),
                ("Boat Rockerz 550", 2000, 25),
                ("JBL Tune 760NC", 5999, 20),
                ("Sennheiser HD 450BT", 9999, 15),
            ],

            "Earphones": [
                ("Boat BassHeads 100", 499, 40),
                ("Realme Buds 2", 599, 35),
                ("JBL C100SI", 799, 30),
            ],

            "Earbuds": [
                ("Apple AirPods Pro 2", 24999, 15),
                ("Samsung Galaxy Buds 3", 14999, 20),
                ("OnePlus Buds 3", 5499, 25),
                ("Boat Airdopes 141", 1299, 40),
            ],

            "Smart Watches": [
                ("Apple Watch Series 10", 46999, 12),
                ("Samsung Galaxy Watch 7", 29999, 15),
                ("Noise ColorFit Pro", 3000, 20),
                ("Boat Wave Sigma", 1999, 25),
            ],

            "Smart Bands": [
                ("Mi Smart Band 9", 3499, 20),
                ("Fitbit Inspire 3", 8999, 15),
                ("Realme Band 2", 2999, 25),
            ],

            "Mobile Accessories": [
                ("Fast Charging Cable", 699, 50),
                ("Wireless Charging Pad", 1499, 30),
                ("Phone Stand", 499, 40),
                ("Mobile Ring Holder", 199, 60),
            ],

            "Laptop Accessories": [
                ("Laptop Cooling Pad", 1299, 30),
                ("Laptop Stand", 999, 35),
                ("USB Hub", 1499, 25),
                ("Laptop Sleeve", 799, 40),
            ],

            "Computer Accessories": [
                ("USB Flash Drive 64GB", 699, 50),
                ("External Hard Drive 1TB", 4999, 20),
                ("USB Bluetooth Adapter", 499, 35),
            ],

            "Keyboards": [
                ("Mechanical Gaming Keyboard", 2499, 25),
                ("Wireless Keyboard", 1299, 35),
                ("RGB Gaming Keyboard", 1999, 30),
            ],

            "Mice": [
                ("Wireless Mouse", 500, 50),
                ("Logitech M331 Mouse", 1299, 30),
                ("Gaming RGB Mouse", 1499, 25),
            ],

            "Monitors": [
                ("LG 24 Inch Monitor", 12999, 15),
                ("Samsung 27 Inch Monitor", 18999, 12),
                ("Dell 24 Inch Monitor", 14999, 15),
            ],

            "Speakers": [
                ("JBL Flip 6", 9999, 20),
                ("Boat Stone 350", 1999, 30),
                ("Sony SRS-XB100", 4999, 20),
            ],

            "Televisions": [
                ("Samsung 55 Inch 4K TV", 64999, 10),
                ("LG 43 Inch Smart TV", 39999, 15),
                ("Sony Bravia 55 Inch", 79999, 8),
            ],

            # ================= FASHION =================

            "T-Shirts": [
                ("Men's Cotton T-Shirt", 799, 40),
                ("Premium Oversized T-Shirt", 999, 35),
                ("Printed Casual T-Shirt", 699, 50),
            ],

            "Shirts": [
                ("Men's Formal Shirt", 1499, 30),
                ("Casual Checked Shirt", 1299, 35),
                ("Cotton Full Sleeve Shirt", 1599, 25),
            ],

            "Jeans": [
                ("Slim Fit Blue Jeans", 1999, 30),
                ("Regular Fit Jeans", 1799, 35),
                ("Black Stretch Jeans", 2199, 25),
            ],

            "Sarees": [
                ("Banarasi Silk Saree", 4999, 15),
                ("Cotton Saree", 1499, 25),
                ("Designer Saree", 6999, 10),
            ],

            "Kurtis": [
                ("Printed Cotton Kurti", 999, 30),
                ("Anarkali Kurti", 1499, 25),
                ("Embroidered Kurti", 1999, 20),
            ],

            "Lehengas": [
                ("Designer Wedding Lehenga", 8999, 10),
                ("Bridal Lehenga", 14999, 8),
                ("Party Wear Lehenga", 5999, 15),
            ],

            # ================= FOOTWEAR =================

            "Shoes": [
                ("Men's Casual Shoes", 1999, 30),
                ("Women's Casual Shoes", 1799, 30),
                ("Comfort Walking Shoes", 2499, 25),
            ],

            "Running Shoes": [
                ("Lightweight Running Shoes", 2999, 25),
                ("Professional Running Shoes", 4999, 15),
                ("Comfort Sports Runner", 3499, 20),
            ],

            "Sneakers": [
                ("Classic White Sneakers", 2499, 30),
                ("High Top Sneakers", 2999, 25),
                ("Street Style Sneakers", 3499, 20),
            ],

            "Sandals": [
                ("Women's Comfort Sandals", 999, 35),
                ("Men's Casual Sandals", 1199, 30),
                ("Leather Sandals", 1999, 20),
            ],

            # ================= BEAUTY =================

            "Makeup": [
                ("Matte Lipstick", 599, 40),
                ("Liquid Foundation", 899, 30),
                ("Compact Powder", 499, 35),
                ("Makeup Brush Set", 799, 30),
            ],

            "Skincare": [
                ("Vitamin C Face Serum", 799, 35),
                ("Hydrating Face Cream", 599, 40),
                ("Gentle Face Cleanser", 499, 45),
            ],

            "Hair Care": [
                ("Anti Hair Fall Shampoo", 499, 40),
                ("Hair Conditioner", 399, 45),
                ("Hair Repair Serum", 699, 30),
            ],

            "Perfumes": [
                ("Floral Eau De Parfum", 1499, 25),
                ("Premium Men's Perfume", 1999, 20),
                ("Fresh Citrus Perfume", 1299, 30),
            ],

            # ================= HOME =================

            "Furniture": [
                ("Modern Study Table", 5999, 10),
                ("Wooden Coffee Table", 4999, 12),
                ("Office Chair", 7999, 10),
            ],

            "Home Decor": [
                ("Decorative Vase", 799, 30),
                ("Wall Art Set", 1299, 25),
                ("Decorative Showpiece", 999, 30),
            ],

            "Bedsheets": [
                ("Cotton Double Bedsheet", 1299, 30),
                ("Printed King Size Bedsheet", 1599, 25),
                ("Premium Bedsheet Set", 1999, 20),
            ],

            "Lighting": [
                ("LED Table Lamp", 999, 30),
                ("Smart LED Bulb", 499, 50),
                ("Decorative Floor Lamp", 2499, 15),
            ],

            # ================= KITCHEN =================

            "Cookware": [
                ("Non Stick Frying Pan", 1299, 30),
                ("Stainless Steel Cookware Set", 3999, 15),
                ("Pressure Cooker 5L", 2499, 20),
            ],

            "Air Fryers": [
                ("Digital Air Fryer 4L", 4999, 15),
                ("Air Fryer 6L", 6999, 10),
                ("Compact Air Fryer", 3499, 20),
            ],

            "Mixer Grinders": [
                ("750W Mixer Grinder", 2999, 20),
                ("500W Mixer Grinder", 2299, 25),
                ("Premium Mixer Grinder", 4499, 15),
            ],

            "Water Bottles": [
                ("Stainless Steel Water Bottle", 699, 40),
                ("Insulated Water Bottle", 999, 35),
                ("Sports Water Bottle", 499, 50),
            ],

            # ================= GROCERY =================

            "Rice": [
                ("Basmati Rice 5kg", 699, 50),
                ("Premium Basmati Rice 5kg", 899, 40),
                ("Sona Masoori Rice 5kg", 599, 45),
            ],

            "Atta & Flour": [
                ("Whole Wheat Atta 5kg", 299, 60),
                ("Multigrain Atta 5kg", 399, 50),
                ("Besan 1kg", 119, 60),
            ],

            "Spices": [
                ("Turmeric Powder 200g", 89, 70),
                ("Red Chilli Powder 200g", 99, 65),
                ("Garam Masala 100g", 129, 60),
            ],

            "Dry Fruits": [
                ("Premium Almonds 500g", 499, 40),
                ("Cashews 500g", 599, 35),
                ("Pistachios 250g", 399, 40),
            ],

            "Biscuits": [
                ("Chocolate Cream Biscuits", 50, 80),
                ("Butter Cookies", 120, 70),
                ("Digestive Biscuits", 90, 75),
            ],

            # ================= SPORTS =================

            "Cricket": [
                ("English Willow Cricket Bat", 8999, 15),
                ("Kashmir Willow Cricket Bat", 2999, 25),
                ("Cricket Ball", 499, 50),
                ("Cricket Batting Gloves", 1299, 30),
            ],

            "Football": [
                ("Professional Football", 1999, 25),
                ("Training Football", 999, 35),
                ("Football Goal Net", 1499, 20),
            ],

            "Badminton": [
                ("Carbon Fiber Badminton Racket", 2499, 25),
                ("Professional Badminton Racket", 3999, 15),
                ("Badminton Shuttlecock Set", 699, 40),
            ],

            "Yoga": [
                ("Premium Yoga Mat", 1299, 35),
                ("Non Slip Yoga Mat", 999, 40),
                ("Yoga Block Set", 599, 45),
            ],

            "Fitness": [
                ("Adjustable Dumbbells", 2999, 20),
                ("Resistance Bands Set", 799, 40),
                ("Fitness Skipping Rope", 399, 50),
            ],

            # ================= TOYS =================

            "Toys": [
                ("Kids Building Toy Set", 999, 30),
                ("Musical Toy Set", 799, 35),
                ("Creative Activity Kit", 599, 40),
            ],

            "Educational Toys": [
                ("Kids Learning Tablet", 1999, 20),
                ("Alphabet Learning Set", 499, 40),
                ("Math Learning Game", 699, 35),
            ],

            "Board Games": [
                ("Classic Chess Board", 799, 30),
                ("Family Board Game", 999, 25),
                ("Strategy Board Game", 1299, 20),
            ],

            "Puzzles": [
                ("100 Piece Jigsaw Puzzle", 399, 40),
                ("500 Piece Puzzle", 699, 30),
                ("Kids Puzzle Set", 299, 50),
            ],

            # ================= BOOKS =================

            "Books": [
                ("The Complete Fiction Collection", 599, 20),
                ("Modern Knowledge Encyclopedia", 799, 15),
                ("World Stories Collection", 499, 25),
            ],

            "Fiction Books": [
                ("The Mystery House", 399, 30),
                ("Journey Beyond Stars", 499, 25),
                ("The Lost Kingdom", 449, 30),
            ],

            "Academic Books": [
                ("Computer Science Fundamentals", 699, 20),
                ("Data Science Handbook", 899, 20),
                ("Database Management Systems", 799, 25),
            ],

            "Technology Books": [
                ("Python Programming Guide", 799, 25),
                ("Django Web Development", 899, 20),
                ("Machine Learning Basics", 999, 15),
            ],

            # ================= AUTOMOTIVE =================

            "Car Accessories": [
                ("Car Mobile Holder", 599, 40),
                ("Car Floor Mat Set", 1999, 20),
                ("Car Seat Cushion", 999, 30),
            ],

            "Bike Accessories": [
                ("Bike Mobile Holder", 699, 35),
                ("Bike Seat Cover", 499, 40),
                ("Bike Cleaning Kit", 799, 30),
            ],

            "Helmets": [
                ("ISI Certified Helmet", 1499, 30),
                ("Full Face Helmet", 2499, 20),
                ("Premium Riding Helmet", 3999, 15),
            ],

            # ================= TRAVEL =================

            "Luggage": [
                ("Hard Shell Luggage Trolley", 4999, 15),
                ("Lightweight Travel Luggage", 3999, 20),
                ("Premium Luggage Set", 7999, 10),
            ],

            "Backpacks": [
                ("Laptop Backpack", 1499, 30),
                ("College Backpack", 999, 40),
                ("Travel Backpack", 1999, 25),
            ],

            "Travel Accessories": [
                ("Travel Pillow", 699, 35),
                ("Travel Adapter", 999, 30),
                ("Luggage Organizer Set", 799, 40),
            ],

            # ================= PETS =================

            "Pet Supplies": [
                ("Pet Grooming Kit", 999, 25),
                ("Pet Feeding Bowl", 499, 40),
                ("Pet Bed", 1999, 20),
            ],

            "Dog Supplies": [
                ("Dog Collar", 399, 40),
                ("Dog Leash", 599, 35),
                ("Dog Grooming Brush", 499, 30),
            ],

            "Cat Supplies": [
                ("Cat Scratching Post", 1499, 20),
                ("Cat Feeding Bowl", 399, 40),
                ("Cat Toy Set", 599, 35),
            ],

            # ================= OFFICE =================

            "Stationery": [
                ("Premium Stationery Set", 499, 40),
                ("Office Stationery Kit", 699, 35),
                ("Student Stationery Kit", 399, 50),
            ],

            "Pens": [
                ("Ball Pen Pack of 10", 199, 80),
                ("Premium Gel Pen Set", 299, 60),
                ("Executive Pen", 499, 40),
            ],

            "Notebooks": [
                ("A5 Ruled Notebook", 149, 80),
                ("Premium Hardcover Notebook", 299, 60),
                ("Spiral Notebook", 199, 70),
            ],

            # ================= BABY =================

            "Baby Products": [
                ("Baby Care Gift Set", 1299, 25),
                ("Newborn Baby Kit", 999, 30),
                ("Baby Essentials Set", 1499, 20),
            ],

            "Baby Clothing": [
                ("Baby Cotton Romper", 499, 40),
                ("Baby Dress Set", 799, 30),
                ("Newborn Clothing Set", 999, 25),
            ],

            "Baby Care": [
                ("Baby Gentle Shampoo", 299, 40),
                ("Baby Lotion", 349, 45),
                ("Baby Bath Kit", 599, 30),
            ],

            "Diapers": [
                ("Newborn Diapers Pack", 699, 40),
                ("Baby Diapers Medium Pack", 799, 35),
                ("Baby Diapers Large Pack", 899, 30),
            ],

            "Baby Accessories": [
                ("Baby Feeding Bottle", 399, 40),
                ("Baby Bib Set", 299, 50),
                ("Baby Grooming Kit", 499, 35),
            ],
        }

        # =========================================================
        # STEP 1 — CREATE THE PRODUCTS ALREADY DEFINED ABOVE
        # =========================================================

        for category_name, product_list in products.items():

            try:
                category = Category.objects.get(name=category_name)

            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Category not found: {category_name}"
                    )
                )
                continue

            for product_name, price, stock in product_list:

                product, created = Product.objects.get_or_create(
                    name=product_name,
                    category=category,
                    defaults={
                        "description": (
                            f"High quality {product_name} "
                            f"available at DiyaMart."
                        ),
                        "price": price,
                        "stock": stock,
                    }
                )

                if created:
                    created_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created: {product_name} → {category_name}"
                        )
                    )

                else:
                    existing_count += 1

        # =========================================================
        # STEP 2 — FIND CATEGORIES WITHOUT PRODUCTS
        # =========================================================

        self.stdout.write("")
        self.stdout.write(
            self.style.WARNING(
                "Checking categories without products..."
            )
        )

        empty_categories = Category.objects.filter(
            product__isnull=True
        )

        # =========================================================
        # STEP 3 — AUTOMATICALLY CREATE 3 PRODUCTS
        #             FOR EVERY EMPTY CATEGORY
        # =========================================================

        for category in empty_categories:

            category_name = category.name

            automatic_products = [

                (
                    f"{category_name} Essential",
                    499,
                    25
                ),

                (
                    f"Premium {category_name}",
                    999,
                    20
                ),

                (
                    f"{category_name} Special",
                    1499,
                    15
                ),
            ]

            for product_name, price, stock in automatic_products:

                # Extra safety:
                # Don't create duplicate products.

                product, created = Product.objects.get_or_create(
                    name=product_name,
                    category=category,
                    defaults={
                        "description": (
                            f"High quality {category_name} product "
                            f"available at DiyaMart. "
                            f"Perfect choice for everyday use."
                        ),
                        "price": price,
                        "stock": stock,
                    }
                )

                if created:

                    created_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created automatic product: "
                            f"{product_name} → {category_name}"
                        )
                    )

                else:

                    existing_count += 1

        # =========================================================
        # FINAL SUMMARY
        # =========================================================

        total_categories = Category.objects.count()
        total_products = Product.objects.count()

        categories_with_products = (
            Category.objects
            .filter(product__isnull=False)
            .distinct()
            .count()
        )

        categories_without_products = (
            Category.objects
            .filter(product__isnull=True)
            .count()
        )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "       DIYAMART PRODUCT SEEDING DONE"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )

        self.stdout.write(
            f"Total Categories: {total_categories}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Categories WITH products: "
                f"{categories_with_products}"
            )
        )

        self.stdout.write(
            self.style.WARNING(
                f"Categories WITHOUT products: "
                f"{categories_without_products}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"New products created: {created_count}"
            )
        )

        self.stdout.write(
            f"Existing products: {existing_count}"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"TOTAL PRODUCTS: {total_products}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "=========================================="
            )
        )