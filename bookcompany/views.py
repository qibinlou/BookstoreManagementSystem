from django.shortcuts import render_to_response

def homepage(request):
    head = 'Book Company Management Website'
    title = 'HomePage'
    return render_to_response('index.html', locals())
