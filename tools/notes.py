def read_file(file_name):
    """Read content from a file and return the content as a string."""
    with open(file_name, 'r') as f:
        return f.read()

def format_commit_and_pull_link(line):
    """Format the commit and pull link based on the provided line."""
    cols = line.split(' ')
    if len(cols) > 2:
        # Format commit link
        cols[1] = "[{0}](https://github.com/fission/fission/commit/{0})".format(cols[1])

        # Extract pull number, format and replace in the column
        pull_number = cols[-1].strip('()')
        formatted_pull_link = "[{0}](https://github.com/fission/fission/pull/{1})".format(pull_number, pull_number.replace('#', ''))
        cols[-1] = formatted_pull_link

        return ' '.join(cols)
    return line

def main():
    data = read_file('notes.txt')
    lines = data.split('\n')

    for line in lines:
        formatted_line = format_commit_and_pull_link(line)
        print(formatted_line)

if __name__ == "__main__":
    main()
