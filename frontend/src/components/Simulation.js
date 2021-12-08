import React from 'react';
import '../styles/Simulation.scss'
import SimulationControls from './SimulationControls';
import 'animate.css';

class Simulation extends React.Component{
    constructor(props){
        super(props);
        this.canvasRef = React.createRef();
    }

    componentDidMount(){
        let ctx = this.canvasRef.current.getContext("2d");
        this.drawSimulationStep(this.props.currentStepData, ctx);
    }

    componentDidUpdate(){
        let ctx = this.canvasRef.current.getContext("2d");
        this.drawSimulationStep(this.props.currentStepData, ctx);
    }

    render(){
            return (
                <div className="Simulation animate__animated animate__fadeInUp">
                    <canvas ref={this.canvasRef} width={this.props.size} height={this.props.size}/>
                    <SimulationControls
                        currentStep={this.props.currentStep}
                        maxStep={this.props.maxStep}
                        isSocketConnected={this.props.isSocketConnected}
                        handleCurrentStepChange={this.props.handleCurrentStepChange}
                        handleChooseParametersButton={this.props.handleChooseParametersButton}
                        handleStartSimulationButton={this.props.handleStartSimulationButton}
                        />
                </div>
            );
    }

    addUser(x, y, ctx)
    {
        let processData = (d, maxValue) => (d+1)*maxValue/2;
        const radius = 3;

        ctx.beginPath();
        ctx.arc(processData(x, this.props.size), processData(y, this.props.size), radius, 0, 2 * Math.PI, false);
        ctx.fillStyle = "#FF0000";
        ctx.fill();
    }

    clearCanvas(ctx)
    {
        ctx.clearRect(0, 0, this.props.size, this.props.size);
    }

    drawSimulationStep(data, ctx)
    {
        if(data == null)
        {
            return;
        }
        this.clearCanvas(ctx);
        for(const u in data){
            this.addUser(data[u][0], data[u][1], ctx);
        }

        if(this.props.waitingForSimulation)
        {
            ctx.rect(0,0, this.props.size, this.props.size);
            ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
            ctx.fill();
           
            ctx.font = '48px sans-serif';
            ctx.textAlign = "center"
            ctx.fillStyle = "rgba(255, 255, 255)"
            ctx.fillText('Proszę czekać', this.props.size/2, this.props.size/2);
        }
    }
}


export default Simulation;
