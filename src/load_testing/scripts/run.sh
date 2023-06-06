#!/bin/bash

# set -e 

# Import common functions
source ../../scripts/common.sh
# Import configs
source ../../../.config/load_test.conf

# Path to the scripts directory
scripts_path=$(pwd)
# Path to the load_testing directory
load_testing_path=$(dirname $scripts_path)

SERVICE_NAME=""
ROOT_DIR=""
HOST_URL=""
NUMBER_OF_USERS=0
SPAWN_RATE=0
RUN_TIME=0
GRAFANA_HOST="http://192.168.49.2:30468"
GRAFANA_API_KEY="eyJrIjoiRFNOQmpobzZTbG1qWDZCMjNJb2xGNHBDM01FUXNHSU8iLCJuIjoiU3BvdGt1YmUyIiwiaWQiOjF9"

function help() {
    print_info "Usage:"
    echo "  -sn, --service_name <service_name>  Name of the service to run locust for"
    echo "  -d, --root_dir <root_dir>           Root directory of the project"
    echo "  -h, --host <host_url>               Host URL"
    echo "  -r, --spawn_rate <spawn_rate>       Spawn rate"
    echo "  -u, --users <number_of_users>       Number of users"
    echo "  -t, --time <run_time>               Running time ex: 10s, 1m"
}

print_title "Load Testing"

# Validate number of arguments
if [ $# -lt 12 ]
then
    print_error "Invalid number of arguments."
    help
    exit
fi

while [ ! -z $1 ]; do
    case "$1" in
        -sn|--service_name)
            if [[ -z $2 ]];	then
				print_error "Service name is not specified"
				exit 1
            fi
            SERVICE_NAME=$2
            shift 2
            ;;
        -d|--root_dir)
            if [[ -z $2 ]];	then
				print_error "Root directory is not specified"
				exit 1
            fi
            ROOT_DIR=$2
            shift 2
            ;;
        -h|--host)
            if [[ -z $2 ]];	then
				print_error "Host is not specified"
				exit 1
            fi
            HOST_URL=$2
            shift 2
            ;;
        -r|--spawn_rate)
            if [[ -z $2 ]];	then
				print_error "Spawn rate is not specified"
				exit 1
            fi
            SPAWN_RATE=$2
            shift 2
            ;;
        -u|--users)
            if [[ -z $2 ]];	then
				print_error "User count is not specified"
				exit 1
            fi
            NUMBER_OF_USERS=$2
            shift 2
            ;;
        -t|--time)
            if [[ -z $2 ]];	then
				print_error "Time is not specified"
				exit 1
            fi
            RUN_TIME=$2
            shift 2
            ;;
        *)
            print_error "Invalid argument: $1"
            exit
            ;;
    esac
done

# Check if locust is installed
if ! command -v locust &> /dev/null
then
    print_error "Locust is not installed. Please install it first."
    exit
fi

# Jump to load_testing directory
pushd $ROOT_DIR/src/$SERVICE_NAME/load_testing

print_info "Running locust for $SERVICE_NAME"

start_time=$(date +%s%3N)
# Run locust
locust -f test.py --csv=results --host $HOST_URL --users $NUMBER_OF_USERS --spawn-rate $SPAWN_RATE --run-time $RUN_TIME --headless

print_info "Moving results to outputs directory"
mv ./results* $load_testing_path/outputs/

print_info "Sleep for 1 min"
sleep 60
end_time=$(date +%s%3N)

popd

print_success "Locust run completed. Start time: $start_time, End time: $end_time"

# Collect metrics from Grafana
python3 ../packages/fetch_metrics.py $SERVICE_NAME $GRAFANA_HOST $NUMBER_OF_USERS $SPAWN_RATE $start_time $end_time $GRAFANA_API_KEY 