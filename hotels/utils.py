menu = [

    {'title': "Отели", 'url_name': 'hotels_list'},
    {'title': "О проекте", 'url_name': 'about'},
    {'title': "Обратная связь", 'url_name': 'contact'},
]

dopmenu = [
    {'title': "Добавить отель", 'url_name': 'add_hotel'},
    {'title': "Добавить номер", 'url_name': 'add_room'},
]


class DaaMixin:
    paginate_by = 6
    title_page = None
    cat_selected = None
    extra_context = {}
