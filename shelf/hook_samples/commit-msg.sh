 #!/bin/sh
 
 python3 -m shelf.cli --msg-filename "$1" run-hook
 exit_code=$?
 exit $exit_code