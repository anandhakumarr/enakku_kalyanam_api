from graphql import GraphQLError
import datetime

def get_wrapper_details(data_wrapper, qs, page, size):
    
    if page <= 1:
        skip = 0
        current_page = 1
    else:
        skip = (page - 1) * size
        current_page = page

    total_elements = qs.count()
    total_pages = int(total_elements / size) 
    total_pages += 1 if (total_elements % size) > 0 else 0

    
    if total_pages > current_page:
        has_next_page = True
    else:
        has_next_page = False

    if skip:
        qs = qs[skip:]
    if size:
        qs = qs[:size]

    number_of_elements = qs.count()

    keyword_args = {
        'results': qs,
        'total_elements': total_elements,
        'size': size,
        'total_pages': total_pages,
        'current_page': current_page,
        'has_next_page': has_next_page,
        'number_of_elements': number_of_elements,         
    }

    return data_wrapper(**keyword_args)


def wrapper_without_pagination(data_wrapper, qs):
    keyword_args = {
        'results': qs  
    }
    return data_wrapper(**keyword_args)


def get_logdate_info(start_logdate, end_logdate):

    if start_logdate:
        start_logdate = datetime.datetime.strptime(start_logdate, '%Y-%m-%d').date()
    if end_logdate:
        end_logdate = datetime.datetime.strptime(end_logdate, '%Y-%m-%d').date()

    key = None
    value = None

    if start_logdate and not end_logdate:
        key = 'logdate__gte'
        value = start_logdate
    elif end_logdate and not start_logdate:
        key = 'logdate__lte'
        value = end_logdate
    else:
        if end_logdate >= start_logdate:
            key = 'logdate__range' 
            value = (start_logdate,end_logdate)
        else:
            raise GraphQLError("StartDate should be <= EndDate")
    return (key, value)