const calculatorButton = document.querySelector("#calculator-button");
const calculator = document.querySelector("#calculator");
const calculatorDisplay = document.querySelector("#calculator-display");
const calculatorClose = document.querySelector("#calculator-close");
const calculatorHeader = document.querySelector("#calculator-header");


//-----------------------------------
//        NORMAL INPUT
//-----------------------------------

function addCalculatorValue(value) {

    const display = calculatorDisplay.value;

    if (value === ".") {

        const lastNumber = display.split(/[+\-*/]/).pop();
        if (lastNumber.includes(".")) {
            return;
        }
    }
    calculatorDisplay.value += value;
}

//-----------------------------------
//         SQUARE ROOT
//-----------------------------------

function calculateSquareRoot() {

    const value = Number(calculatorDisplay.value);

    if (isNaN(value) || value < 0) {

        calculatorDisplay.value = "Error";
        return;
    }
    calculatorDisplay.value = Math.sqrt(value);
}

//-----------------------------------
//          PERCENTAGE
//-----------------------------------

function calculatePercent() {

    const value = Number(calculatorDisplay.value);

    if (isNaN(value)) {

        calculatorDisplay.value = "Error";
        return;
    }
    calculatorDisplay.value = value / 100;
}

//-----------------------------------
//        POSITIVE/NEGATIVE
//-----------------------------------

function changeSign() {

    const value = Number(calculatorDisplay.value);

    if (isNaN(value)) {
        return;
    }
    calculatorDisplay.value = String(value * -1);
}

//-----------------------------------
//          CALCULATE
//-----------------------------------

function calculateResult() {

    const expression = calculatorDisplay.value;

    if (!/^[0-9+\-*/().\s]+$/.test(expression)) {

        calculatorDisplay.value = "Error";
        return;
    }

    try {
        const result = Function(`"use strict"; return (${expression})`)();

        if (!Number.isFinite(result)) {

            calculatorDisplay.value = "Error";
            return;
        }
        calculatorDisplay.value = result;
    }

    catch {
        calculatorDisplay.value = "Error";
    }
}

//--------------------------------------
//           DRAGGABILITY
//--------------------------------------

let dragging = false;

let offsetX = 0;
let offsetY = 0;


calculatorHeader.addEventListener("mousedown", (event) => {

        dragging = true;

        offsetX = event.clientX - calculator.offsetLeft;

        offsetY = event.clientY - calculator.offsetTop;

    }
);


document.addEventListener("mousemove", (event) => {

        if (!dragging) return;

        calculator.style.left = `${event.clientX - offsetX}px`;

        calculator.style.top = `${event.clientY - offsetY}px`;

        calculator.style.right = "auto";
    }
);


document.addEventListener("mouseup", () => {

        dragging = false;
    }
);

//--------------------------------------
//        CALCULATOR LOGIC
//--------------------------------------





calculatorButton.addEventListener("click", () => {

    calculator.classList.toggle("hidden");
});


calculatorClose.addEventListener("click", () => {

    calculator.classList.add("hidden");
});


document.querySelector(".calculator-buttons").addEventListener("click", (event)=>{

        const button = event.target.closest("button");

        if (!button) return;


        const value = button.dataset.value;
        const action = button.dataset.action;


        if (value !== undefined) {
            addCalculatorValue(value);
        }

        if (action === "clear") {
            calculatorDisplay.value = "";
        }

        if (action === "backspace") {
            calculatorDisplay.value = calculatorDisplay.value.slice(0, -1);
        }

        if (action === "equals") {
            calculateResult();
        }

        if (action === "sqrt") {
            calculateSquareRoot();
        }

        if (action === "percent") {
            calculatePercent();
        }

        if (action === "sign") {
            changeSign();
        }

    });