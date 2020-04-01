
// import { select, layout, event } from "d3"; 

// var feelings = [':laughing:', ':innocent:',':relaxed:', ':yum:', ':relieved:', ':heart_eyes:', ':kissing_heart:', ':kissing:', ':kissing_smiling_eyes:', ':kissing_closed_eyes:', ':stuck_out_tongue_winking_eye:', ':stuck_out_tongue_closed_eyes:', ':stuck_out_tongue:', ':money_mouth:', ':nerd:', ':sunglasses:', ':hugging:', ':smirk:', ':no_mouth:', ':neutral_face:', ':expressionless:', ':unamused:', ':rolling_eyes:', ':thinking:', ':flushed:', ':disappointed:', ':worried:', ':angry:', ':rage:', ':pensive:', ':confused:', ':slight_frown:', ':frowning2:', ':persevere:', ':confounded:', ':tired_face:', ':weary:', ':triumph:', ':open_mouth:', ':scream:', ':fearful:', ':cold_sweat:', ':hushed:', ':frowning:'];
// feelings.reverse();

// var width = 500;
// var height = 500;

// var nodes = [];
// var links = [];

// var svg = select("svg")
//     .attr("width", width)
//     .attr("height", height);

// var node = svg.selectAll(".node");

// var force = layout.force()
//     .nodes(nodes)
//     .links(links)
//     .size([width, height])
//     .on("tick", tick)
//     .linkStrength(0.1)
//     .friction(0.9)
//     .linkDistance(40)
//     .charge(-60)
//     .gravity(0.1)
//     .theta(0.8)
//     .alpha(0.1);


// function start() {
//     node = node.data(force.nodes(), function(d) {
//         return d.index;
//     });
//     node.enter()
//         .append("svg:image")
//         .attr("xlink:href", function (d) {
//           return d.imageUrl;
//         })
//         .attr("class", function(d) {
//             return "node";
//         })
//         .attr("width", 36)
//         .attr("height", 36)
      
//     node.exit().remove();

//     node.call(force.drag)
//         .on("mousedown", function() {
//             event.stopPropagation();
//         });

//     force.start();
// }

// function tick() {
//     node.attr("x", function(d) {
//             return d.x;
//         })
//         .attr("y", function(d) {
//             return d.y;
//         });
// }

// function getInitialPosition() {
//   var position = {};
//   var dir = Math.floor(Math.random() * 4);
//   if (dir === 1) {
//     position.x = Math.random() * width;
//     position.y = 0;
//   } else if (dir === 2) {
//     position.x = Math.random() * width;
//     position.y = height;
//   } else if (dir === 3) {
//     position.x = 0;
//     position.y = Math.random() * height;
//   } else if (dir === 4) {
//     position.x = width;
//     position.y = Math.random() * height;
//   }
//   return position;
// }

// var delay = 1000;
// function addPerson() {
//     var feeling = feelings.pop();
    
//     var position = getInitialPosition();
//     feeling.x = position.x;
//     feeling.y = position.y;
  
//     nodes.push(feeling);

//     start();
  
//     if (feelings.length > 0) {
//       setTimeout(function () {
//         addPerson();
//       }, delay);
//       if (delay > 100) {
//         delay -= 100;
//       }
//     }
// }

// addPerson();
