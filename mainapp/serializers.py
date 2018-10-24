from rest_framework import serializers

from mainapp.models import Category
from mainapp.models import FamilyMember
from mainapp.models import Records
from mainapp.models import TypeEntry


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class FamilyMemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FamilyMember
        fields = ("id", "name")


class TypeEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypeEntry
        fields = ("id", "name")


class RecordsSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()
    name = FamilyMemberSerializer()
    type_entry = TypeEntrySerializer()

    class Meta:
        model = Records
        fields = (
            "id",
            "db_included_date_time",
            "create_date_time",
            "payment_date_time",
            "debit",
            "credit",
            "category",
            "name",
            "type_entry",
            "description",
        )
