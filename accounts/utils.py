from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from constants import FRONTEND_URL
from django.conf import settings

def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verify_url = f"{FRONTEND_URL}/verify-email?token={token}&email={user.email}"

    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
        font-family: Arial, sans-serif;
        }}
        .verify-button {{
        background-color: #fd851c;
        }}
        .verify-button:hover {{
        opacity: 0.8;
        }}
    </style>
    </head>
    <body>
        <div style='color:black;'>
            <div width="100%" height="100%" style="padding:50px; background-color: #f5f5f5">
            <div border="0" cellpadding="0" cellspacing="0">
                <div>
                    <h1>
                        Jourist Learn Registration
                    </h1>
                </div>
                <div style='margin-bottom: 20px;'>
                    <div style="padding:20px; font-size:16px; background-color: #ffffff">
                        <p>Hello,</p>
                        <p>Thank you for registering on <a href="{FRONTEND_URL}">Jourist Learn</a>.</p>
                        <p>To complete your registration, please confirm your email address by clicking the following button:</p>
                        <a href="{verify_url}" class="verify-button" style="color: white; display: inline-block; padding: 10px 20px; font-size: 16px; text-decoration: none; border-radius: 5px; margin-top: 0px;">Confirm Email Address</a>
                        <br />
                        <p>Please note that this link is only valid for 15 minutes.</p>
                        <p>If you did not register at <a href="{FRONTEND_URL}">jourist-learn.jourist.cloud</a>, you can ignore this email.</p>
                        <p style='margin:0px;'>Best regards</p>
                        <p style='margin:0px;'>Jourist Learn Team</p>
                        <a href="{FRONTEND_URL}">jourist-learn.jourist.cloud</a>
                    </div>
                </div>
                <div>
                    <div style="font-size:10px; background-color: #f5f5f5">
                        Jourist Verlags GmbH, Diagonalstraße 41, 20537 Hamburg, Germany<br>
                        Ust-IdNr.: DE 201975776, HRB: 71336, Place of jurisdiction: Hamburg, Managing director: Igor Jourist
                    </div>
                </div>
                <div style='margin-top: 10px;'>
                    <div style="font-size:10px; background-color: #f5f5f5">
                        <a href="{FRONTEND_URL}/privacy">Privacy Policy</a> • <a href="{FRONTEND_URL}/impress">Impress</a> • <a href="{FRONTEND_URL}/contact">Contact Us</a>
                    </div>
                </div>
            </div>
            </div>
        </div>
    </body>
    </html>
    '''

    text_content = strip_tags(html_content)  # fallback for non-HTML email clients

    email_msg = EmailMultiAlternatives("Confirm your email address", text_content, settings.EMAIL_SENDER, [user.email])
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()

def send_forgot_password_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = f"{FRONTEND_URL}/reset-password?uid={uid}&token={token}"

    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
        font-family: Arial, sans-serif;
        }}
        .reset-button {{
        background-color: #fd851c;
        }}
        .reset-button:hover {{
        opacity: 0.8;
        }}
    </style>
    </head>
    <body>
        <div style='color:black;'>
            <div width="100%" height="100%" style="padding:50px; background-color: #f5f5f5">
            <div border="0" cellpadding="0" cellspacing="0">
                <div>
                    <h1>
                        Reset your password – Jourist Learn
                    </h1>
                </div>
                <div style='margin-bottom: 20px;'>
                    <div style="padding:20px; font-size:16px; background-color: #ffffff">
                        <p>Hello,</p>
                        <p>You have requested to reset your password on <a href="{FRONTEND_URL}">Jourist Learn</a>.</p>
                        <p>Click on the following button to reset your password:</p>
                        <a href="{reset_url}" class="reset-button" style="color: white; display: inline-block; padding: 10px 20px; font-size: 16px; text-decoration: none; border-radius: 5px; margin-top: 0px;">Reset password</a>
                        <br />
                        <p>This link is only valid for 15 minutes.</p>
                        <p>If you did not request this, you can ignore this email.</p>
                        <p style='margin:0px;'>Best regards</p>
                        <p style='margin:0px;'>Jourist Learn Team</p>
                        <a href="{FRONTEND_URL}">jourist-learn.jourist.cloud</a>
                    </div>
                </div>
                <div>
                    <div style="font-size:10px; background-color: #f5f5f5">
                        Jourist Verlags GmbH, Diagonalstraße 41, 20537 Hamburg, Germany<br>
                        Ust-IdNr.: DE 201975776, HRB: 71336, Place of jurisdiction: Hamburg, Managing director: Igor Jourist
                    </div>
                </div>
                <div style='margin-top: 10px;'>
                    <div style="font-size:10px; background-color: #f5f5f5">
                        <a href="{FRONTEND_URL}/privacy">Datenschutz</a> • <a href="{FRONTEND_URL}/impress">Impress</a> • <a href="{FRONTEND_URL}/contact">Kontakt</a>
                    </div>
                </div>
            </div>
            </div>
        </div>
    </body>
    </html>
    '''

    text_content = strip_tags(html_content)

    email_msg = EmailMultiAlternatives("Reset your password – Jourist Learn", text_content, settings.EMAIL_SENDER, [user.email])
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()
