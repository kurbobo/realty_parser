import re
from geopy.geocoders import Nominatim
import datetime
from datetime import timedelta

correct_building_name = ['address:\n', 'р-н ', 'На карте', 'дор. ', 'просп.', 'ул.']


def housing_complex_parser(flat_string):
	reg_for_hc = r'в\s+ЖК\s+«(\w+\s*\w*)+»'
	if bool(re.search(reg_for_hc, flat_string))==False:
		housing_complex = None
	else: housing_complex = re.search(reg_for_hc , flat_string).group(0).split('«')[1].split('»')[0]
	return housing_complex


def address_parser(flat_string):
	reg_for_address = re.search(r'address:\n.+', flat_string)
	if bool(reg_for_address)==False:
		city = district = municipal = street = building = None
	else:
		reg_for_address = reg_for_address.group(0)
		for name in correct_building_name:
			reg_for_address = reg_for_address.replace(name, '')
		adress_list = reg_for_address.split(',')
		city, district, municipal, street, building = adress_list[0], adress_list[1], adress_list[2], adress_list[-2], adress_list[-1]
	return city, district, municipal, street, building


def amount_and_square_parser(flat_string):
	reg_for_amount_and_square = re.search(r'\d+-комн.\s+квартира,\s+\d+,?\d*', flat_string)
	if bool(reg_for_amount_and_square)==False:
		amount_of_rooms = total_square = None
	else:
		reg_for_amount_and_square = reg_for_amount_and_square.group(0)
		amount_of_rooms, total_square = re.findall('\s*\d+,?\d*', reg_for_amount_and_square)
		amount_of_rooms, total_square = int(amount_of_rooms), float(total_square.replace(',', '.'))
	return amount_of_rooms, total_square


def living_area_parser(flat_string):
	reg_for_liv_ar = re.search(r'\d+,?\d*\s+\w+\sЖилая', flat_string)
	if bool(reg_for_liv_ar)==False:
		living_area = None
	else:
		living_area = reg_for_liv_ar.group(0).split()[0]
		living_area = float(living_area.replace(',', '.'))
	return living_area


def kitchen_area_parser(flat_string):
	reg_for_liv_ar = re.search(r'\d+,?\d*\s+\w+\sКухня', flat_string)
	if bool(reg_for_liv_ar)==False:
		kitchen_area = None
	else:
		kitchen_area = reg_for_liv_ar.group(0).split()[0]
		kitchen_area = float(kitchen_area.replace(',', '.'))
	return kitchen_area


def type_of_flat_parser(flat_string):
	reg_for_type = re.search(r'Тип жилья\s+\w+', flat_string)
	if bool(reg_for_type)==False:
		type_of_flat = None
	else:
		type_of_flat = reg_for_type.group(0).split()[-1]
	return type_of_flat


def storey_number_parser(flat_string):
	reg_for_liv_ar = re.search(r'\d+\s+из\s+\d+\s*Этаж', flat_string)
	if bool(reg_for_liv_ar)==False:
		storey_number = None, None
	else:
		storey_number = reg_for_liv_ar.group(0).split()[0], reg_for_liv_ar.group(0).split()[2]
	return storey_number


def building_year_parser(flat_string):
	reg_for_building_year = re.search(r'\d+\s*Построен', flat_string)
	if bool(reg_for_building_year)==False:
		building_year = None
	else:
		building_year = int(reg_for_building_year.group(0).split()[0])
	return building_year


def price_parser(flat_string):
	reg_for_price = re.search(r'\d+\s*\d*\s*\d*\s*₽\s*'*2, flat_string)
	if bool(reg_for_price)==False:
		price, dens = None, None
	else:
		fin = reg_for_price.group(0).replace(' ','').replace('\n','').split('₽')
		price, dens =fin[0] , fin[1] 
	return price, dens


def seiling_hight_parser(flat_string):
	reg_for_ceiling_height = re.search(r'Высота потолков\s+\w+', flat_string)
	if bool(reg_for_ceiling_height)==False:
		ceiling_height = None
	else:
		ceiling_height = float(reg_for_ceiling_height.group(0).split()[-1])
	return ceiling_height


def bathroom_parser(flat_string):
	reg_for_bathroom = re.search(r'Санузел\s+\w+\s+\w+', flat_string)
	if bool(reg_for_bathroom)==False:
		bathroom_num = None
		bathroom_separate = None
	else:
		bathroom_num = int(reg_for_bathroom.group(0).split()[1])
		bathroom_separate = 'Yes' if "разд" in reg_for_bathroom.group(0).split()[2] else 'No'
	return bathroom_num, bathroom_separate


def windows_to_street_parser(flat_string):
	reg_for_windows_to_street = re.search(r'Вид из окон\s+\w+\s+\w+', flat_string)
	if bool(reg_for_windows_to_street)==False:
		windows_to_street = None
	else:
		windows_to_street = 'Yes' if "двор" in reg_for_windows_to_street.group(0).split() else 'No'
	return windows_to_street


def house_type_parser(flat_string):
	reg_for_house_type = re.search(r'Тип дома\s+\w+', flat_string)
	if bool(reg_for_house_type)==False:
		house_type = None
	else:
		house_type = reg_for_house_type.group(0).split()[-1]
	return house_type


def ceiling_type_parser(flat_string):
	reg_for_ceiling_type = re.search(r'Тип перекрытий\s+\w+', flat_string)
	if bool(reg_for_ceiling_type)==False:
		ceiling_type = None
	else:
		ceiling_type = reg_for_ceiling_type.group(0).split()[-1]
	return ceiling_type


def porch_num_parser(flat_string):
	reg_for_porch_num = re.search(r'Подъезды\s+\w+', flat_string)
	if bool(reg_for_porch_num)==False:
		porch_num = None
	else:
		porch_num = int(reg_for_porch_num.group(0).split()[-1])
	return porch_num


def central_heating_parser(flat_string):
	reg_for_central_heating = re.search(r'Отопление\s+\w+', flat_string)
	if bool(reg_for_central_heating)==False:
		central_heating = None
	else:
		central_heating = 'Yes' if "Центральное" in reg_for_central_heating.group(0).split() else 'No'
	return central_heating


def elevator_service_parser(flat_string):
	reg_for_elevator_service = re.search(r'\d+\s*пассажирских', flat_string)
	if bool(reg_for_elevator_service)==False:
		elevator_service = None
	else:
		elevator_service = int(reg_for_elevator_service.group(0).split()[0])
	return elevator_service


def elevator_passangers_parser(flat_string):
	reg_for_elevator_passangers = re.search(r'\d+\s*пассажирских', flat_string)
	if bool(reg_for_elevator_passangers)==False:
		elevator_passangers = None
	else:
		elevator_passangers = int(reg_for_elevator_passangers.group(0).split()[0])
	return elevator_passangers


def emergency_condition_parser(flat_string):
	reg_for_emergency_condition = re.search(r'Аварийность\s+\w+', flat_string)
	if bool(reg_for_emergency_condition)==False:
		emergency_condition = None
	else:
		emergency_condition = 'No' if "Нет" in reg_for_emergency_condition.group(0).split() else 'Yes'
	return emergency_condition


def room1_square_parser(flat_string):
	reg_for_room1_square = re.search(r'Площадь комнат\s+\w+', flat_string)
	if bool(reg_for_room1_square)==False:
		room1_square = None
	else:
		try:
			room1_square = float(reg_for_room1_square.group(0).split('-')[0].split('\n')[1])
		except:
			room1_square = None
	return room1_square


def room2_square_parser(flat_string):
	reg_for_room2_square = re.search(r'Площадь комнат\s+\w+.*', flat_string)
	if bool(reg_for_room2_square)==False:
		room2_square = None
	else:
		try:
			room2_square = float(reg_for_room2_square.group(0).split('-')[1].split()[0])
		except:
			room2_square = None
	return room2_square


def room3_square_parser(flat_string):
	reg_for_room3_square = re.search(r'Площадь комнат\s+\w+.*', flat_string)
	if bool(reg_for_room3_square)==False:
		room3_square = None
	else:
		try:
			room3_square = float(reg_for_room3_square.group(0).split('-')[2].split()[0])
		except:
			room3_square = None
	return room3_square


def id_num_parser(flat_string):
	reg_for_id_num = re.search(r'ID_num:\s+\w+.*', flat_string)
	if bool(reg_for_id_num)==False:
		id_num = None
	else:
		id_num = int(reg_for_id_num.group(0).split()[-1])
	return id_num

def building_for_coordinates(building):
	if ('к' in building) and building is not None:
		lst = building.split('к')
		building_correct = lst[0] + ' к' + lst[1]
	elif ('К' in building) and building is not None:
		lst = building.split('К')
		building_correct = lst[0] + ' к' + lst[1]
	else:
		building_correct = building
	return building_correct


def latitude(city, street, building):
	place = city + ',' + street + ',' + building_for_coordinates(building)
	nom = Nominatim()
	n = nom.geocode(place)
	if n is None:
		return None
	else:
		return n.latitude


def longitude(city, street, building):
	place = city + ',' + street + ',' + building_for_coordinates(building)
	nom = Nominatim()
	n = nom.geocode(place)
	if n is None:
		return None
	else:
		return n.longitude


def visitors_parser(flat_string):
	reg_for_visitors = re.findall(r'Количество просмотров.+', flat_string)
	if bool(reg_for_visitors)==False:
		visitors = None
	else:
		visitors = {}
		today = datetime.datetime.today()
		oneday = timedelta(days=1)
		previousday = today - oneday
		for visitor_day in reg_for_visitors:
			visitors.update({previousday.strftime('%Y-%m-%d'): visitor_day.split()[-1]})
			previousday = previousday - oneday
	return visitors

def date_of_place_parser(flat_string):
	reg_for_date_of_place = re.search(r'с даты создания объявления.*', flat_string)
	if bool(reg_for_date_of_place)==False:
		date_of_place = None
	else:
		try:
			date_of_place = ''.join(re.findall(r'\d*\.\d*\.\d*', reg_for_date_of_place.group(0)))
		except:
			date_of_place = None
	return date_of_place

def total_number_views_parser(flat_string):
	reg_for_total_number_views = re.search(r'.*с даты создания объявления', flat_string)
	if bool(reg_for_total_number_views)==False:
		total_number_views = None
	else:
		try:
			total_number_views = ''.join(re.findall(r'\d*', reg_for_total_number_views.group(0)))
		except:
			total_number_views = None
	return total_number_views