import React from 'react';
import '../styles/Title.scss'
import Title from './Title';
import Simulation from './Simulation';
import ParametersForm from './ParametersForm';
import io from "socket.io-client";
import SimulationParameters from '../helpers/SimulationParameters';
import { ConvertingFunctions } from '../helpers/SimulationParameters';

class App extends React.Component
{
    constructor(props){
        super(props);

        this.state = {
            size: window.innerWidth/2.5 < 300 ? 300 : window.innerWidth/2.5,
            currentStep: 0,
            maxStep: 0,
            currentStepData: null,
            isSocketConnected: false,
            choosingParameters: false,
            simulationParameters: new SimulationParameters(),
            waitingForSimulation: true,
        }

        this.parametersHandlers = {};
        for(let u in this.state.simulationParameters){
            this.parametersHandlers[u] = this.prepareParameterHandler(u);
        }

        console.log(this.parametersHandlers);

        this.socket = io("http://localhost:5000");
        this.socket.on("connect", () => {
            console.log("Connected");
            this.handleSocketConnected();
        });
        this.socket.on("disconnect", () => {
            console.log("Disconnected");
            this.handleSocketDisconnected();
        });
        this.socket.on("simulation_finished", (data) => {
            this.handleSimulationFinished(data);
        });
        this.socket.on("simulation_step_sent", (data) => {
            this.handleSimulationStepReceived(data);
        });
    }

    render(){
        return (
            <div>
                <Title/>
                {this.state.choosingParameters
                    ? <ParametersForm
                        handleChooseParametersButton={this.handleChooseParametersButton}
                        parameters={this.state.simulationParameters}
                        parametersHandlers={this.parametersHandlers}
                    />
                    : <Simulation
                        size={this.state.size}
                        currentStep={this.state.currentStep}
                        currentStepData={this.state.currentStepData}
                        isSocketConnected={this.state.isSocketConnected}
                        maxStep={this.state.maxStep}
                        waitingForSimulation={this.state.waitingForSimulation}
                        handleCurrentStepChange={this.handleCurrentStepChange}
                        handleChooseParametersButton={this.handleChooseParametersButton}
                        handleStartSimulationButton={this.handleStartSimulationButton}
                    />}
            </div>
        );
    }

    handleSocketConnected(){
        this.setState({isSocketConnected: true});
    }

    handleSocketDisconnected(){
        this.setState({isSocketConnected: false});
    }

    handleSimulationFinished(data){
        console.log("Simulation finished");
        this.setState({
            maxStep: data,
            waitingForSimulation: false,
        });
    }

    handleSimulationStepReceived(data){
        console.log("Simulation step received")
        this.setState({
            currentStepData: data
        });
    }

    handleCurrentStepChange = (event) => {
        this.setState({currentStep: event.target.value});
        this.socket.emit("simulation_step_requested", event.target.value)
    }

    handleChooseParametersButton = () => {
        const choosingParameters = this.state.choosingParameters;
        this.setState({choosingParameters: !choosingParameters});
    }

    prepareParameterHandler = (parameterName) => {
        return (event) => {
            let params = {...this.state.simulationParameters};
            params[parameterName] = ConvertingFunctions[parameterName](event.target.value);
            this.setState({simulationParameters: params});
        }
    }

    handleStartSimulationButton = () => {
        this.setState({waitingForSimulation: true});
        this.socket.emit(
            "start_simulation",
            this.state.simulationParameters);
        console.log("Event sent");
    }
}

export default App;
