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

    asset_result = Asset.objects.filter(Q(barcode__icontains=query) | Q(serial_no__icontains=query) |
                                        Q(designation__icontains=query) | Q(serial_no__icontains=query))

    user_result = User.objects.filter(Q(name__icontains=query) | Q(username__icontains=query) |
                                      Q(department__icontains=query) | Q(office__icontains=query))

    return render(request, 'inventory/results.html', {
        'assets': asset_result,
        'users': user_result,
    })


def create_user(request):
    if request.method == 'POST':
        if request.POST.get('name') and request.POST.get('username') and request.POST.get('department') and request.POST.get('office'):
            user = User()
            user.name = request.POST.get('name')
            user.username = request.POST.get('username')
            user.department = request.POST.get('department')
            user.office = request.POST.get('office')
            user.save()
            return redirect('inventory:total')
        else:
            return redirect('inventory:create_user')
    else:
        return render(request, 'inventory/create_user.html')


def create_asset(request):
    if request.method == 'POST':
        if request.POST.get('barcode') and request.POST.get('serial_no') and request.POST.get('designation'):
            asset = Asset()
            asset.barcode = request.POST.get('barcode')
            asset.serial_no = request.POST.get('serial_no')
            asset.designation = request.POST.get('designation')
            asset.other = request.POST.get('other')
            # the default user on new asset creation is stock
            asset.user_id = 1
            asset.save()
            return redirect('inventory:total')
        else:
            return redirect('inventory:create_asset')
    else:
        return render(request, 'inventory/create_asset.html')


def modify(request, id):
    if request.method == 'POST':
        if 'stock' in request.POST:
            current_asset = Asset.objects.get(id=id)
            prev_user = current_asset.user_id
            current_asset.user_id = 1
            current_asset.save()
            return redirect('inventory:user', id=prev_user)
        elif 'waste' in request.POST:
            current_asset = Asset.objects.get(id=id)
            prev_user = current_asset.user_id
            current_asset.user_id = 2
            current_asset.save()
            return redirect('inventory:user', id=prev_user)
        elif 'delete_user' in request.POST:
            current_user = User.objects.get(id=id)
            current_user.delete()
            return redirect('inventory:total')
        elif 'delete_asset' in request.POST:
            current_asset = Asset.objects.get(id=id)
            current_asset.delete()
            return redirect('inventory:total')
        elif 'user' in request.POST:
            current_asset = Asset.objects.get(id=id)
            prev_user = current_asset.user_id
            current_asset.user_id = request.POST.get('user')
            current_asset.save()
            return redirect('inventory:user', id=prev_user)


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
