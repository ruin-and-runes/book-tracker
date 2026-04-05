from django.shortcuts import render, get_object_or_404
from .models import Book
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse
import requests
import random


def home(request):

    # THEME (default DARK)
    theme = request.GET.get("theme")
    if theme == "pastel":
        css = "css/style.css"
    else:
        css = "css/dark.css"

    # SHELF FILTER
    shelf = request.GET.get("shelf")
    books = Book.objects.all()

    if shelf:
        books = books.filter(shelf=shelf)

    # SEARCH (FIXED)
    query = request.GET.get('q')
    if query:
        books = books.filter(Q(title__icontains=query) | Q(tropes__name__icontains=query)).distinct()

    # FETCH COVERS
    books_with_covers = []

    for book in books:

        cover_url = None

        # 1. Uploaded image
        if hasattr(book, "cover_image") and book.cover_image:
            cover_url = book.cover_image.url

        # 2. Manual URL
        elif hasattr(book, "cover_url") and book.cover_url:
            cover_url = book.cover_url

        # 3. Auto fetch
        else:
            try:
                response = requests.get(
                    f"https://openlibrary.org/search.json?title={book.title}&author={book.author}"
                )
                data = response.json()

                best_match = None

                for doc in data.get("docs", []):
                    title_match = book.title.lower() in doc.get("title", "").lower()
                    author_match = book.author.lower() in " ".join(doc.get("author_name", [])).lower()

                    if title_match and author_match:
                        best_match = doc
                        break

                if not best_match and data.get("docs"):
                    best_match = data["docs"][0]

                if best_match:
                    cover_id = best_match.get("cover_i")
                    if cover_id:
                        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"

            except:
                pass

        # fallback
        if not cover_url:
            cover_url = "https://via.placeholder.com/140x210?text=No+Cover"

        books_with_covers.append({
            "book": book,
            "cover": cover_url
        })

    # RANDOM BOOK
    random_book = random.choice(books) if books else None

    return render(request, "books/home.html", {
        "books_with_covers": books_with_covers,
        "css_file": css,
        "random_book": random_book,
    })


def stats(request):

    css = "css/dark.css"

    total_books = Book.objects.count()
    tbr_count = Book.objects.filter(shelf="tbr").count()
    reading_count = Book.objects.filter(shelf="reading").count()
    read_count = Book.objects.filter(shelf="read").count()

    top_trope = (
        Book.objects
        .values("tropes__name")
        .annotate(count=Count("tropes"))
        .order_by("-count")
        .first()
    )

    return render(request, "books/stats.html", {
        "css_file": css,
        "total_books": total_books,
        "tbr_count": tbr_count,
        "reading_count": reading_count,
        "read_count": read_count,
        "top_trope": top_trope,
    })


def book_detail(request, book_id):

    css = "css/dark.css"
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":

        if "toggle_read" in request.POST:
            book.shelf = "read" if book.shelf != "read" else "tbr"

        else:
            book.notes = request.POST.get("notes")
            book.progress = request.POST.get("progress") or 0

        book.save()

    # COVER LOGIC
    cover_url = None

    if hasattr(book, "cover_image") and book.cover_image:
        cover_url = book.cover_image.url

    elif hasattr(book, "cover_url") and book.cover_url:
        cover_url = book.cover_url

    else:
        try:
            response = requests.get(
                f"https://openlibrary.org/search.json?title={book.title}&author={book.author}"
            )
            data = response.json()

            if data.get("docs"):
                cover_id = data["docs"][0].get("cover_i")
                if cover_id:
                    cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

        except:
            pass

    if not cover_url:
        cover_url = "https://via.placeholder.com/200x300?text=No+Cover"

    return render(request, "books/detail.html", {
        "book": book,
        "cover": cover_url,
        "css_file": css,
    })

def reset_admin(request):
    user = User.objects.get(username='admin')
    user.set_password('admin123')
    user.save()
    return HttpResponse("Password reset")
