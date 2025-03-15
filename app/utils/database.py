# products_db = {
#     "home_appliances": [
#         {"id": 1, "name": "Air Conditioner", "price": "$300", "specs": "1.5HP, Inverter Technology", "image": "https://example.com/ac.jpg"},
#         {"id": 2, "name": "Refrigerator", "price": "$500", "specs": "250L, Double Door", "image": "https://example.com/fridge.jpg"},
#     ],
#     "clothes": [
#         {"id": 3, "name": "Men’s Suit", "price": "$120", "specs": "Slim Fit, Black", "image": "https://example.com/suit.jpg"},
#         {"id": 4, "name": "Women’s Dress", "price": "$80", "specs": "Evening Gown, Red", "image": "https://example.com/dress.jpg"},
#     ],
#     "gadgets": [
#         {"id": 5, "name": "Smartphone", "price": "$1000", "specs": "128GB, 8GB RAM, 5G Enabled", "image": "https://pin.it/6ZlSp3cYJ"},
#         {"id": 6, "name": "Wireless Earbuds", "price": "$150", "specs": "Noise Cancelling, Bluetooth 5.0", "image": "https://example.com/earbuds.jpg"},
#         {"id": 7, "name": "Smart Watch", "price": "$200", "specs": "Waterproof, Heart Rate Monitor", "image": "https://example.com/watch.jpg"},
#     ],
#     "food": [
#         {"id": 8, "name": "Pizza", "price": "$10", "specs": "Pepperoni, Large Size", "image": "https://example.com/pizza.jpg"},
#         {"id": 9, "name": "Burger", "price": "$5", "specs": "Cheese, Beef Patty", "image": "https://example.com/burger.jpg"},
#     ],
# }



products_db = {
    "gadgets": {
        "smartphones": {
            "Apple": [
                {"id": 1, "name": "iPhone 14 Pro", "price": "$999", "specs": "128GB, 6GB RAM", "image": "https://example.com/iphone14.jpg"},
                {"id": 2, "name": "iPhone 13", "price": "$799", "specs": "128GB, 4GB RAM", "image": "https://example.com/iphone13.jpg"},
            ],
            "Samsung": [
                {"id": 3, "name": "Samsung Galaxy S23", "price": "$899", "specs": "256GB, 8GB RAM", "image": "https://example.com/s23.jpg"},
                {"id": 4, "name": "Samsung A54", "price": "$499", "specs": "128GB, 6GB RAM", "image": "https://example.com/a54.jpg"},
            ]
        },
        "smartwatches": {
            "Apple": [
                {"id": 5, "name": "Apple Watch Series 8", "price": "$399", "specs": "GPS, 41mm", "image": "https://example.com/watch8.jpg"},
            ],
            "Samsung": [
                {"id": 6, "name": "Samsung Galaxy Watch 5", "price": "$299", "specs": "Wear OS, 44mm", "image": "https://example.com/watch5.jpg"},
            ]
        }
    },
    "home_appliances": {
        "kitchen": {
            "LG": [
                {"id": 7, "name": "LG Microwave", "price": "$120", "specs": "20L, Auto Cook", "image": "https://example.com/microwave.jpg"}
            ]
        }
    }
}
