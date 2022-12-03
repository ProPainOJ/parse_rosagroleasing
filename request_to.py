import requests
from fake_useragent import UserAgent
import random
import time


class RealizeRequests:
    """Класс запрос, обрабатывает обект ссылка, ожидает - (url)"""
    _UserAgent = UserAgent()
    _UserAgent = _UserAgent.random
    _headers = {
        "User-Agent": _UserAgent,
        "Accept": "*/*"
    }
    _list_proxy = ['0', '0']

    def __init__(self, url):
        self.url = url
        self.proxy = None
        self.req = None

    def get_html(self):
        """Возвращает объект requests в формате TEXT """

        time.sleep(random.randint(0, 2))
        try:
            self.req = requests.get(self.url, headers=self._headers)
            # request = self.connect_proxy()
        except:
            false_connect_counter = 0
            while self.req is None:
                false_connect_counter += 1
                try:
                    # request = self.connect_proxy()
                    self.req = requests.get(self.url, headers=self._headers)
                    if false_connect_counter == 1:
                        print(f"  [FINE] Доступ к ссылке [{self.url}] открыт c первого раза!")
                    else:
                        print(f"  [FINE] Доступ к ссылке [{self.url}] открыт!")
                except:
                    t_reset = random.randint(1, 15)
                    print(f"    [WARRNING] Ошибка доступа к ссылке {self.url}, попытка [{false_connect_counter}], переподключение через {t_reset} секунд(ы)...")
                    time.sleep(t_reset)
                else:
                    return self.check_status_code(request=self.req)
        else:
            return self.check_status_code(request=self.req)

    def check_status_code(self, request):
        if request.status_code == 200:
            return request.text
        else:
            limit_connect = 25
            counter_of_error = 0
            while (request.status_code != requests.codes.ok) and counter_of_error <= limit_connect:
                counter_of_error += 1
                print(
                    f'    [ERROR] Ошибка подключения {request.status_code}, попытка переподключения'
                    f' {counter_of_error}...')
                print('-' * 60)
                # Прокси, то нет :)
                # request = requests.get(self.url, headers=self._headers, proxies=self.random_proxy())
                request = requests.get(self.url, headers=self._headers)  # <- Когда будет Proxy удалить
                time.sleep(random.randint(1, 15))
            if counter_of_error >= limit_connect:
                return 0
            else:
                return request.text

    def random_proxy(self):
        self.proxy = {
            'https': random.choice(self._list_proxy)
        }
        return self.proxy

    # noinspection PyGlobalUndefined
    def connect_proxy(self):
        """Совершает запрос через рандомный Proxy

        !!! Если запрос не был отработан через список прокси, запрос отрабатывает без Proxy !!!"""
        global req
        try:
            req = requests.get(self.url, headers=self._headers, proxies=(x := self.random_proxy()))
        except requests.ConnectionError:
            for i in range(1, y := len(self._list_proxy) + 1):
                try:
                    req = requests.get(self.url, headers=self._headers, proxies=(x := self.random_proxy()))
                    return req
                except:
                    print(f'    [ERROR] Ошибка Proxy {x}, попытка №{i}')
            print('     [WARNING] Подключение без Proxy')
            req = requests.get(self.url, headers=self._headers)
            return req
        else:
            return req
