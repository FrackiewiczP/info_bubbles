const { io } = require("socket.io-client");

const socket = io("http://127.0.0.1:5000");

socket.on("connect", () => {
    console.log("connected");
    document.getElementById("connection-square").style.backgroundColor = "green";
});

socket.on("disconnect", () => {
    console.log("disconnected");
    document.getElementById("connection-square").style.backgroundColor = "red";
});

socket.on("simulation_finished", (data) => {
    console.log(data);
    clearCanvas();
    for(const u in data){
        addUser(data[u][0], data[u][1]);
    }
});

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

window.updateCurrentStep = () =>
{
    let currentStep = document.getElementById("step-slider").value;
    document.getElementById("current-step").textContent = currentStep.toString();
}

window.updateMaxStep = () =>
{
    console.log("Max step")
    let maxStep = document.getElementById("step-num").value;
    document.getElementById("step-slider").max = maxStep;
}

window.startSimulation = () =>
{
    let numUsers = document.getElementById("agent-num").value;
    socket.emit("start_simulation", numUsers);
    console.log("Event sent");
}
