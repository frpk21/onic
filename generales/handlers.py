
from generales.choices import LinkType
from generales.models import Categoria


class MenuHandler:

    @classmethod
    def make_tree(cls) -> list[dict]:
        values = ['id', 'parent_id', 'url', 'nombre', 'link_type']
        categories = list(Categoria.objects.filter(activo=True).order_by('orden').values(*values))

        for category in categories:
            category['children'] = [x for x in categories if category['id'] == x['parent_id']]

        return [x for x in categories if not x['parent_id']]

    @classmethod
    def render_menu(cls):
        menu_items = cls.make_tree()
        return cls.render_menu_html(menu_items)

    @classmethod
    def render_menu_html(cls, menu_data: list[dict]) -> str:
        """Recursively renders the HTML for the menu."""
        html = '<div class="main-nav__main-navigation"><ul class="main-nav__navigation-box">'
        for item in menu_data:
            html += cls.render_item_html(item)
        html += '</ul></div>'
        return html

    @classmethod
    def render_item_html(cls, item: dict):
        """Render each item and its children recursively."""
        if item['children']:
            html = f'<li class="dropdown"><a href="#">{item["nombre"]}</a><ul>'
            for child in item['children']:
                html += cls.render_item_html(child)
            html += '</ul><button class="dropdown-btn"><i class="fa fa-angle-right"></i></button></li>'
        else:
            target = ' target="_blank"' if item['url'] and LinkType.BLANK in item['link_type'] else ''
            html = f'<li><a href="{item["url"]}?category={item["id"]}"{target}>{item["nombre"]}</a></li>'
        return html
