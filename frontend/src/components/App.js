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
import {toast} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css'

class App extends React.Component
{
    constructor(props){
        super(props);
        toast.configure(
            "top-center",
            5000
        );
        this.state = {
            size: window.innerWidth/2.5 < 300 ? 300 : window.innerWidth/2.5,
            currentStep: null,
            lastStepReceived: null,
            maxStep: null,
            currentGroups: null,
            currentGroupCount: null,
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
        this.socket.on("groups_for_simulation_sent", (data) => {
            this.handleGroupsForSimulationReceived(data);
        })
        this.socket.on("error", (data) => {
            toast.error(data, {
                position: "top-right",
                autoClose: 5000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
                });
        });
    }

    render(){
        return (
            <div className="App">
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
                            currentGroups={this.state.currentGroups}
                            currentGroupCount={this.state.currentGroupCount}
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

    handleGroupsForSimulationReceived(data){
        console.log(data)
        this.setState({
            currentGroups: data["groups"],
            currentGroupCount: data["group_count"]
        })
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
        let val = this.validateParameters() //[0] - result, [1] - message
        console.log(val[0]);
        if(!val[0])
        {
            toast.error(val[1], {
                position: "top-right",
                autoClose: 5000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
                });
            return;
        }
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

    validateParameters = () => {
        if(this.state.simulationParameters.number_of_agents < 0)
            return [false, "Liczba agentów musi być większa od 0"];
        if(this.state.simulationParameters.number_of_steps < 0)
            return [false, "Liczba kroków musi być większa od 0"];
        if(this.state.simulationParameters.number_of_links < 0)
            return [false, "Liczba połączeń musi być większa od 0"];
        if(this.state.simulationParameters.number_of_links > this.state.simulationParameters.number_of_agents - 1)
            return [false, "Liczba połączeń nie może być większa niż liczba agentów"];
        if(this.state.simulationParameters.mem_capacity < 0)
            return [false, "Pojemność pamięci musi być większa od 0"];
        if(this.state.simulationParameters.friend_lose_prob < 0 || this.state.simulationParameters.friend_lose_prob > 1)
            return [false, "Prawdopodobieństwo utraty przyjaciela musi być liczbą z przedziału [0,1]"];
        if(this.state.simulationParameters.acc_latitude < 0 || this.state.simulationParameters.acc_latitude > 1)
            return [false, "Próg akceptacji musi być liczbą z przedziału [0,1]"];
        if(this.state.simulationParameters.acc_sharpness < 0)
            return [false, "Ostrość akceptacji musi być większa od 0"];
        if(this.state.simulationParameters.percent_of_the_same_group < 0 || this.state.simulationParameters.percent_of_the_same_group > 100)
            return [false, "Procent znajomych w tej samej grupie musi być liczbą z przedziału [0,100]"];
        if(this.state.simulationParameters.no_of_groups < 0)
            return [false, "Liczba grup musi być większa od zera"];
        if(this.state.simulationParameters.no_of_groups > this.state.simulationParameters.number_of_agents)
            return [false, "Liczba grup nie może być większa niż liczba agentów"];
        return [true, ""]
    }
}

export default App;
