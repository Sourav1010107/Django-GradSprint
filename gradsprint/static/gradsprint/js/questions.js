
//--------------------------
//       CHOICES  
//--------------------------

function variableInitialisation(){
    //initializing the env
    const container = document.querySelector('#choices');
    const containerPassage = document.querySelector('#passage');
    const containerImage = document.querySelector('#image');
    const containerQsImage = document.querySelector('#qs-image');


    container.innerHTML= "";
    containerPassage.innerHTML = "";
    containerImage.innerHTML = "";
    containerQsImage.innerHTML= "";
}


function renderChoices(){


    if (questions[currentQuestion].type === "sentence-equivalence") {
        renderSentenceEquivalence();
    }
    else if(questions[currentQuestion].type === "text-completion"){
        renderTextCompletion();
    }
    else if(questions[currentQuestion].type === "reading-single"){
        renderReadingPassage();
    }
    else{
        renderQuantChoices();
    }
}



//----------------------------------
//       SENTENCE EQUIVALENCE  
//----------------------------------


function renderSentenceEquivalence(){
    //initializing the env
    const container = document.querySelector('#choices');
    const containerPassage = document.querySelector('#passage');
    const containerImage = document.querySelector('#image');
    const containerQsImage = document.querySelector('#qs-image');


    container.innerHTML= "";
    containerPassage.innerHTML = "";
    containerImage.innerHTML = "";
    containerQsImage.innerHTML= "";


    questions[currentQuestion].choices.forEach((choice)=>{
        const checkbox = document.createElement('input');
        const label = document.createElement('label');
        const linebreak = document.createElement('br');

        checkbox.type= "checkbox";
        checkbox.value= choice;

        // creating the checkbox element prop.

        label.append(checkbox);
        label.append(' '+ choice);

        // loading the saved answers in the question paper

        checkbox.checked = answers[currentQuestion].includes(choice);

        // save the choice in the answer array

        checkbox.addEventListener("change", ()=>{

            if(answers[currentQuestion].length >= 2){
                checkbox.checked = false;
            }
            if (checkbox.checked) {
                if (!answers[currentQuestion].includes(choice)) {
                    answers[currentQuestion].push(choice);
                }
            }
            else{
                answers[currentQuestion] = answers[currentQuestion].filter(
                    savedChoice => savedChoice != choice
                );
            }
                
        });
    

        // add choices in the HTML element

        container.append(label);
        container.append(linebreak);

    });
}


//------------------------------
//       TEXT-COMPLETION
//------------------------------

function renderTextCompletion(){
    //initializing the env
    const container = document.querySelector('#choices');
    const containerPassage = document.querySelector('#passage');
    const containerImage = document.querySelector('#image');
    const containerQsImage = document.querySelector('#qs-image');


    container.innerHTML= "";
    containerPassage.innerHTML = "";
    containerImage.innerHTML = "";
    containerQsImage.innerHTML= "";


    questions[currentQuestion].blanks.forEach((blank, index)=>{

        const table = document.createElement('table');
        const  th =  document.createElement('th');
        const hrow = document.createElement('tr');

        th.textContent = `Blank ${index +1}`;
        hrow.append(th);
        table.append(hrow);

        blank.choices.forEach((choice)=>{
            const row = document.createElement('tr');
            const td = document.createElement('td');
            const label = document.createElement('label');
            const radio = document.createElement('input');

            radio.type = "radio";
            radio.name = `Blank ${index +1}`;
            radio.value = choice;

            label.append(radio);
            label.append(' '+ choice)

            td.append(label);
            row.append(td);
            table.append(row);

            // reload answer

            if (answers[currentQuestion][index]=== choice) {
                radio.checked = true;
            }

            // make entire row clickable and save answer

            row.addEventListener("click", ()=>{
                radio.checked = true;
                answers[currentQuestion][index] = choice; // save answer
            });           

        });

        table.classList.add("tc-table");
        container.append(table);
    });
}


//------------------------------
//    READING PASSAGE
//------------------------------

function renderReadingPassage(){
    //initializing the env
    const container = document.querySelector('#choices');
    const containerPassage = document.querySelector('#passage');
    const containerImage = document.querySelector('#image');
    const containerQsImage = document.querySelector('#qs-image');


    container.innerHTML= "";
    containerPassage.innerHTML = "";
    containerImage.innerHTML = "";
    containerQsImage.innerHTML= "";


    questions[currentQuestion].choices.forEach((choice)=>{

        const label = document.createElement('label');
        const radio = document.createElement('input');
        const linebreak = document.createElement('br');

        radio.type = "radio";
        radio.name = "passage";
        radio.value = choice;

        label.append(radio);
        label.append(' '+ choice);

        containerChoice.append(label);
        containerChoice.append(linebreak);

        // reload answer

        if (answers[currentQuestion] === choice) {
            radio.checked = true;
        }

        // save answer

        radio.addEventListener("click", ()=>{
            radio.checked = true;
            answers[currentQuestion] = choice; // save answer
        });
        
    });

    // loading reference passage

    //const loadingquestionNo = questions[currentQuestion].passageRef-1;

    const passageRef = questions[currentQuestion].passageRef;

    const passageQuestion = questions.find(
        question=> question.id === passageRef
    );

    if (passageQuestion) {
        containerPassage.innerHTML = passageQuestion.passage;
    }

}


//--------------------------------------
//        QUANTATIVE QUESTION
//--------------------------------------


function renderQuantChoices() {

    //initializing the env
    const container = document.querySelector('#choices');
    const containerPassage = document.querySelector('#passage');
    const containerImage = document.querySelector('#image');
    const containerQsImage = document.querySelector('#qs-image');


    container.innerHTML= "";
    containerPassage.innerHTML = "";
    containerImage.innerHTML = "";
    containerQsImage.innerHTML= "";

    // --------------------------------
    // SINGLE ANSWER
    // --------------------------------

    if (questions[currentQuestion].type === "quant-single") {

        questions[currentQuestion].choices.forEach((choice)=>{

            const label = document.createElement('label');
            const radio = document.createElement('input');
            const linebreak = document.createElement('br');

            radio.type = "radio";
            radio.name = "comparison";
            radio.value = choice;

            label.append(radio);
            label.append(' '+ choice);

            // reload answer

            if (answers[currentQuestion] === choice) {
                radio.checked = true;
            }

            container.append(label);
            container.append(linebreak);

            // save answer

            radio.addEventListener("click", ()=>{
                radio.checked = true;
                answers[currentQuestion] = choice; // save answer
            });
        
        });
    }


    
    else if (questions[currentQuestion].type === "data-interpretation-single") {

        questions[currentQuestion].choices.forEach((choice)=>{

            const label = document.createElement('label');
            const radio = document.createElement('input');
            const linebreak = document.createElement('br');

            radio.type = "radio";
            radio.name = "comparison";
            radio.value = choice;

            label.append(radio);
            label.append(' '+ choice);

            // reload answer

            if (answers[currentQuestion] === choice) {
                radio.checked = true;
            }

            container.append(label);
            container.append(linebreak);

            // save answer

            radio.addEventListener("click", ()=>{
                radio.checked = true;
                answers[currentQuestion] = choice; // save answer
            });
        
        });

        const passageRef = questions[currentQuestion].passageRef;

        const passageQuestion = questions.find(
            question=> question.id === passageRef
        );

        if (passageQuestion) {
            containerImage.innerHTML = passageQuestion.image;
        }
    }


    // --------------------------------
    // MULTIPLE ANSWERS
    // --------------------------------

    else if (questions[currentQuestion].type === "quant-multiple") {

        questions[currentQuestion].choices.forEach((choice)=>{
            const checkbox = document.createElement('input');
            const label = document.createElement('label');
            const linebreak = document.createElement('br');

            checkbox.type= "checkbox";
            checkbox.value= choice;

            //creating the checkbox element prop.
            label.append(checkbox);
            label.append(' '+ choice);

            //add choices in the HTML element
            container.append(label);
            container.append(linebreak);

            //loading the saved answers in the question paper
            checkbox.checked = answers[currentQuestion].includes(choice);

            //save the choice in the answer array
            checkbox.addEventListener("change", ()=>{

                if (checkbox.checked) {
                    if (!answers[currentQuestion].includes(choice)) {
                        answers[currentQuestion].push(choice);
                    }
                }
                else{
                    answers[currentQuestion] = answers[currentQuestion].filter(
                        savedChoice => savedChoice != choice
                    );
                }              
            });
    
            
        });
    }


    // --------------------------------
    // NUMERIC ENTRY
    // --------------------------------

    else if (questions[currentQuestion].type === "numeric-entry") {

        const input = document.createElement("input");

        input.type = "text";
        input.className = "numeric-input";
        input.placeholder = " Enter Answer";
        input.style.width = "110px";
        input.style.height = "30px";

        //load answer
        input.value = answers[currentQuestion];

        container.append(input);

        //save answer
        input.addEventListener("input", ()=>{
            answers[currentQuestion] = input.value;
        });
    }


    // --------------------------------
    // QUANTITATIVE COMPARISON
    // --------------------------------

    else if (questions[currentQuestion].type === "quantitative-comparison") {

        const quantA = document.querySelector('#quantity-a');
        const quantB = document.querySelector('#quantity-b');

        quantA.innerHTML = "";
        quantB.innerHTML = "";

        quantA.innerHTML = questions[currentQuestion].quantityA;
        quantB.innerHTML = questions[currentQuestion].quantityB;

        questions[currentQuestion].choices.forEach((choice)=>{

            const label = document.createElement('label');
            const radio = document.createElement('input');
            const linebreak = document.createElement('br');

            radio.type = "radio";
            radio.name = "comparison";
            radio.value = choice;

            label.append(radio);
            label.append(' '+ choice);

            // reload answer
            if (answers[currentQuestion] === choice) {
                radio.checked = true;
            }

            container.append(label);
            container.append(linebreak);

            // save answer
            radio.addEventListener("click", ()=>{
                radio.checked = true;
                answers[currentQuestion] = choice; // save answer
            });
        
        });
    }
}



    