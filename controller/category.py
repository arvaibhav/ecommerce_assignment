from controller.base import BaseResource
from http_schema.category import CategoryPostSchema, CategoryPutSchema
from dao.category import delete_category_by_id, create_category, update_category, get_category_by_id, \
    get_categories_by_filters
from utils.http_response import ok_response, error_response
from flask import request


class ProductCategory(BaseResource):
    def get(self, category_id=None):
        if category_id:
            category = get_category_by_id(category_id)
            return ok_response(category)
        else:
            limit = int(request.args.get('limit', 10))
            offset = int(request.args.get('offset', 0))
            categories, count = get_categories_by_filters(limit, offset)
            return ok_response(
                {
                    'results': categories,
                    'count': count,
                    'has_next': (limit + offset) < count,
                    'has_previous': offset > 0
                }
            )

    def put(self, category_id):
        request_json = request.json
        request_json['id'] = category_id
        success, parsed_input = CategoryPutSchema.parse_json_dataset(request_json)
        if not success:
            return error_response(parsed_input)

        parsed_input: CategoryPutSchema

        updated_product = update_category(
            category_id=category_id,
            name=parsed_input.name,
            parent_ids=parsed_input.parent_ids
        )
        return ok_response(updated_product)

    def post(self):
        success, parsed_input = CategoryPostSchema.parse_json_dataset(request.json)
        if not success:
            return error_response(parsed_input)

        parsed_input: CategoryPostSchema
        category_data: CategoryPostSchema
        category = create_category(
            name=parsed_input.name,
            parent_ids=parsed_input.parent_ids
        )
        return ok_response(category)

    def delete(self, category_id):
        delete_category_by_id(category_id)
        return ok_response({'message': 'Delete Successfully !!'})
