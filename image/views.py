import traceback
import logging
logger = logging.getLogger('mysite.error')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ImageForm
from .models import Image
    
# Create your views here.
@login_required(login_url='/account/login/')
@require_POST
def upload_image(request):
    form = ImageForm(data=request.POST)
    if form.is_valid():
        try:
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return JsonResponse({'status':'1'})
        except:
            logger.error(traceback.print_exc())
            return JsonResponse({'status':'0'})
    else:
        logger.error("The form is not valid {} {}".format(form.errors, request.POST))
        return JsonResponse({'status':'2'})

@login_required(login_url='/account/login/')
def list_images(request):
    logger.info("[visited:]list_images{}".format(request.user))
    images = Image.objects.filter(user=request.user)
    return render(request, 'image/list_images.html', {'images': images})

@login_required(login_url='/account/login/')
@require_POST
def del_image(request):
    image_id = request.POST['image_id']
    try:
        image = Image.objects.get(id=image_id)
        image.image.delete()
        image.delete()
        return JsonResponse({"status":"1"})
    except:
        logger.error(traceback.print_exc())
        return JsonResponse({"status":"2"})

def falls_images(request):
    images = Image.objects.all()
    return render(request, 'image/falls_images.html', {"images":images})

