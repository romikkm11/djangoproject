from django.shortcuts import render, redirect
from .models import Articles
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView, DeleteView
from .models import Company, ServiceType, Service, Price
from django.http import JsonResponse
from django.db.models import Q


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

def show_companies_on_map(request):
    companies = Company.objects.all()
    companies_data = [
        {'latitude': company.latitude, 'longititude': company.longititude, 'name': company.name}
        for company in companies
    ]
    return JsonResponse({'companies': companies_data}) 


def get_filters(request):
    service_types = ServiceType.objects.all().values('id', 'name')
    services = Service.objects.all().values('id', 'name', 'type_id')
    companies = Company.objects.all().values('id', 'name')

    filters = {
        "service_types": list(service_types),
        "services": list(services),
        "companies": list(companies)
    }

    return JsonResponse(filters)

def filter_companies(request):
    service_type_id = request.GET.get('service_type')
    service_id = request.GET.get('service')
    company_id = request.GET.get('company')

    filters = Q()

    if company_id:
        filters &= Q(company__id=company_id)

    if service_id:
        filters &= Q(service__id=service_id)

    if service_type_id:
        filters &= Q(service__type__id=service_type_id)

    prices = Price.objects.filter(filters)
    data_element = [
        {
            "name": price.company.name,
            'latitude' : price.company.latitude,
            'longititude' : price.company.longititude,
            "service_type": price.service.type.name,
            "service": price.service.name,
            "from": price.min_price,
            "to": price.max_price
        }
        for price in prices
    ]

    return JsonResponse({"results": data_element}, safe=False)