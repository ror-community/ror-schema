import sys
import validate.validation as vt
import validate.validateror as vs
import validate.utilities as u
def main():
    args = sys.argv[1:]
    if (len(args) == 0):
        u.help()
        exit(0)
    file = args[0]
    schema = args[1] if len(args) > 1 else None
    valid, msg = vs.validate_file(file,schema)
    if valid:
        exit(0)
    else:
        for file, err in msg.items():
            sys.stderr.write(f"\nERROR: {file}: {err}\n")
        exit(1)

if __name__ == "__main__":
    main()
