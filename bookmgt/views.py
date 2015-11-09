from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from bookmgt.models import Author,Book
from django.template import Context
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import datetime
import time
#afdsf
class BF(forms.Form):
	ISBN = forms.IntegerField()
	Title = forms.CharField(max_length = 30)
	Publisher = forms.CharField(max_length = 30)
	PublishDate = forms.DateTimeField()
	Price = forms.FloatField()

class AF(forms.Form):
    AuthorID = forms.IntegerField()
    Name = forms.CharField(max_length= 30)
    Age = forms.CharField(max_length = 10)
    #timestamp = forms.DateTimeField(auto_now_add=True)
    country = forms.CharField(max_length = 30)

def getDoc(request):
	   if(request.GET.get('id',False)):
	   	g = request.GET
	   	pap = Book.objects.get(ISBN = g['id'])
	   	if(pap):
	   		pap.delete()
	   if(request.method == "POST"):
	      post = request.POST
	      bf = BF(request.POST)
	      af = AF(request.POST)
	      if bf.is_valid() and af.is_valid():
	        a = Author(
	            AuthorID = af.cleaned_data['AuthorID'],
	            Name = af.cleaned_data["Name"],
	            Age = af.cleaned_data["Age"],
	            country = af.cleaned_data['country']
	        )
	        b = Book(
	             ISBN = bf.cleaned_data['ISBN'],
	             Title = bf.cleaned_data["Title"],
	             Publisher = bf.cleaned_data["Publisher"],
	             PublishDate = bf.cleaned_data["PublishDate"],
	             Price = bf.cleaned_data["Price"]
	            )
	        try:
	        	au = Author.objects.get(AuthorID = a.AuthorID)
	        	au.Name = a.Name
	        	au.Age =a.Age
	        	au.country =a.country
	        except ObjectDoesNotExist:
	        	au = a
	        au.save()
	        try:
	        	bo = Book.objects.get(ISBN = b.ISBN)
	        	bo.Title =b.Title
	        	bo.Publisher =b.Publisher
	        	bo.PublishDate =b.PublishDate
	        	bo.Price =b.Price
	        except ObjectDoesNotExist:
	        	bo = b
	        bo.Author = au
	        bo.save()
	        return HttpResponse(
	        '''
	        <html>
	
									<body>
									
										<h1>OK</h1>
									</body>
									
					</html>
	        
	        '''
	        
	        )
	      else:
	        return	 HttpResponse(
	        '''
	        <html>
	
									<body>
									
										<h1>unvaild!</h1>
									</body>
									
					</html>
	        
	        ''')
	   else:
	     return render(request,"reg2.html")


def ok():
	return HttpResponse(
		 '''
        <html>

								<body>
								
									<h1>OK</h1>
								</body>
								
				</html>
        
        '''
  )
def notvalid():
	return HttpResponse(
			 '''
	        <html>
	
									<body>
									
										<h1>not valid!</h1>
									</body>
									
					</html>
	        
	        '''
			
			)
def ViewPaper(request):
	b ={}
	if len(request.GET):
		Get = request.GET
		if(Get.get('name',False)):
			try:
				au = Author.objects.filter(Name = Get["name"])
			except ObjectDoesNotExist:
				return notvalid()
			print au
			if(len(au)):
				for i in au:
					if(not b):
						b = Book.objects.filter(Author = i)
					b = b | Book.objects.filter(Author = i)
				return render_to_response("liu.html",{"paper_list":b})
			else:
				return 	 HttpResponse(
		        '''
		        <html>
		
										<body>									
											<h1>Not Found!</h1>
										</body>
										
						</html>
		        
		        ''')
		elif(Get.get('id',False)):
			b = Book.objects.filter(ISBN = Get['id'])
			return render_to_response("liu.html",{"paper_list":b})
		else:
			return notvalid()
	else:
		print 2
		b = Book.objects.all()
		return render_to_response("liu.html",{"paper_list":b})




def dele(req):
	if(req.GET.get('id',False)):
		g = req.GET
		pap = Book.objects.get(ISBN = g['id'])
		if(pap):
			pap.delete()
			return ok()
		return notvalid()


def change(req):
	if(req.GET.get('id',False)):
		print 2
		g = req.GET
		pap = Book.objects.get(ISBN = g['id'])
		if(pap):
			#pap.delete()
			return render_to_response("reg.html",{"paper":pap})
	return notvalid()

def readonly(req):
	if(req.GET.get('id',False)):
		g = req.GET
		pap = Book.objects.get(ISBN = g['id'])
		if(pap):
			#pap.delete()
			return render_to_response("readonly.html",{"paper":pap})
	return notvalid()


def tst(req):
	return render(req,"liu.html")


def tst2(req):
	return render(req,"reg2.html")