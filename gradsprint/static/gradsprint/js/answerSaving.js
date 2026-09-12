function getCSRFToken(){
    const cookies=document.cookie.split(";");

    for(let cookie of cookies){
        cookie=cookie.trim();

        if(cookie.startsWith("csrftoken=")){
            return decodeURIComponent(
                cookie.substring("csrftoken=".length)
            );
        }
    }

    return null;
}


async function saveCurrentAnswer() {

    const question = questions[currentQuestion];
    const answer = answers[currentQuestion];

    if (!question) {
        return;
    }

    // --------------------------------
    // CALCULATE TIME TAKEN
    // --------------------------------

    let timeTaken = 0;
    if (questionStartTime != null) {
        timeTaken = Math.round(
            (Date.now() - questionStartTime)/1000
        );
    }

    try {
        const response = await fetch(
            "/api/save-answer/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },

                body: JSON.stringify({
                    question_id: question.id,
                    selected_answer: answer,
                    time_taken: timeTaken
                })
            }
        );


        const data = await response.json();

        if (!response.ok) {
            console.error(
                "Answer save failed:",
                data
            );
            return;
        }

        console.log(
            "Answer saved:",
            data
        );
    }

    catch (error) {
        console.error(
            "Error saving answer:",
            error
        );
    }
}