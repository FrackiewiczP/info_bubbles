import React from 'react';
import '../styles/Simulation.scss'
import 'animate.css';

class Statistics extends React.Component{
    render(){
            return (
                <div className="Statistics animate__animated animate__fadeInLeft">
                    <button onClick={this.props.handleSeeSimulationButton}>Widok symulacji</button>
                </div>
            );
    }
}


export default Statistics;
