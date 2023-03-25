from typing import List
from flask import request
from controller.base import BaseResource
from dao.product import get_product_by_id, ProductFilters, get_product_by_filters, delete_product_by_id, create_product, \
    update_product
from http_schema.product import ProductPostSchema, ProductPutSchema
from utils.http_response import error_response, ok_response


class Product(BaseResource):
    def get(self, product_id=None):
        if product_id:
            return ok_response(get_product_by_id(product_id))

        name_search_text = request.args.get('name_search_text', None)
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
        category_ids = [int(x) for x in request.args.get('category_ids', '').split(',') if x] or None
        filters = ProductFilters(name_search_text=name_search_text, category_ids=category_ids)
        products, count = get_product_by_filters(filters, limit=limit, offset=offset)
        return ok_response(
            {
                'results': products,
                'count': count,
                'has_next': (limit + offset) < count,
                'has_previous': offset > 0
            }
        )

    def put(self, product_id):
        request_json = request.json
        request_json['id'] = product_id
        success, parsed_input = ProductPutSchema.parse_json_dataset(request_json)
        if not success:
            return error_response(parsed_input)

        parsed_input: ProductPutSchema

        updated_product = update_product(
            product_id=product_id,
            name=parsed_input.name,
            price=parsed_input.price,
            category_ids=parsed_input.category_ids
        )

        return ok_response(updated_product)

    def post(self):
        # create product/products
        success, parsed_input = ProductPostSchema.parse_json_dataset(request.json['products'])
        if not success:
            return error_response(parsed_input)

        parsed_input: List[parsed_input]
        created_products = []
        product_data: ProductPostSchema
        for product_data in parsed_input:
            product = create_product(
                name=product_data.name,
                price=product_data.price,
                category_ids=product_data.category_ids
            )
            created_products.append(product)
        # todo: for huge payload background jobs
        return ok_response({'created_products': created_products})

    def delete(self, product_id):
        delete_product_by_id(product_id)
        return ok_response({'message': 'Delete Successfully !!'})
