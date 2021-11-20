const { io } = require("socket.io-client");

const socket = io("http://127.0.0.1:5000");
let currentResult;

socket.on("connect", () => {
    console.log("connected");
    document.getElementById("connection-square").style.backgroundColor = "green";
});

socket.on("disconnect", () => {
    console.log("disconnected");
    document.getElementById("connection-square").style.backgroundColor = "red";
});

socket.on("simulation_finished", (data) => {
    currentResult = data[0];
    let first_step = data[0][0];
    let stepCount = data[1];

    drawSimulationStep(first_step);
    document.getElementById("step-slider").value = 1;
    document.getElementById("step-slider").max = stepCount;
    updateCurrentStep();
});

function clearCanvas()
{
    let canvas = document.getElementById("simulation-canvas");
    let ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function addUser(x, y)
{
    let processData = (d, maxValue) => (d+1)*maxValue/2;
    let canvas = document.getElementById("simulation-canvas");
    let ctx = canvas.getContext("2d");
    const radius = 3;

    ctx.beginPath();
    ctx.arc(processData(x, canvas.width), processData(y, canvas.height), radius, 0, 2 * Math.PI, false);
    ctx.fillStyle = "#FF0000";
    ctx.fill();
}

function drawSimulationStep(data)
{
    clearCanvas();
    for(const u in data){
        addUser(data[u][0], data[u][1]);
    }
}

window.updateCurrentStep = () =>
{
    let currentStep = document.getElementById("step-slider").value;
    document.getElementById("current-step").textContent = currentStep.toString();

    drawSimulationStep(currentResult[currentStep-1]);
}

window.startSimulation = () =>
{
    let numAgents = document.getElementById("agent-num").value;
    let numSteps = document.getElementById("step-num").value;
    let numLinks = document.getElementById("links-num").value;
    let memCapacity = document.getElementById("mem-capacity").value;
    let friendLoseProb = document.getElementById("friend-lose-prob").value;
    let communicationForm = document.querySelector('input[name="info-sharing-mode"]:checked').value;
    let interUserCommunicationForm = document.querySelector('input[name="inter-user-sharing-mode"]:checked').value;
    let accLatitude = document.getElementById("acc-latitude").value;
    let accSharpness = document.getElementById("acc-sharpness").value;

    socket.emit(
        "start_simulation",
        {
            number_of_agents: parseInt(numAgents),
            number_of_steps: parseInt(numSteps),
            number_of_links: parseInt(numLinks),
            mem_capacity: parseInt(memCapacity),
            friend_lose_prob: parseFloat(friendLoseProb),
            communication_form: communicationForm,
            inter_user_communication_form: interUserCommunicationForm,
            acc_latitude: parseFloat(accLatitude),
            acc_sharpness: parseFloat(accSharpness),
        });
    console.log("Event sent");
}
