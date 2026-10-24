from django.shortcuts import render
from django.http import JsonResponse
from .models import Message


def contact(request):
    if request.method == 'POST':
        # Must be logged in
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'You must be logged in to send a message.'})

        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([name, email, subject, message]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'})

        try:
            Message.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )
            return JsonResponse({'status': 'success', 'message': 'Your message has been sent successfully!'})
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'Something went wrong. Please try again.'})

    return render(request, 'contact.html', {'user': request.user})
