#!/bin/bash

usage="$(basename "$0") [-t] [-u] [-p='part1'] -- Program to run tests and/or update the TMC Module for exercises
Script goes through only following exercise structure:
osa1/01_hymio
osa1/02_ei_hymio
...
osa3/01_input_file
osa3/18_last_exercise
Where:
    -t          Runs tests for exercises
    -u          Updates TMC Module from tmc-python-tester repository
    -p='part1'  Applies only to given folder"


# Manually ignored folders if needed
ignored_dirs=("tmc-python-tester" ".vscode" "osax")
ignored_subdirs=("")

TEST=false
UPDATE=false
PART=""

for i in "$@"; do
    case $i in
        -t|--test)
            TEST=true
            shift
            ;;
        -u|--update)
            UPDATE=true
            shift
            ;;
        -p=*|--part=*)
            PART="${i#*=}"
            shift
            ;;
        *)
            echo "$usage" >&2
            exit 1
            ;;
    esac
done

if [[ "$UPDATE" = true ]]; then
    git clone https://github.com/testmycode/tmc-python-tester.git
fi

for dir in *; do
    # Only process directories
    if [ ! -d "${dir}" ]; then
        continue
    fi

    # Skip ignored directories
    skip_dir=false
    for ignored_dir in "${ignored_dirs[@]}"
    do
        if [[ $ignored_dir =~ $dir ]]; then
            skip_dir=true
            break
        fi
    done
    if $skip_dir; then
        continue
    fi

    # Filter by part argument, if given
    if [[ "$PART" != "" && "$PART" != "$dir" ]]; then
        continue
    fi

    # Go to part/osa folder
    cd "${dir}" || exit

    for subdir in *; do
        # Only process directories
        if [ ! -d "${subdir}" ]; then
            continue
        fi

        # Skip ignored subdirectories
        skip_subdir=false
        for ignored_subdir in "${ignored_subdirs[@]}"
        do
            if [[ $ignored_subdir =~ $subdir ]]; then
                skip_subdir=true
            fi
        done
        if $skip_subdir; then
            continue
        fi

        # Go to exercise folder under part
        cd "${subdir}" || exit

        if find . | grep -q ".tmcignore"; then
            echo "Skipped update for ${dir}/${subdir} due to .tmcignore file."
            # Leave exercise folder
            cd ..
            continue
        fi

        if [[ "$UPDATE" = true ]]; then
            echo "Updating TMC Module for ${dir}/${subdir}."
            rm -rf tmc/
            cp -r ../../tmc-python-tester/tmc/ tmc/
        fi

        if [[ "$TEST" = true ]]; then

            output=$( (python -m tmc) 2>&1 )

            skipped=false
            while [[ "$output" =~ "FAIL" || "$output" =~ "ERROR" ]]; do

                    python -m tmc
                    echo ""
                    echo "Some test failed after update for ${dir}/${subdir}, please fix failed tests."
                    read -n 1 -r -p "Press (s) to skip or any key to continue... " key
                    if [[ "$key" == "s" || "$key" == "S" ]]; then
                        skipped=true
                        git restore "tmc/."
                        echo ""
                        break
                    fi
                    output=$( (python -m tmc) 2>&1 )

            done

            if [[ "$skipped" = false ]]; then
                echo "All tests passed for ${dir}/${subdir}."
            fi
        fi

        # Go away from exercise folder
        cd ..
    done

    # Away from part/osa folder
    cd ..
done

if [[ "$UPDATE" = true ]]; then
    echo "Removing cloned tmc-python-tester repo."
    rm -rf tmc-python-tester
fi
