from django.shortcuts import render, redirect
from .models import Articles
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView, DeleteView
from .models import Service
from django.http import JsonResponse


def news_home(request):
    news = Articles.objects.order_by('-date')
    return render(request, 'news/news_home.html', {'news': news})

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article'



class NewsDeleteView(DeleteView):
    model = Articles
    success_url = '/news/'
    template_name = 'news/news-delete.html'





class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'news/create.html'

    form_class = ArticlesForm



def create(request):
    error = ''
    if request.method == 'POST': 
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма була невірною'
    form = ArticlesForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'news/create.html', data)

def show_services_on_map(request):
    services = Service.objects.all()  # Отримуємо всі записи
    services_data = [
        {'latitude': service.latitude, 'longititude': service.longititude, 'name': service.name}
        for service in services
    ]
    return JsonResponse({'services': services_data})  # JSON-відповідь

