from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import email_verification_token
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

verified_emails = set()

def send_verification_email(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_active:
        token = email_verification_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        print(f"uid in send-verification function : {uid}")
        verification_link = request.build_absolute_uri(
            reverse('verify_email', args=[uid, token])
        )
        subject = "Verify your email address"
        message = f"Click the link to verify your email: {verification_link}"
        send_mail(subject, message, 'your_email@example.com', [user.email])
        return HttpResponse("Verification email sent.")
    return HttpResponse("User is already active.")


def verify_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if a user with this email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse("Email not registered!")

        # Generate the email verification link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        print(f"ud inside verify-email : {uid}")
        token = default_token_generator.make_token(user)
        verification_link = request.build_absolute_uri(
            f"/verify-email/{uid}/{token}/"
        )

        # Send the verification email
        send_mail(
            subject='Verify Your Email',
            message=f'Click the link to verify your email: {verification_link}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return HttpResponse("Verification email sent! Check your inbox.")

    return render(request, 'verify_email.html')

def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        print(f"uid inside confirm-email : {uid}")
        user = User.objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            verified_emails.add(user.email)
            return redirect('/verify-email/?verified=true')
    except Exception as e:
        print(e)
    return HttpResponse('Invalid or expired link')

