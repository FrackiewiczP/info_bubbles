const CommunicationMode={
    INDIVIDUAL: "individual",
    CENTRAL: "central",
}

const UsersCommunicationMode={
    TO_ONE_RANDOM: "to_one_random",
    TO_ALL: "to_all",
}

const MainViewState={
    SIMULATION_VIEW: 1,
    CHOOSING_PARAMETERS: 2,
    CHARTS_VIEW: 3,
}

const StatisticsNames={
    FLUCTUATION: 1,
    AVG_FRIEND_DIST: 2,
    AVG_INFO_DIST: 3,
}

function StatisticToString(statistic){
    switch (statistic){
        case StatisticsNames.FLUCTUATION:
            return "Fluktuacja";
        case StatisticsNames.AVG_FRIEND_DIST:
            return "Średnia odległość do przyjaciół";
        case StatisticsNames.AVG_INFO_DIST:
            return "Średnia odległość do informacji";
        default:
            return "";
    }
}

export {CommunicationMode, UsersCommunicationMode, MainViewState, StatisticsNames, StatisticToString};
