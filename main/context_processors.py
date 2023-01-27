from .models import information


def get_information(request):
    return {'info': information.objects.all()}
