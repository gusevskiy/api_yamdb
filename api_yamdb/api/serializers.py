import datetime

from rest_framework import serializers

from reviews.models import (
    Genre, User, Category, Title, TitleGenre, Review, Comment
)
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError



class UserSerializer(serializers.ModelSerializer):
    Genre, User, Category, Title, TitleGenre
)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        email = value
        if len(email) > 254:
            raise serializers.ValidationError("Email is too long!")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already using!")
        return email

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


class UsersMeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


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


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')

    def validate_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Future year is prohibited")
        return value

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = genre
            TitleGenre.objects.create(
                genre=current_genre, title=title)
        return title


class TitleSerializerGET(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')


############################################################

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    
    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Может существовать только один отзыв!')
        return data
    
    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        read_onlyfields = ['title']

    def validate_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Future year is prohibited")
        return value

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = genre
            TitleGenre.objects.create(
                genre=current_genre, title=title)
        return title


class TitleSerializerGET(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
