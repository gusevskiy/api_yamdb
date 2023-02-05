from rest_framework import serializers
from reviews.models import Review, Comment, Genre, User, Category


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
