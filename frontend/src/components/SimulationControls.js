import React from 'react';
import '../styles/SimulationControls.scss'
import ConnectionIndicator from './ConnectionIndicator';
import ProgressIndicator from './ProgressIndicator';

const SimulationControls = (props) => (
    <div className="SimulationControls">
        <button onClick={props.handleChooseParametersButton}>Wybierz Parametry</button>
        <button onClick={props.handleSeeStatsButton}>Statystyki</button>
        <button onClick={props.handleStartSimulationButton} disabled={!props.isSocketConnected}>Rozpocznij symulację</button>
        <button onClick={props.handleDownloadSimulationButton}>Pobierz zapis symulacji</button>
        <div className="simulation-step">Krok symulacji</div>
        <input type="number" value={props.currentStep} min={1} max={props.lastStepReceived} onInput={props.handleCurrentStepChange}></input>
        <ConnectionIndicator className="ConnectionIndicator" isSocketConnected={props.isSocketConnected}/>
        {props.lastStepReceived == null ? null : <ProgressIndicator className="ProgressIndicator" lastStepReceived={props.lastStepReceived} maxStep={props.maxStep}/>}
    </div>
)


export default SimulationControls;
