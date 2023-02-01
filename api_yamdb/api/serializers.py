from rest_framework import serializers
from reviews.models import (
    Review,
    Comment,
    Genre, 
    Category,
    Title,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class ReviewSerializer(serializers.ModelSerializer):
    # review = serializers.
    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(
    #     read_only=True, slug_field='username'
    # )
    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'post')


class TitleSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'
