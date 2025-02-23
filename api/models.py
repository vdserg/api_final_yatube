from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title}"


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts")
    group = models.ForeignKey(
        Group, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="group_posts",
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    text = models.TextField()
    created = models.DateTimeField("Дата добавления", auto_now_add=True,
                                   db_index=True)


class Follow(models.Model):
    user = models.ForeignKey(User, related_name="following",
                             on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="follower",
                                  on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'following']

    def __str__(self):
        return f"Follower: {self.user} - Following: {self.following}"

