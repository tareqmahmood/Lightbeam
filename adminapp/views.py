from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect

from userapp.models import User, Product, Book, Author
from .forms import *


def administration(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')

    id = request.session['id']
    if not User.objects.get(id=id).role == 'A':
        return HttpResponseRedirect('/')

    template = loader.get_template('administration-home.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def users(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')

    id = request.session['id']
    if not User.objects.get(id=id).role == 'A':
        return HttpResponseRedirect('/')

    template = loader.get_template('administration-users.html')
    admin_list = User.objects.filter(role='A')
    context = {
        'id' : id,
        'admin_list' : admin_list,
        'admin_count' : len(admin_list),
        'user_list' : User.objects.filter(role='U'),
        'addAdminForm' : AddAdminForm(),
    }
    return HttpResponse(template.render(context, request))


def change_role(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')

    id = request.session['id']
    if not User.objects.get(id=id).role == 'A':
        return HttpResponseRedirect('/')

    if request.is_ajax():
        user_id = request.POST['user_id']
        role = request.POST['role']
        if user_id == id:
            status = 0
        else:
            try:
                user = User.objects.get(id=user_id)
                user.role = role
                user.save()
                status = 1
            except Exception:
                status = 0
        mimetype = 'application/json'
        return HttpResponse(status, mimetype)


def remove_user(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')

    id = request.session['id']
    if not User.objects.get(id=id).role == 'A':
        return HttpResponseRedirect('/')

    if request.is_ajax():
        user_id = request.POST['user_id']
        if user_id == id:
            status = 0
        else:
            try:
                User.objects.get(id=user_id).delete()
                status = 1
            except Exception:
                status = 0
        mimetype = 'application/json'
        return HttpResponse(status, mimetype)


def book_approvals(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')

    id = request.session['id']
    if not User.objects.get(id=id).role == 'A':
        return HttpResponseRedirect('/')

    template = loader.get_template('administration-book-approvals.html')
    context = {
        'pending_products' : Product.objects.filter(book__approval_status='P')
    }
    return HttpResponse(template.render(context, request))


def approve_book(request):
    if not request.session.has_key('id'):
        return HttpResponseRedirect('/')

    id = request.session['id']
    if not User.objects.get(id=id).role == 'A':
        return HttpResponseRedirect('/')

    if request.is_ajax():
        product_id = request.POST['product_id']
        action = request.POST['action']
        try:
            product = Product.objects.get(id=product_id)
            if action == 'approve':
                product.book.approval_status = 'A'
                product.book.save()
                product.save()
            elif action == 'reject':
                product.delete()
                # generate notification
            status = 1
        except Exception:
            status = 0
        mimetype = 'application/json'
        return HttpResponse(status, mimetype)