var nodes = null;
var edges = null;
var network = null;

function destroy() {
    if (network !== null) {
        network.destroy();
        network = null;
    }
}

function setUrl(wfyaml) {
    currentLoc = window.location.href.split("#")[0];
    newData = btoa(wfyaml);
    window.location.href = currentLoc + "#" + newData;
}

function getFromUrl() {
    newData = window.location.href.split("#")[1];
    return atob(newData);
}

function getParsedWorkflow() {
    var wfyaml = document.getElementById('wf').value;

    // set url
    setUrl(wfyaml);
    
    var doc = jsyaml.safeLoad(wfyaml);
    // TODO deal with errors
    return doc;
}

function onload() {
    if (document.getElementById('wf').value.length == 0) {
        newYaml = getFromUrl();
        document.getElementById('wf').value = newYaml;
    }
    draw();
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

    // get graph from yaml file
    data = makeGraph();
    
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
            color: "#555",
        },
        physics: {
            hierarchicalRepulsion: {
                centralGravity: 0,
                nodeDistance: 200
            },
            minVelocity: 0.75,
            solver: "hierarchicalRepulsion"
        }
// configure lets us interactively mess with all these options
//        configure: { 
//            enabled: true,
//            showButton: true
//        }
    };
    network = new vis.Network(container, data, options);

    // add event listeners
    network.on('select', function (params) {
        document.getElementById('selection').innerHTML = 'Selection: ' + params.nodes;
    });
}
