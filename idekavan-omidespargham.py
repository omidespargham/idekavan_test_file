from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status,viewsets
from django.shortcuts import get_object_or_404
from .models import Category,Country,City,Brand,Advert
from .serializers import (
    MakeAdvertSerializer,
    CategorySerializer,
    CountrySerializer,
    CitySerializer,
    BrandSerializer,
    AdvertDetailSerializer
)



class AdvertViewSet(viewsets.ViewSet):
    queryset = Advert.objects.all()

    # this method will create a advert 
    def create(self,request):
        serializer = MakeAdvertSerializer(data=request.POST)
        if serializer.is_valid():
            valided = serializer.validated_data
            # valided["user"] = request.user
            # TODO 
            # make the user and pass the phone_number to the advert data !
            # valided["phone_number"] = request.user.phone_number
            serializer.create(valided)
            return Response({'ok':'make it as avatar ;)'})
        return Response(data=serializer.errors)
    
    # this method will return a specific advert
    def retrieve(self, request, pk=None):
        advert = get_object_or_404(self.queryset, pk=pk)
        advert_srz = AdvertDetailSerializer(instance=advert)
        return Response(data=advert_srz.data)
    
    # you can use this api to update your advert in partial mode
    def partial_update(self, request, pk=None):
        advert = get_object_or_404(self.queryset, pk=pk)
        srz_data = MakeAdvertSerializer(instance=advert, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data)
        return Response(data=srz_data.errors)
    
    #delete your advert 
    def destroy(self, request, pk=None):
        advert = get_object_or_404(self.queryset, pk=pk)
        advert.delete()
        return Response ({'message': 'advert deleted !' })
    
# in view baraye return subcategory haye yek category ast(garm,srd,...).
class CategoryChildsView(APIView):
    """
    this endpoint is for return subcategorys of one category
    
    """
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        srz_data = CategorySerializer(instance=category.get_children(), many=True)
        return Response(data={'products': srz_data.data})





class MakeAdvert(CreateAPIView):
    """
    this endpoint is for pass advert parameters and it will make a new 
    advert for user !.
    you can see parameters in swagger api, in /swagger path
    """
    serializer_class = MakeAdvertSerializer

    def create(self, request, *args, **kwargs):
        serializer = MakeAdvertSerializer(data=request.data)

        if serializer.is_valid():
            valided = serializer.validated_data
            serializer.create(valided)
            return Response({'ok':'make it as avatar ;)'})

        return Response(data=serializer.errors)


    
class CountrysMakeByView(APIView):
    def get(self,request):
        countrys = Country.objects.all()
        country_srz = CountrySerializer(instance=countrys,many=True)
        return Response(data=country_srz.data)

class CityView(APIView):
    def get(self,request):
        citys = City.objects.all()
        citys_srz = CitySerializer(instance=citys,many=True)
        return Response(data=citys_srz.data)

class BrandView(APIView):
    def get(self,request):
        brands = Brand.objects.all()
        brands_srz = BrandSerializer(instance=brands,many=True)
        return Response(data=brands_srz.data)
    


