from django.shortcuts import render


def main_page(request):
    return render(request, 'educational_service/main_page.html')
