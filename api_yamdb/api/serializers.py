from rest_framework import serializers
from reviews.models import (
    Review,
    Comment,
    Genre, 
    Category,
    Title,
    User
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


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)