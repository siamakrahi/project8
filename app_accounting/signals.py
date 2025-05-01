from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(social_account_added)
def update_user_social_data(request, sociallogin, **kwargs):
    user = sociallogin.user
    account = sociallogin.account
    
    if account.provider == 'google':
        extra_data = account.extra_data
        user.social_avatar = extra_data.get('picture')
        user.email = extra_data.get('email')
        user.first_name = extra_data.get('given_name', '')
        user.last_name = extra_data.get('family_name', '')
    
    elif account.provider == 'linkedin_oauth2':
        extra_data = account.extra_data
        profile_data = extra_data.get('profile', {})
        user.social_avatar = profile_data.get('picture-url')
        user.social_profile_url = profile_data.get('public-profile-url')
        user.first_name = profile_data.get('firstName', {}).get('localized', {}).get('en_US', '')
        user.last_name = profile_data.get('lastName', {}).get('localized', {}).get('en_US', '')
    
    user.save()