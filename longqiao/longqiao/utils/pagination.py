from rest_framework.pagination import PageNumberPagination

class StandardResultPagination(PageNumberPagination):
    page_size = 8 # 一页展示多少条数据
    page_size_query_param = 'page_size'
    max_page_size = 20