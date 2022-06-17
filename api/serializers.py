from rest_framework.serializers import ModelSerializer

from django.contrib.auth import get_user_model

from map.models import Trip,UserPosition,UserHistory,UserBookPlace,Vehicle,DriverTransportPassenger

from rest_framework.authtoken.views import Token

User = get_user_model()

class UserSerializers(ModelSerializer):
    
    class Meta:
        
        model = User
        fields = ['id','first_name','last_name','username','sex','phone','country','user_type','status','password']
        extra_kwargs = {'password':{
            'write_only':True,
            'required':True
        }}
        
    def create(self,validate_data):
        user = User.objects.create(**validate_data)
        Token.objects.create(user=user)
        return user
    
class TripSerializers(ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
        
class UserPositionSerializers(ModelSerializer):
    
    class Meta:
        model = UserPosition
        fields ='__all__'
        
class UserHistorySerializers(ModelSerializer):
    
    class Meta:
        model = UserHistory
        fields = '__all__'
        
class UserBookPlaceSerializers(ModelSerializer):
    
    class Meta:
        model = UserBookPlace
        fields = '__all__'
        
class VehicleSerializers(ModelSerializer):
    
    
    class Meta:
        model = Vehicle
        fields = '__all__'
        
class DriverTransportPassengerSerializers(ModelSerializer):
    
    class Meta:
        
        model = DriverTransportPassenger
        fields = '__all__'