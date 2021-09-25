#!/usr/bin/env bash

# Global variables
CURRENT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BASE_DIR="$(dirname "$CURRENT_DIR")"


# Read .env file and get the variables
function env_up {
    if [ -f "$BASE_DIR/.env" ]; then
        set -a
        source "$BASE_DIR/.env"
        set +a
    else
        printf "ERROR: .env file not found in project root \n"
        return 2
    fi
}

function rmi {
    docker rmi -f ${DOCKER_IMAGE}
}

function prune {
    docker image prune -f
}

function build {
    cd "$BASE_DIR"

    docker build --rm --tag ${DOCKER_IMAGE} --file docker/Dockerfile .    
}

function build-stage {
    case "$2" in
    test|lint)
        printf "Building ${DOCKER_IMAGE}:$2 image... \n"
        cd "$BASE_DIR"
        docker build --rm --tag ${DOCKER_IMAGE}:"$2" --file docker/Dockerfile --target "$2" .
        ;;
    *)
        printf "Wrong argument for building. \n"
        printf "Usage: \n"
        printf "build-stage [test|lint] \n"
        exit 1
        ;;
    esac
}

function run {
    docker run -it ${DOCKER_IMAGE}:latest bash
}

function lint {
    black --config "${BASE_DIR}/pyproject.toml" "${BASE_DIR}"
    isort --settings-path "${BASE_DIR}/pyproject.toml" "${BASE_DIR}"
}

function test {
    coverage run --rcfile "${BASE_DIR}/pyproject.toml" -m pytest "${BASE_DIR}/tests" "$*"
    coverage html --rcfile "${BASE_DIR}/pyproject.toml"
    coverage report --fail-under 95
}

function lsc {
    docker ps --last=10 --format="table {{.ID}}\\t{{.Image}}\\t{{.Status}}\\t{{.Names}}"
}

function lsi {
    docker images
}

function help {
    printf "Available commands: \n build \n build-stage \n run \n rm \n rmi \n lsc \n lsi \n test \n lint \n prune \n help \n"
}

function main () {
    env_up 
    case "$1" in
        build)
            build
            ;;
        build-stage)
            build-stage "$@"
            ;;
        run)
            run
            ;;
        rm)
            rm
            ;;
        rmi)
            rmi
            ;;
        lsc)
            lsc
            ;;
        lsi)
            lsi
            ;;
        test)
            test
            ;;
        lint)
            lint
            ;;
        prune)
            prune
            ;;
        help)
            help
            ;;    
        *)
            printf "ERROR: Missing command. \n"
            help
            exit 1
            ;;
    esac
}

main "$@"
