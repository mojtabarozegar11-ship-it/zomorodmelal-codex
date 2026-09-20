from django.core.management.base import BaseCommand

from apps.ai.seo_blog_agent import SeoBlogOperationsAgent


class Command(BaseCommand):
    help = "Run the scheduled SEO blog operations agent."

    def add_arguments(self, parser):
        parser.add_argument(
            "--topic",
            default="معرفی ارزشمند شرکت و سایت",
            help="Content topic for the daily blog run.",
        )

    def handle(self, *args, **options):
        run = SeoBlogOperationsAgent().run(topic=options["topic"])
        self.stdout.write(
            self.style.SUCCESS(
                f"SEO blog run {run.run_date} {run.scheduled_time} status={run.status} "
                f"published={run.published_count} pending={run.pending_count} failed={run.failed_count}"
            )
        )
