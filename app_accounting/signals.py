"""
Signal handlers for social authentication flows.

Handles automatic profile updates when users connect social accounts.
"""

from django.dispatch import receiver
from django.contrib.auth import get_user_model
from allauth.socialaccount.signals import social_account_added

User = get_user_model()


@receiver(social_account_added)
def update_user_social_data(request, sociallogin, **kwargs):
    """
    Update user profile data when connecting social accounts.
    
    Args:
        request: HttpRequest object
        sociallogin: SocialLogin instance containing provider data
        **kwargs: Additional keyword arguments
    """
    user = sociallogin.user
    account = sociallogin.account
    
    # Handle Google account connections
    if account.provider == "google":
        extra_data = account.extra_data
        user.social_avatar = extra_data.get("picture")
        user.email = extra_data.get("email")
        user.first_name = extra_data.get("given_name", "")
        user.last_name = extra_data.get("family_name", "")
    
    # Handle LinkedIn account connections
    elif account.provider == "linkedin_oauth2":
        extra_data = account.extra_data
        profile_data = extra_data.get("profile", {})
        user.social_avatar = profile_data.get("picture-url")
        user.social_profile_url = profile_data.get("public-profile-url")
        
        # Extract localized name data
        user.first_name = (
            profile_data.get("firstName", {})
            .get("localized", {})
            .get("en_US", "")
        )
        user.last_name = (
            profile_data.get("lastName", {})
            .get("localized", {})
            .get("en_US", "")
        )
    
    user.save()
