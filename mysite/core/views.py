from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from .forms import BookForm
from .models import Book


class Home(TemplateView):
    template_name = 'home.html'



def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'



from django.shortcuts import render, redirect
import os
import folium
from django.views.generic import TemplateView
# Create your views here.


def map(request):
    shp_dir = os.path.join(os.getcwd(), 'media', 'books', 'pdfs')
    dir_list = os.listdir(shp_dir)

     # folium
    m = folium.Map(location=[-16.22,-71.59],zoom_start=10, tiles = 'Stamen Terrain')
    style_basin = {'fillColor': '#228B22', 'color': '#228B22'}
    style_rivers = { 'color': 'red'}
    ## rendering
    ## style

    tooltip = 'Identify Feature'

    for file in dir_list:
        folium.GeoJson(os.path.join(shp_dir, file),name=file,style_function=lambda x:style_basin).add_to(m)
     
      
    folium.Marker(
        [-16.22,-71.59], popup="<i>Basin</i>", tooltip=tooltip
    ).add_to(m)

    folium.LayerControl().add_to(m)
    ## exporting
    m=m._repr_html_()
    context = {'my_map': m}
    template_name = 'map.html'
    return render(request, 'map.html', context)


def upload(request):
    return render(request, 'upload.html')