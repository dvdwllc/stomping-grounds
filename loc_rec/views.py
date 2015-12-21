from django.template.response import TemplateResponse

def index(request):
    context = {'user': request.user}

    return TemplateResponse(
        request,
        'base/index.html',
        context
    )