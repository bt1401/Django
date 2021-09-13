from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from.models import Title, Headline
from.forms import PostForm
from django.contrib.auth import authenticate, login 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import requests
from bs4 import BeautifulSoup 
# Create your views here.

def scrape(request):
  Headline.objects.all().delete()
  session = requests.Session()
  session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
  url = "https://www.theonion.com/latest"
  content = session.get(url).content
  soup = BeautifulSoup(content, "html.parser")
  News = soup.find_all('div', {"class":"cw4lnv-11 dFCKPx"})
  for article in News:
    linkx = article.find('a', {"class":"sc-1out364-0 hMndXN js_link"})
    link=linkx['href']
    titlex = article.find('h2', {"class":"sc-759qgu-0 iRbzKE cw4lnv-6 bqAYXy"})
    title = titlex.text
    new_headline = Headline()
    new_headline.title = title
    new_headline.url = link
    new_headline.save()
  return redirect("../")


def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {'object_list': headlines,}
    return render(request, "mysite/scrape.html", context)
    
    
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
            return HttpResponse('You do not have access!')
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

