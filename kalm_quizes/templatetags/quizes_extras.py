from django import template

register = template.Library()


@register.simple_tag
def get_dict_val(dict:dict, key):
    key_f = str(key)
    return dict[key_f]


@register.simple_tag
def get_list_element(list, index):
    try:
        back = list[index]
    except (IndexError):
        back = None
    return back