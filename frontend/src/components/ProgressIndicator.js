import React from 'react';
import '../styles/ProgressIndicator.scss'

const ProgressIndicator = (props) => (
    <div className="ProgressIndicator">
        <div>Postęp symulacji:</div>
    <div className="simulation-progress">{props.lastStepReceived}/{props.maxStep}</div>
    </div>
);

export default ProgressIndicator;
