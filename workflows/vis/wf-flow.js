
function getParsedWorkflow() {
    if (!window.workflowYaml) {
        window.workflowYaml = document.getElementById('wfyaml').innerHTML;
    }
    var wfyaml = window.workflowYaml;
    var doc = jsyaml.safeLoad(wfyaml);
    // TODO deal with errors
    //console.log(doc);
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
                    //
                    // this edge assumes no else-task in the if; we'll
                    // have to handle that case separately.
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
    if (!window.graph) {
        console.log("Parsing YAML to generate graph");
        window.graph = makeGraph();
    }

    txt = [];
    txt.push("start=>start: Start");
    txt.push("end=>end: End");

    for (var node of window.graph.nodes) {
        var nodeStr = `${node.id}=>${node.type}: ${node.label}`;
        if (node.flowstate == 'current') {
            nodeStr = `${nodeStr}|current`;
        }
        txt.push(nodeStr);
    }
    txt.push(`start->${window.graph.nodes[0].id}`);
    for (var edge of window.graph.edges) {
        if (edge.type == 'condition') {
            txt.push(`${edge.from}(${edge.which})->${edge.to}`);
        } else {
            // this is reversed because the edges are actually dependencies.
            txt.push(`${edge.to}->${edge.from}`);
        }
    }
    txt.push(`${window.graph.nodes[window.graph.nodes.length-1].id}->end`);
    //console.log(txt);
    return txt.join("\n");
}

function getCanvasCenterX() {
    var $this = $("#flowchart");
    var width = $this.width();
    var centerX = width / 2;
    return centerX;
}

function draw() {
    $("#flowchart").empty();
    var txt = getFlowchartTxt();
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
        },
        'flowstate' : {
            'current' : {
                'fill' : window.currentTaskColor,
                'font-color' : '#444',
                'font-weight' : 'bold'
            },
        }
    });
}

function highlight() {
  $('pre code').each(function(i, block) {
    hljs.highlightBlock(block);
  });
}

function toggleFlowState(node) {
    if (node.flowstate == 'current') {
        node.flowstate = '';
    } else {
        node.flowstate = 'current';
    }
}

function attachClicks() {
    // find each task elem in the highlighted yaml, and attach a click
    // handler that toggles that task's current state in window.graph.

    $("span.hljs-attr").click(function () {
        var t = $(this).text();
        var mr = t.match("  ([^:]*):");
        if (mr && mr.length == 2) {
            var name = mr[1];
            var isTask = false;
            for (var node of window.graph.nodes) {
                if (node.id === name) {
                    console.log(`toggle flow state for ${name}`);
                    toggleFlowState(node);
                    draw();
                    $(this).toggleClass("current-task");
                    // don't propagate click event
                    return false;
                }
            }
        }
    });

    $("span.hljs-string").click(function () {
        var t = $(this).text();
        console.log(`str text = |${t}|`);
        for (var node of window.graph.nodes) {
            if (node.id === t) {
                console.log(`toggle flow state for ${t}`);
                toggleFlowState(node);
                draw();
                $(this).toggleClass("current-task");
                // don't propagate click event
                return false;
            }
        }
    });
}

function onload() {
    window.currentTaskColor = '#b3feae';//'#c5a7ff';
    draw();
    highlight();
    setTimeout(attachClicks, 100);
}

$(document).ready(function() {
    onload();
});
