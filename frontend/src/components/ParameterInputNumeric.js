import React from 'react';
import '../styles/ParameterInputNumeric.scss'

const ParameterInputNumeric = (props) => (
    <div className="ParameterInputNumeric">
        <div className="label">{props.label}</div>
        <input type="number" value={props.value} onChange={props.handleOnChange}></input>
    </div>
)


export default ParameterInputNumeric;
