import requests
from bs4 import BeautifulSoup
from django.core.cache import cache

class GiftCategory:
    """
    The Category class for parent and children gifts
    """
    PARSER = 'lxml'
    def __init__(self, url) -> None:
        self.url = url


    def get_html(self):
        html_string = cache.get(self.url)
        if html_string is None:
            r = requests.get(self.url)
            if r.status_code not in range(200, 299):
                return None

            html_string = r.text
            cache.set(self.url, html_string, timeout=60*60) #Cashe for 1 hour
        html = BeautifulSoup(html_string, self.PARSER)
        return html


    def get__gift_menu(self):
        """
        return gift menu
        """
        html = self.get_html()
        if html == None:
            return []
        
        gifts_menu = html.find("li", {'class': "megaMenuWithIndex_5"})
        return gifts_menu


    def get_categories_of_gift(self):
        """
        Return category of gift's menu :)
        """
        menu = self.get__gift_menu()
        if not menu:
            return []
        categories = menu.find_all("div", {'class': 'tb-megamenu-column span2 mega-col-nav'})
        return categories


    def get_gifts(self):
        categories = self.get_categories_of_gift()
        gifts = []
        for gift in categories:
            gift_title = gift.find("a", {"class": "mega-group-title"})
            next_tag_for_children = gift_title.next_sibling
            children_gifts = next_tag_for_children.find_all("li", {"class": "tb-megamenu-item level-3 mega"})
            data = {
            "parent": gift_title.string,
            "children": []
            }
            for child in children_gifts:
                a_tag = child.a
                child_data = {'name': a_tag.string}
                data['children'].append(child_data)
            gifts.append(data)
        return gifts
    

    def filter_gift(self, num: int):
        return self.get_gifts()[num]



