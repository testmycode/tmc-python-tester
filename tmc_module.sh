#!/bin/bash

usage="$(basename "$0") [-t] [-u] [-p='part1'] -- Program to run tests and/or update the TMC Module for exercises

Script goes through only following exercise structure:

osa1/01_hymio
osa1/02_ei_hymio
...
osa3/01_input_file
osa3/18_last_exercise

Where:
    -t  		Runs tests for exercises
    -u  		Updates TMC Module from tmc-python-tester repository
	-p='part1' 	Applies only to given folder"
	

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

    if [[ -d "${dir}" ]] && [[ ! "${ignored_dirs[@]}" =~ "${dir}" ]]; then
			
		if [[ "$PART" = "" || "$PART" = "$dir" ]]; then
			cd ${dir} # Go to part/osa folder
		else
			continue 
		fi
		
        for subdir in *; do
		
            if [[ -d "${subdir}" ]]; then
				if [[ ! "${ignored_subdirs[@]}" =~ "${subdir}" ]]; then
				
					cd ${subdir} # Go to exercise folder under part
					
					if [[ $(ls -la | grep ".tmcignore") ]]; then
						echo "Skipped update for ${dir}/${subdir} due to .tmcignore file."
						cd ..
						continue
					fi

					if [[ "$UPDATE" = true ]]; then
						echo "Updating TMC Module for ${dir}/${subdir}."
						rm -rf tmc/
						cp -r ../../tmc-python-tester/tmc/ tmc/
					fi

					if [[ "$TEST" = true ]]; then
						output=$((python -m tmc) 2>&1)

						if [[ $output == *"FAIL"* ]]; then
							echo "Some test failed after update for ${dir}/${subdir}, please fix failed tests or add to ignored_subdirs and run again."
							python -m tmc
							git restore "tmc/."
							break
						elif [[ $output == *"ERROR"* ]]; then
							echo "Some test errored after update for ${dir}/${subdir}, please fix errors or add to ignored_subdirs and run again."
							python -m tmc
							git restore "tmc/."
							break
						fi
						
						echo "All tests passed for ${dir}/${subdir}."
					fi
					
					cd .. # Go away from exercise folder
					
				else
					echo "Skipped update for ${dir}/${subdir}."
				fi
            fi
			
        done
		
        cd .. # Away from part/osa folder
		
    fi

done

if [[ "$UPDATE" = true ]]; then
	rm -rf tmc-python-tester
fi
