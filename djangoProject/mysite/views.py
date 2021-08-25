from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from.models import Title
from.forms import PostForm
from django.contrib.auth import authenticate, login 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from bs4 import BeautifulSoup
import requests
# Create your views here.

def get_html_content(request):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://xe.baogiaothong.vn/mg5-sap-ra-mat-viet-nam-co-phien-ban-scorpio-the-thao-d521996.html').text
    return html_content


def home(request):
    result = None
    html_content = get_html_content(request)
    soup = BeautifulSoup(html_content, 'html.parser')
    result = dict()
    result['title'] = soup.find("span", attrs={"class": "tit"}).text
    result['time_post'] = soup.find("span", attrs={"class": "sb-tpic clrGre"}).text
    result['body_text']= soup.find("div", attrs={"class": "content-body bodyArt"}).text
    return render(request, 'mysite/home.html', {'result': result})
    

class IndexClass(View):
    def get(self, request):
        webname = "TNews"
        nav = ["Health", "Sport", "Fashion"]
        context = {"name":webname, "navi":nav}
        return render(request, "mysite/index.html", context)

class HomeClass(View):
    def get(self, request):
        list_title = Title.objects.all()
        context = {"baiviet" : list_title}
        return render(request, 'mysite/home.html', context)
    


class LoginClass(View):
    def get(self, request):
         return render(request, 'mysite/login.html')

    def post(self, request):
        username = request.POST.get('user_name')
        password = request.POST.get('pass_word')
        my_user = authenticate(username=username, password=password)
        if my_user is None:
          return render(request, 'mysite/login_unsuccess.html')
        
        login(request, my_user)
        return render(request, 'mysite/login_success.html')

class AddPost(LoginRequiredMixin,View):
    login_url='/login/'

    def get(self, request):
        f = PostForm()
        context = {'fm': f}
        return render(request,'mysite/add_post.html',context )

    def post(self, request):
        f = PostForm(request.POST)
        if not f.is_valid():
            return render(request, 'mysite/add_unsuccess.html')
        if request.user.has_perm('mysite.add_post'):
            f.save()
        else:
            return HttpResponse('khong co quyen')
        return render(request, 'mysite/add_success.html')

class AdminView(ListView):
    model = Title
    template_name = 'mysite/admin_site.html'

class TestDetailView(DetailView):
    model = Title
    template_name = 'mysite/admin_detailview.html'

class UpdatePost(UpdateView):
    model = Title
    template_name = 'mysite/update_post.html'
    fields = ['title', 'body_text', 'date']

class DeletePost(DeleteView):
    model = Title
    template_name = 'mysite/delete_post.html'
    success_url = reverse_lazy('mysite:admin-site')

