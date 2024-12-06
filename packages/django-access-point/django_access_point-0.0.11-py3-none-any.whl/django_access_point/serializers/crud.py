from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django_access_point.models.custom_field import CUSTOM_FIELD_RULES, CUSTOM_FIELD_STATUS
from django_access_point.serializers.validations import validate


class CrudSerializer(serializers.ModelSerializer):
    """
    Base serializer class for CRUD operations.
    """

    class Meta:
        model = None  # This should be defined in the child class
        fields = None  # This should be defined in the child class
        custom_field_model = None  # This should be defined in the child class
        custom_field_value_model = None  # This should be defined in the child class

    def __init__(self, *args, **kwargs):
        # Ensure that the 'model' and 'fields' are set in the child class Meta
        if not hasattr(self.Meta, 'model'):
            raise ImproperlyConfigured("Django Access Point: The 'model' attribute must be defined in the child class Meta.")
        if not hasattr(self.Meta, 'fields'):
            raise ImproperlyConfigured("Django Access Point: The 'fields' attribute must be defined in the child class Meta.")

        super().__init__(*args, **kwargs)

    def validate(self, data):
        tenant = data.get('tenant', None)

        # Access the context here, after the serializer is initialized
        self.custom_field_model = self.context.get('custom_field_model', None)
        self.custom_field_value_model = self.context.get('custom_field_value_model', None)

        if self.custom_field_model:
            _req_custom_fields_data = {}
            _req_custom_fields_id = []
            custom_fields_data = {}
            custom_field_errors = {}

            for key, value in self.initial_data.items():
                if key.startswith("custom_field_"):
                    # Extract the custom field ID from the key (assuming format is custom_field_<id>)
                    custom_field_id = key.split("_")[2]  # Example: custom_field_1, custom_field_2
                    _req_custom_fields_data[custom_field_id] = value

            _req_custom_fields_id = list(_req_custom_fields_data.keys())

            custom_fields_configured = self.custom_field_model.objects.filter(tenant=tenant, status=CUSTOM_FIELD_STATUS[1][0])

            for custom_field in custom_fields_configured:
                _custom_field_id = str(custom_field.id)
                if _custom_field_id not in _req_custom_fields_id:
                    custom_field_errors["custom_field_" + _custom_field_id] = "This field is required."
                else:
                    custom_field_label = custom_field.label
                    custom_field_type = custom_field.field_type
                    custom_field_validation_rule = custom_field.validation_rule
                    custom_field_value = _req_custom_fields_data[_custom_field_id]

                    field_error = self.validate_custom_field_data(
                        _custom_field_id, custom_field_label, custom_field_type,
                        custom_field_validation_rule, custom_field_value
                    )

                    if len(field_error) != 0:
                        custom_field_errors.update(field_error)

            # If there are any custom field validation errors, raise validation errors
            if custom_field_errors:
                raise ValidationError(custom_field_errors)

            # Add custom fields data to the validated data if there are no errors
            data["custom_fields"] = _req_custom_fields_data

        return data

    def validate_custom_field_data(self, field_id, field_label, field_type, field_validation_rule, field_value):
        validation_errors = {}

        # If field has validation 'required'
        if CUSTOM_FIELD_RULES[0][0] in field_validation_rule and field_validation_rule['required']:
            error = validate.is_empty(field_value)
            if error:
                validation_errors["custom_field_" + field_id] = f"{field_label} may not be blank."
                return validation_errors

        # If field has validation 'minlength'
        if CUSTOM_FIELD_RULES[1][0] in field_validation_rule and field_value:
            minlength = field_validation_rule['minlength']
            error = validate.minlength(field_value, minlength, field_type)
            if error:
                validation_errors["custom_field_" + field_id] = f"{field_label} must contain at least {minlength} characters."
                return validation_errors

        # If field has validation 'maxlength'
        if CUSTOM_FIELD_RULES[2][0] in field_validation_rule and field_value:
            maxlength = field_validation_rule['maxlength']
            error = validate.maxlength(field_value, maxlength, field_type)
            if error:
                validation_errors["custom_field_" + field_id] = f"{field_label} should not be greater than {maxlength} characters."
                return validation_errors

        # If field has validation 'min' - for 'number' field
        if CUSTOM_FIELD_RULES[3][0] in field_validation_rule and field_value:
            min_value = field_validation_rule['min']
            error = validate.min_value(field_value, min_value)
            if error:
                validation_errors["custom_field_" + field_id] = f"{field_label} should be equal or greater than {min_value}."
                return validation_errors

        # If field has validation 'max' - for 'number' field
        if CUSTOM_FIELD_RULES[4][0] in field_validation_rule and field_value:
            max_value = field_validation_rule['max']
            error = validate.max_value(field_value, max_value)
            if error:
                validation_errors["custom_field_" + field_id] = f"{field_label} should be equal or less than {max_value}."
                return validation_errors

        # If field has validation 'email'
        if CUSTOM_FIELD_RULES[5][0] in field_validation_rule and field_value and field_validation_rule['email']:
            error = validate.is_email(field_value)
            if error:
                validation_errors["custom_field_" + field_id] = f"{field_label} is invalid."
                return validation_errors

        # If field has validation 'url'
        if CUSTOM_FIELD_RULES[6][0] in field_validation_rule and field_value and field_validation_rule['url']:
            error = validate.is_url(field_value)
            if error:
                validation_errors["custom_field_" + field_id] = f"{field_label} is invalid."
                return validation_errors


    def create(self, validated_data):
        # Extract custom fields data from validated data
        custom_fields_data = validated_data.pop("custom_fields", {})

        # Create the user or relevant model instance
        instance = self.Meta.model.objects.create(**validated_data)

        # Save custom fields (if applicable)
        for field_id, value in custom_fields_data.items():
            try:
                custom_field = self.custom_field_model.objects.get(id=field_id)
                # Logic to save or associate the custom field with the instance (e.g., create a relation)
                # This is just an example:
                # instance.custom_fields.create(custom_field=custom_field, value=value)
            except self.custom_field_model.DoesNotExist:
                raise ValidationError(f"Custom field with ID {field_id} does not exist.")

        return instance
