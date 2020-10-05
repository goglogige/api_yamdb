from rest_framework import serializers

from .models import User, Category, Genre, Title


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'bio', 'email', 'role']


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=75)


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=75)
    confirmation_code = serializers.CharField(max_length=10)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


# class TitleSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(many=False, read_only=True)
#     genre = GenreSerializer(many=True, read_only=True)
#     rating = serializers.SerializerMethodField()
#
#     class Meta:
#         fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
#         model = Title
#
#     def get_rating(self, obj):
#         return sum([review.score for review in obj.reviews.all()]) / obj.reviews.count()


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())
    # rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category',
        )

    # def get_rating(self, obj):
    #     return sum([review.score for review in obj.reviews.all()]) / obj.reviews.count()


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    # rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'description', 'genre', 'category',
        )

    # def get_rating(self, obj):
    #     return sum([review.score for review in obj.reviews.all()]) / obj.reviews.count()

