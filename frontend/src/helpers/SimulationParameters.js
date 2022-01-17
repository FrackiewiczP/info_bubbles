import { CommunicationMode, FriendsLinksTypes, UsersCommunicationMode } from "./Consts";

class SimulationParameters{
    constructor(
        number_of_agents=100,
        number_of_steps=100,
        number_of_links=10,
        mem_capacity=10,
        friend_lose_prob=0.1,
        communication_form=CommunicationMode.INDIVIDUAL,
        inter_user_communication_form=UsersCommunicationMode.TO_ONE_RANDOM,
        initial_connections=FriendsLinksTypes.RANDOM_NON_DIRECTED,
        acc_latitude=0.1,
        acc_sharpness=20,
        percent_of_the_same_group=80,
        no_of_groups=4
    ){
        this.number_of_agents=number_of_agents;
        this.number_of_steps=number_of_steps;
        this.number_of_links=number_of_links;
        this.mem_capacity=mem_capacity;
        this.friend_lose_prob=friend_lose_prob;
        this.communication_form=communication_form;
        this.inter_user_communication_form=inter_user_communication_form;
        this.initial_connections=initial_connections;
        this.acc_latitude=acc_latitude;
        this.acc_sharpness=acc_sharpness;
        this.percent_of_the_same_group=percent_of_the_same_group;
        this.no_of_groups=no_of_groups;
    }

    parseValues(){
        this.number_of_agents = parseInt(this.number_of_agents);
        this.number_of_steps = parseInt(this.number_of_steps);
        this.number_of_links = parseInt(this.number_of_links);
        this.mem_capacity = parseInt(this.mem_capacity);
        this.friend_lose_prob = parseFloat(this.friend_lose_prob);
        this.acc_latitude = parseFloat(this.acc_latitude);
        this.acc_sharpness = parseFloat(this.acc_sharpness);
        this.percent_of_the_same_group=parseFloat(this.percent_of_the_same_group);
        this.no_of_groups=parseInt(this.no_of_groups);
    }
}

const ParametersNames={
    NUMBER_OF_AGENTS: 'number_of_agents',
    NUMBER_OF_STEPS: 'number_of_steps',
    NUMBER_OF_LINKS: 'number_of_links',
    MEM_CAPACITY: 'mem_capacity',
    FRIEND_LOSE_PROB: 'friend_lose_prob',
    COMMUNICATION_FORM: 'communication_form',
    INTER_USER_COMMUNICATION_FORM: 'inter_user_communication_form',
    ACC_LATITUDE: 'acc_latitude',
    ACC_SHARPNESS: 'acc_sharpness',
    PERCENT_OF_THE_SAME_GROUP: 'percent_of_the_same_group',
    NO_OF_GROUPS: 'no_of_groups',
    INITIAL_CONNECTIONS: 'initial_connections',
}

const ConvertingFunctions={
    number_of_agents: x => parseInt(x),
    number_of_steps: x => parseInt(x),
    number_of_links: x => parseInt(x),
    mem_capacity: x => parseInt(x),
    friend_lose_prob: x => parseFloat(x),
    communication_form: x => x,
    inter_user_communication_form: x => x,
    initial_connections: x => x,
    acc_latitude: x => parseFloat(x),
    acc_sharpness: x => parseFloat(x),
    percent_of_the_same_group: x => parseFloat(x),
    no_of_groups: x => parseInt(x),
}

export default SimulationParameters;
export {ParametersNames, ConvertingFunctions};
