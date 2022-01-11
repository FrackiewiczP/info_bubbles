import React from 'react';
import '../styles/Simulation.scss'
import 'animate.css';
import '../styles/Statistics.scss'
import {Line} from "react-chartjs-2";
import {StatisticsNames} from '../helpers/Consts';
// These have to be imported for the chart to show correctly
// eslint-disable-next-line
import { Chart as ChartJS } from 'chart.js/auto'
// eslint-disable-next-line
import { Chart }            from 'react-chartjs-2'

class Statistics extends React.Component{
    render(){
        return (
            <div className="Statistics">
            <select onChange={this.props.handleChangeShownStatistic}>
                <option value="" selected={this.props.statisticsChartData.chosenStatistic === null} disabled hidden>Wybierz statystykę</option>
                <option value={StatisticsNames.FLUCTUATION} selected={this.props.statisticsChartData.chosenStatisti === StatisticsNames.FLUCTUATION}>Fluktuacja</option>
                <option value={StatisticsNames.AVG_FRIEND_DIST} selected={this.props.statisticsChartData.chosenStatisti === StatisticsNames.AVG_FRIEND_DIST}>Średnia odległość do przyjaciół</option>
                <option value={StatisticsNames.AVG_INFO_DIST} selected={this.props.statisticsChartData.chosenStatisti === StatisticsNames.AVG_INFO_DIST}>Średnia odległość do informacji</option>
            </select>
            <div className="Line">
                <Line data={this.props.statisticsChartData.data}/>
            </div>
            <button onClick={this.props.handleSeeSimulationButton}>
                Widok Symulacji
            </button>
            </div>
        );
    }
}


export default Statistics;
