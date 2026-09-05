document.addEventListener("DOMContentLoaded",function(){
    const colors=[
        "#1abebe",
        "#0a0a0a",
        "#c5341a",
        "#03a747"
    ];

    const randomColor=colors[Math.floor(Math.random()*colors.length)];

    const logoLeft=document.querySelector("#kaoo");
    const logoRight=document.querySelector("#shi");

    if(logoLeft&&logoRight){
        logoLeft.style.backgroundColor=randomColor;
        logoRight.style.color=randomColor;
    }
});