import React from 'react';
import '../styles/ConnectionIndicator.scss'

const ConnectionIndicator = (props) => (
    <div className="ConnectionIndicator">
        <div>Połączenie z serwerem:</div>
        <div className={props.isSocketConnected ? "green-square" : "red-square"}></div>
    </div>
);

export default ConnectionIndicator;
