from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets, status
from rest_framework.response import Response


class CrudViewSet(viewsets.GenericViewSet):
    """
    Base view class for CRUD operations.
    Child classes must define `queryset` and `serializer_class`.
    Optionally, `custom_field_model` and `custom_field_value_model` can also be set.
    """

    queryset = None  # Should be defined in the child class
    serializer_class = None  # Should be defined in the child class
    custom_field_model = None  # Optional, should be defined in the child class if needed
    custom_field_value_model = None  # Optional, should be defined in the child class if needed

    def get_serializer_context(self):
        context = super().get_serializer_context()

        # Add custom field models to context if they are defined
        if self.custom_field_model:
            context["custom_field_model"] = self.custom_field_model
        if self.custom_field_value_model:
            context["custom_field_value_model"] = self.custom_field_value_model

        return context

    def get_list_fields(self):
        """
        This method should be overridden by child class to define the list fields,
        or the child class should define a `list_fields` attribute.
        """
        if hasattr(self, 'list_fields') and isinstance(self.list_fields, dict) and self.list_fields:
            return self.list_fields
        else:
            raise ImproperlyConfigured("Django Access Point: Either 'list_fields' or 'get_list_fields' must be defined and return a dict.")

    def validate_custom_fields_attributes(self):
        """
        Validates that if `custom_field_model` is defined, `custom_field_value_model` must also be defined.
        Validates that if `custom_field_value_model` is defined, `custom_field_model` must also be defined.
        """
        if self.custom_field_model and not self.custom_field_value_model:
            raise ImproperlyConfigured(
                "Django Access Point: 'custom_field_value_model' must be defined if 'custom_field_model' is set.")
        elif self.custom_field_value_model and not self.custom_field_model:
            raise ImproperlyConfigured(
                "Django Access Point: 'custom_field_model' must be defined if 'custom_field_value_model' is set.")


    def list(self, request, *args, **kwargs):
        """
        List all objects in the queryset with pagination and ordering.
        """
        list_fields_to_use = self.get_list_fields()

        # Ensure that the list_fields_to_use is a dictionary
        if not isinstance(list_fields_to_use, dict) or not list_fields_to_use:
            raise ValueError("Django Access Point: 'list_fields' or 'get_list_fields' must return a dictionary.")

        queryset = self.get_queryset()

        # Pagination parameters from the request
        page = request.query_params.get('page', 1)  # Default to page 1
        page_size = request.query_params.get('page_size', 10)  # Default to 10 items per page

        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            return Response({
                "status": "error",
                "msg": "Invalid page or page_size parameter",
                "data": {},
            }, status=status.HTTP_400_BAD_REQUEST)

        # Handle ordering (order_by and direction)
        order_by = request.query_params.get('order_by', 'created_at')  # Default to 'created_at'
        direction = request.query_params.get('direction', 'desc')  # Default to 'desc'

        # Validate order_by field
        if order_by not in ['created_at', 'updated_at']:
            return Response({
                "status": "error",
                "msg": "Invalid order_by field. Only 'created_at' or 'updated_at' are allowed.",
                "data": {},
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate direction field
        if direction not in ['asc', 'desc']:
            return Response({
                "status": "error",
                "msg": "Invalid direction. Only 'asc' or 'desc' are allowed.",
                "data": {},
            }, status=status.HTTP_400_BAD_REQUEST)

        # Apply ordering
        if direction == 'desc':
            order_by = f"-{order_by}"  # Prefix with '-' for descending order
        queryset = queryset.order_by(order_by)

        # Set up paginator
        paginator = Paginator(queryset, page_size)

        # Handle empty or invalid page
        try:
            page_obj = paginator.get_page(page)
        except (EmptyPage, PageNotAnInteger):
            return Response({
                "status": "error",
                "msg": "Invalid Page",
                "data": {},
            }, status=status.HTTP_400_BAD_REQUEST)

        # Handle the case when page is out of range
        if page_obj.number > paginator.num_pages:
            return Response({
                "status": "error",
                "msg": "Invalid Page",
                "data": {
                        "per_page": 0,
                        "page": 0,
                        "total": 0,
                        "total_pages": 0,
                        "data": [],
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        column_headers = list(list_fields_to_use.values())

        # Prepare the data rows
        data = []
        for obj in page_obj.object_list:
            row = []
            for field in list_fields_to_use:
                row.append(getattr(obj, field, None))  # Extract values based on defined fields
            data.append(row)

        # Prepare the response data with pagination info and the rows
        response_data = {
                "per_page": page_obj.paginator.per_page,
                "page": page_obj.number,
                "total": page_obj.paginator.count,
                "total_pages": page_obj.paginator.num_pages,
                "columns": column_headers,
                "data": data,
        }

        return Response({
            "status": "success",
            "data": response_data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        Create a new object.
        """
        self.validate_custom_fields_attributes()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Retrieve a single object by primary key.
        """
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        """
        Update an existing object by primary key.
        """
        self.validate_custom_fields_attributes()

        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Delete an object by primary key.
        """
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
