import time
import lxml.html
import request_to
import Database_MongoDB


class Parse:

    all_show_case_count = 0

    def __init__(self):
        self.all_pages = 0
        self.number_of_subcategory = None
        self.number_of_category = None
        self.name_of_subcategory = None
        self.category = None
        self.url = 'https://www.rosagroleasing.ru/leasing/catalog/'
        self.domain = 'https://www.rosagroleasing.ru'
        self.count_catalog = None  # Число категорий в каталоге
        self.r_start_url = None  # Text страницы self.url

    def count_catalog_len(self):
        """HTML стартовой страницы, а также возвращает кол-во элементов в каталоге"""

        r = request_to.RealizeRequests(self.url)
        req = r.get_html()
        tree = lxml.html.document_fromstring(req)
        count = tree.xpath('//*[@class="side-bar__wrapper"]/div')
        self.count_catalog = len(count)
        self.r_start_url = req
        return self.count_catalog, self.r_start_url

    def search_category(self):
        """Поиск всех категорий сайта + href, а также список всех подкатегорий + href"""

        tree = lxml.html.document_fromstring(self.r_start_url)
        self.number_of_category = 1
        for i in range(self.number_of_category, self.count_catalog + 1):
            category = tree.xpath(f'//*[@id="CRMProductControl"]'
                                  f'/div/aside/div/div/div[{i}]/div/a[1]/text()')
            self.category = category[0]
            count_li_subcategory = len(tree.xpath(f'//*[@id="CRMProductControl"]'
                                                  f'/div/aside/div/div/div[{i}]/ul/li'))
            print(f'Категория - [{category[0]}] {self.number_of_category}/{self.count_catalog}')
            self.number_of_subcategory = 1
            for j in range(self.number_of_subcategory, count_li_subcategory + 1):
                name_of_subcategory = tree.xpath(f'//*[@id="CRMProductControl"]'
                                                 f'/div/aside/div/div/div[{i}]'
                                                 f'/ul/li[{j}]/a/text()')
                self.name_of_subcategory = name_of_subcategory[0]
                href_of_subcategory = self.domain + str(tree.xpath(f'//*[@id="CRMProductControl"]'
                                                                   f'/div/aside/div/div/div[{i}]/'
                                                                   f'ul/li[{j}]/a[1]/@href')[0])
                print(f'  Подкатегория: {name_of_subcategory[0]}')
                # self.all_pages += self.count_page_on_url(href_of_subcategory)
                self.parse_url_subcategory(href_of_subcategory)

    def parse_url_subcategory(self, href_of_subcategory):
        """Поиск всех ссылок витрины подкатегории"""

        count_pages_subcategory = self.count_page_on_url(href_of_subcategory)
        if count_pages_subcategory == 1:
            r = request_to.RealizeRequests(href_of_subcategory)
            tree = lxml.html.document_fromstring(r.get_html())
            self.parse_showcase(tree_showcase=tree)
        else:
            page_start_debug = 1
            for page in range(page_start_debug, count_pages_subcategory + 1):
                print(f"  Страница подкатегории - {page}/{count_pages_subcategory}...")
                href = href_of_subcategory + f'-npg1-page{page}'
                r = request_to.RealizeRequests(href)
                tree = lxml.html.document_fromstring(r.get_html())
                self.parse_showcase(tree_showcase=tree)

    @staticmethod
    def count_page_on_url(url_parse_page):
        r = request_to.RealizeRequests(url_parse_page)
        tree = lxml.html.document_fromstring(r.get_html())
        len_all_page_button = len(tree.xpath('//*[@id="CRMProductControl"]/div/div[2]/div[2]/ul/li'))
        max_page = tree.xpath(f'//*[@id="CRMProductControl"]/div/div[2]/div[2]/ul/li[{len_all_page_button}]/a/text()')
        if bool(max_page):
            max_page = int(max_page[0])
            return max_page
        else:
            max_page = 1
            return max_page

    # noinspection PyGlobalUndefined
    def parse_showcase(self, tree_showcase):
        global name_spec
        count_showcase = len(tree_showcase.xpath('//*[@id="CRMProductControl"]/div/div[2]/div[2]/div[2]/div'))
        for i in range(1, count_showcase + 1):
            self.all_show_case_count += 1
            if self.all_show_case_count % 50 == 0:
                print(f"  [INFO] Число витрин обработано: {self.all_show_case_count}")
            keys = []
            value = []
            keys.append('Категория')
            keys.append('Подкатегория')
            value.append(self.category)
            value.append(self.name_of_subcategory)
            href_showcase = tree_showcase.xpath(f'//*[@id="CRMProductControl"]'
                                                f'/div/div[2]/div[2]/div[2]/div[{i}]/div/div/@onclick')
            href = self.domain + href_showcase[0].split('=')[1].strip()[1: -1]
            # print(f"Ссылка на витрину{i}: {self.domain + href_showcase[0].split('=')[1].strip()[1: -1]}")
            req = request_to.RealizeRequests(href)
            tree = lxml.html.document_fromstring(req.get_html())

            """ Сбор общей инф. [item__info] """

            try:
                product_name = (tree.xpath('//*[@id="CRMProductCardControl"]/div/div/div/div[2]/div/h2/text()'))[0]
                product_name = product_name.strip()
            except:
                product_name = ''
            keys.append('Товар')
            value.append(product_name)
            try:
                supplier = (tree.xpath('//*[@id="CRMProductCardControl"]'
                                       '/div/div/div/div[2]/div/table/tbody/tr[1]/td[2]/b/text()'))[0]
                supplier = supplier.strip()
            except:
                supplier = ''
            keys.append('Поставщик')
            value.append(supplier)
            try:
                first_contribution = (tree.xpath('//*[@id="CRMProductCardControl"]'
                                                 '/div/div/div/div[2]/div/table/tbody/tr[3]/td[2]/text()'))[0]
                first_contribution = str(first_contribution).replace('\xa0', ' ').strip()
            except:
                first_contribution = ''

            keys.append('Первоначальный взнос')
            value.append(first_contribution)

            try:
                lease_term = (tree.xpath('//*[@id="CRMProductCardControl"]'
                                         '/div/div/div/div[2]/div/table/tbody/tr[4]/td[2]/text()'))[0]
                lease_term = str(lease_term).replace('\xa0', ' ').strip()
            except:
                lease_term = ''
            keys.append('Срок лизинга')
            value.append(lease_term)
            try:
                summa = (tree.xpath('//*[@id="CRMProductCardControl"]'
                                    '/div/div/div/div[2]/div/table/tbody/tr[5]/td[2]/text()'))[0]
                summa = str(summa).replace('\xa0', ' ').strip()
            except:
                summa = ''

            keys.append('Сумма договора')
            value.append(summa)

            """ Сбор Технических характеристик """

            all_tr_specifications = tree.xpath('//*[@id="tab-2"]/div/div/div[1]/div[1]/div[2]/table/tbody/tr')
            len_specifications = len(all_tr_specifications)

            for tr in range(1, len_specifications + 1):
                try:
                    name_spec = (tree.xpath(f'//*[@id="tab-2"]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[{tr}]/td[1]/text()')[0]).strip()
                except:
                    name_spec = ''
                    value_spec = ''
                    break
                else:
                    try:
                        if bool(tree.xpath(f'//*[@id="tab-2"]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[{tr}]/td[2]/text()')):
                            value_spec = (tree.xpath(f'//*[@id="tab-2"]/div/div/div[1]/div[1]/div[2]/table/tbody/tr[{tr}]/td[2]/text()')[0]).strip()
                            try:
                                value_spec = int(value_spec)
                            except:
                                keys.append(name_spec)
                                value.append(value_spec)
                            else:
                                keys.append(name_spec)
                                value.append(value_spec)
                        else:
                            name_spec = ''
                            value_spec = ''
                    except:
                        print(f'Значение {name_spec} - {value_spec} с ошибкой - {href}')

            try:
                nomination_name = (tree.xpath('//*[@id="tab-2"]/div/div/div[1]/div[2]/div/text()')[0]).strip()
                nomination_value = (tree.xpath('//*[@id="tab-2"]/div/div/div[1]/div[2]/p/text()')[0]).strip()
                keys.append(nomination_name)
                value.append(nomination_value)
            except:
                print("    [WARRNING] Нет доступа к [Наименование]")

            try:
                len_manufacturer_value = len(tree.xpath('//*[@id="tab-2"]/div/div/'
                                                        'div[2]/div[2]/div[2]/table/tbody/tr'))
                for tr in range(1, len_manufacturer_value + 1):
                    manufacturer_name = ((tree.xpath('//*[@id="tab-2"]/div/div/'
                                                     'div[2]/div[2]/div[2]/table/tbody/tr/td[1]/text()')[0]).strip())
                    try:
                        manufacturer_value = (tree.xpath('//*[@id="tab-2"]/div/div/div[2]/'
                                                         'div[2]/div[2]/table/tbody/tr[1]/td[2]/text()')[0]).strip()
                    except:
                        manufacturer_value = '-'

                    keys.append(manufacturer_name)
                    value.append(manufacturer_value)
            except:
                print("    [WARRNING] Нет доступа к [Производитель]")

            keys.append('Ссылка')
            value.append(href)
            # print(f"        [INFO] Время парса страницы [{time.time() - time_start_debug}] секунд!")

            # запись в словарь
            try:
                # time_start_debug = time.time()
                insert_dict = {}
                if len(keys) == len(value):
                    for key, val in zip(keys, value):
                        if key.endswith('.'):
                            # print(f'    [WARRNING] Ключ {key} заканчивается на [.]')
                            if key == '.':
                                key = ''
                            while key.endswith('.'):
                                key = key[:-1]

                        insert_dict[key] = val
                    db = Database_MongoDB.DB_Mongo(insert_dict)
                    db.connection()
                    # print(f"        [INFO] Время записи страницы в БД [{time.time() - time_start_debug}] секунд!")
                else:
                    print("   [ERROR] Списки не равны!")
            except:
                print('   [ERROR] Ошибка записи словаря в БД!')
                print(len(keys), keys)
                print(len(value), value)
                pass


if __name__ == '__main__':
    time_start = time.time()
    parse = Parse()
    parse.count_catalog_len()
    parse.search_category()
    print(f"Скопированно [{parse.all_show_case_count}] ветрин!")
    print(f"Конец!  Время работы прораммы - {(time.time() - time_start) / 60} минут")
