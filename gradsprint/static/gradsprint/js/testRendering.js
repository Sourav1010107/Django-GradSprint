//------------------------------------
//    VARIABLE INITIALIZATION
//------------------------------------
let greTest = null;
let currentSection = 0;
let currentQuestion = 0;
let timerVisible = true;
let timerStatus = false;
let questions, answers;
let timeRemaining, timer;
let markStatus;
let questionStartTime=null;


//------------------------------------
//      GRE TEST STRUCTURE
//------------------------------------


async function loadTest(testId) {

    try {
        const response = await fetch(`/api/test/${testId}/`);
        if (!response.ok) {
            throw new Error("Could not load test");
        }

        greTest = await response.json();
        console.log("Test loaded:", greTest);
        renderTest();
    }

    catch (error) {
        
        console.error("Error loading test:", error);

    }
}
//--------------------------
//    NEXT QUESTION  
//--------------------------

async function nextQuestion(){
    await saveCurrentAnswer();
    currentQuestion++;
    currentQuestion = Math.min(questions.length-1, currentQuestion);
    renderQuestion();
}

//--------------------------
//    PREVIOUS QUESTION  
//--------------------------

async function previousQuestion(){
    await saveCurrentAnswer();
    currentQuestion--;
    currentQuestion = Math.max(0, currentQuestion);
    renderQuestion();
}



//-------------------------
//     TIME UPDATE
//-------------------------


function timerDisplay(){
    const minutes = Math.floor(timeRemaining/60);
    const seconds = timeRemaining % 60;

    document.querySelector("#timer").textContent = 
    `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

}


async function timerUpdate() {

    if (timeRemaining > 0) {
        timeRemaining--;
        timerDisplay();
    }
    //end section condition
    if(timeRemaining <= 0){
        clearInterval(timer);
        timer = null;

        await saveCurrentAnswer();
        currentSection++;

        if (currentSection >= greTest.sections.length) {
            finishTest();
            return;
        }

        renderTest();
        return;
    }
}


//------------------------------
//      TIME TOGGLE
//------------------------------

function toggleTime() {
    timerStatus = !timerStatus;
    const timer = document.querySelector("#timer");
    if(timerStatus){
        timer.classList.add("time-hide");
        document.querySelector('#hide').innerHTML ="Show";
    }
    else{
        timer.classList.remove("time-hide");
        document.querySelector('#hide').innerHTML ="Hide";
    }
}


//------------------------------
//      REVIEW WINDOW
//------------------------------


function reviewTable() {

    //calculator
    const calculator = document.querySelector("#calculator");
    calculator.classList.add("hidden");
    //calculator close
    const tableBody = document.querySelector('#review-table-body');
    const modal = document.querySelector('#modal');
    const mainPrompt = document.querySelector('#main-prompt');

    const navBar = document.querySelector('#nav');
    const reviewNav = document.querySelector('#review-nav');

    const questionNum = document.querySelector('#question-number');
    questionNum.classList.add("hidden");


    tableBody.innerHTML = "";
    modal.classList.remove("hidden");
    mainPrompt.classList.add("hidden");

    navBar.classList.add("hidden");
    reviewNav.classList.remove("hidden");

    questions.forEach((question, index)=>{

        // CREATE ROW
        const row = document.createElement("tr");

        // CREATE CELLS
        const questionCell = document.createElement("td");
        const statusCell = document.createElement("td");
        const markCell = document.createElement("td");

        // PUT DATA INSIDE THE CELLS
        questionCell.textContent = index + 1;

        // ANSWER CELL LOGIC
        if(question.type === "sentence-equivalence"){
            if (answers[index].length >= 2) {
                statusCell.textContent = "Answered";
            }
            else{
                statusCell.textContent = "Not Answered";
            }
        }
        else{
            if(answers[index].length > 0){
                statusCell.textContent = "Answered";
            }
            else{
                statusCell.textContent = "Not Answered";
            }
        }

        // MARK CELL LOGIC
        if(markStatus[index]){
            markCell.textContent = "✓";
        }
        else{
            markCell.textContent = "";
        }

        // PUT CELLS INSIDE THE ROW
        row.append(questionCell);
        row.append(statusCell);
        row.append(markCell);

        // Make entire row clickable
        row.addEventListener("click",async ()=>{
            await saveCurrentAnswer();

            currentQuestion = index;
            renderQuestion();

            modal.classList.add("hidden");
            mainPrompt.classList.remove("hidden");

            navBar.classList.remove("hidden");
            reviewNav.classList.add("hidden");

            const questionNum = document.querySelector('#question-number');
            questionNum.classList.remove("hidden");
        });

        // PUT ROW INSIDE THE TABLE
        tableBody.append(row);
    });
}


//----------------------------------
//        CLOSE REVIEW WINDOW
//----------------------------------

function closeReview(){
    const mainPrompt = document.querySelector('#main-prompt');
    const modal = document.querySelector('#modal');
    const navBar = document.querySelector('#nav');
    const reviewNav = document.querySelector('#review-nav');

    modal.classList.add("hidden");
    mainPrompt.classList.remove("hidden");

    navBar.classList.remove("hidden");
    reviewNav.classList.add("hidden");

    const questionNum = document.querySelector('#question-number');
    questionNum.classList.remove("hidden");
}


//-----------------------------
//      MARK QUESTION
//-----------------------------


function markQuestion(){
    markStatus[currentQuestion] = !markStatus[currentQuestion];
        
    markQuestionStatus();
}



function markQuestionStatus() {

    const mark = document.querySelector('#mark');

    if(markStatus[currentQuestion]){
        mark.innerHTML = "Marked";
        mark.classList.add("mark-active");
        }
        else{
        mark.innerHTML = "Mark";
        mark.classList.remove("mark-active");
        }
}


//-----------------------------
//       RENDER TEST 
//-----------------------------


function renderTest() {

    const sectionHeader = document.querySelector('#section-header');
    const sectionPrompt = document.querySelector('#section-prompt');

    sectionHeader.classList.add("hidden");
    sectionPrompt.classList.add("hidden");

    const startSection = document.querySelector('#start-section');
    startSection.classList.remove("hidden");

    if (currentSection != 0) {
        document.querySelector('#start-section').innerHTML = "Next Section";
    }
    
    document.querySelector('#start-section').onclick = renderSection;

}

//------------------------------------
//         RENDER SECTION
//------------------------------------


function renderSection() {

    if(!greTest){
        console.error("Test data has not loaded yet");
        return;
    }

    // Activate section-header and section-prompt
    const sectionHeader = document.querySelector('#section-header');
    const sectionPrompt = document.querySelector('#section-prompt');


    //-------CALCULATOR BUTTON AVAILABILITY--------
    const nameSection = greTest.sections[currentSection].name;

    if ((nameSection === "Quantitative Reasoning 1")||(nameSection === "Quantitative Reasoning 2") || (nameSection === "Quantitative Reasoning 3")) {
        document.querySelector('#calculator-button').classList.remove("hidden");
    }else{
        document.querySelector('#calculator-button').classList.add("hidden");
    }
    //---------

    sectionHeader.classList.remove("hidden");
    sectionPrompt.classList.remove("hidden");

    const startSection = document.querySelector('#start-section');
    startSection.classList.add("hidden");

    
    
    currentQuestion = 0;
    timeRemaining = greTest.sections[currentSection].time;
    questions = greTest.sections[currentSection].set_name;
    answers = questions.map(()=>[]);
    markStatus = questions.map(()=>false);
    


    //--------START TIMER-------

    if (timer) {
        clearInterval(timer);
    }
    timer = setInterval(timerUpdate, 1000);

    renderQuestion();

}


//------------------------------------
//        QUESTION ENVIRONMENT
//------------------------------------


function questionEnv() {

    const passageContainer = document.querySelector(".passage-container");
    const imageContainer = document.querySelector(".image-container");
    const questionContainer = document.querySelector(".question-container");
    const quantComparison = document.querySelector(".quantity-comparison");

    
        

    if ((questions[currentQuestion].type !== "reading-single") && (questions[currentQuestion].type !== "reading-multiple")) {

        // Hide passage
        passageContainer.style.display = "none";

        // Make question area 80%
        questionContainer.style.flex = "none";
        questionContainer.style.width = "100%";
        questionContainer.style.padding = "0 5%";


        const envChoice = document.querySelector('#choices');
        envChoice.style.margin = "0 3%";

        if (questions[currentQuestion].type !== "quantitative-comparison") {
            quantComparison.style.display = "none";

            if (questions[currentQuestion].type !== "data-interpretation-single") {
                // Hide image
                imageContainer.style.display = "none";

            }else{
                // Show image
                imageContainer.style.display = "";

                // Return to two equal columns
                questionContainer.style.width = "";
                questionContainer.style.flex = "4";
                questionContainer.style.padding = "0 0";


                const envChoice = document.querySelector('#choices');
                envChoice.style.margin = "0";
            }
        }else{
            quantComparison.style.display = "";
        }

    } else {
        // Show passage
        passageContainer.style.display = "";

        // Return to two equal columns
        questionContainer.style.width = "";
        questionContainer.style.flex = "4";
        questionContainer.style.padding = "0 0";

        const envChoice = document.querySelector('#choices');
        envChoice.style.margin = "0";

    }
}

//----------------------------------
//       QUESTION RENDERING
//----------------------------------


function renderQuestion() {
    
    //document.querySelector('test-title').textContent = greTest.testName;
    document.querySelector('#question-number').innerHTML=`Question ${currentQuestion + 1} of  ${questions.length}`;
    document.querySelector('#question').innerHTML= questions[currentQuestion].question;
    document.querySelector('#instruction').innerHTML= questions[currentQuestion].instruction;

    questionEnv();
    renderChoices();
    markQuestionStatus();
    



    document.querySelector('#next').onclick = nextQuestion;
    document.querySelector('#previous').onclick = previousQuestion;
    document.querySelector('#hide').onclick = toggleTime;
    document.querySelector('#mark').onclick = markQuestion;
    document.querySelector('#review').onclick = reviewTable;
    document.querySelector('#close-Review').onclick = closeReview;
    document.querySelector('#go-question').onclick = closeReview;

    document.querySelector('#quit').onclick = confirmTestExit;
    document.querySelector('#end-section').onclick = confirmSectionExit;
    document.querySelector('#quit-r').onclick = confirmTestExit;
    document.querySelector('#end-section-r').onclick = confirmSectionExit;

    document.querySelector('#sec-yes').onclick = finishSection;
    document.querySelector('#sec-no').onclick = closeSectionExit;
    document.querySelector('#test-yes').onclick = finishTest;
    document.querySelector('#test-no').onclick = closeTestExit;
    
    questionStartTime = Date.now();
}


//--------------------------------------
//     FINISH SECTION AND QUIT TEST ?
//--------------------------------------


//-------------------
//   SECTION EXIT
//-------------------

function closeSectionExit(){
    const secExit = document.querySelector('#section-exit');
    
    secExit.classList.add("hidden");
}

function confirmSectionExit(){
    const secExit = document.querySelector('#section-exit');
    
    secExit.classList.remove("hidden");
}



async function finishSection() {
    await saveCurrentAnswer();

    if (currentSection < greTest.sections.length - 1) {
        nextSection();
    }
    else {
        finishTest();
    }
    closeSectionExit();
}


function nextSection() {
    currentSection++;
    renderTest();
}

//---------------
//  FINISH TEST
//---------------

function closeTestExit(){
    const secExit = document.querySelector('#test-exit');
    
    secExit.classList.add("hidden");
}

function confirmTestExit(){
    const secExit = document.querySelector('#test-exit');
    
    secExit.classList.remove("hidden");
}

async function finishTest() {
    await saveCurrentAnswer();

    clearInterval(timer);
    timer = null;

    await generateTestResult();
    closeTestExit();

    alert("Test Completed.");
}

//-----------------------------------
//        CONTENT LOADING 
//-----------------------------------

document.addEventListener("DOMContentLoaded", ()=>{
    loadTest(4);
    
});
