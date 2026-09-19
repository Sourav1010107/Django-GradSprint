TYPE_CHOICES = [
        ("quantitative-comparison", "Quantitative Comparison"),
        ("quant-single", "Quant Single"),
        ("quant-multiple", "Quant Multiple"),
        ("numeric-entry", "Numeric Entry"),
        ("data-interpretation-single", "Data Interpretation Single"),
        ("text-completion", "Text Completion"),
        ("sentence-equivalence", "Sentence Equivalence"),
        ("reading-single", "Reading Single"),
        ("reading-multiple", "Reading Multiple"),
    ]
QUANT_TOPIC_CHOICES =[ 
        ("arithmetic", "Arithmetic"),
        ("algebra", "Algebra"),
        ("geometry", "Geometry"),
        ("data-analysis", "Data Analysis"),
        ("mixed", "Mixed Topics"),
    ]

VERBAL_TOPIC_CHOICES = [
        ("reading-comprehension","Reading Comprehension"),
        ("text-completion","Text Completion"),
        ("sentence-equivalence","Sentence Equivalence"),
    ]

VERBAL_SUBTOPIC_CHOICES=[
    # Reading Comprehension
    ("rc-main-purpose","RC — Main Idea / Primary Purpose"),
    ("rc-detail","RC — Detail / Supporting Information"),
    ("rc-inference","RC — Inference"),
    ("rc-function-structure","RC — Function / Structure"),
    ("rc-author-attitude","RC — Author's View / Tone"),
    ("rc-meaning-context","RC — Meaning in Context"),
    ("rc-strengthen","RC — Strengthen Argument"),
    ("rc-weaken","RC — Weaken Argument"),
    ("rc-assumption","RC — Assumption"),
    ("rc-evaluate","RC — Evaluate Argument"),
    ("rc-resolve","RC — Resolve Paradox"),

    # Text Completion
    ("tc-logic","TC — Sentence Logic"),
    ("tc-vocabulary","TC — Vocabulary in Context"),

    # Sentence Equivalence
    ("se-logic","SE — Sentence Logic"),
    ("se-vocabulary","SE — Vocabulary / Equivalence"),
]

QUANT_SUBTOPIC_CHOICES=[
    # Arithmetic
    ("arithmetic-number-properties","Arithmetic — Number Properties"),
    ("arithmetic-fractions-decimals","Arithmetic — Fractions & Decimals"),
    ("arithmetic-exponents-roots","Arithmetic — Exponents & Roots"),
    ("arithmetic-ratios-percentages","Arithmetic — Ratios & Percentages"),
    ("arithmetic-rates-work","Arithmetic — Rates & Work"),
    ("arithmetic-averages","Arithmetic — Averages"),
    ("arithmetic-sequences","Arithmetic — Sequences"),

    # Algebra
    ("algebra-expressions","Algebra — Expressions"),
    ("algebra-equations","Algebra — Equations"),
    ("algebra-inequalities","Algebra — Inequalities"),
    ("algebra-functions","Algebra — Functions"),
    ("algebra-coordinate","Algebra — Coordinate Geometry"),
    ("algebra-word-problems","Algebra — Word Problems"),

    # Geometry
    ("geometry-lines-angles","Geometry — Lines & Angles"),
    ("geometry-triangles","Geometry — Triangles"),
    ("geometry-quadrilaterals-polygons","Geometry — Quadrilaterals & Polygons"),
    ("geometry-circles","Geometry — Circles"),
    ("geometry-area-perimeter","Geometry — Area & Perimeter"),
    ("geometry-three-dimensional","Geometry — 3D Geometry"),
    ("geometry-coordinate","Geometry — Coordinate Geometry"),

    # Data Analysis
    ("data-tables-graphs","Data Analysis — Tables & Graphs"),
    ("data-statistics","Data Analysis — Statistics"),
    ("data-sets","Data Analysis — Sets"),
    ("data-counting","Data Analysis — Counting"),
    ("data-probability","Data Analysis — Probability"),
    ("data-distributions","Data Analysis — Distributions"),

    # Mixed
    ("mixed-multiple-topics","Mixed — Multiple Topics"),
]

DIFFICULTIES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
        ("very-hard", "Very Hard"),
    ]

TEST_TOPIC_CHOICES = (
        QUANT_TOPIC_CHOICES
       +VERBAL_TOPIC_CHOICES
    )

TEST_SUBTOPIC_CHOICES = (
    QUANT_SUBTOPIC_CHOICES
   +VERBAL_SUBTOPIC_CHOICES
)

