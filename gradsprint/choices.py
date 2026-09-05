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

VERBAL_SUBTOPIC_CHOICES = [
        # Reading Comprehension
        ("rc-main-idea","RC — Main Idea"),
        ("rc-primary-purpose","RC — Primary Purpose"),
        ("rc-supporting-detail","RC — Supporting Detail"),
        ("rc-inference","RC — Inference"),
        ("rc-passage-structure","RC — Passage Structure"),
        ("rc-sentence-function","RC — Sentence Function"),
        ("rc-authors-view","RC — Author's View"),
        ("rc-tone-attitude","RC — Tone and Attitude"),
        ("rc-meaning-in-context","RC — Meaning in Context"),
        ("rc-compare-viewpoints","RC — Comparing Viewpoints"),
        ("rc-strengthen-argument","RC — Strengthen the Argument"),
        ("rc-weaken-argument","RC — Weaken the Argument"),
        ("rc-assumption","RC — Assumption"),
        ("rc-evaluate-argument","RC — Evaluate the Argument"),
        ("rc-resolve-paradox","RC — Resolve the Paradox"),
        ("rc-argument-conclusion","RC — Argument and Conclusion"),
        ("rc-evidence-reasoning","RC — Evidence and Reasoning"),
        ("rc-general","RC — General"),

        # Text Completion
        ("tc-single-blank","TC — Single Blank"),
        ("tc-double-blank","TC — Double Blank"),
        ("tc-triple-blank","TC — Triple Blank"),
        ("tc-context-clues","TC — Context Clues"),
        ("tc-contrast","TC — Contrast"),
        ("tc-continuation","TC — Continuation"),
        ("tc-cause-effect","TC — Cause and Effect"),
        ("tc-definition-restatement","TC — Definition and Restatement"),
        ("tc-sentence-logic","TC — Sentence Logic"),
        ("tc-tone","TC — Tone"),
        ("tc-vocabulary-in-context","TC — Vocabulary in Context"),
        ("tc-general","TC — General"),

        # Sentence Equivalence
        ("se-sentence-meaning","SE — Sentence Meaning"),
        ("se-sentence-logic","SE — Sentence Logic"),
        ("se-context-clues","SE — Context Clues"),
        ("se-synonym-pairs","SE — Synonym Pairs"),
        ("se-contrast","SE — Contrast"),
        ("se-continuation","SE — Continuation"),
        ("se-cause-effect","SE — Cause and Effect"),
        ("se-tone","SE — Tone"),
        ("se-word-connotation","SE — Word Connotation"),
        ("se-vocabulary-in-context","SE — Vocabulary in Context"),
        ("se-general","SE — General"),
    ]

QUANT_SUBTOPIC_CHOICES = [
        # Arithmetic
        ("arithmetic-number-properties","Arithmetic — Integers and Number Properties"),
        ("arithmetic-factors-multiples","Arithmetic — Factors, Multiples and Primes"),
        ("arithmetic-remainders","Arithmetic — Remainders"),
        ("arithmetic-fractions-decimals","Arithmetic — Fractions and Decimals"),
        ("arithmetic-exponents-roots","Arithmetic — Exponents and Roots"),
        ("arithmetic-ratios-proportions","Arithmetic — Ratios and Proportions"),
        ("arithmetic-percentages","Arithmetic — Percentages"),
        ("arithmetic-rates-work","Arithmetic — Rates and Work"),
        ("arithmetic-averages","Arithmetic — Averages"),
        ("arithmetic-sequences-patterns","Arithmetic — Sequences and Patterns"),
        ("arithmetic-estimation-units","Arithmetic — Estimation and Unit Conversion"),

        # Algebra
        ("algebra-expressions-factoring","Algebra — Expressions and Factoring"),
        ("algebra-linear-equations","Algebra — Linear Equations"),
        ("algebra-quadratic-equations","Algebra — Quadratic Equations"),
        ("algebra-inequalities","Algebra — Inequalities"),
        ("algebra-absolute-value","Algebra — Absolute Value"),
        ("algebra-systems-equations","Algebra — Systems of Equations"),
        ("algebra-functions","Algebra — Functions"),
        ("algebra-coordinate-geometry","Algebra — Coordinate Geometry"),
        ("algebra-word-problems","Algebra — Word Problems"),
        ("algebra-variation","Algebra — Direct and Inverse Variation"),

        # Geometry
        ("geometry-lines-angles","Geometry — Lines and Angles"),
        ("geometry-triangles","Geometry — Triangles"),
        ("geometry-special-triangles","Geometry — Special Right Triangles"),
        ("geometry-quadrilaterals","Geometry — Quadrilaterals"),
        ("geometry-polygons","Geometry — Polygons"),
        ("geometry-circles","Geometry — Circles"),
        ("geometry-area-perimeter","Geometry — Area and Perimeter"),
        ("geometry-similarity-congruence","Geometry — Similarity and Congruence"),
        ("geometry-three-dimensional","Geometry — Three-Dimensional Figures"),
        ("geometry-coordinate-figures","Geometry — Figures on the Coordinate Plane"),

        # Data Analysis
        ("data-tables-graphs","Data Analysis — Tables and Graphs"),
        ("data-mean-median-mode","Data Analysis — Mean, Median and Mode"),
        ("data-range-standard-deviation","Data Analysis — Range and Standard Deviation"),
        ("data-quartiles-percentiles","Data Analysis — Quartiles and Percentiles"),
        ("data-frequency-distributions","Data Analysis — Frequency Distributions"),
        ("data-sets-venn-diagrams","Data Analysis — Sets and Venn Diagrams"),
        ("data-counting-methods","Data Analysis — Counting Methods"),
        ("data-probability","Data Analysis — Probability"),
        ("data-conditional-probability","Data Analysis — Conditional Probability"),
        ("data-random-variables","Data Analysis — Random Variables and Distributions"),
        ("data-interpretation","Data Analysis — Data Interpretation"),

        # Mixed
        ("mixed-multiple-topics","Mixed — Multiple Quantitative Topics"),
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