import { StatisticToString } from "./Consts";

class StatisticsChartData
{
    constructor(maxStep, data, statistic)
    {
        this.chosenStatistic = statistic;
        this.data = {
            labels: this.prepareLabels(maxStep),
            datasets: [{
                label: StatisticToString(statistic),
                data: data,
                fill: true,
                borderColor: 'rgb(0, 221, 255, 1)',
                tension: 0.1
            }],
        };
    }

    prepareLabels(maxStep)
    {
        if(maxStep === null)
        {
            return [];
        }
        let labels = [];
        for(let i = 0; i < maxStep; i++)
        {
            labels.push((i+1).toString());
        }
        return labels;
    }
}

export default StatisticsChartData;