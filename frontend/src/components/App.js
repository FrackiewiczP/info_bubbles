import React from 'react';
import axios from 'axios';
import FileSaver from 'file-saver';
import '../styles/Title.scss'
import Title from './Title';
import Simulation from './Simulation';
import ParametersForm from './ParametersForm';
import Statistics from './Statistics';
import io from "socket.io-client";
import SimulationParameters from '../helpers/SimulationParameters';
import { ConvertingFunctions } from '../helpers/SimulationParameters';
import { MainViewState } from '../helpers/Consts';
import StatisticsChartData from '../helpers/StatisticsChartData';

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
            statisticsChartData: new StatisticsChartData(null, null, null),
            isSocketConnected: false,
            mainViewState: MainViewState.SIMULATION_VIEW,
            simulationParameters: new SimulationParameters(),
        }

        this.parametersHandlers = {};
        for(let u in this.state.simulationParameters){
            this.parametersHandlers[u] = this.prepareParameterHandler(u);
        }

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
        this.socket.on("simulation_stats_sent", (data) => {
            this.handleSimulationStatsReceived(data);
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
                {this.state.mainViewState === MainViewState.CHOOSING_PARAMETERS
                    ? <ParametersForm
                        handleSeeSimulationButton={this.getChangeViewHandler(MainViewState.SIMULATION_VIEW)}
                        parameters={this.state.simulationParameters}
                        parametersHandlers={this.parametersHandlers}
                    />
                    : this.state.mainViewState === MainViewState.SIMULATION_VIEW 
                        ? <Simulation
                            size={this.state.size}
                            currentStep={this.state.currentStep}
                            currentStepData={this.state.currentStepData}
                            isSocketConnected={this.state.isSocketConnected}
                            maxStep={this.state.maxStep}
                            lastStepReceived={this.state.lastStepReceived}
                            handleCurrentStepChange={this.handleCurrentStepChange}
                            handleChooseParametersButton={this.getChangeViewHandler(MainViewState.CHOOSING_PARAMETERS)}
                            handleSeeStatsButton={this.getChangeViewHandler(MainViewState.CHARTS_VIEW)}
                            handleStartSimulationButton={this.handleStartSimulationButton}
                            handleDownloadSimulationButton={this.handleDownloadSimulationButton}
                        />
                        : <Statistics
                            handleSeeSimulationButton={this.getChangeViewHandler(MainViewState.SIMULATION_VIEW)}
                            handleChangeShownStatistic={this.handleChangeShownStatistic}
                            maxStep={this.state.maxStep}
                            statisticsChartData={this.state.statisticsChartData}
                        />
                }
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

    handleChangeShownStatistic = (event) => {
        const currChartData = this.state.statisticsChartData;
        const currMaxStep = this.state.maxStep;
        this.setState({statisticsChartData: new StatisticsChartData(
            currMaxStep,
            currChartData.data.data,
            parseInt(event.target.value))});
        this.socket.emit("simulation_stats_requested", event.target.value)
    }

    handleSimulationStatsReceived(data)
    {
        const currchosenStatistic = this.state.statisticsChartData.chosenStatistic;
        const currMaxStep = this.state.maxStep;
        this.setState({statisticsChartData: new StatisticsChartData(
            currMaxStep,
            data,
            currchosenStatistic)});
    }

    getChangeViewHandler = (state) => () => {
        this.setState({mainViewState: state});
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
