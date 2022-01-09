import React from 'react';
import '../styles/ParametersForm.scss'
import 'animate.css'
import ParameterInputNumeric from './ParameterInputNumeric';
import { ParametersNames } from '../helpers/SimulationParameters';
import ParameterInputRadio from './ParameterInputRadio';
import { CommunicationMode, UsersCommunicationMode } from '../helpers/Consts';

class ParametersForm extends React.Component{
    render(){
        return(
            <div className="ParametersForm animate__animated animate__fadeInDown">
                <h1>Wybór parametrów</h1>
                <ParameterInputNumeric
                    label="Liczba agentów"
                    value={this.props.parameters[ParametersNames.NUMBER_OF_AGENTS]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.NUMBER_OF_AGENTS]}    
                />
                <ParameterInputNumeric
                    label="Liczba kroków"
                    value={this.props.parameters[ParametersNames.NUMBER_OF_STEPS]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.NUMBER_OF_STEPS]}    
                />
                <ParameterInputNumeric
                    label="Liczba początkowych znajomych"
                    value={this.props.parameters[ParametersNames.NUMBER_OF_LINKS]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.NUMBER_OF_LINKS]}    
                />
                <ParameterInputNumeric
                    label="Pojemność pamięci użytkownika"
                    value={this.props.parameters[ParametersNames.MEM_CAPACITY]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.MEM_CAPACITY]}    
                />
                <ParameterInputNumeric
                    label="Prawdopodobieństwo utraty przyjaciela"
                    value={this.props.parameters[ParametersNames.FRIEND_LOSE_PROB]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.FRIEND_LOSE_PROB]}    
                />
                <ParameterInputNumeric
                    label="Próg akceptacji"
                    value={this.props.parameters[ParametersNames.ACC_LATITUDE]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.ACC_LATITUDE]}    
                />
                <ParameterInputNumeric
                    label="Ostrość akceptacji"
                    value={this.props.parameters[ParametersNames.ACC_SHARPNESS]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.ACC_SHARPNESS]}    
                />
                <ParameterInputNumeric
                    label="Liczba grup"
                    value={this.props.parameters[ParametersNames.NO_OF_GROUPS]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.NO_OF_GROUPS]}    
                />
                <ParameterInputNumeric
                    label="Procent znajomych w tej samej grupie"
                    value={this.props.parameters[ParametersNames.PERCENT_OF_THE_SAME_GROUP]}
                    handleOnChange={this.props.parametersHandlers[ParametersNames.PERCENT_OF_THE_SAME_GROUP]}    
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
                            }
                        ]
                    }
                />
                <ParameterInputRadio
                    name={ParametersNames.INTER_USER_COMMUNICATION_FORM}
                    value={this.props.parameters[ParametersNames.INTER_USER_COMMUNICATION_FORM]}
                    groupName="Komunikacja między użytkownikami"
                    handleOnChange={this.props.parametersHandlers[ParametersNames.INTER_USER_COMMUNICATION_FORM]} 
                    options={
                        [
                            {
                                label: "Do jednego przyjaciela",
                                value: UsersCommunicationMode.TO_ONE_RANDOM,
                            },
                            {
                                label: "Do wszystkich przyjaciół",
                                value: UsersCommunicationMode.TO_ALL,
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
