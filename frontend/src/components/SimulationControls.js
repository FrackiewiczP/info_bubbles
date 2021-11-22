import React from 'react';
import '../styles/SimulationControls.scss'
import ConnectionIndicator from './ConnectionIndicator';

const SimulationControls = (props) => (
    <div className="SimulationControls">
        <button onClick={props.handleChooseParametersButton}>Wybierz Parametry</button>
        <button onClick={props.handleStartSimulationButton} disabled={!props.isSocketConnected}>Rozpocznij symulację</button>
        <div className="simulation-step">Krok symulacji: {props.currentStep}</div>
        <input type="range" value={props.currentStep} min={1} max={props.maxStep} onChange={props.handleCurrentStepChange} disabled={props.currentSimulationData == null}></input>
        <ConnectionIndicator isSocketConnected={props.isSocketConnected}/>
    </div>
)


export default SimulationControls;
