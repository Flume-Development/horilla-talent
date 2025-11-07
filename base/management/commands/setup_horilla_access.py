from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

# App labels based on your settings.py
PERFORMANCE_APPS = ("pms",)           # Performance Management
RECRUITMENT_APPS = ("recruitment",)   # Recruitment
ASSET_APPS = ("asset",)               # Assets

EMP_GROUP = "Employees"
RECR_GROUP = "Recruiters"
ASSET_GROUP = "AssetManagers"


class Command(BaseCommand):
    help = (
        "Grant Performance module view access to all non-admin employees. "
        "Also grant Tebatso access to Recruitment and Enhle access to Assets."
    )

    def add_arguments(self, parser):
        parser.add_argument("--tebatso", required=True, help="Username for Tebatso")
        parser.add_argument("--enhle", required=True, help="Username for Enhle")
        parser.add_argument(
            "--dry-run", action="store_true",
            help="Show actions without making changes"
        )

    def handle(self, *args, **opts):
        User = get_user_model()

        # Get/create groups
        emp_group, _ = Group.objects.get_or_create(name=EMP_GROUP)
        rec_group, _ = Group.objects.get_or_create(name=RECR_GROUP)
        asset_group, _ = Group.objects.get_or_create(name=ASSET_GROUP)

        # Helper: all view_* permissions for given app labels
        def view_perms_for(app_labels):
            return Permission.objects.filter(
                content_type__app_label__in=app_labels,
                codename__startswith="view_",
            )

        perf_perms = view_perms_for(PERFORMANCE_APPS)
        recr_perms = view_perms_for(RECRUITMENT_APPS)
        asset_perms = view_perms_for(ASSET_APPS)

        # Assign perms to groups
        if opts["dry_run"]:
            self.stdout.write("--- DRY RUN ---")
            self.stdout.write(f"{EMP_GROUP}: would add {perf_perms.count()} view perms from {PERFORMANCE_APPS}")
            self.stdout.write(f"{RECR_GROUP}: would add {recr_perms.count()} view perms from {RECRUITMENT_APPS}")
            self.stdout.write(f"{ASSET_GROUP}: would add {asset_perms.count()} view perms from {ASSET_APPS}")
        else:
            emp_group.permissions.add(*perf_perms)
            rec_group.permissions.add(*recr_perms)
            asset_group.permissions.add(*asset_perms)

        # Add all non-admin, active users to Employees
        non_admin_users = User.objects.filter(is_active=True, is_superuser=False)
        if opts["dry_run"]:
            self.stdout.write(f"{non_admin_users.count()} users would be added to {EMP_GROUP}")
        else:
            for u in non_admin_users:
                u.groups.add(emp_group)

        # Tebatso → Recruiters
        try:
            tebatso = User.objects.get(username=opts["tebatso"])
        except User.DoesNotExist:
            raise CommandError(f"User not found: {opts['tebatso']}")
        if opts["dry_run"]:
            self.stdout.write(f"Tebatso ({tebatso}) would be added to {RECR_GROUP}")
        else:
            tebatso.groups.add(rec_group)

        # Enhle → AssetManagers
        try:
            enhle = User.objects.get(username=opts["enhle"])
        except User.DoesNotExist:
            raise CommandError(f"User not found: {opts['enhle']}")
        if opts["dry_run"]:
            self.stdout.write(f"Enhle ({enhle}) would be added to {ASSET_GROUP}")
        else:
            enhle.groups.add(asset_group)

        self.stdout.write(self.style.SUCCESS("✔ Access setup complete"))
        self.stdout.write(f"- {EMP_GROUP}: {emp_group.permissions.count()} perms total")
        self.stdout.write(f"- {RECR_GROUP}: {rec_group.permissions.count()} perms total")
        self.stdout.write(f"- {ASSET_GROUP}: {asset_group.permissions.count()} perms total")
