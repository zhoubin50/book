from django.shortcuts import render, redirect, HttpResponse
from app01 import models

# Create your views here.


def publisher_list(request):
    ret = models.Publisher.objects.all().order_by('id')
    return render(request, "publisher_list.html", {"publisher_list": ret})


def add_publisher(request):
    err_msg = ""
    if request.method == 'POST':
        new_publisher = request.POST.get('publisher_name')
        if models.Publisher.objects.filter(name=new_publisher):
            err_msg = "出版社名称重复"
        elif new_publisher:
            models.Publisher.objects.create(name=new_publisher)
            return redirect("/publisher_list/")
        else:
            err_msg = "出版社名称不能为空"
    return render(request, "add_publisher.html", {"err_msg": err_msg})


def del_publisher(request):
    publisher_id = request.GET.get('id', None)
    if publisher_id:
        publisher = models.Publisher.objects.get(id=publisher_id)
        publisher.delete()
    else:
        return HttpResponse("要删除的出版不存在")
    return redirect("/publisher_list/")


def edit_publisher(request):
    if request.method == 'POST':
        publisher_id = request.POST.get('id', None)
        new_name = request.POST.get('publisher_name')
        if publisher_id:
            publisher = models.Publisher.objects.get(id=publisher_id)
            if not new_name:
                err_msg = "出版社不能为空"
                return render(request, "edit_publisher.html", {"publisher": publisher, "err_msg": err_msg})
            publisher.name = new_name
            publisher.save()
            return redirect("/publisher_list/")

    elif request.method == 'GET':
        publisher_id = request.GET.get('id', None)
        if publisher_id:
            if not models.Publisher.objects.filter(id=publisher_id):
                err_msg = "编辑的出版社不存在"
                return render(request, "edit_publisher.html", {"err_msg": err_msg})
            publisher = models.Publisher.objects.get(id=publisher_id)
            return render(request, "edit_publisher.html",{"publisher": publisher})
        else:
            err_msg = "编辑的出版社不存在"
            return render(request, "edit_publisher.html", {"err_msg": err_msg})


def book_list(request):
    books = models.Book.objects.all()
    return render(request, "book_list.html", {"books": books})


def add_book(request):
    err_msg = ""
    if request.method == 'POST':
        new_book = request.POST.get('book_title')
        publisher_id = request.POST.get("publisher")
        if models.Book.objects.filter(title=new_book):
            err_msg = "书名称重复"
        elif new_book:
            models.Book.objects.create(title=new_book, publisher_id_id=publisher_id)
            return redirect("/book_list/")
        else:
            err_msg = "书名称不能为空"
    publishers = models.Publisher.objects.all()
    return render(request, "add_book.html", {"err_msg": err_msg, "publishers": publishers})


def del_book(request):
    book_id = request.GET.get('id')
    if book_id:
        book = models.Book.objects.get(id=book_id)
        book.delete()
        return redirect("/book_list/")


def edit_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('id', None)
        new_title = request.POST.get('book_title')
        new_publisher = request.POST.get('publisher')
        if book_id:
            book = models.Book.objects.get(id=book_id)
            if not new_title:
                err_msg = "书名不能为空"
                publishers = models.Publisher.objects.all()
                edit_book = models.Book.objects.get(id=book_id)
                return render(request, "edit_book.html", {"publishers": publishers, "edit_book": edit_book,
                                                          "err_msg": err_msg})
            book.title = new_title
            book.publisher_id_id = new_publisher
            book.save()
            return redirect("/book_list/")
    if request.method == 'GET':
        edit_book_id = request.GET.get("id")
        publishers = models.Publisher.objects.all()
        edit_book = models.Book.objects.get(id=edit_book_id)
        return render(request, "edit_book.html", {"publishers": publishers, "edit_book": edit_book})


def author_list(request):
    authors = models.Author.objects.all()
    return render(request, 'author_list.html', {"authors": authors})


def add_author(request):
    if request.method == 'POST':
        new_name = request.POST.get('author_name')
        books = request.POST.getlist('books')
        author = models.Author.objects.create(name=new_name)
        author.book.set(books)
        author.save()
        return redirect('/author_list/')
    book_list = models.Book.objects.all()
    return render(request, 'add_author.html', {"book_list": book_list})


def del_author(request):
    author_id = request.GET.get("id")
    models.Author.objects.get(id=author_id).delete()
    return redirect('/author_list/')


def edit_author(request):
    if request.method == 'POST':
        author_id = request.POST.get('author_id')
        new_name = request.POST.get('author_name')
        new_books = request.POST.getlist('books')
        edit_author = models.Author.objects.get(id=author_id)
        edit_author.name = new_name
        edit_author.book.set(new_books)
        edit_author.save()
        return redirect('/author_list/')
    books = models.Book.objects.all()
    author_id = request.GET.get('id')
    author = models.Author.objects.get(id=author_id)
    return render(request, 'edit_author.html', {'author': author, 'book_list': books})