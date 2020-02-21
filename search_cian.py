from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from parser_tools import *
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import start_xvfb, stop_xvfb
import pymongo
import time
import random
import os


number_of_pages = 200
open('cian.txt','w').close()
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("no-sandbox")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--headless")
# driver = os.path.join("/usr/local/bin","chromedriver")
# prefs = {'disk-cache-size': 4096}
# chrome_options.add_experimental_option("prefs", prefs)

tbb_dir = "/home/jovyan/work/tor-browser_en-US"
def pars_price_range(browser):
    try:
        price_range = browser.find_element_by_css_selector('a.a10a3f92e9--price_range-link--3Kdo-').text
        price_range = removeNonAscii(str(price_range))
        k_max=0
        for k in range(len(price_range),1,-1):
            if k*' ' in price_range:
                k_max = k
                break
        price_range = price_range.split(k_max*' ')
        price_range = list(map(lambda x: int(x.replace(' ', '')), price_range))
    except NoSuchElementException:
            price_range = None
    return price_range




def pars_house_analytics(browser):
    try:
        header = browser.find_element_by_css_selector("div.a10a3f92e9--averages--3nUh3")
        house = header.find_elements_by_css_selector("div.a10a3f92e9--wrapper--2U64R")[0]
        price, rent = house.find_elements_by_css_selector("div.a10a3f92e9--average--ITlDQ")

        price_list = list(map(lambda x: removeNonAscii(str(x.text.replace(' ', ''))), price.find_elements_by_css_selector('*')))
        price_list = list(filter(lambda a: a != '', price_list))
        for i in price_list:
            if not re.search(r'%\d+', i) is None and i in price_list:
                price_list.remove(i)
        price_list = list(map(lambda x: float(x.replace('%', '').replace(',', '.')),price_list))
        purchase_price, purchase_dynamics = price_list
        rent = list(map(lambda x: removeNonAscii(str(x.text.replace(' ', ''))), rent.find_elements_by_css_selector('*')))
        rent_list = []
        rent = list(filter(lambda a: a != '', rent))
        for i in rent:
            if re.search(r'%\d+', i) is None and '.' not in i:
                rent_list.append(i)
        rent_price, rent_dynamics = list(map(lambda x: float(x.replace('%', '').replace(',', '.').replace('/', '')),rent_list))
    except NoSuchElementException:
        purchase_price, purchase_dynamics, rent_price, rent_dynamics = [None, None,None, None]
    return purchase_price, purchase_dynamics, rent_price, rent_dynamics
        
        
        
def pars_district_analytics(browser):
    try:
        header = browser.find_element_by_css_selector("div.a10a3f92e9--averages--3nUh3")
        house = header.find_elements_by_css_selector("div.a10a3f92e9--wrapper--2U64R")[1]
        price_per_m, price_per_h, month_rent = house.find_elements_by_css_selector("div.a10a3f92e9--average--ITlDQ")

        price_per_m_list = list(map(lambda x: removeNonAscii(str(x.text.replace(' ', ''))), price_per_m.find_elements_by_css_selector('*')))
        price_per_m_list = list(filter(lambda a: a != '', price_per_m_list))
        for i in price_per_m_list:
            if not re.search(r'%\d+', i) is None and i in price_per_m_list:
                price_per_m_list.remove(i)
        price_per_m_list = list(map(lambda x: float(x.replace('%', '').replace(',', '.')),price_per_m_list))
        price_per_m, price_per_m_dynamics = price_per_m_list

        price_per_h_list = list(map(lambda x: removeNonAscii(str(x.text.replace(' ', ''))), price_per_h.find_elements_by_css_selector('*')))
        price_per_h_list = list(filter(lambda a: a != '' and re.search(r'%\d+', a) is None and not '.' in a, price_per_h_list))
        price_per_h_list = list(map(lambda x: float(x.replace('%', '').replace(',', '.')),price_per_h_list))
        price_per_h, price_per_h_dynamics = price_per_h_list
        
        
        
        month_rent = list(map(lambda x: removeNonAscii(str(x.text.replace(' ', ''))), month_rent.find_elements_by_css_selector('*')))
        rent_list = []
        month_rent = list(filter(lambda a: a != '', month_rent))
        for i in month_rent:
            if re.search(r'%\d+', i) is None and '.' not in i:
                rent_list.append(i)
        rent_price, rent_dynamics = list(map(lambda x: float(x.replace('%', '').replace(',', '.').replace('/', '')),rent_list))
    except NoSuchElementException:
        price_per_m, price_per_m_dynamics, price_per_h, price_per_h_dynamics, rent_price, rent_dynamics = [None, None,None, None,None, None]
    return price_per_m, price_per_m_dynamics, price_per_h, price_per_h_dynamics, rent_price, rent_dynamics

db_free = 1
initial_id = 220843621

def parser(flat_string):
    element_dict = {'id': id_num_parser(flat_string),
                    'Number_of_rooms': number_of_rooms_parser(flat_string),
                    'housing_complex': housing_complex_parser(flat_string),
                    'total_area': total_square_parser(flat_string),
                    'living_area': living_area_parser(flat_string),
                    'kitchen_area': kitchen_area_parser(flat_string),
                    'storey_number': storey_number_parser(flat_string),
                    'whole_storey_number': whole_storeys_parser(flat_string),
                    'Building_year': building_year_parser(flat_string),
                    'total_price': total_price_parser(flat_string),
                    'price_per_sq_meter': price_per_sq_meter_parser(flat_string),
                    'address' : address_parser(flat_string),
                    'type_of_flat':type_of_flat_parser(flat_string),
                    'сeiling_height': seiling_hight_parser(flat_string),
                    'bathroom_number': bathroom_num_parser(flat_string),
                    'bathroom_separated': bathroom_separate_parser(flat_string),
                    'windows_to_street': windows_to_street_parser(flat_string),
                    'house_type': house_type_parser(flat_string),
                    'ceiling_type': ceiling_type_parser(flat_string),
                    'porch_num': porch_num_parser(flat_string),
                    'central_heating': central_heating_parser(flat_string),
                    'service_elevator_number': elevator_service_parser(flat_string),
                    'passengers_elevator_number': elevator_passangers_parser(flat_string),
                    'emergency_condition': emergency_condition_parser(flat_string),
                    'room1_square': room1_square_parser(flat_string),
                    'room2_square': room2_square_parser(flat_string),
                    'room3_square': room3_square_parser(flat_string),
                    'latitude': latitude(address_parser(flat_string)),
                    'longitude': longitude(address_parser(flat_string)),
                    'visitors' : visitors_parser(flat_string),
                    'date_of_place': date_of_place_parser(flat_string),
                    'total_number_views': total_number_views_parser(flat_string),
                    'active': active_parser(flat_string)}
    return element_dict
    
def crawler(page_id, page_num):
    print('start crawler')
    time.sleep(4*random.random())
    stop_trying = 0
    start_time = time.process_time()
    while( 'connection refused' in str(download_data(page_id)) and stop_trying < 10):
        if (time.process_time() - start_time>5*60):
            print('took time more than 5 mins')
            break
        stop_trying += 1
        if (stop_trying < 10):
            print('Restarting this process.')
        else:
            print('Stop trying to download ad num:' + str(page_id))
        print('time is ', str(time.process_time() - start_time))
    print('Ad with number: ' + str(page_num) + ' finished parsing.')
    
    ''' increment the global counter, do something with the input '''




def download_data(page_id):
    print('start download_data')
    try:
        with open( '/home/jovyan/work/alex-realty-parser/ads_texts/'+ str(page_id) + '.txt', 'a', encoding='utf-8') as output_file:
            xvfb_display = start_xvfb()
            # browser = webdriver.Chrome(options=chrome_options)
            browser = TorBrowserDriver(tbb_dir)
            # Get the URL of next page to be parsed
            browser.get("https://spb.cian.ru/sale/flat/" + str(page_id) + "/")

            element_list = list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--header--2Ayiz')))
            element_list += ["address:\n"]
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('address.a10a3f92e9--address--140Ec')))
            element_list += ["\n"]
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--description--10czU')))
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--price-container--29gwP')))
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--section_divider--1zGrv')))
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-main--1glTM a10a3f92e9--aside_banner--2FWCV')))
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--offer_card_page-bti--2BrZ7')))
            element_list += ["\n"]
            element_list += ["ID_num: " + str(page_id)]
            element_list += ["\n"]
            element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--container--1In69')))
            element_list += ["\n"]
            purchase_price, purchase_dynamics, rent_price, rent_dynamics = pars_house_analytics(browser)
            # dst = district
            price_per_meter_in_dst, price_per_meter_in_dst_dynamics, price_per_house_in_dst, price_per_house_in_dst_dynamics, rent_price_in_dst, rent_dynamics_in_dst = pars_district_analytics(browser)
            price_range = pars_price_range(browser)
            try:
                browser.find_element_by_css_selector('a.a10a3f92e9--link--1t8n1.a10a3f92e9--link--2mJJk').click()
                time.sleep(0.5)
                element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector('div.a10a3f92e9--information--AyP9e')))
                element_list += ["\n"]
                for elementName in browser.find_elements_by_css_selector("path.highcharts-point"):
                    hover = ActionChains(browser).move_to_element(elementName).click().perform()
                    time.sleep(0.1)
                    element_list += list(map(lambda x: x.text, browser.find_elements_by_css_selector("g.highcharts-label.highcharts-tooltip.highcharts-color-undefined")))
                    element_list += ["\n"]
            except:
                print("No info about visitors in ad: " + str(page_id))
            element_str = "".join(element_list)
            for text in element_list:
                output_file.write(text + '\n')
            output_file.write('-------------------------------------------------------------------------\n')
            info_dict = parser(element_str)
            info_dict['price_range'] = price_range
            info_dict['purchase_price'] = purchase_price
            info_dict['purchase_dynamics'] = purchase_dynamics
            info_dict['rent_price'] = rent_price
            info_dict['rent_dynamics'] = rent_dynamics
            info_dict['price_per_meter_in_dst'] = price_per_meter_in_dst
            info_dict['price_per_meter_in_dst_dynamics'] = price_per_meter_in_dst_dynamics
            info_dict['price_per_house_in_dst'] = price_per_house_in_dst
            info_dict['price_per_house_in_dst_dynamics'] = price_per_house_in_dst_dynamics
            info_dict['rent_price_in_dst'] = rent_price_in_dst
            info_dict['rent_dynamics_in_dst'] = rent_dynamics_in_dst
            info_dict['cian_id'] = page_id
            info_dict.update( {'pic_urls' : list(map(lambda x: x.get_attribute("src"), browser.find_elements_by_css_selector('img.fotorama__img')))})
            # соединяемся с сервером базы данных
            # (по умолчанию подключение осуществляется на localhost:27017)
            connect = pymongo.MongoClient('localhost', 27017, maxPoolSize=200)
            # выбираем базу данных
            db = connect.flats
            # выбираем коллекцию документов
            db.user
            global db_free
            while db_free == 0:
                time.sleep(0.01)
            else:
                db_free = 0
                db.coll.insert_one(info_dict)
                db_free = 1
            connect.close()
            browser.quit()
            stop_xvfb(xvfb_display)
            return 0
    except TypeError:
        time.sleep(4*random.random())
        browser.quit()
        stop_xvfb(xvfb_display)
    except Exception as exception:
        print("Error has occured in: " + str(page_id))
        print(exception)
        f= open("errors.txt","a+")
        f.write(str(page_id) + "\n")
        browser.quit()
        stop_xvfb(xvfb_display)
        return exception


if __name__=="__main__":
    import multiprocessing as mp
    num_of_cores = mp.cpu_count()//3
    #num_of_cores = 4
    print('Start execution with ' + str(num_of_cores) + ' cores.')
    pool = mp.Pool(num_of_cores)
    for ad in range(100000):
        pool.apply_async(crawler, args=(initial_id + ad, ad))
    pool.close()
    pool.join()


print('Parsing is done!!!')

