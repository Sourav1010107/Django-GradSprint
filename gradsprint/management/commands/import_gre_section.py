import json

from django.core.management.base import BaseCommand,CommandError
from django.db import transaction

from ...models import (
    Test,
    Section,
    Question,
    Choice,
    Blank,
    BlankChoice,
    NumericValue,
)

from ...choices import (
    TYPE_CHOICES,
    TEST_TOPIC_CHOICES,
    TEST_SUBTOPIC_CHOICES,
    DIFFICULTIES,
)


class Command(BaseCommand):
    help="Import or replace one GRE section inside a test"

    def add_arguments(self,parser):
        parser.add_argument(
            "json_file",
            type=str,
            help="Path to GRE section JSON file",
        )

    def handle(self,*args,**options):
        json_file=options["json_file"]

        try:
            with open(json_file,"r",encoding="utf-8") as file:
                data=json.load(file)

        except FileNotFoundError:
            raise CommandError(
                f"File not found: {json_file}"
            )

        except json.JSONDecodeError as error:
            raise CommandError(
                f"Invalid JSON: {error}"
            )

        self.validate_file(data)

        with transaction.atomic():
            test,created=Test.objects.get_or_create(
                name=data["test_name"]
            )

            section_data=data["section"]

            existing_section=Section.objects.filter(
                test=test,
                name=section_data["name"]
            ).first()

            if existing_section:
                self.stdout.write(
                    self.style.WARNING(
                        f'Section "{existing_section.name}" '
                        f'already exists and will be replaced.'
                    )
                )

                existing_section.delete()

            conflicting_section=Section.objects.filter(
                test=test,
                order=section_data["order"]
            ).first()

            if conflicting_section:
                raise CommandError(
                    f'Section order {section_data["order"]} '
                    f'is already used by '
                    f'"{conflicting_section.name}".'
                )

            if test.sections.count()>=5:
                raise CommandError(
                    f'"{test.name}" already contains 5 sections.'
                )

            section=self.import_section(
                test,
                section_data
            )

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created test "{test.name}".'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Imported section "{section.name}" '
                f'with {section.questions.count()} questions.'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'"{test.name}" currently contains '
                f'{test.sections.count()}/5 sections.'
            )
        )

    # ==========================================
    # FILE VALIDATION
    # ==========================================

    def validate_file(self,data):
        if not isinstance(data,dict):
            raise CommandError(
                "Top-level JSON must be an object."
            )

        test_name=data.get("test_name")

        if not test_name:
            raise CommandError(
                '"test_name" is required.'
            )

        section=data.get("section")

        if not isinstance(section,dict):
            raise CommandError(
                '"section" must be an object.'
            )

        self.validate_section(section)

    # ==========================================
    # SECTION VALIDATION
    # ==========================================

    def validate_section(self,section):
        name=section.get("name")

        if not name:
            raise CommandError(
                "Section name is required."
            )

        time=section.get("time")

        if time is None:
            raise CommandError(
                f'Section "{name}" requires time.'
            )

        if not isinstance(time,int) or time<=0:
            raise CommandError(
                f'Section "{name}" time must be '
                f'a positive integer.'
            )

        order=section.get("order")

        if order is None:
            raise CommandError(
                f'Section "{name}" requires order.'
            )

        if not isinstance(order,int):
            raise CommandError(
                f'Section "{name}" order must '
                f'be an integer.'
            )

        if order<1 or order>5:
            raise CommandError(
                f'Section "{name}" order must '
                f'be between 1 and 5.'
            )

        questions=section.get("questions")

        if not isinstance(questions,list):
            raise CommandError(
                '"questions" must be a list.'
            )

        if not questions:
            raise CommandError(
                f'Section "{name}" contains no questions.'
            )

        question_orders=set()

        for question in questions:
            self.validate_question(
                question,
                question_orders
            )

        self.validate_passage_refs(
            questions,
            question_orders
        )

    # ==========================================
    # SECTION IMPORT
    # ==========================================

    def import_section(self,test,section_data):
        section=Section.objects.create(
            test=test,
            name=section_data["name"],
            time=section_data["time"],
            order=section_data["order"],
        )

        questions_by_order={}

        for question_data in section_data["questions"]:
            question=self.create_question(
                section,
                question_data
            )

            questions_by_order[
                question.order
            ]=question

        self.connect_passages(
            section_data["questions"],
            questions_by_order
        )

        return section

    # ==========================================
    # QUESTION CREATION
    # ==========================================

    def create_question(self,section,data):
        question=Question.objects.create(
            section=section,
            topic=data.get("topic"),
            subtopic=data.get("subtopic"),
            expected_time_seconds=data.get(
                "expected_time_seconds",
                90
            ),
            question_type=data["question_type"],
            difficulty=data["difficulty"],
            question=data["question"],
            quantity_a=data.get("quantity_a"),
            quantity_b=data.get("quantity_b"),
            instruction=data.get(
                "instruction",
                ""
            ),
            passage=data.get("passage"),
            explanation=data.get(
                "explanation",
                ""
            ),
            order=data["order"],
        )

        self.create_choices(
            question,
            data.get("choices",[])
        )

        self.create_blanks(
            question,
            data.get("blanks",[])
        )

        self.create_numeric_value(
            question,
            data
        )

        return question

    # ==========================================
    # NORMAL CHOICES
    # ==========================================

    def create_choices(self,question,choices):
        for choice_data in choices:
            Choice.objects.create(
                question=question,
                text=choice_data["text"],
                order=choice_data["order"],
                is_correct=choice_data["is_correct"],
            )

    # ==========================================
    # TEXT COMPLETION BLANKS
    # ==========================================

    def create_blanks(self,question,blanks):
        for blank_data in blanks:
            blank=Blank.objects.create(
                question=question,
                order=blank_data["order"],
            )

            for choice_data in blank_data.get(
                "choices",
                []
            ):
                BlankChoice.objects.create(
                    blank=blank,
                    text=choice_data["text"],
                    order=choice_data["order"],
                    is_correct=choice_data["is_correct"],
                )

    # ==========================================
    # NUMERIC ENTRY
    # ==========================================

    def create_numeric_value(self,question,data):
        if question.question_type!="numeric-entry":
            return

        NumericValue.objects.create(
            question=question,
            correct_value=data["numeric_value"],
        )

    # ==========================================
    # PASSAGE REFERENCES
    # ==========================================

    def connect_passages(
        self,
        questions_data,
        questions_by_order
    ):
        for data in questions_data:
            reference_order=data.get(
                "passage_ref_order"
            )

            if reference_order is None:
                continue

            question=questions_by_order[
                data["order"]
            ]

            reference_question=(
                questions_by_order[
                    reference_order
                ]
            )

            question.passage_ref=reference_question

            question.save(
                update_fields=["passage_ref"]
            )

    # ==========================================
    # QUESTION VALIDATION
    # ==========================================

    def validate_question(
        self,
        question,
        question_orders
    ):
        if not isinstance(question,dict):
            raise CommandError(
                "Every question must be an object."
            )

        order=question.get("order")

        if order is None:
            raise CommandError(
                "Every question requires order."
            )

        if not isinstance(order,int):
            raise CommandError(
                f"Question order {order} must be an integer."
            )

        if order<1:
            raise CommandError(
                f"Question order {order} is invalid."
            )

        if order in question_orders:
            raise CommandError(
                f"Duplicate question order: {order}"
            )

        question_orders.add(order)

        if not question.get("question"):
            raise CommandError(
                f"Question {order}: question text is required."
            )

        self.validate_model_choice(
            question,
            "question_type",
            TYPE_CHOICES
        )

        self.validate_model_choice(
            question,
            "topic",
            TEST_TOPIC_CHOICES
        )

        self.validate_model_choice(
            question,
            "subtopic",
            TEST_SUBTOPIC_CHOICES
        )

        self.validate_model_choice(
            question,
            "difficulty",
            DIFFICULTIES
        )

        expected_time=question.get(
            "expected_time_seconds",
            90
        )

        if (
            not isinstance(expected_time,int)
            or expected_time<=0
        ):
            raise CommandError(
                f"Question {order}: "
                f"expected_time_seconds must "
                f"be a positive integer."
            )

        question_type=question["question_type"]

        if question_type=="text-completion":
            self.validate_text_completion(
                question
            )

        elif question_type=="sentence-equivalence":
            self.validate_sentence_equivalence(
                question
            )

        elif question_type=="reading-single":
            self.validate_single_choice(
                question,
                expected_choices=5
            )

        elif question_type=="reading-multiple":
            self.validate_multiple_choice(
                question,
                expected_choices=3
            )

        elif question_type=="quant-single":
            self.validate_single_choice(
                question,
                expected_choices=5
            )

        elif question_type=="quant-multiple":
            self.validate_multiple_choice(
                question,
                expected_choices=3
            )

        elif question_type=="data-interpretation-single":
            self.validate_single_choice(
                question,
                expected_choices=5
            )

        elif question_type=="quantitative-comparison":
            self.validate_quantitative_comparison(
                question
            )

        elif question_type=="numeric-entry":
            self.validate_numeric_entry(
                question
            )

        self.validate_topic_type_match(
            question
        )

    # ==========================================
    # MODEL CHOICE VALIDATION
    # ==========================================

    def validate_model_choice(
        self,
        question,
        field,
        choices
    ):
        order=question.get("order")
        value=question.get(field)

        valid_values={
            item[0]
            for item in choices
        }

        if value not in valid_values:
            raise CommandError(
                f'Question {order}: invalid '
                f'{field} "{value}".'
            )

    # ==========================================
    # TOPIC / TYPE CONSISTENCY
    # ==========================================

    def validate_topic_type_match(
        self,
        question
    ):
        order=question["order"]
        question_type=question["question_type"]
        topic=question["topic"]

        verbal_types={
            "reading-single":"reading-comprehension",
            "reading-multiple":"reading-comprehension",
            "text-completion":"text-completion",
            "sentence-equivalence":"sentence-equivalence",
        }

        expected_topic=verbal_types.get(
            question_type
        )

        if (
            expected_topic
            and topic!=expected_topic
        ):
            raise CommandError(
                f'Question {order}: '
                f'question_type "{question_type}" '
                f'requires topic "{expected_topic}".'
            )

        quant_types={
            "quantitative-comparison",
            "quant-single",
            "quant-multiple",
            "numeric-entry",
            "data-interpretation-single",
        }

        quant_topics={
            "arithmetic",
            "algebra",
            "geometry",
            "data-analysis",
            "mixed",
        }

        if (
            question_type in quant_types
            and topic not in quant_topics
        ):
            raise CommandError(
                f"Question {order}: "
                f"quantitative question has "
                f'invalid topic "{topic}".'
            )

    # ==========================================
    # SINGLE CHOICE
    # ==========================================

    def validate_single_choice(
        self,
        question,
        expected_choices=None
    ):
        order=question["order"]
        choices=question.get("choices",[])

        if expected_choices is not None:
            if len(choices)!=expected_choices:
                raise CommandError(
                    f"Question {order}: requires exactly "
                    f"{expected_choices} choices."
                )

        if not choices:
            raise CommandError(
                f"Question {order}: choices are required."
            )

        if self.count_correct(choices)!=1:
            raise CommandError(
                f"Question {order}: exactly "
                f"1 answer must be correct."
            )

        if question.get("blanks"):
            raise CommandError(
                f"Question {order}: cannot contain blanks."
            )

        if question.get("numeric_value") is not None:
            raise CommandError(
                f"Question {order}: numeric_value is "
                f"only allowed for numeric-entry."
            )

        self.validate_choice_list(
            choices,
            order
        )

    # ==========================================
    # MULTIPLE CHOICE
    # ==========================================

    def validate_multiple_choice(
        self,
        question,
        expected_choices=None
    ):
        order=question["order"]
        choices=question.get("choices",[])

        if expected_choices is not None:
            if len(choices)!=expected_choices:
                raise CommandError(
                    f"Question {order}: requires exactly "
                    f"{expected_choices} choices."
                )

        if not choices:
            raise CommandError(
                f"Question {order}: choices are required."
            )

        if self.count_correct(choices)<1:
            raise CommandError(
                f"Question {order}: at least "
                f"one choice must be correct."
            )

        if question.get("blanks"):
            raise CommandError(
                f"Question {order}: cannot contain blanks."
            )

        if question.get("numeric_value") is not None:
            raise CommandError(
                f"Question {order}: numeric_value is "
                f"only allowed for numeric-entry."
            )

        self.validate_choice_list(
            choices,
            order
        )

    # ==========================================
    # SENTENCE EQUIVALENCE
    # ==========================================

    def validate_sentence_equivalence(
        self,
        question
    ):
        order=question["order"]
        choices=question.get("choices",[])

        if len(choices)!=6:
            raise CommandError(
                f"Question {order}: "
                f"sentence-equivalence requires "
                f"exactly 6 choices."
            )

        if self.count_correct(choices)!=2:
            raise CommandError(
                f"Question {order}: "
                f"sentence-equivalence requires "
                f"exactly 2 correct answers."
            )

        if question.get("blanks"):
            raise CommandError(
                f"Question {order}: "
                f"sentence-equivalence cannot "
                f"contain blanks."
            )

        if question.get("numeric_value") is not None:
            raise CommandError(
                f"Question {order}: numeric_value is "
                f"only allowed for numeric-entry."
            )

        self.validate_choice_list(
            choices,
            order
        )

    # ==========================================
    # TEXT COMPLETION
    # ==========================================

    def validate_text_completion(
        self,
        question
    ):
        order=question["order"]

        if question.get("choices"):
            raise CommandError(
                f"Question {order}: text-completion "
                f"must use blanks instead of "
                f"normal choices."
            )

        blanks=question.get("blanks",[])

        if len(blanks)<1 or len(blanks)>3:
            raise CommandError(
                f"Question {order}: text-completion "
                f"requires between 1 and 3 blanks."
            )

        if question.get("numeric_value") is not None:
            raise CommandError(
                f"Question {order}: numeric_value is "
                f"not allowed for text-completion."
            )

        blank_orders=set()

        for blank in blanks:
            blank_order=blank.get("order")

            if blank_order is None:
                raise CommandError(
                    f"Question {order}: blank order "
                    f"is required."
                )

            if blank_order in blank_orders:
                raise CommandError(
                    f"Question {order}: duplicate "
                    f"blank order {blank_order}."
                )

            blank_orders.add(blank_order)

            choices=blank.get(
                "choices",
                []
            )

            if len(blanks)==1:
                expected_choices=5
            else:
                expected_choices=3

            if len(choices)!=expected_choices:
                raise CommandError(
                    f"Question {order}, blank "
                    f"{blank_order}: requires exactly "
                    f"{expected_choices} choices."
                )

            if self.count_correct(choices)!=1:
                raise CommandError(
                    f"Question {order}, blank "
                    f"{blank_order}: exactly one "
                    f"choice must be correct."
                )

            self.validate_choice_list(
                choices,
                order
            )

    # ==========================================
    # QUANTITATIVE COMPARISON
    # ==========================================

    def validate_quantitative_comparison(
        self,
        question
    ):
        order=question["order"]

        if not question.get("quantity_a"):
            raise CommandError(
                f"Question {order}: quantity_a is required."
            )

        if not question.get("quantity_b"):
            raise CommandError(
                f"Question {order}: quantity_b is required."
            )

        choices=question.get("choices",[])

        if len(choices)!=4:
            raise CommandError(
                f"Question {order}: "
                f"quantitative-comparison requires "
                f"exactly 4 choices."
            )

        if self.count_correct(choices)!=1:
            raise CommandError(
                f"Question {order}: "
                f"quantitative-comparison requires "
                f"exactly 1 correct answer."
            )

        if question.get("blanks"):
            raise CommandError(
                f"Question {order}: quantitative-comparison "
                f"cannot contain blanks."
            )

        if question.get("numeric_value") is not None:
            raise CommandError(
                f"Question {order}: numeric_value is "
                f"only allowed for numeric-entry."
            )

        self.validate_choice_list(
            choices,
            order
        )

    # ==========================================
    # NUMERIC ENTRY
    # ==========================================

    def validate_numeric_entry(
        self,
        question
    ):
        order=question["order"]

        if question.get("numeric_value") is None:
            raise CommandError(
                f"Question {order}: numeric-entry "
                f"requires numeric_value."
            )

        if question.get("choices"):
            raise CommandError(
                f"Question {order}: numeric-entry "
                f"cannot contain choices."
            )

        if question.get("blanks"):
            raise CommandError(
                f"Question {order}: numeric-entry "
                f"cannot contain blanks."
            )

        if question.get("quantity_a") is not None:
            raise CommandError(
                f"Question {order}: numeric-entry "
                f"cannot contain quantity_a."
            )

        if question.get("quantity_b") is not None:
            raise CommandError(
                f"Question {order}: numeric-entry "
                f"cannot contain quantity_b."
            )

    # ==========================================
    # CHOICE VALIDATION
    # ==========================================

    def validate_choice_list(
        self,
        choices,
        question_order
    ):
        orders=set()

        for choice in choices:
            if not isinstance(choice,dict):
                raise CommandError(
                    f"Question {question_order}: "
                    f"every choice must be an object."
                )

            order=choice.get("order")

            if order is None:
                raise CommandError(
                    f"Question {question_order}: "
                    f"choice order is required."
                )

            if not isinstance(order,int):
                raise CommandError(
                    f"Question {question_order}: "
                    f"choice order must be an integer."
                )

            if order in orders:
                raise CommandError(
                    f"Question {question_order}: "
                    f"duplicate choice order {order}."
                )

            orders.add(order)

            if not choice.get("text"):
                raise CommandError(
                    f"Question {question_order}: "
                    f"choice text cannot be empty."
                )

            if "is_correct" not in choice:
                raise CommandError(
                    f"Question {question_order}, "
                    f"choice {order}: is_correct "
                    f"is required."
                )

            if not isinstance(
                choice["is_correct"],
                bool
            ):
                raise CommandError(
                    f"Question {question_order}, "
                    f"choice {order}: is_correct "
                    f"must be true or false."
                )

    # ==========================================
    # PASSAGE REFERENCE VALIDATION
    # ==========================================

    def validate_passage_refs(
        self,
        questions,
        valid_orders
    ):
        questions_by_order={
            question["order"]:question
            for question in questions
        }

        for question in questions:
            order=question["order"]
            ref=question.get(
                "passage_ref_order"
            )

            if ref is None:
                continue

            if question["question_type"] not in {
                "reading-single",
                "reading-multiple",
                "data-interpretation-single"
            }:
                raise CommandError(
                    f"Question {order}: passage_ref_order "
                    f"is only valid for reading questions."
                )

            if ref not in valid_orders:
                raise CommandError(
                    f"Question {order}: passage_ref_order "
                    f"{ref} does not exist in this section."
                )

            if ref==order:
                raise CommandError(
                    f"Question {order}: cannot "
                    f"reference itself."
                )

            reference_question=(
                questions_by_order[ref]
            )

            if question["question_type"] in {
                "reading-single",
                "reading-multiple",
            }:
                if not reference_question.get("passage"):
                    raise CommandError(
                        f"Question {order}: referenced "
                        f"question {ref} does not "
                        f"contain a passage."
                    )

            elif question["question_type"]=="data-interpretation-single":
                if not reference_question.get("image"):
                    raise CommandError(
                        f"Question {order}: referenced "
                        f"question {ref} does not "
                        f"contain an image."
                    )

    # ==========================================
    # HELPER
    # ==========================================

    def count_correct(self,choices):
        return sum(
            1
            for choice in choices
            if choice.get("is_correct") is True
        )