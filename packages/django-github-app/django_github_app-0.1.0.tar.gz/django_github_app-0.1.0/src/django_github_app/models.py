from __future__ import annotations

import datetime
from typing import Any

from asgiref.sync import async_to_sync
from django.db import models
from django.utils import timezone
from gidgethub import abc
from gidgethub import sansio
from gidgethub.apps import get_installation_access_token

from ._typing import override
from .conf import app_settings
from .github import AsyncGitHubAPI
from .github import GitHubAPIEndpoint
from .github import GitHubAPIUrl


class EventLogManager(models.Manager["EventLog"]):
    async def acreate_from_event(self, event: sansio.Event):
        return await self.acreate(
            event=event.event,
            payload=event.data,
            received_at=timezone.now(),
        )

    def create_from_event(self, event: sansio.Event):
        return async_to_sync(self.acreate_from_event)(event)

    async def acleanup_events(
        self, days_to_keep: int = app_settings.DAYS_TO_KEEP_EVENTS
    ):
        deleted = await self.filter(
            received_at__lte=timezone.now() - datetime.timedelta(days=days_to_keep)
        ).adelete()
        return deleted

    def cleanup_events(self, days_to_keep: int = 7):
        return async_to_sync(self.acleanup_events)(days_to_keep)


class EventLog(models.Model):
    id: int
    event = models.CharField(max_length=255, null=True)
    payload = models.JSONField(default=None, null=True)
    received_at = models.DateTimeField(help_text="Date and time event was received")

    objects = EventLogManager()

    @override
    def __str__(self) -> str:
        ret = [str(self.pk), self.event if self.event is not None else "unknown"]
        if self.action is not None:
            ret.append(self.action)
        return " ".join(ret)

    @property
    def action(self) -> str | None:
        if self.payload is None:
            return None
        return self.payload.get("action")


class InstallationManager(models.Manager["Installation"]):
    async def acreate_from_event(self, event: sansio.Event):
        installation_data = event.data["installation"]

        app_id = installation_data["app_id"]

        if str(app_id) == app_settings.APP_ID:
            installation = await self.acreate(
                installation_id=installation_data["id"],
                data=installation_data,
            )

            repository_data = event.data["repositories"]

            repositories = [
                Repository(
                    installation=installation,
                    repository_id=repository["id"],
                    repository_node_id=repository["node_id"],
                    full_name=repository["full_name"],
                )
                for repository in repository_data
            ]
            await Repository.objects.abulk_create(repositories)

            return installation

    def create_from_event(self, event: sansio.Event):
        return async_to_sync(self.acreate_from_event)(event)

    async def aget_from_event(self, event: sansio.Event):
        try:
            installation_id = event.data["installation"]["id"]
            return await self.aget(installation_id=installation_id)
        except (Installation.DoesNotExist, KeyError):
            return None

    def get_from_event(self, event: sansio.Event):
        return async_to_sync(self.aget_from_event)(event)


class InstallationStatus(models.IntegerChoices):
    ACTIVE = 1, "Active"
    INACTIVE = 2, "Inactive"

    @classmethod
    def from_event(cls, event: sansio.Event) -> InstallationStatus:
        action = event.data["action"]
        match action:
            case "deleted" | "suspend":
                return cls.INACTIVE
            case "created" | "new_permissions_accepted" | "unsuspend":
                return cls.ACTIVE
            case _:
                raise ValueError(f"Unknown installation action: {action}")


class Installation(models.Model):
    id: int
    installation_id = models.PositiveBigIntegerField(unique=True)
    data = models.JSONField(default=dict)
    status = models.SmallIntegerField(
        choices=InstallationStatus.choices, default=InstallationStatus.ACTIVE
    )

    objects = InstallationManager()

    @override
    def __str__(self) -> str:
        return str(self.installation_id)

    async def aget_access_token(self, gh: abc.GitHubAPI):  # pragma: no cover
        data = await get_installation_access_token(
            gh,
            installation_id=str(self.installation_id),
            app_id=app_settings.APP_ID,
            private_key=app_settings.PRIVATE_KEY,
        )
        return data.get("token")

    def get_access_token(self, gh: abc.GitHubAPI):  # pragma: no cover
        return async_to_sync(self.aget_access_token)(gh)


class RepositoryManager(models.Manager["Repository"]):
    async def aget_from_event(self, event: sansio.Event):
        try:
            repository_id = event.data["repository"]["id"]
            return await self.aget(repository_id=repository_id)
        except Repository.DoesNotExist:
            return None

    def get_from_event(self, event: sansio.Event):
        return async_to_sync(self.aget_from_event)(event)


class Repository(models.Model):
    id: int
    installation = models.ForeignKey(
        "django_github_app.Installation",
        on_delete=models.CASCADE,
        related_name="repositories",
    )
    repository_id = models.PositiveBigIntegerField(unique=True)
    repository_node_id = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)

    objects = RepositoryManager()

    class Meta:
        verbose_name_plural = "repositories"

    @override
    def __str__(self) -> str:
        return self.full_name

    def get_gh_client(self):
        return AsyncGitHubAPI(  # pragma: no cover
            self.full_name, installation_id=self.installation.installation_id
        )

    async def aget_issues(self, params: dict[str, Any] | None = None):
        url = GitHubAPIUrl(
            GitHubAPIEndpoint.REPO_ISSUES,
            {"owner": self.owner, "repo": self.repo},
            params,
        )
        async with self.get_gh_client() as gh:
            issues = [issue async for issue in gh.getiter(url.full_url)]
        return issues

    def get_issues(self, params: dict[str, Any] | None = None):
        return async_to_sync(self.aget_issues)(params)

    @property
    def owner(self):
        return self.full_name.split("/")[0]

    @property
    def repo(self):
        return self.full_name.split("/")[1]
