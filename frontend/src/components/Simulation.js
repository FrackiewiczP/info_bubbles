import React from 'react';
import '../styles/Simulation.scss'
import SimulationControls from './SimulationControls';
import 'animate.css';
import ColorPaletteGenerator from '../helpers/ColorPaletteGenerator';

class Simulation extends React.Component{
    constructor(props){
        super(props);
        this.canvasRef = React.createRef();
    }

    componentDidMount(){
        this.colorPalette = ColorPaletteGenerator.GetColorPalette(this.props.currentGroupCount);
        let ctx = this.canvasRef.current.getContext("2d");
        this.drawSimulationStep(this.props.currentStepData, ctx);
    }

    componentDidUpdate(){
        this.colorPalette = ColorPaletteGenerator.GetColorPalette(this.props.currentGroupCount);
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
                        handleSeeStatsButton={this.props.handleSeeStatsButton}
                        handleStartSimulationButton={this.props.handleStartSimulationButton}
                        handleDownloadSimulationButton={this.props.handleDownloadSimulationButton}
                        lastStepReceived={this.props.lastStepReceived}
                        />
                </div>
            );
    }

    addUser(id, x, y, ctx)
    {
        let processData = (d, maxValue) => (d+1)*maxValue/2;
        const radius = 3;

        ctx.beginPath();
        ctx.arc(processData(x, this.props.size), processData(y, this.props.size), radius, 0, 2 * Math.PI, false);
        ctx.fillStyle = this.colorPalette[this.props.currentGroups[id]];
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
            this.addUser(u, data[u][0], data[u][1], ctx);
        }
    }
}


export default Simulation;
