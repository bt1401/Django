from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from.models import Title
from.forms import PostForm
from django.contrib.auth import authenticate, login 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

class IndexClass(View):
    def get(self, requset):
        webname = "TNews"
        nav = ["Health", "Sport", "Fashion"]
        context = {"name":webname, "navi":nav}
        return render(requset, "mysite/index.html", context)

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

