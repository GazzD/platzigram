""" Platigram Views """

from django.http import HttpResponse
from datetime import datetime
import json 



def hellow_world(request):
    """ Return a greeting. """
    return HttpResponse('Oh, hi! Current server time es {now}'.format(
        now=datetime.now().strftime('%b %dth, %Y - %H:%M hrs')
    ))

def sort_integers(request):
    """ Hi. """
    numbers = request.GET['numbers']
    # numbers = list(map(int, numbers.split(',')))
    # List comprehantions
    numbers = [int(i) for i in numbers.split(',')]
    numbers.sort()
    # import pdb; pdb.set_trace()
    response = {
        'status': 'ok',
        'numbers': numbers,
        'message': 'Integer s sorted successfully'
    }
    return HttpResponse(json.dumps(response, indent=4), content_type="application/json")

def say_hi(request, name, age):
    """ Return greeting. """
    # if age < 12:
    #     message = 'Sorry {}, you are not allowed to be here'.format(name)
    # else:
    #     message = 'Welcome {}'.format(name)
    return 'message'