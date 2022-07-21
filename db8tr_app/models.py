from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):

    """A user's profile contains a list of others the user follows."""
    # This makes a profile to be associated with one and only one user.
    # Also specifies that when a user is deleted, the associated profile will too.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # One user's profile can follow many other user profiles.
    # One user's profile can be followed by many other profiles.
    follows = models.ManyToManyField(
        "self",
        # Handy name to access the reverse side of the relationship.
        related_name="followed_by",
        # Users can follow someone without them following back.
        symmetrical=False,
        # Users don’t *have* to follow anyone.
        blank=True
    )

    # A user's debate queue contains a list of users this user wants to debate with.
    wants_to_debate = models.ManyToManyField(
        "self",
        related_name="wants_me_to_debate",
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        # return f"{self.user.username}-profile"
        return f"user_id: {self.user_id}, follows: {self.follows}."


# class DebateQueue(models.Model):


#     def __str__(self):
#         return f"{self.user.username}"


# Note: The Django documentation mentions that the best place
# to put your signals is in a new signals.py submodule of the app.
# However, this requires making additional changes in the app
# configuration. Since we only need to build out a single signal
# for the tutorial, we’re keeping it in models.py.
#
# Add a hook for every time the User model's save() is called.
@receiver(post_save, sender=User)
# Set up a Profile (with a debate queue) for each new user.
def setup_user(sender, instance, created, **kwargs):

    print("post-save-hook:")
    print(f"sender: {sender}")
    print(f"instance: {instance}")
    print(f"instance.profile: {instance.profile}")
    print(f"created: {created}")
    # Only create a new Profile and a new DebateQueue for this User
    # if it was newly created, and created successfully.
    if created:
        user_profile = Profile(user=instance)
        print(f"user_profile: {user_profile}")
        user_profile.save()
        user_profile.follows.add(instance.profile)
        print(f"user_profile.follows: {user_profile.follows}")
        user_profile.save()
