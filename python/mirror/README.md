# Mirror

**Creates an exact copy of the directory specified in (source) to the directory specified in (mirror).**

**Warning**: The file synchronization flow is (source) -> (mirror). Any content (files and folders) in the (mirror) directory that is not present in the (source) will be deleted to maintain an exact copy of the (source) directory. Swapping the directories in the --source and --mirror arguments may result in file loss.