from django.shortcuts import render
from rest_framework import permissions, generics
from computerapp.models import Product, UserProfile, DeliveryAddress
from computerapp.serializers import ProductListSerializer, ProductRetrieveSerializer, UserInfoSerializer, UserProfileSerializer,UserSerializer, DeliveryAddressSerializer
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
# Create your views here.


class ProductListView(generics.ListAPIView):
	queryset = Product.objects.all()
	permission_classes = (permissions.AllowAny,)
	serializer_class = ProductListSerializer
	filter_backends = (OrderingFilter,SearchFilter,)
	ordering_fields = ('category', 'manufacturer', 'created', 'sold',)
	search_fields = ('description', )
	ordering = ('id',)
	pagination_class = LimitOffsetPagination


class ProductListByCategoryView(generics.ListAPIView):
	
	permission_classes = (permissions.AllowAny,)
	serializer_class = ProductListSerializer
	filter_backends = (OrderingFilter,SearchFilter,)
	ordering_fields = ('category', 'manufacturer', 'created', 'sold', 'price')
	search_fields = ('description', )
	ordering = ('id',)
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		category = self.request.query_params.get('category', None)
		if category is not None:
			queryset = Product.objects.filter(category=category)
		else:
			queryset = Product.objects.all()

		return queryset


class ProductListByCategoryManufacturerView(generics.ListAPIView):
	
	permission_classes = (permissions.AllowAny,)
	serializer_class = ProductListSerializer
	filter_backends = (OrderingFilter,SearchFilter,)
	ordering_fields = ('category', 'manufacturer', 'created', 'sold', 'price')
	search_fields = ('description', )
	ordering = ('id',)
	pagination_class = LimitOffsetPagination

	def get_queryset(self):
		category = self.request.query_params.get('category', None)
		manufacturer = self.request.query_params.get('manufacturer', None)
		if category is not None:
			queryset = Product.objects.filter(category=category, manufacturer=manufacturer)
		else:
			queryset = Product.objects.all()

		return queryset


class ProductRetrieveView(generics.RetrieveAPIView):
	queryset = Product.objects.all()
	permission_classes = (permissions.AllowAny,)
	serializer_class = ProductRetrieveSerializer


class UserInfoView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	def get(self, request, format=None):
		user = self.request.user
		serializer = UserInfoSerializer(user)
		return Response(serializer.data)

class UserProfileRUView(generics.RetrieveUpdateAPIView):

    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):

    	user = self.request.user

    	obj = UserProfile.objects.get(user=user)

    	return obj


class UserCreateView(generics.CreateAPIView):
	serializer_class = UserSerializer


class DeliveryAddressLCView(generics.ListCreateAPIView):
	'''
	delivery address
	'''
	permission_classes = (permissions.IsAuthenticated,)
	serializer_class = DeliveryAddressSerializer


	def get_queryset(self):
		user = self.request.user

		queryset = DeliveryAddress.objects.filter(user=user)

		return queryset

	def perform_create(self, serializer):
		user = self.request.user
		s = serializer.save(user = user)
		profile = user.profile_of
		profile.delivery_address = s
		profile.save()


class DeliveryAddressRUDView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = DeliveryAddressSerializer
	permission_classes = (permissions.IsAuthenticated,)
	def get_object(self):
		user = self.request.user
		try:
			obj = DeliveryAddress.objects.get(id=self.kwargs['pk'], user=user)
		except Exception as e:
			raise NotFound('not found')
		return obj