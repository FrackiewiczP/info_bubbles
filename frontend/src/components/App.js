import React from 'react';
import axios from 'axios';
import FileSaver from 'file-saver';
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
            currentStep: null,
            lastStepReceived: null,
            maxStep: null,
            currentStepData: null,
            isSocketConnected: false,
            choosingParameters: false,
            simulationParameters: new SimulationParameters(),
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
        this.socket.on("simulation_step_sent", (data) => {
            this.handleSimulationStepReceived(data);
        });
        this.socket.on("simulation_step_finished", (data) => {
            this.handleSimulationStepFinished(data);
        });
        this.socket.on("simulation_already_running", () => {
            console.log("Simulation already running");
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
                        lastStepReceived={this.state.lastStepReceived}
                        handleCurrentStepChange={this.handleCurrentStepChange}
                        handleChooseParametersButton={this.handleChooseParametersButton}
                        handleStartSimulationButton={this.handleStartSimulationButton}
                        handleDownloadSimulationButton={this.handleDownloadSimulationButton}
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

    handleSimulationStepFinished(data){
        this.setState({
            currentStepData: data["step_data"],
            lastStepReceived: data["step_number"],
            currentStep: data["step_number"],
            maxStep: this.state.simulationParameters.number_of_steps
        })
    }

    handleSimulationStepReceived(data){
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
        this.socket.emit(
            "start_simulation",
            this.state.simulationParameters);
        console.log("Event sent");
    }

    handleDownloadSimulationButton = async () => {
        axios.get("http://localhost:5000/simulation?socket_id="+this.socket.id, {
            responseType: 'blob',
        })
        .then(response => FileSaver.saveAs(response.data, "simulation.csv"))
        .catch(response => console.log("Failure downloading a file"));
    }
}

export default App;
