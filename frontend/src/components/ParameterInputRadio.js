import React from 'react';
import '../styles/ParameterInputRadio.scss'

const ParameterInputRadio= (props) => (
    <div className="ParameterInputRadio">
        <div className="group-label">
            {props.groupName}
        </div>
        <div className="border">
            {props.options.map((value, index) => {
                return(
                    <div class="single-option" key={index}>
                        <div class="label">{value.label}</div>
                        <input type="radio" name={props.name} value={value.value} onChange={props.handleOnChange} checked={value.value === props.value}/>
                    </div>
                );
            })}
        </div>

    </div>
)


export default ParameterInputRadio;
