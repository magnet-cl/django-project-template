from django import template

register = template.Library()


@register.simple_tag
def get_order_by_querytring(**kwargs):

    '''
    returns a remove user url from an object, based on the context
    '''

    ordering = kwargs['ordering']
    current_order = kwargs['current_order']
    remove = kwargs.get('remove')

    reversed_current_order = '-{}'.format(current_order)

    query_string = []

    for order in ordering:
        if order == current_order:
            if remove:
                continue
            query_string.append(reversed_current_order)
        elif order == reversed_current_order:
            if remove:
                continue
            query_string.append(current_order)
        else:
            query_string.append(order)

    # if the current orderd and it's reversed are not being currently used
    if not (current_order in ordering or reversed_current_order in ordering):
        if not remove:
            query_string.append(current_order)

    return '&'.join(['o={}'.format(o) for o in query_string])
