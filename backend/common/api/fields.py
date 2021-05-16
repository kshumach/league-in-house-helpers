from typing import TypeVar, Generic

from django.contrib.auth import get_user_model
from rest_framework import serializers
import enum


M = TypeVar("M")


# For some reason the internal implementation returns a mapping for str(key): key for key in choices instead of mapping
# the value. See _set_choices in serializers.ChoiceField.
class EnumModelField(serializers.ChoiceField, Generic[M]):
    def __init__(self, choices: enum.EnumMeta, model: M, **kwargs):
        self._enum_model = model
        self._enum_reference = choices

        choices_as_tuple_list = list(map(lambda r: (r.name, r.value), choices))

        super().__init__(choices_as_tuple_list, **kwargs)

    def to_internal_value(self, data):
        initial_value = super().to_internal_value(data)

        return self._enum_model.objects.get(value=self.choices[initial_value])

    def to_representation(self, instance):
        return self._enum_reference(instance.value).name.lower().capitalize()


# Custom field that extracts the user_id from a given user object.
# Model serializers won't allow an override to an int field. Since the user field is a FK relation it expects a user
# object. Just passing one fails due to requiring a PK value on save. Overriding it like so just skips all that
class UserField(serializers.Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value.id
