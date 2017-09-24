
function getParsedWorkflow() {
    var wfyaml = document.getElementById('wfyaml').innerHTML;
    var doc = jsyaml.safeLoad(wfyaml);
    // TODO deal with errors
    console.log(doc);
    return doc;
}

function makeGraph() {
    var taskIds={};
    var nodes=[];
    var edges=[];

    var doc = getParsedWorkflow();
    var tasks = doc.tasks;
    for (var taskName in tasks) {
        var t = tasks[taskName];
        var type = "operation";
        console.log(t);

        if (t.run == "if") {
            type = "condition";
            var newNodeId = t.inputs.then.run;
            nodes.push({
                id: newNodeId,
                label: t.inputs.then.run,
                type: 'operation'
            });
            edges.push({
                id: `${taskName}--${newNodeId}--yes`,
                type: 'condition',
                which: 'yes', // then=yes, else=no
                from: taskName, // the if statement
                to: newNodeId,
            });
        }
        
        nodes.push({
            id: taskName,
            label: taskName,
            task: tasks[taskName],
            type: type
        });
        
        if (tasks[taskName].requires) {
            for (var dep of tasks[taskName].requires) {
                if (tasks[dep].run == "if") {
                    // if the task we depend on is an if-then
                    // statement, add two edges instead of one (for
                    // the then-branch and else branch).
                    edges.push({
                        id: `${dep}--${taskName}--no`,
                        type: "condition",
                        which: "no",
                        from: dep,
                        to: taskName
                    });
                    var thenNodeId = tasks[dep].inputs.then.run;
                    edges.push({
                        from: taskName,
                        to: thenNodeId,
                        type: "dependency",
                        id: `${taskName}--${thenNodeId}`,
                    });
                } else {
                    edges.push({
                        from: taskName,
                        to: dep,
                        id: `${taskName}--${dep}`,
                        type: "dependency"
                    });
                }
            }
        }
    }    
    return {nodes: nodes, edges: edges}
}

function getFlowchartTxt() {
    g = makeGraph();
   
    txt = [];
    txt.push("start=>start: Start");
    txt.push("end=>end: End");
    
    for (var node of g.nodes) {
        txt.push(`${node.id}=>${node.type}: ${node.label}`);
    }
    txt.push(`start->${g.nodes[0].id}`);
    for (var edge of g.edges) {
        if (edge.type == 'condition') {
            txt.push(`${edge.from}(${edge.which})->${edge.to}`);
        } else {
            // this is reversed because the edges are actually dependencies.
            txt.push(`${edge.to}->${edge.from}`);
        }
    }
    txt.push(`${g.nodes[g.nodes.length-1].id}->end`);
    console.log(txt);
    return txt.join("\n");
}

function getCanvasCenterX() {
    var $this = $("#flowchart");
    var width = $this.width();
    var centerX = width / 2;
    return centerX;
}

function draw() {
    var txt = getFlowchartTxt();
    console.log(txt);
    var diagram = flowchart.parse(txt);
    var scale=1.2;
    diagram.drawSVG('flowchart', {
        'x': 100,
        'y': 0,
        'line-width': 1.5,
        'line-length': 40,
        'text-margin': 10,
        'font-size': 14,
        'font-color': '#444',
        'line-color': '#444',
        'element-color': '#444',
        'fill': 'white',
        'yes-text': 'yes',
        'no-text': 'no',
        'arrow-end': 'block',
        'scale': scale,

        'symbols': {
            'start': {
                'font-color': '#444',
                'element-color': '#444',
                'fill': '#fff'
            },
            'end':{
                'class': 'end-element'
            }
        }
    });
}

function highlight() {
  $('pre code').each(function(i, block) {
    hljs.highlightBlock(block);
  });
}

function onload() {
    draw();
    highlight();
}

$(document).ready(function() {
    onload();
});

