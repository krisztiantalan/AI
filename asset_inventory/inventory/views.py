from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.db.models import Q

from .models import Asset, User


def index(request):
    return render(request, 'inventory/index.html', {
        'users': User.objects.all(),
        'assets': Asset.objects.all(),
    })


def results(request):
    query = request.GET.get('q')

    if not query:
        return redirect('inventory:index')

    asset_result = Asset.objects.filter(Q(barcode__icontains=query) | Q(serial_no__icontains=query))

    user_result = User.objects.filter(Q(name__icontains=query) | Q(username__icontains=query))

    return render(request, 'inventory/results.html', {
        'assets': asset_result,
        'users': user_result,
    })


def modify(request, id):
    if request.method == 'POST':
        current_asset = Asset.objects.get(id=id)
        prev_user = current_asset.user_id
        if 'stock' in request.POST:
            current_asset.user_id = 1
            current_asset.save()
            return redirect('inventory:user', id=prev_user)
        elif 'waste' in request.POST:
            current_asset.user_id = 2
            current_asset.save()
            return redirect('inventory:user', id=prev_user)
        elif 'user' in request.POST:
            current_asset.user_id = request.POST.get('user')
            current_asset.save()
            return redirect('inventory:user', id=prev_user)
        else:
            return redirect('inventory:index')


def asset(request, id):
    return render(request, 'inventory/asset.html', {
        'asset': Asset.objects.get(id=id),
        'users': User.objects.all(),
        'assets': Asset.objects.all(),
    })


def user(request, id):
    return render(request, 'inventory/user.html', {
        'user': User.objects.get(id=id),
        'users': User.objects.all(),
        'assets': Asset.objects.all(),
    })


def total(request):
    return render(request, 'inventory/total.html', {
        'users': User.objects.all(),
        'assets': Asset.objects.all(),
    })
