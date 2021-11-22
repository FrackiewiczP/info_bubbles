import React from 'react';
import '../styles/ParameterInputRadio.scss'

const ParameterInputRadio= (props) => (
    <div className="ParameterInputRadio">
        <div class="group-label">
            {props.groupName}
        </div>
        <div class="border">
            {props.values.map((value, index) => {
                return(
                    <div class="single-option" key={index}>
                        <div class="label">{value.label}</div>
                        <input type="radio" name={props.name} value={value.value} onChange={props.handleOnChange}/>
                    </div>
                );
            })}
        </div>

    </div>
)


export default ParameterInputRadio;