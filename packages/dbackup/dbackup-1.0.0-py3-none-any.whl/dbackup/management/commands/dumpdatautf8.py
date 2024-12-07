import os, json
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = "Dump data in UTF-8 format and save to a file"

    def add_arguments(self, parser):
        parser.add_argument(
            "-o", "--output", help="Specify output file (default: dump_utf8.json)", default="dump_utf8.json"
        )
        parser.add_argument(
            "-i", "--indent", type=int, help="Indent level for pretty-printed JSON output (default: 4)", default=4
        )
        parser.add_argument(
            "-a", "--app", help="Specify app_label or app_label.ModelName to restrict dump", default=None
        )
        parser.add_argument(
            "-e",
            "--exclude",
            action="append",
            default=[],
            help="An app_label or app_label.ModelName to exclude (use multiple --exclude to exclude multiple apps/models)",
        )

    def handle(self, *args, **options):
        output_file = options["output"]
        indent = options["indent"]
        app_label = options["app"]
        excludes = options["exclude"]

        try:
            # Temp file to capture dumpdata output
            temp_file = "tmp_utf_8_dump.json"

            dumpdata_args = {"format": "json", "indent": indent, "exclude": excludes}
            if app_label:
                dumpdata_args["args"] = [app_label]

            # Call Django's dumpdata command
            with open(temp_file, "w", encoding="utf-8") as temp:
                call_command("dumpdata", **dumpdata_args, stdout=temp)

            # Read from temp file and write to specified output in UTF-8
            with open(temp_file, "r", encoding="utf-8") as temp:
                data = temp.read()

            with open(output_file, "w", encoding="utf-8") as output:
                output.write(data)

            # Cleanup
            os.remove(temp_file)

            self.stdout.write(self.style.SUCCESS(f"Data successfully dumped to {output_file} in UTF-8 format."))

        except Exception as e:
            raise CommandError(f"Error while dumping data: {e}")
