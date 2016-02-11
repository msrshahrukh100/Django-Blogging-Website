from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Post
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import PostForm
# Create your views here.


def post_create(request):
	form = PostForm(request.POST or None,request.FILES or None )
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Successfully Created!")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context = {
	"form":form,
	}
	return render(request,'post_form.html',context) 

def post_detail(request,id):
	instance = get_object_or_404(Post,id=id)
	context = {
	"title":instance.title,
	"instance":instance
	}
	return render(request,'post_detail.html',context)
	

def post_list(request):
	queryset_total = Post.objects.all()#.order_by("-timestamp")
	# contact_list = Contacts.objects.all()
	paginator = Paginator(queryset_total, 2) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	# return render(request, 'list.html', {'contacts': contacts})

	context = {
		"object_list":queryset,
		"title":"List"
	}
	return render(request,'base.html',context)
	# return HttpResponse("<h1>List</h1>") 

#

    

#




def post_update(request,id=None): 
	instance = get_object_or_404(Post,id=id)
	form = PostForm(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Successfully Updated!")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
	"form":form,
	}
	return render(request,'post_form.html',context) 




def post_delete(request,id=None):
	instance = get_object_or_404(Post,id=id)
	instance.delete()
	messages.success(request,"Successfully Deleted!")
	return redirect("/posts")
	 