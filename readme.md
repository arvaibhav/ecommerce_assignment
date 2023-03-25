#   Instructions for setting up and running the application.
* python version 3.9
* pip install -r requirements.txt
* python sample_db_setup.py #will add some sample data in database (sqlite used as database)
* python service_app.py #this runs the app

# Details
### Validation Strategy Used
* for schema input checks designed http_schema.base.Base which can be inherited as per required contract
* example http_schema.product.ProductPostSchema


### For class based Api controller 
used flask lib.  Flask-RESTful (flask by default had function based view)


### Orm
used Sqlalchemy and database for simplicity in assignment used sqlite.
db models defined in db/models

### Basic Behaviour
client --> controller --> dao --> db call --> controller response .

### Product Api Behaviour
```
product_view : {
            "id": 4,
            "name": "Dell XPS 13.3-Inch Laptop - Intel Core i7 - 16GB Memory - 512GB Solid State Drive - Platinum Silver",
            "price": 1399.99,
            "category_ids": [
                8,
                9
            ]
}
here category could be any level of subcategory and details of category name and its subcategory
client can get from category api call (not adding in product api) to reduce the cost of extra category detail .
and for category client may can make caching in client side layer in order to reduce cost for getting category detail
```

### Category Api Behaviour
```
category_view : {
    "id": 1,
    "name": "Electronics",
    "subcategories": [
        {
            "id": 5,
            "name": "Mobile Phones",
            "subcategories": []
        },
        {
            "id": 6,
            "name": "Tablets",
            "subcategories": []
        },
        {
            "id": 7,
            "name": "Televisions",
            "subcategories": []
        },
        {
            "id": 8,
            "name": "Computers",
            "subcategories": [
                {
                    "id": 9,
                    "name": "Laptops",
                    "subcategories": []
                },
                {
                    "id": 10,
                    "name": "Desktops",
                    "subcategories": []
                },
                {
                    "id": 11,
                    "name": "Monitors",
                    "subcategories": []
                }
            ]
        },
        {
            "id": 32,
            "name": "Random Category",
            "subcategories": []
        },
        {
            "id": 33,
            "name": "Random Category 22",
            "subcategories": []
        }
    ]
}

here subcategories deepness would be max 3 (which can be increase if required)
```

### for optimization in category tree fetching caching layer required
default used as inmemory , which can be replace with redis (ref dao.category.CachedCategoryMapping)

### postman collection added for ref
ref postman_collection.json 
