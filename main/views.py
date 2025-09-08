from django.shortcuts import render

def show_main(request):
    context = {
        'app_name': 'Football Shop',
        'name': 'Saffana Firsta Aqila',
        'class': 'PBP B'
    }

    return render(request, "main.html", context)
