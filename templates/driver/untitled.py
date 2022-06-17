class User:

	def __init__(self,username,email,password,phone,sex,country):

		self._name = username
		self._email = email
		self._password = password
		self._phone = phone
		self._sex = sex
		self._country = country


	def auth(email,password) -> bool:
		pass

	def findPathBetween(origin,destination,profile) -> str:
		pass

	def logout():
		pass

class Passenger(User):

	def __init__(self,username,email,password,phone,sex,country):
		User.__init__(self,username,email,password,phone,sex,country)


	def bookPlace(self,origin,destination,price,vehicle) -> bool:
		pass


class Driver(User):

	def __init__(self,username,email,password,phone,sex,country):
		User.__init__(self,username,email,password,phone,sex,country)

	def transportPassengers(self,origin:str,destination:str,passengers:list):
		pass
	


class Vehicle:

	def __init__(self,owner:Driver,license_plate,color,max_place,avail_plac,veh_type,brand):
		self.owner = owner
		self.license_plate = license_plate
		self.color = color
		self.max_place = max_place
		self.avail_plac = avail_plac
		self.type = veh_type
		self.brand = brand

	def updatePLace(self,np):
		self.avail_plac  = np

	def carryPassengers(self,origin:str,destination:str,passengers:list):
		pass



