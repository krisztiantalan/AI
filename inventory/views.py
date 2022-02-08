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

    try:
        asset_result = Asset.objects.get(Q(vonalkod=query) | Q(gyari_szam=query) | Q(gep_szam=query))
        return redirect('inventory:asset', id=asset_result.id)
    except ObjectDoesNotExist:
        try:
            user_result = User.objects.get(Q(nev=query) | Q(felhasznalo_nev=query))
            return redirect('inventory:user', id=user_result.id)
        except ObjectDoesNotExist:
            return render(request, 'inventory/index.html', {
                    'error': 'Nincs találat.',
                    'users': User.objects.all(),
                    'assets': Asset.objects.all(),
                })


def modify(request, id):
    if request.method == 'POST':
        current_asset = Asset.objects.get(id=id)
        user_after_modify = current_asset.user_id
        if 'raktar' in request.POST:
            current_asset.user_id = 1
            current_asset.save()
            return redirect('inventory:user', id=user_after_modify)
        elif 'selejt' in request.POST:
            current_asset.user_id = 2
            current_asset.save()
            return redirect('inventory:user', id=user_after_modify)
        elif 'user' in request.POST:
            current_asset.user_id = request.POST.get('user')
            current_asset.save()
            return redirect('inventory:asset', id=current_asset.id)
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
