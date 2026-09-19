//--------------------------
//       CHOICES
//--------------------------

function renderChoices(){

    clearChoiceContainers();

    const question=questions[currentQuestion];
    const type=question.type;

    if(type==="sentence-equivalence"){
        renderSentenceEquivalence();
    }
    else if(type==="text-completion"){
        renderTextCompletion();
    }
    else if(type==="reading-single"){
        renderReadingSingle();
    }
    else if(type==="reading-multiple"){
        renderReadingMultiple();
    }
    else{
        renderQuantChoices();
    }

    renderRegularQuestionImage();
}


//------------------------------
//     CLEAR OLD CONTENT
//------------------------------

function clearChoiceContainers(){

    const choices=document.querySelector("#choices");
    const passage=document.querySelector("#passage");
    const image=document.querySelector("#image");
    const questionImage=document.querySelector("#qs-image");
    const quantA=document.querySelector("#quantity-a");
    const quantB=document.querySelector("#quantity-b");
    const quantComparison=document.querySelector("#quantity-comparison");

    choices.innerHTML="";
    passage.innerHTML="";
    image.innerHTML="";
    questionImage.innerHTML="";
    quantA.innerHTML="";
    quantB.innerHTML="";

    quantComparison.style.display="none";
}


//----------------------------------
//     SENTENCE EQUIVALENCE
//----------------------------------

function renderSentenceEquivalence(){

    const container=document.querySelector("#choices");
    const question=questions[currentQuestion];

    if(!Array.isArray(answers[currentQuestion])){
        answers[currentQuestion]=[];
    }

    question.choices.forEach(choice=>{

        const checkbox=document.createElement("input");
        const label=document.createElement("label");
        const linebreak=document.createElement("br");

        checkbox.type="checkbox";
        checkbox.value=choice;

        checkbox.checked=answers[currentQuestion].includes(choice);

        label.append(checkbox);
        label.append(" "+choice);

        checkbox.addEventListener("change",()=>{

            if(checkbox.checked){

                if(
                    answers[currentQuestion].length>=2 &&
                    !answers[currentQuestion].includes(choice)
                ){
                    checkbox.checked=false;
                    return;
                }

                if(!answers[currentQuestion].includes(choice)){
                    answers[currentQuestion].push(choice);
                }
            }
            else{
                answers[currentQuestion]=answers[currentQuestion].filter(
                    savedChoice=>savedChoice!==choice
                );
            }
        });

        container.append(label);
        container.append(linebreak);
    });
}


//------------------------------
//       TEXT COMPLETION
//------------------------------

function renderTextCompletion(){

    const container=document.querySelector("#choices");
    const question=questions[currentQuestion];

    if(!Array.isArray(answers[currentQuestion])){
        answers[currentQuestion]=[];
    }

    question.blanks.forEach((blank,index)=>{

        const table=document.createElement("table");
        const headerRow=document.createElement("tr");
        const th=document.createElement("th");

        th.textContent=`Blank ${index+1}`;

        headerRow.append(th);
        table.append(headerRow);

        blank.choices.forEach(choice=>{

            const row=document.createElement("tr");
            const td=document.createElement("td");
            const label=document.createElement("label");
            const radio=document.createElement("input");

            radio.type="radio";
            radio.name=`blank-${currentQuestion}-${index}`;
            radio.value=choice;

            if(answers[currentQuestion][index]===choice){
                radio.checked=true;
            }

            label.append(radio);
            label.append(" "+choice);

            td.append(label);
            row.append(td);
            table.append(row);

            row.addEventListener("click",()=>{
                radio.checked=true;
                answers[currentQuestion][index]=choice;
            });
        });

        table.classList.add("tc-table");
        container.append(table);
    });
}


//------------------------------
//       READING PASSAGE
//------------------------------

function renderPassage(){

    const container=document.querySelector("#passage");
    const question=questions[currentQuestion];

    if(question.passage){
        container.innerHTML=question.passage;
        return;
    }

    if(
        question.passageRef!==null &&
        question.passageRef!==undefined
    ){
        const passageQuestion=questions.find(
            item=>Number(item.id)===Number(question.passageRef)
        );

        if(passageQuestion && passageQuestion.passage){
            container.innerHTML=passageQuestion.passage;
        }
    }
}


//------------------------------
//       READING SINGLE
//------------------------------

function renderReadingSingle(){

    const container=document.querySelector("#choices");
    const question=questions[currentQuestion];

    renderPassage();

    question.choices.forEach(choice=>{

        const label=document.createElement("label");
        const radio=document.createElement("input");
        const linebreak=document.createElement("br");

        radio.type="radio";
        radio.name=`reading-${currentQuestion}`;
        radio.value=choice;

        if(answers[currentQuestion]===choice){
            radio.checked=true;
        }

        label.append(radio);
        label.append(" "+choice);

        radio.addEventListener("change",()=>{
            if(radio.checked){
                answers[currentQuestion]=choice;
            }
        });

        container.append(label);
        container.append(linebreak);
    });
}


//------------------------------
//      READING MULTIPLE
//------------------------------

function renderReadingMultiple(){

    const container=document.querySelector("#choices");
    const question=questions[currentQuestion];

    renderPassage();

    if(!Array.isArray(answers[currentQuestion])){
        answers[currentQuestion]=[];
    }

    question.choices.forEach(choice=>{

        const checkbox=document.createElement("input");
        const label=document.createElement("label");
        const linebreak=document.createElement("br");

        checkbox.type="checkbox";
        checkbox.value=choice;

        checkbox.checked=answers[currentQuestion].includes(choice);

        label.append(checkbox);
        label.append(" "+choice);

        checkbox.addEventListener("change",()=>{

            if(checkbox.checked){

                if(!answers[currentQuestion].includes(choice)){
                    answers[currentQuestion].push(choice);
                }
            }
            else{
                answers[currentQuestion]=answers[currentQuestion].filter(
                    savedChoice=>savedChoice!==choice
                );
            }
        });

        container.append(label);
        container.append(linebreak);
    });
}


//--------------------------------------
//        QUANTITATIVE QUESTIONS
//--------------------------------------

function renderQuantChoices(){

    const container=document.querySelector("#choices");
    const question=questions[currentQuestion];

    //------------------------------
    //       QUANT SINGLE
    //------------------------------

    if(question.type==="quant-single"){

        renderSingleChoice(question,container,"quant");
    }

    //------------------------------
    // DATA INTERPRETATION SINGLE
    //------------------------------

    else if(question.type==="data-interpretation-single"){

        renderDataInterpretationImage();
        renderSingleChoice(question,container,"di");
    }

    //------------------------------
    //       QUANT MULTIPLE
    //------------------------------

    else if(question.type==="quant-multiple"){

        if(!Array.isArray(answers[currentQuestion])){
            answers[currentQuestion]=[];
        }

        question.choices.forEach(choice=>{

            const checkbox=document.createElement("input");
            const label=document.createElement("label");
            const linebreak=document.createElement("br");

            checkbox.type="checkbox";
            checkbox.value=choice;

            checkbox.checked=answers[currentQuestion].includes(choice);

            label.append(checkbox);
            label.append(" "+choice);

            checkbox.addEventListener("change",()=>{

                if(checkbox.checked){

                    if(!answers[currentQuestion].includes(choice)){
                        answers[currentQuestion].push(choice);
                    }
                }
                else{
                    answers[currentQuestion]=answers[currentQuestion].filter(
                        savedChoice=>savedChoice!==choice
                    );
                }
            });

            container.append(label);
            container.append(linebreak);
        });
    }

    //------------------------------
    //       NUMERIC ENTRY
    //------------------------------

    else if(question.type==="numeric-entry"){

        const input=document.createElement("input");

        input.type="text";
        input.className="numeric-input";
        input.placeholder="Enter Answer";
        input.style.width="110px";
        input.style.height="30px";

        input.value=answers[currentQuestion] ?? "";

        input.addEventListener("input",()=>{
            answers[currentQuestion]=input.value;
        });

        container.append(input);
    }

    //------------------------------
    // QUANTITATIVE COMPARISON
    //------------------------------

    else if(question.type==="quantitative-comparison"){

        const quantComparison=document.querySelector("#quantity-comparison");
        const quantA=document.querySelector("#quantity-a");
        const quantB=document.querySelector("#quantity-b");

        quantComparison.style.display="flex";

        quantA.innerHTML=question.quantityA ?? "";
        quantB.innerHTML=question.quantityB ?? "";

        renderSingleChoice(
            question,
            container,
            "comparison"
        );
    }
}


//------------------------------
//   SINGLE CHOICE HELPER
//------------------------------

function renderSingleChoice(
    question,
    container,
    name
){

    question.choices.forEach(choice=>{

        const label=document.createElement("label");
        const radio=document.createElement("input");
        const linebreak=document.createElement("br");

        radio.type="radio";
        radio.name=`${name}-${currentQuestion}`;
        radio.value=choice;

        if(answers[currentQuestion]===choice){
            radio.checked=true;
        }

        label.append(radio);
        label.append(" "+choice);

        radio.addEventListener("change",()=>{

            if(radio.checked){
                answers[currentQuestion]=choice;
            }
        });

        container.append(label);
        container.append(linebreak);
    });
}


//----------------------------------
// DATA INTERPRETATION IMAGE
//----------------------------------

function renderDataInterpretationImage(){

    const container=document.querySelector("#image");
    const question=questions[currentQuestion];

    let imageSource=question.image;

    if(
        !imageSource &&
        question.passageRef!==null &&
        question.passageRef!==undefined
    ){
        const referenceQuestion=questions.find(
            item=>Number(item.id)===Number(question.passageRef)
        );

        if(referenceQuestion){
            imageSource=referenceQuestion.image;
        }
    }

    if(!imageSource){
        return;
    }

    const img=document.createElement("img");

    img.src=imageSource;
    img.alt="Data interpretation graph";

    container.append(img);
}


//----------------------------------
//   REGULAR QUESTION IMAGE
//----------------------------------

function renderRegularQuestionImage(){

    const question=questions[currentQuestion];
    const container=document.querySelector("#qs-image");

    if(
        question.type==="data-interpretation-single" ||
        !question.image
    ){
        return;
    }

    const img=document.createElement("img");

    img.src=question.image;
    img.alt="Question image";

    container.append(img);
}