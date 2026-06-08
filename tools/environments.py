import json, sys

# Map each upstream environment to a site catalog entry.
# We key by the upstream "image" (runtime image) name because it is unique and
# stable, whereas the upstream "name" field is not: jvm and jvm-jersey both use
# "JVM Environment". The image name also matches the GHCR package name exactly.
image_dict = {
    'jvm-env': 'Java',
    'jvm-jersey-env-25': 'Java (JVM-Jersey)',
    'ruby-env': 'Ruby',
    'rust-env': 'Rust',
    'python-env': 'Python',
    'python-fastapi-env': 'Python (FastAPI)',
    'binary-env': 'Misc',
    'php-env': 'PHP',
    'dotnet20-env': '.NET Core',
    'go-env': 'Go',
    'go-env-1.26': 'Go',
    'dotnet-env': '.NET',
    'dotnet8-env': '.NET 8',
    'perl-env': 'Perl',
    'tensorflow-serving-env': 'TensorFlow',
    'node-env': 'Node.js',
    'node-env-22': 'Node.js',
    'node-env-debian': 'Node.js',
}

def load_environment_json(file_name):
    """Read content from a JSON file and return the content as a string."""
    with open(file_name, 'r') as f:
        # Load the JSON data from the file
        return json.load(f)

def create_env_string(src_envs, dst_envs):
    for dst_env in dst_envs:
        name = dst_env['name']
        data_list = []
        for src_env in src_envs:
            num_envs = len(src_env)
            for i in range(0, num_envs):
                src = src_env[i]
                image = src.get('image')
                if image not in image_dict:
                    print("no site mapping for upstream image", image,
                          "(", src.get('name'), ")")
                    sys.exit(1)
                if image_dict[image] != name:
                    continue
                if 'image' in src and 'builder' in src:
                    data_list.append({
                        "main": src['image'],
                        "builder": src['builder']
                    })
                elif 'image' in src:
                    data_list.append({
                        "main": src['image']
                    })
                elif 'builder' in src:
                    data_list.append({
                        "builder": src['builder']
                    })
                else:
                    print("image and builder not present for", src.get('name'))
                    sys.exit(1)
        dst_env['images'] = data_list

    return dst_envs

def main():
    src_envs = load_environment_json('environments.json')
    dst_envs = load_environment_json('../static/data/environments.json')

    env_json_string = create_env_string(src_envs=src_envs, dst_envs=dst_envs)
    with open('../static/data/environments.json', 'w') as file:
        json.dump(env_json_string, file, indent=4)

if __name__ == "__main__":
    main()
