import datetime as dt
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Review, Comment, Genre, User, Category, Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name'
        )
        lookup_field = 'username'
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
        }


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
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    
    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        read_onlyfields = ['title']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', many=False, queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = ('__all__')
        model = Title


class TitleViewSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, required=True)
    genre = GenreSerializer(many=True, required=False)
    # rating = serializers.IntegerField()
    
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        read_only_fields = ('id', 'name', 'year', 'description', 'genre', 'category')