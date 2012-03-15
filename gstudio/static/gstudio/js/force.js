var w = 960,
        h = 700,
        fill = d3.scale.category20();

var vis = d3.select("#chart")
        .append("svg:svg")
        .attr("width", w)
        .attr("height", h);

    vis.append("svg:g").attr("class", "edges");        
    vis.append("svg:g").attr("class", "nodes");


$(function() {
  $.ajax({
    url: '/gstudio/graphs/rgraph',
    //crossDomain: true,
    //dataType: 'jsonp',
    success : function(json) {

      var force; 
      
      var nodes_by_id = _.reduce(json.node_metadata, function(acc, n) {
        acc[n._id] = n;
        return acc;
      }, {});


      var follows_edges = _(json.is_followed_by).chain().map(function(e) {
        e.source = nodes_by_id[e.from];
        e.target = nodes_by_id[e.to];
        e.type = 'follows_edges';
        return e;
      }).filter(function(e){
        return nodes_by_id[e.from] && nodes_by_id[e.to]
      }).value();
      
      var mentions_edges = _(json.is_mentioned_by).chain().map(function(e) {
        e.source = nodes_by_id[e.from];
        e.target = nodes_by_id[e.to];
        e.type = 'mentions_edges';
        return e;
      }).filter(function(e){
        return nodes_by_id[e.from] && nodes_by_id[e.to]
      }).value();
      

      nodes_by_id['189087228'].x = w/2.0;
      nodes_by_id['189087228'].y = h/2.0;
      
      var force = d3.layout.force()
              .linkStrength(0.5)
              .charge(-2000)
              .friction(0.7)
              .linkDistance(50)
              .nodes([])
              .links([])
              .size([w, h])
              .start();

      function update(edges){
        
        _.each(nodes_by_id, function(n){n.added = false});
        
        var nodes = _.reduce(edges, function(acc, e) {
          if(nodes_by_id[e.from] && !nodes_by_id[e.from].added){
            nodes_by_id[e.from].added = true;
            acc.push(nodes_by_id[e.from]);
          }
          if(nodes_by_id[e.to] && !nodes_by_id[e.to].added){
            nodes_by_id[e.to].added = true;
            acc.push(nodes_by_id[e.to]);
          }       
          return acc;
        }, []);
        
        force.nodes(nodes);
        force.links(edges);
        force.start();

        var link = d3.select("#chart g.edges").selectAll("line.link")
                .data(edges, function(e){return e.from + "-" + e.to + "-" + e.type});
                
                link.enter().append("svg:line")
                .attr("class", "link")
                .style("stroke-width", function(d) {
                  return Math.sqrt(d.value);
                })
                .attr("x1", function(d) {
                  return d.source.x;
                })
                .attr("y1", function(d) {
                  return d.source.y;
                })
                .attr("x2", function(d) {
                  return d.target.x;
                })
                .attr("y2", function(d) {
                  return d.target.y;
                });
                
                link.exit().remove();

        var node = d3.select("#chart g.nodes").selectAll("g.node").data(nodes);              
                
                var new_g = node.enter().append("svg:g")
                  .attr("class", "node")
                  .call(force.drag);
                
                new_g.append("svg:image").attr('xlink:href',
                        function(d) {
                          return d.profile_image_url;
                        }).attr('height', 32).attr('width', 32);
                        
                new_g.append("svg:text")
                        .attr("dy", 46)
                        .attr("text-anchor", "middle")
                        .text(function(d) {
                          return d.screen_name;
                        });        
                
                node.exit().remove();
        

        force.on("tick", function() {

          var x_center = $("#chart").width() / 2;
          var y_center = $("#chart").height() / 2;

          link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

          node.attr("transform", function(d) { return "translate(" + (d.x-16) + "," + (d.y-16) + ")"; });

        });
      }
      
      update(follows_edges);
      vis.style("opacity", 1e-6)
              .transition()
              .duration(1000)
              .style("opacity", 1);
      
      $('input#follows').change(function(){
        update(follows_edges);
      });
      
      $('input#mentions').change(function(){
        update(mentions_edges);
      });
    }
  });
  
  $("#relation_type").buttonset();
  
  $('input#mentions').change(function(){console.log(this)});
  $('input#hashtags').change(function(){console.log(this)});
  
});
