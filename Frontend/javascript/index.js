function clearCanvas()
{
    let canvas = document.getElementById("simulation-canvas");
    let ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function addUser()
{
    let canvas = document.getElementById("simulation-canvas");
    let ctx = canvas.getContext("2d");
    const centerX = Math.random() * canvas.width;
    const centerY = Math.random() * canvas.height;
    const radius = 5;

    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
    ctx.fillStyle = "#" + Math.floor(Math.random()*16777215).toString(16);
    ctx.fill();
}

function startSimulation()
{
    clearCanvas()
    let numUsers = document.getElementById("agent-num").value
    for(let i = 0; i < numUsers; i++){
        addUser();
    }
}

function updateCurrentStep()
{
    let currentStep = document.getElementById("step-slider").value;
    document.getElementById("current-step").textContent = currentStep.toString();
}
