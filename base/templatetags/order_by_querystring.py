from django import template

register = template.Library()


@register.simple_tag
def get_order_by_querystring(ordering, current_order=None, remove=False):
    """
    Using the ordering parameter (a list), returns a query string with the
    orders of the columns

    The parameter current_order can be passed along to handle the specific
    order of a single column. So for example if you are ordering by 'email' and
    'first_name', you can pass on 'email' as the current order, so the system
    can keep every other order, but inverse the order of the email field.
    """

    if not current_order:
        return '&'.join(['o={}'.format(o) for o in ordering])

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
