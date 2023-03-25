import os
from dao.product import create_product, get_product_by_filters, ProductFilters

try:
    os.remove('data.db')
except:
    pass
from dao.category import create_category
from db.create_tables import create_table

sample_categories = [
    {'name': 'Electronics', 'parent_ids': []},
    {'name': 'Mobile Phones', 'parent_ids': ['Electronics']},
    {'name': 'Tablets', 'parent_ids': ['Electronics']},
    {'name': 'Televisions', 'parent_ids': ['Electronics']},
    {'name': 'Computers', 'parent_ids': ['Electronics']},
    {'name': 'Laptops', 'parent_ids': ['Computers']},
    {'name': 'Desktops', 'parent_ids': ['Computers']},
    {'name': 'Monitors', 'parent_ids': ['Computers']},
    {'name': 'Home & Kitchen', 'parent_ids': []},
    {'name': 'Bedding', 'parent_ids': ['Home & Kitchen']},
    {'name': 'Kitchen & Dining', 'parent_ids': ['Home & Kitchen']},
    {'name': 'Small Appliances', 'parent_ids': ['Home & Kitchen']},
    {'name': 'Coffee & Tea', 'parent_ids': ['Home & Kitchen', 'Kitchen & Dining']},
    {'name': 'Cookware', 'parent_ids': ['Home & Kitchen', 'Kitchen & Dining']},
    {'name': 'Dining & Entertaining', 'parent_ids': ['Home & Kitchen', 'Kitchen & Dining']},
    {'name': 'Appliances', 'parent_ids': ['Home & Kitchen', 'Kitchen & Dining']},
    {'name': 'Furniture', 'parent_ids': []},
    {'name': 'Living Room Furniture', 'parent_ids': ['Furniture']},
    {'name': 'Bedroom Furniture', 'parent_ids': ['Furniture']},
    {'name': 'Office Furniture', 'parent_ids': ['Furniture']},
    {'name': 'Chairs', 'parent_ids': ['Furniture', 'Office Furniture']},
    {'name': 'Desks', 'parent_ids': ['Furniture', 'Office Furniture']},
    {'name': 'Clothing, Shoes & Jewelry', 'parent_ids': []},
    {'name': "Women's Clothing", 'parent_ids': ['Clothing, Shoes & Jewelry']},
    {'name': "Men's Clothing", 'parent_ids': ['Clothing, Shoes & Jewelry']},
    {'name': 'Shirts', 'parent_ids': ["Men's Clothing", "Women's Clothing"]},
    {'name': 'Jeans', 'parent_ids': ["Men's Clothing", "Women's Clothing"]},
    {'name': 'Shoes', 'parent_ids': ['Clothing, Shoes & Jewelry']},
    {'name': 'Athletic Shoes', 'parent_ids': ['Shoes']},
    {'name': 'Dress Shoes', 'parent_ids': ['Shoes']},
    {'name': 'Jewelry', 'parent_ids': ['Clothing, Shoes & Jewelry']}
]

sample_products = [
    {
        "name": "Apple iPhone 12 - 64GB - Blue",
        "price": 799.99,
        "categories": ["Mobile Phones"]
    },
    {
        "name": "Samsung Galaxy Tab S7 - 128GB - Mystic Black",
        "price": 549.99,
        "categories": ["Tablets"]
    },
    {
        "name": "Samsung 55-Inch Class QLED Q70T Series 4K UHD Smart TV",
        "price": 999.99,
        "categories": ["Televisions"]
    },
    {
        "name": "Dell XPS 13.3-Inch Laptop - Intel Core i7 - 16GB Memory - 512GB Solid State Drive - Platinum Silver",
        "price": 1399.99,
        "categories": ["Laptops", "Computers"]
    },
    {
        "name": "HP Pavilion 23.8-Inch All-in-One Desktop - Intel Core i5 - 12GB Memory - 256GB Solid State Drive - Snowflake White",
        "price": 799.99,
        "categories": ["Desktops", "Computers"]
    },
    {
        "name": "ASUS ProArt 32-Inch 4K UHD Monitor - Black",
        "price": 999.99,
        "categories": ["Monitors", "Computers"]
    }, {
        "name": "Sony WH-1000XM4 Wireless Noise-Canceling Over-Ear Headphones",
        "price": 349.99,
        "categories": ["Electronics"]
    },
    {
        "name": "Apple iPad Air 10.9-Inch - Wi-Fi - 64GB - Sky Blue",
        "price": 599.99,
        "categories": ["Tablets"]
    },
    {
        "name": "LG OLED65CXPUA 65-Inch 4K Smart OLED TV",
        "price": 2196.99,
        "categories": ["Televisions"]
    },
    {
        "name": "Lenovo ThinkPad X1 Carbon Gen 9 14-Inch Laptop - Intel Core i7 - 16GB Memory - 512GB Solid State Drive - Black",
        "price": 1649.99,
        "categories": ["Laptops", "Computers"]
    },
    {
        "name": "HP EliteOne 1000 G2 23.8-Inch All-in-One Desktop - Intel Core i7 - 16GB Memory - 512GB Solid State Drive - Black/Silver",
        "price": 1699.99,
        "categories": ["Desktops", "Computers"]
    },
    {
        "name": "Dell UltraSharp 32-Inch 4K USB-C Monitor - Black",
        "price": 1199.99,
        "categories": ["Monitors", "Computers"]
    },
    {
        "name": "Instant Pot Duo 7-in-1 Electric Pressure Cooker - 6 Quart",
        "price": 79.99,
        "categories": ["Small Appliances", "Kitchen & Dining"]
    },
    {
        "name": "Calphalon Premier Space-Saving Hard-Anodized Nonstick Cookware Set - 15 Piece",
        "price": 649.99,
        "categories": ["Cookware", "Kitchen & Dining"]
    },
    {
        "name": "Riedel Vinum XL Cabernet Wine Glass - Set of 2",
        "price": 69.99,
        "categories": ["Dining & Entertaining", "Kitchen & Dining"]
    },
    {
        "name": "Cuisinart PurePrecision Pour-Over Coffee Brewer - Stainless Steel",
        "price": 199.99,
        "categories": ["Coffee & Tea", "Kitchen & Dining"]
    },
    {
        "name": "Breville Barista Express Espresso Machine - Stainless Steel",
        "price": 699.99,
        "categories": ["Appliances", "Kitchen & Dining"]
    },
    {
        "name": "Ashley Furniture Signature Design - Ralene Upholstered Dining Room Bench - Rustic Finish",
        "price": 99.99,
        "categories": ["Dining & Entertaining", "Home & Kitchen"]
    },
    {
        "name": "Zinus Shalini Upholstered Platform Bed Frame - Queen - Dark Grey",
        "price": 289.99,
        "categories": ["Bedroom Furniture", "Furniture"]
    },
    {
        "name": "Lorell SOHO 18-Inch 3-Drawer Vertical File Cabinet - Black",
        "price": 109.99,
        "categories": ["Office Furniture", "Furniture"]
    },
    {"name": "Executive Office Chair", "price": 299.99, "categories": ["Office Furniture", "Chairs"]},
    {"name": "L-Shaped Desk", "price": 499.99, "categories": ["Office Furniture", "Desks"]},
    {"name": "Slim Fit Button-Down Shirt", "price": 49.99, "categories": ["Men's Clothing", "Shirts"]},
    {"name": "Straight Leg Jeans", "price": 79.99, "categories": ["Men's Clothing", "Jeans"]},
    {"name": "Athletic Sneakers", "price": 99.99, "categories": ["Shoes", "Athletic Shoes"]},
    {"name": "Leather Loafers", "price": 129.99, "categories": ["Shoes", "Dress Shoes"]}
]

create_table()
category_name_id_map = {}
for category in sorted(sample_categories, key=lambda c: c['parent_ids'] == [], reverse=True):
    if category['parent_ids']:
        parent_ids = [category_name_id_map[x] for x in category['parent_ids']]
    else:
        parent_ids = None
    created_category = create_category(
        name=category['name'],
        parent_ids=parent_ids
    )
    category_name_id_map[created_category['name']] = created_category['id']

for product in sample_products:
    created_product = create_product(
        name=product['name'],
        price=product['price'],
        category_ids=[category_name_id_map[c] for c in product['categories']]
    )

print(get_product_by_filters(
    ProductFilters(
        name="Leather Loafers"
    )
))


# catefory :[parent. ... ]
#  category : [child ... ]
