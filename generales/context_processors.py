from generales.models import Categoria

def menu_categories(request):
    categorias = Categoria.objects.all()
    print(">>>>>>>> TOTAL CATEGORIAS:", categorias.count())

    roots = Categoria.objects.filter(parent=None, activo=True).order_by("orden")
    print(">>>>>>>> ROOT ITEMS:", roots.count())

    return {
        "MENU_TREE": build_tree(roots)
    }

def build_tree(nodes):
    tree = []
    for n in nodes:
        children = Categoria.objects.filter(parent=n).order_by("orden")
        tree.append({
            "id": n.id,
            "nombre": n.nombre,
            "url": n.url,
            "children": build_tree(children) if children.exists() else []
        })
    return tree
