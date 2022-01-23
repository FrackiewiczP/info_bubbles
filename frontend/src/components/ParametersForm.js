import React from 'react';
import '../styles/ParametersForm.scss'
import 'animate.css'
import ParameterInputNumeric from './ParameterInputNumeric';
import { ParametersNames } from '../helpers/SimulationParameters';
import ParameterInputRadio from './ParameterInputRadio';
import { CommunicationMode, UsersCommunicationMode, FriendsLinksTypes } from '../helpers/Consts';

class ParametersForm extends React.Component{
    render(){
        return(
            <div className="ParametersForm animate__animated animate__fadeInDown">
                <h1>Wybór parametrów</h1>
                <ParameterInputNumeric
                    label="Liczba agentów"
                    value={this.props.parameters[ParametersNames.NUMBER_OF_AGENTS]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.NUMBER_OF_AGENTS]}
                    min = {0}
                />
                <ParameterInputNumeric
                    label="Liczba kroków"
                    value={this.props.parameters[ParametersNames.NUMBER_OF_STEPS]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.NUMBER_OF_STEPS]}
                    min = {0}
                />
                <ParameterInputNumeric
                    label="Liczba początkowych znajomych"
                    value={this.props.parameters[ParametersNames.NUMBER_OF_LINKS]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.NUMBER_OF_LINKS]}
                    min = {0}
                    max = {this.props.parameters[ParametersNames.NUMBER_OF_AGENTS]}  
                />
                <ParameterInputNumeric
                    label="Pojemność pamięci agenta"
                    value={this.props.parameters[ParametersNames.MEM_CAPACITY]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.MEM_CAPACITY]}
                    min = {0}   
                />
                <ParameterInputNumeric
                    label="Prawdopodobieństwo utraty znajomego"
                    value={this.props.parameters[ParametersNames.FRIEND_LOSE_PROB]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.FRIEND_LOSE_PROB]}
                    min = {0}
                    max = {1}
                />
                <ParameterInputNumeric
                    label="Próg akceptacji"
                    value={this.props.parameters[ParametersNames.ACC_LATITUDE]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.ACC_LATITUDE]}
                    min = {0}
                    max = {1} 
                />
                <ParameterInputNumeric
                    label="Ostrość akceptacji"
                    value={this.props.parameters[ParametersNames.ACC_SHARPNESS]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.ACC_SHARPNESS]}
                    min = {0}  
                />
                <ParameterInputNumeric
                    label="Liczba grup"
                    value={this.props.parameters[ParametersNames.NO_OF_GROUPS]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.NO_OF_GROUPS]}   
                    min = {1}
                    max = {this.props.parameters[ParametersNames.NUMBER_OF_AGENTS]} 
                />
                <ParameterInputNumeric
                    label="Procent znajomych w tej samej grupie"
                    value={this.props.parameters[ParametersNames.PERCENT_OF_THE_SAME_GROUP]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.PERCENT_OF_THE_SAME_GROUP]}    
                    min = {0}
                    max = {100}
                />
                <ParameterInputRadio
                    name={ParametersNames.COMMUNICATION_FORM}
                    value={this.props.parameters[ParametersNames.COMMUNICATION_FORM]}
                    groupName="Komunikacja serwisu"
                    handleOnChange={this.props.parametersHandlers[ParametersNames.COMMUNICATION_FORM]} 
                    options={
                        [
                            {
                                label: "Indywidualna",
                                value: CommunicationMode.INDIVIDUAL,
                            },
                            {
                                label: "Centralna",
                                value: CommunicationMode.CENTRAL,
                            },
                            {
                                label: "Filtr bliski",
                                value: CommunicationMode.FILTER_CLOSE,
                            },
                            {
                                label: "Filtr daleki",
                                value: CommunicationMode.FILTER_DISTANT,
                            },
                        ]
                    }
                />
                <ParameterInputRadio
                    name={ParametersNames.INTER_USER_COMMUNICATION_FORM}
                    value={this.props.parameters[ParametersNames.INTER_USER_COMMUNICATION_FORM]}
                    groupName="Komunikacja między agentami"
                    handleOnChange={this.props.parametersHandlers[ParametersNames.INTER_USER_COMMUNICATION_FORM]} 
                    options={
                        [
                            {
                                label: "Do jednego znajomego",
                                value: UsersCommunicationMode.TO_ONE_RANDOM,
                            },
                            {
                                label: "Do wszystkich znajomych",
                                value: UsersCommunicationMode.TO_ALL,
                            }
                        ]
                    }
                />
                <ParameterInputRadio
                    name={ParametersNames.INITIAL_CONNECTIONS}
                    value={this.props.parameters[ParametersNames.INITIAL_CONNECTIONS]}
                    groupName="Znajomości"
                    handleOnChange={this.props.parametersHandlers[ParametersNames.INITIAL_CONNECTIONS]} 
                    options={
                        [
                            {
                                label: "Skierowane",
                                value: FriendsLinksTypes.RANDOM_DIRECTED,
                            },
                            {
                                label: "Nieskierowane",
                                value: FriendsLinksTypes.RANDOM_NON_DIRECTED,
                            }
                        ]
                    }
                />
                <button onClick={this.props.handleSeeSimulationButton}>Widok symulacji</button>
            </div>
        );
    }
}

export default ParametersForm;
