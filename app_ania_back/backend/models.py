from django.db import models


class Guild(models.Model):
    guild_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class User(models.Model):
    discord_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=50)
    avatar_url = models.URLField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    guilds = models.ManyToManyField(Guild, related_name="members")

    def __str__(self):
        return self.username


class Channel(models.Model):
    CHANNEL_TYPE = [
        ("voice", "Voice"),
        ("text", "Text"),
        ("category", "Category"),
    ]

    guild = models.ForeignKey(
        Guild,
        on_delete=models.CASCADE,
        related_name="channels"
    )

    channel_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=150)
    channel_type = models.CharField(max_length=20, choices=CHANNEL_TYPE)

    def __str__(self):
        return self.name


class GuildConfig(models.Model):
    guild = models.OneToOneField(
        Guild,
        on_delete=models.CASCADE,
        related_name="config"
    )

    listening_enabled = models.BooleanField(default=True)

    voice_channel = models.ForeignKey(
        Channel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="voice_configs"
    )

    text_channel = models.ForeignKey(
        Channel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="text_configs"
    )

    confidence_threshold = models.FloatField(default=0.7)
    auto_actions_enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)


class ActionLog(models.Model):
    guild = models.ForeignKey(
        Guild,
        on_delete=models.CASCADE,
        related_name="actions"
    )

    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="actions"
    )

    action_type = models.CharField(max_length=150)
    payload = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)

class BotPermission(models.Model) :
    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code
    

class GuildRolePermission(models.Model) :
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    role_id = models.BigIntegerField()
    permissions = models.ManyToManyField(BotPermission)
    


