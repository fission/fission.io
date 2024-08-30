import json, sys

env_dict = {
    'JVM Environment': 'Java',
    'JVM Jersey Environment': 'Java (JVM-Jersey)',
    'Ruby Environment': 'Ruby',
    'Python Environment': 'Python',
    'Fission Binary Environment': 'Misc',
    'PHP Environment': 'PHP',
    'Dotnet 2 Environment': '.NET Core',
    'Go Environment': 'Go',
    'Dotnet Environment': '.NET',
    'Perl Environment': 'Perl',
    'Tensorflow Serving Environment': 'TensorFlow',
    'Nodejs Environment': 'Node.js',
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
                if name == env_dict[src_env[i]['name']]:
                    print(name)
                    if 'image' in src_env[i] and 'builder' in src_env[i]:
                        data_list.append({
                            "main": src_env[i]['image'],
                            "builder": src_env[i]['builder']
                        })
                    elif 'image' in src_env[i]:
                        data_list.append({
                            "main": src_env[i]['image']
                        })
                    elif 'builder' in src_env[i]:
                        data_list.append({
                            "builder": src_env[i]['builder']
                        })
                    else:
                        print("image and builder not present for", src_env[i]['name'])
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