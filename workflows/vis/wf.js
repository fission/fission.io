var nodes = null;
var edges = null;
var network = null;

function destroy() {
    if (network !== null) {
        network.destroy();
        network = null;
    }
}

function getParsedWorkflow() {
    var wfyaml = document.getElementById('wf').value;
    var doc = jsyaml.load(wfyaml);
    return doc;
}

function makeGraph() {
    var taskIds={};
    var nodes=[];
    var edges=[];

    var doc = getParsedWorkflow();
    var tasks = doc.tasks;
    for (var taskName in tasks) {
        nodes.push({
            id: taskName,
            label: taskName
        });
        if (tasks[taskName].requires) {
            for (var dep of tasks[taskName].requires) {
                edges.push({
                    from: taskName,
                    to: dep,
                    id: `${taskName}--${dep}`
                });
            }
        }
    }    
    return {nodes: nodes, edges: edges}
}

function draw() {
    destroy();

    nodes = [
        {
            id: 0,
            label: "FetchWeather"
        },
        {
            id: 1,
            label: "ToCelsius"
        },
        {
            id: 2,
            label: "CheckTemperatureThreshold"
        },
        {
            id: 3,
            label: "SendSlackMessage"
        },
        {
            id: 4,
            label: "SomethingElse"
        }
    ];
    dependencyEdges = [
        {
            from: 1,
            to: 0,
            id: "10"
        },
        {
            from: 2,
            to: 1,
            id: "21"
        },
        {
            from: 3,
            to: 2,
            id: "32"
        },
        {
            from: 4,
            to: 1,
            id: "41"
        },
        {
            from: 3,
            to: 4,
            id: "34"
        },
    ];
    //data = {nodes: nodes, edges: dependencyEdges};
    data = makeGraph();
    console.log(data);
    
    // create a network
    var container = document.getElementById('mynetwork');
    var options = {
        layout: {
            hierarchical: {
                direction: "DU",
                sortMethod: "directed"
            }
        },
        nodes: {
            shape: 'box',
            margin: 10,
            font: { //'20px Lato black',
                color: '#000',
                size: 18, // px
                face: 'Open Sans'
            },
            shapeProperties: {
                borderRadius: 4
            },
            color: {
                border: '#000',
                background: '#EEE',
                highlight: {
                    border: '#000',
                    background: '#AAAAFF'
                },
                hover: {
                    border: '#000',
                    background: '#D2E5FF'
                }
            }            
        },
        edges: {
            arrows: 'from',
            color: "#555"
        }
    };
    network = new vis.Network(container, data, options);

    // add event listeners
    network.on('select', function (params) {
        document.getElementById('selection').innerHTML = 'Selection: ' + params.nodes;
    });
}
