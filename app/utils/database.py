# Mock data for users and orders
users_db = {
    "ndiyoedward@gmail.com": {
        "name": "Edward",
        "email": "ndiyoedward@gmail.com",  # Add email to user data
        "otp": "123456",
        "phone_number": "+2348073342004",
        "date_joined": "2023-01-01",  # Add date_joined
        "reward_points": 100,  # Add reward_points
        "orders": {
            "pending_orders": [
                {"id": "ORD123", "product": "iPhone 14 Pro", "price": "$999", "status": "Pending", "seller_id": "seller_123"},
                {"id": "ORD456", "product": "Samsung Galaxy S23", "price": "$899", "status": "Processing", "seller_id": "seller_456"},
            ],
            "order_history": [
                {"id": "ORD789", "product": "MacBook Air M2", "price": "$1199", "status": "Delivered", "seller_id": "seller_789"},
            ],
        },
    }
}

# Mock database to store messages (replace with your actual database)
messages_db = {
    "buyer1@example.com": [
        {"sender": "buyer1@example.com", "message": "Hi, is this available?", "timestamp": "2023-10-01 10:00:00"},
        {"sender": "seller@example.com", "message": "Yes, it is!", "timestamp": "2023-10-01 10:05:00"},
    ],
    "buyer2@example.com": [
        {"sender": "buyer2@example.com", "message": "What's the price?", "timestamp": "2023-10-02 12:00:00"},
    ],
}

# Mock function to fetch matching products (replace with actual database query)
def fetch_matching_products(product_name: str):
    """Simulate fetching top 3 matching products."""
    return [
         {"id": "ORD123", "name": "iPhone 14 Pro", "image": "https://pin.it/6bukAcfm5", "price": "$999", "details": "Color: Red, Size: M"},
        {"id": "ORD456", "name": "Samsung Galaxy S23", "image": "https://pin.it/6bukAcfm5", "price": "$899", "details": "Color: Blue, Size: L"},
        {"id": "ORD789", "name": "MacBook Air M2", "image": "https://pin.it/6bukAcfm5", "price": "$1199", "details": "Color: Green, Size: S"},
        {"id": "ORD789", "name": "MacBook Air M2", "image": "https://pin.it/6bukAcfm5", "price": "$1199", "details": "Color: Green, Size: S"},

    ]

# Mock product database - for compare module

compare_product_db = {
    "iphone 13": {
        "price": "$799",
        "features": "6.1\" Display, A15 Bionic Chip, Dual Camera",
        "image": "https://pin.it/6bukAcfm5"  # Add image link
    },
    "samsung galaxy s21": {
        "price": "$749",
        "features": "6.2\" Display, Exynos 2100, Triple Camera",
        "image": "https://pin.it/6bukAcfm5"  # Add image link
    },
    "google pixel 6": {
        "price": "$599",
        "features": "6.4\" Display, Google Tensor, Dual Camera",
        "image": "https://pin.it/6bukAcfm5"  # Add image link
    },
    "oneplus 9": {
        "price": "$729",
        "features": "6.55\" Display, Snapdragon 888, Triple Camera",
        "image": "https://pin.it/6bukAcfm5"  # Add image link
    },
    "xiaomi mi 11": {
        "price": "$699",
        "features": "6.81\" Display, Snapdragon 888, Triple Camera",
        "image": "https://pin.it/6bukAcfm5"  # Add image link
    }
}


# Mock data for products
products_db = {
    "gadgets": {
        "smartphones": {
            "Apple": [
                {"id": 1, "name": "iPhone 14 Pro", "price": "$999", "specs": "128GB, 6GB RAM", "image": "https://pin.it/6bukAcfm5"},
                {"id": 2, "name": "iPhone 13", "price": "$799", "specs": "128GB, 4GB RAM", "image": "https://pin.it/6bukAcfm5"},
                {"id": 3, "name": "iPhone SE", "price": "$429", "specs": "64GB, 3GB RAM", "image": "https://pin.it/6bukAcfm5"},
            ],
            "Samsung": [
                {"id": 4, "name": "Samsung Galaxy S23", "price": "$899", "specs": "256GB, 8GB RAM", "image": "https://example.com/s23.jpg"},
                {"id": 5, "name": "Samsung A54", "price": "$499", "specs": "128GB, 6GB RAM", "image": "https://example.com/a54.jpg"},
                {"id": 6, "name": "Samsung Z Flip", "price": "$999", "specs": "256GB, 8GB RAM", "image": "https://example.com/zflip.jpg"},
            ],
            "Xiaomi": [
                {"id": 7, "name": "Xiaomi 13 Pro", "price": "$799", "specs": "256GB, 12GB RAM", "image": "https://example.com/xiaomi13.jpg"},
                {"id": 8, "name": "Xiaomi Redmi Note 12", "price": "$299", "specs": "128GB, 6GB RAM", "image": "https://example.com/redmi12.jpg"},
            ]
        },
        "smartwatches": {
            "Apple": [
                {"id": 9, "name": "Apple Watch Series 8", "price": "$399", "specs": "GPS, 41mm", "image": "https://example.com/watch8.jpg"},
                {"id": 10, "name": "Apple Watch Ultra", "price": "$799", "specs": "GPS, 49mm", "image": "https://example.com/watchultra.jpg"},
            ],
            "Samsung": [
                {"id": 11, "name": "Samsung Galaxy Watch 5", "price": "$299", "specs": "Wear OS, 44mm", "image": "https://example.com/watch5.jpg"},
                {"id": 12, "name": "Samsung Galaxy Watch 4", "price": "$249", "specs": "Wear OS, 40mm", "image": "https://example.com/watch4.jpg"},
            ],
            "Fitbit": [
                {"id": 13, "name": "Fitbit Sense 2", "price": "$299", "specs": "GPS, Heart Rate Monitor", "image": "https://example.com/fitbitsense2.jpg"},
                {"id": 14, "name": "Fitbit Versa 4", "price": "$229", "specs": "GPS, Sleep Tracking", "image": "https://example.com/fitbitversa4.jpg"},
            ]
        },
        "laptops": {
            "Apple": [
                {"id": 15, "name": "MacBook Air M2", "price": "$1199", "specs": "13.6-inch, 8GB RAM", "image": "https://pin.it/6bukAcfm5"},
                {"id": 16, "name": "MacBook Pro 14", "price": "$1999", "specs": "14-inch, 16GB RAM", "image": "https://pin.it/6bukAcfm5"},
            ],
            "Dell": [
                {"id": 17, "name": "Dell XPS 13", "price": "$999", "specs": "13.4-inch, 8GB RAM", "image": "https://example.com/dellxps13.jpg"},
                {"id": 18, "name": "Dell Inspiron 15", "price": "$799", "specs": "15.6-inch, 16GB RAM", "image": "https://example.com/dellinspiron15.jpg"},
            ],
            "HP": [
                {"id": 19, "name": "HP Spectre x360", "price": "$1299", "specs": "13.5-inch, 16GB RAM", "image": "https://example.com/hpspectre.jpg"},
                {"id": 20, "name": "HP Envy 13", "price": "$899", "specs": "13.3-inch, 8GB RAM", "image": "https://example.com/hpenvy13.jpg"},
            ]
        }
    },
    "home_appliances": {
        "kitchen": {
            "LG": [
                {"id": 21, "name": "LG Microwave", "price": "$120", "specs": "20L, Auto Cook", "image": "https://example.com/microwave.jpg"},
                {"id": 22, "name": "LG Refrigerator", "price": "$899", "specs": "20 cu. ft., Smart Inverter", "image": "https://example.com/lgfridge.jpg"},
            ],
            "Samsung": [
                {"id": 23, "name": "Samsung Refrigerator", "price": "$999", "specs": "22 cu. ft., Twin Cooling", "image": "https://example.com/samsungfridge.jpg"},
                {"id": 24, "name": "Samsung Washer", "price": "$799", "specs": "Front Load, 10kg", "image": "https://example.com/samsungwasher.jpg"},
            ]
        },
        "cleaning": {
            "Dyson": [
                {"id": 25, "name": "Dyson V11 Vacuum", "price": "$599", "specs": "Cordless, 60min Runtime", "image": "https://example.com/dysonv11.jpg"},
                {"id": 26, "name": "Dyson Pure Cool", "price": "$399", "specs": "Air Purifier, HEPA Filter", "image": "https://example.com/dysonpure.jpg"},
            ],
            "Shark": [
                {"id": 27, "name": "Shark Navigator", "price": "$199", "specs": "Upright Vacuum, HEPA Filter", "image": "https://example.com/sharknavigator.jpg"},
                {"id": 28, "name": "Shark Steam Mop", "price": "$129", "specs": "Steam Cleaning, Washable Pads", "image": "https://example.com/sharksteam.jpg"},
            ]
        }
    },
    "clothes": {
        "men": {
            "Nike": [
                {"id": 29, "name": "Nike Air Max", "price": "$150", "specs": "Size 10, Black", "image": "https://example.com/nikeairmax.jpg"},
                {"id": 30, "name": "Nike T-Shirt", "price": "$25", "specs": "Size M, White", "image": "https://example.com/niketshirt.jpg"},
            ],
            "Adidas": [
                {"id": 31, "name": "Adidas Ultraboost", "price": "$180", "specs": "Size 9, Blue", "image": "https://example.com/adidasultraboost.jpg"},
                {"id": 32, "name": "Adidas Hoodie", "price": "$60", "specs": "Size L, Black", "image": "https://example.com/adidashoodie.jpg"},
            ]
        },
        "women": {
            "Zara": [
                {"id": 33, "name": "Zara Dress", "price": "$49", "specs": "Size S, Red", "image": "https://example.com/zaradress.jpg"},
                {"id": 34, "name": "Zara Blouse", "price": "$39", "specs": "Size M, White", "image": "https://example.com/zarablouse.jpg"},
            ],
            "H&M": [
                {"id": 35, "name": "H&M Jeans", "price": "$29", "specs": "Size 28, Blue", "image": "https://example.com/hmjeans.jpg"},
                {"id": 36, "name": "H&M Jacket", "price": "$59", "specs": "Size M, Black", "image": "https://example.com/hmjacket.jpg"},
            ]
        }
    },
    "food": {
        "snacks": {
            "Lays": [
                {"id": 37, "name": "Lays Classic", "price": "$2", "specs": "200g, Salted", "image": "https://example.com/laysclassic.jpg"},
                {"id": 38, "name": "Lays Barbecue", "price": "$2", "specs": "200g, Barbecue Flavor", "image": "https://example.com/laysbbq.jpg"},
            ],
            "Pringles": [
                {"id": 39, "name": "Pringles Original", "price": "$3", "specs": "150g, Salted", "image": "https://example.com/pringlesoriginal.jpg"},
                {"id": 40, "name": "Pringles Sour Cream", "price": "$3", "specs": "150g, Sour Cream Flavor", "image": "https://example.com/pringlessourcream.jpg"},
            ]
        },
        "beverages": {
            "Coca-Cola": [
                {"id": 41, "name": "Coca-Cola Classic", "price": "$1", "specs": "330ml, Canned", "image": "https://example.com/cocacola.jpg"},
                {"id": 42, "name": "Coca-Cola Zero", "price": "$1", "specs": "330ml, Sugar-Free", "image": "https://example.com/cocacolazero.jpg"},
            ],
            "Pepsi": [
                {"id": 43, "name": "Pepsi Classic", "price": "$1", "specs": "330ml, Canned", "image": "https://example.com/pepsi.jpg"},
                {"id": 44, "name": "Pepsi Max", "price": "$1", "specs": "330ml, Sugar-Free", "image": "https://example.com/pepsimax.jpg"},
            ]
        }
    }
}