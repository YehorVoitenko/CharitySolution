from django.shortcuts import render


# Page not found
def handler404(request):
    return render(request, "error_pages/404.html")


# Forbidden - client has valid credentials but not enough privileges to perform an action
def handler403(request):
    return render(request, "error_pages/403.html")


# Unauthorized - client provides no credentials or invalid credentials
def handler401(request):
    return render(request, "error_pages/401.html")


# HttpResponseBadRequest - wrong input data
def handler400(request):
    return render(request, "error_pages/400.html")
