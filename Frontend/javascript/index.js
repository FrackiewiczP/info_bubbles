function clearCanvas()
{
    let canvas = document.getElementById("simulation-canvas");
    let ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function addUser(x, y)
{
    let canvas = document.getElementById("simulation-canvas");
    let ctx = canvas.getContext("2d");
    const radius = 5;

    ctx.beginPath();
    ctx.arc(x*canvas.width, y*canvas.height, radius, 0, 2 * Math.PI, false);
    ctx.fillStyle = "#" + Math.floor(Math.random()*16777215).toString(16);
    ctx.fill();
}

function updateCurrentStep()
{
    let currentStep = document.getElementById("step-slider").value;
    document.getElementById("current-step").textContent = currentStep.toString();
}
