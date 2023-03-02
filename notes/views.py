from django.http import HttpResponse
from django.template import loader

# тут також можна трішки скоротити цей код використовуючи render
def index(request):
    template = loader.get_template('notes/index.html')
    return HttpResponse(template.render())
