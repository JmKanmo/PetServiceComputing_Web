import requests
import xmltodict
import json

API_KEY = "ZbgMgKa7yiF%2BH655L2q2bhPmTslw6qWOLQEB2plfkrRtwZPSn4y7V0P%2FXEkSS85j32cYyuDvan4LQSeo0cMuZQ%3D%3D"


class Location_Resource:
    def __init__(self):
        pass

    def get_sidolist(self):
        sido_result = requests.get(
            'http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/sido?ServiceKey='+API_KEY)
        dict_type = xmltodict.parse(sido_result.content)
        json_type = json.dumps(dict_type)
        dict2_type = json.loads(json_type)
        body = dict2_type['response']['body']
        items = body['items']
        return [] if items == None else items['item']

    def get_sidocode(self, address):
        for json_data in self.get_sidolist():
            if json_data['orgdownNm'] == address:
                return json_data['orgCd']
        return ''

    def get_sigungulist(self, uprCd):
        sigungu_result = requests.get(
            'http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/sigungu?upr_cd='+uprCd+'&ServiceKey='+API_KEY)
        dict_type = xmltodict.parse(sigungu_result.content)
        json_type = json.dumps(dict_type)
        dict2_type = json.loads(json_type)
        body = dict2_type['response']['body']
        items = body['items']
        return [] if items == None else items['item']

    def get_sigungucode(self, uprCd, address):
        for sigungu in self.get_sigungulist(uprCd):
            if sigungu['orgdownNm'] == address:
                return sigungu['orgCd']
        return ''


class Animal_Resource:
    def __init__(self):
        pass

    def get_searchAnimal(self, *param):
        bgnde = param[0] if param[0] != '' else '20190101'  # 유기날짜(검색시작일)
        endde = param[1] if param[1] != '' else '20191113'  # 유기날짜(검색종료일)
        # 축종코드(기본 - 개 - 417000, 고양이 - 422400 , 기타 - 429900)
        upkind = param[2] if param[2] != '' else '417000'
        kind = ''  # 품종코드 - 품종코드API 참조
        upr_cd = param[3] if param[3] != '' else ''  # 시도조회 API 참조
        org_cd = param[4] if param[4] != '' else ''  # 시군구조회 API 참조
        care_reg_no = ''  # 보호소번호 API 참조
        state = 'null'  # 기본값(null), 공고중(notice), 보호중(protect)
        neuter_yn = param[5] if param[5] != '' else 'U'  # 중성화여부 (Y , N , U)
        pageNo = '1'  # 페이지번호
        numOfRows = '500'  # 페이지당 보여줄 개수

        option = 'bgnde='+bgnde\
            + '&endde='+endde\
            + '&upr_cd='+upr_cd\
            + '&org_cd='+org_cd\
            + '&pageNo='+pageNo\
            + '&numOfRows='+numOfRows\
            + '&upkind='+upkind\
            + '&neuter_yn='+neuter_yn\
            + '&state='+state\

        queryParams = option + '&ServiceKey='+API_KEY\

        try:
            URL = 'http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic?' + queryParams
            result = requests.get(URL)
            dict_type = xmltodict.parse(result.content)
            json_type = json.dumps(dict_type)
            dict2_type = json.loads(json_type)
            body = dict2_type['response']['body']
            items = body['items']
            return items['item']

        except:
            return []

    def get_NearAnimal(self, address):
        parsed_address = address.split(' ')  # 파싱주소([0]-시도, [1]-시군구)
        animal_info = []
        animal_sigunguinfo = []

        try:
            for json_data in Location_Resource().get_sidolist():
                if json_data['orgdownNm'] == parsed_address[0]:
                    for sigungu in Location_Resource().get_sigungulist(json_data['orgCd']):
                        if sigungu['orgdownNm'] == parsed_address[1]:
                            for animal in self.get_searchAnimal(
                                    '20190101', '20191204', '', json_data['orgCd'], sigungu['orgCd'], ''):
                                if animal['processState'] == '보호중' or animal['processState'] == '공고중':
                                    animal_sigunguinfo.append(animal)
                            break
                    break

            animal_info = animal_sigunguinfo
            return animal_info
        except:
            return []
