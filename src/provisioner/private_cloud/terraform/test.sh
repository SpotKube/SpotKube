# Set the provisioner log file path
LOG_FILE="test.log"


# Redirect stdout to the log file
# exec 3>&1 1> >(tee -a "${LOG_FILE}" >&3) 2>&1
# exec 3>&1 1> >(sed -E "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g" >> "${LOG_FILE}") 2>&1
# Redirect stdout to the log file and remove color codes
# exec 3>&1 1> >(tee >(sed -E "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g" >&3) "${LOG_FILE}") 2>&1
exec 3>&1 1> >(tee >(sed 's/\x1B\[[0-9;]*[JKmsu]//g' >>"${LOG_FILE}") >&3) 2>&1
# exec 3>&1 1> >(sed -E "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g" | tee "${LOG_FILE}" >&3) 2>&1





# Set the trap to log the date and time of each command
trap "date -Is" DEBUG

echo
# print_title "Provisioning private cloud environment"

terraform plan