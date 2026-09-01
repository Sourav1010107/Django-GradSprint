import json

from django.core.management.base import BaseCommand

from gradsprint.models import (
    Test,
    Section,
    Question,
    Choice,
    Blank,
    BlankChoice,
)


class Command(BaseCommand):

    help = "Import GRE test questions from JSON into PostgreSQL"


    def add_arguments(self, parser):

        parser.add_argument(
            "json_file",
            type=str,
            help="Path to GRE JSON file"
        )

        parser.add_argument(
            "--test-name",
            type=str,
            default="GRE Practice Test 1",
            help="Name of the GRE test"
        )


    def handle(self, *args, **options):

        json_file = options["json_file"]
        test_name = options["test_name"]


        # -------------------------
        # LOAD JSON FILE
        # -------------------------

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)


        section_data = data["section"]

        questions_data = section_data["questions"]


        # -------------------------
        # CREATE / GET TEST
        # -------------------------

        test, created = Test.objects.get_or_create(
            name=test_name
        )

        if created:

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created test: {test.name}"
                )
            )

        else:

            self.stdout.write(
                f"Using existing test: {test.name}"
            )

        # -------------------------
        # CREATE / GET SECTION
        # -------------------------

        section, created = Section.objects.get_or_create(

            test=test,

            name=section_data["name"],

            defaults={
                "time": section_data["time"],
                "order": section_data["order"],
            }

        )


        if created:

            self.stdout.write(
                self.style.SUCCESS(
                    f"Created section: {section.name}"
                )
            )

        else:

            self.stdout.write(
                f"Using existing section: {section.name}"
            )


        # ------------------------------------------------
        # DELETE OLD QUESTIONS IN THIS SECTION
        # ------------------------------------------------
        #
        # This makes re-import easier during development.
        #

        section.questions.all().delete()


        # ------------------------------------------------
        # STORE JSON QUESTION ID -> DJANGO QUESTION OBJECT
        # ------------------------------------------------

        question_map = {}


        # ------------------------------------------------
        # FIRST PASS
        #
        # Create questions and choices.
        #
        # passageRef is handled later because the referenced
        # question might not exist yet.
        # ------------------------------------------------

        for question_index, item in enumerate(
            questions_data,
            start=1
        ):

            question = Question.objects.create(

                section=section,

                question_type = item["type"],

                difficulty=item["difficulty"],

                question=item["question"],

                instruction=item["instruction"],

                passage=item.get("passage"),

                quantityA = item.get("quantityA"),

                quantityB = item.get("quantityB"),

                max_selections=item.get(
                    "maxSelections",
                    1
                ),

                order=question_index

            )


            # Save mapping:
            #
            # JSON id 11 -> Django Question object
            #

            source_id = item["id"]

            question_map[source_id] = question


            # ---------------------------------
            # NORMAL CHOICE QUESTIONS
            # ---------------------------------

            if "choices" in item:

                correct_answers = item.get(
                    "answer",
                    []
                )


                for choice_index, choice_text in enumerate(
                    item["choices"]
                ):

                    Choice.objects.create(

                        question=question,

                        text=choice_text,

                        order=choice_index,

                        is_correct=(
                            choice_index
                            in correct_answers
                        )

                    )


            # ---------------------------------
            # DOUBLE / TRIPLE TEXT COMPLETION
            # ---------------------------------

            if "blanks" in item:

                for blank_index, blank_data in enumerate(
                    item["blanks"],
                    start=1
                ):

                    blank = Blank.objects.create(

                        question=question,

                        order=blank_index

                    )


                    correct_answer = blank_data.get(
                        "answer"
                    )


                    for choice_index, choice_text in enumerate(
                        blank_data["choices"]
                    ):

                        BlankChoice.objects.create(

                            blank=blank,

                            text=choice_text,

                            order=choice_index,

                            is_correct=(
                                choice_index
                                == correct_answer
                            )

                        )


            self.stdout.write(
                f"Imported Question {question_index}"
            )


        # ------------------------------------------------
        # SECOND PASS
        #
        # Handle passageRef relationships.
        # ------------------------------------------------

        for item in questions_data:

            current_question = question_map[item["id"]]


            # Question contains its own passage
            if item.get("passage"):

                current_question.passage_ref = current_question

                current_question.save(
                    update_fields=["passage_ref"]
                )


            # Question uses another question's passage
            elif item.get("passageRef") is not None:

                source_question = question_map.get(
                    item["passageRef"]
                )

                if source_question:

                    current_question.passage_ref = source_question

                    current_question.save(
                        update_fields=["passage_ref"]
                    )

        # -------------------------
        # FINISHED
        # -------------------------

        self.stdout.write(
            self.style.SUCCESS(
                "GRE section imported successfully."
            )
        )