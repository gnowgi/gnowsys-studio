'use strict';

/*
    jQuery plugin to embed video from a pan.do/ra instance
    Usage:
        html:
            <div id="video" data-pandora-id="AA"></div>
        js:
            $('#video').pandoravideo();

    Options can be passed as data- attributes in the html or in an options object - read code for docs
*/

(function($) {
    $.fn.pandoravideo = function(options) {

        //get options, giving preference, in order, to data- attributes defined on the html element, options passed when instantiatiing $(element).pandoravideo(options), defaults.
        var options = options || {},
            namespace = options.namespace || "pandora",
            
            optionTypes = {
                'strings': ['api', 'base', 'resolution', 'action', 'id'],
                'integers': ['width', 'interval'],
                'floats': ['in', 'out'],
                'arrays':  ['layers', 'keys'],
                'booleans': []
                //'functions': ['callback'] FIXME: lets not.
            };

     
        return this.each(function() {   
             
            var $this = $(this),
                dataOptions = $.extend(options, $this.getDataOptions(optionTypes, namespace)),
                opts = $.extend({
                    'id': 'ABC', //FIXME: throw an error if id is undefined at this point
                    'layers': ['transcripts', 'descriptions', 'keywords', 'places'],
                    'keys': ['layers'], //data keys to fetch from API call. FIXME: add more apt keys
                    'api': "http://wetube.gnowledge.org/api/", //pandora instance api end-point - see http://pad.ma/api
                    'in': 0, //in point (float, in seconds) of clip
                    'out': 0, //out point of clip
                    'pandora_base': 'wetube.gnowledge.org/', //pandora instance from where to fetch video and image data
                    'resolution': '480p', //resolution of video (96p, 240p, or 480p)
                    'width': '640', //display (css) width
                    'interval': 300, //interval (in ms) to run updatePlayer polling loop
                    'action': 'get', //action POST param to send to url
                    'callback': function() { $.noop(); } //function to call after done instantiating pandoraVideo object, called with the object.
                }, dataOptions),
                id = opts.id,
                $loading = $('<div />').addClass("pandoraLoading").text("Loading video...").appendTo($this),
                sendData = JSON.stringify({'id': id, 'keys': opts.keys});

            //get the pandora id and instantiate a pandoraVideo object with the current element and render it and execute optional callback    
            console.log(opts.api);                              
            var deferred = $.post(opts.api, {'action': opts.action, 'data': sendData}, function(response) {
                $loading.hide().remove();
                var pandora = new PandoraVideo(id, response.data, $this, opts);
                pandora.render();
                opts.callback(pandora);
            }, "json");

            deferred.error(function(data) {
                alert("failed to load video data");
            });
        });
    };
    /*
    pandoraVideo class
    Parameters:
        id: <string> pandora video id
        data: <object> data for the video object
        $el: <jQuery element>
        opts: <object> options object

    */
    var PandoraVideo = function(id, data, $el, opts) {
        var that = this;
        this.id = id;
        this.data = data;
        this.$el = $el;
        this.o = opts;
        this.annotPoint = -1;
        this.getVideoURL = function() {
            var rand = parseInt(Math.random() * 10000);
            return "http://" + opts.pandora_base + id + "/" + opts.resolution + ".webm";
            };

        //empties element, appends video widget
        this.render = function() {
            var that = this;
            this.$el.empty();
            this.$el.append(that.getWidget());    
        };
       
        /*
        Get points
        */
        var flattenedPoints = [];
        $.each(that.o.layers, function(i,layerType) {
            $.each(that.data.layers[layerType], function(j,layer) {
                flattenedPoints.push(layer['in']);
                flattenedPoints.push(layer.out);
            });
        });
        this.points = makeArrayUnique(flattenedPoints);


        this.crossesPoint = function(newPos) {
            var that = this;
            var positions = [that.annotPoint, newPos].sort();
            return this.points.some(function(point) {
                return point >= positions[0] && point <= positions[1];
            });        
        };

        function makeArrayUnique(arr) {
            var o = {}, i, l = arr.length, r = [];
            for(i=0; i<l;i+=1) o[arr[i]] = arr[i];
            for(i in o) r.push(o[i]);
            return r;
        };

        /*
            Use this to set options on the player from the outside.
            Example:
                pandoraVideoObject.setOption("width", 250);
        */
        this.setOption = function(key, val) {
            var that = this;
            this.o[key] = val;
            if ($.inArray(key, ['resolution']) != -1) {
                this.destroy();
                this.render();
                return this;
            }
            if ($.inArray(key, ['in', 'out', 'layers']) != -1) {
                this.updatePlayer();
                return this;
            }
            if ($.inArray(key, ['width']) != -1) {
                this.$video.animate({'width': that.o.width + "px"});
                return this;
            }            
            console.log("attempt to set invalid option or option which will make no difference to player state");
        };


        /*
        Returns currently defined option for key specified
        Parameters:
            key: <string> eg. 'width'
        */
        this.getOption = function(key) {
            return this.o[key] || "invalid option";
        };


        //returns <jQuery element> widget for this pandoraVideo object
        this.getWidget = function() {
            var that = this;
            var $container = this.$container = $('<div />').addClass("pandoraContainer");
            var $video = this.$video = $('<video />')
                .appendTo($container)
                .attr("src", that.getVideoURL())
                .attr("controls", "controls")
                .addClass("pandoraVideo")
                .animate({'width': that.o.width})
                .load()
                .bind("loadedmetadata", function() {
                    this.currentTime = that.o['in'];                    
                    that.updatePlayer();
        
                })
                .bind("play", function() {
                    that.interval = setInterval(function() {
                        that.updatePlayer();
                    }, that.o.interval)
                })                            
                .bind("pause", function() {
                    clearInterval(that.interval);
                })
                .bind("ended", function() {
                    clearInterval(that.interval);
                })
                .bind("seeked", function() {
                    that.updatePlayer();
                });
            var $annotations = this.$annotations = $('<div />')
                .addClass("pandoraAnnotations")
                .appendTo($container);
            return $container;                        
        };

        //update annotations, etc. based on video currentTime
        this.updatePlayer = function() {
            var that = this;            
            var currentTime = this.$video[0].currentTime;
            
            //first, handle if video has crossed out-point or is before in-point
            if (that.o.out != 0) {
                if (currentTime > (that.o.out + 2)) {
                    that.$video[0].currentTime = that.o.out;
                    that.$video[0].pause();
                }
                if (currentTime < (that.o['in'] - 2)) {
                    that.$video[0].currentTime = that.o['in'];
                    that.$video[0].pause();
                }
            }


            //if layers are the same as last update, return 
            if (!that.crossesPoint(currentTime)) { return false; }
            //console.log("annot point changed");

            //else, set new annotPoint, construct DOM elements for currently matched layers, etc.
            that.annotPoint = currentTime;
            //now get all matching layers at current time code
            var layerNames = this.o.layers,
                matchedLayers = {};

            $.each(layerNames, function(i, layerName) {
                
                matchedLayers[layerName] = that.getLayersAtTimecode(layerName, currentTime)
            });
            that.currentLayers = matchedLayers;
            that.$annotations.empty();
            for (var layer in matchedLayers) {
                if (matchedLayers.hasOwnProperty(layer)) {
                    var theseLayers = matchedLayers[layer];
                    //console.log(theseLayers);
                    if (theseLayers.length > 0) {
                        var $annotsForLayer = getElemForLayer(layer, theseLayers);
                        $annotsForLayer.appendTo(that.$annotations);                            
                    }
                }
            }                        
        };

        /*
        Parameters:
            layerName: <string> eg. 'transcripts'
            currentTime: <float> in seconds    
        Returns <array> of matched layer objects
        */
        this.getLayersAtTimecode = function(layerName, currentTime) {
            var ret = [];
            var theseLayers = this.data.layers[layerName];
            $.each(theseLayers, function(i,layer) {
                if (layer['in'] < currentTime && layer.out > currentTime) {
                    ret.push(layer);
                } 
            });
            return ret;
        };

        this.destroy = function() {
            this.$video[0].pause();
            this.$video.remove();
            this.$el.empty();
        };
    };    

    /*
    Parameters:
        layerName: <string> eg. 'transcripts'
        layers: <array> layer objects to render
    Returns <jQuery element> for an annotation type - i.e. all 'transcripts', or all 'descriptions'
    */
    function getElemForLayer(layerName, layers) {
        if (layers.length === 0) {
            return $('<div />'); //FIXME
        }
        var $elem = $('<div />').addClass("pandoraLayer").addClass(layerName);
        var title = layerName.substr(0,1).toUpperCase() + layerName.substr(1, layerName.length);
        var $title = $('<div />').addClass("pandoraLayerTitle").text(title).appendTo($elem);

        $.each(layers, function(i,v) {
            var $annot = $('<div />').addClass("pandoraAnnot");
            //TODO: add time-code div
            var $annotText = $('<div />')
                .addClass("pandoraAnnotText")
                .html(v.value)
                .appendTo($annot);
            $annot.appendTo($elem);
        });
        return $elem;
    }

    /*
    Silly function to check if two layer arrays are the same (i.e. to check if matchedLayers have changed)
    Parameters:
        layers1: <array> of layer objects
        layers2: <array> of layer objects to compare with
    Returns <boolean> true if layer arrays are the same, false if different
    FIXME: this id concatenation string comparison is a bit weird, but it seemed like a non-expensive simple way to do it
    */
    function isSameLayers(layers1, layers2) {
        var idString1 = '',
            idString2 = '';
        for (var l in layers1) {
            if (layers1.hasOwnProperty(l)) {
                $.each(layers1[l], function(i,v) {
                    idString1 += v.id;
                });
            }
        }
        for (var l in layers2) {
            if (layers2.hasOwnProperty(l)) {
                $.each(layers2[l], function(i,v) {
                    idString2 += v.id;
                });
            }
        }
        return idString1 == idString2
    }

    //Returns <boolean> true or false based on whether the browser can play pandora video
    //FIXME: actually implement this function
    function canPlayVideo() {
        return true;
    }


    /*
    Get options from data- attributes
        Parameters:                            
            optionTypes: <object>
                example: {
                    'strings': ['option1', 'option2', 'option3'],
                    'integers': ['fooint', 'barint'],
                    'arrays': ['list1', 'list2'],
                    'booleans': ['bool1']
                }

            namespace: <string>
                example: 'pandora'
                    namespace for data- attributes
                
            example html:
                <div id="blah" data-pandora-option1="foobar" data-pandora-fooint="23" data-pandora-list2="apples, oranges" data-pandora-bool1="true">

            usage:
                var dataOptions = $('#blah').getDataOptions(optionTypes, namespace);
    */
    $.fn.getDataOptions = function(optionTypes, namespace) {
        var $element = this;
        var prefix = "data-" + namespace + "-",
            options = {};        
        $.each(optionTypes['strings'], function(i,v) {
            var attr = prefix + v;
            options[v] = $element.hasAttr(attr) ? $element.attr(attr) : undefined;
        });
        $.each(optionTypes['integers'], function(i,v) {
            var attr = prefix + v;
            options[v] = $element.hasAttr(attr) ? parseInt($element.attr(attr)) : undefined;
        });
        $.each(optionTypes['floats'], function(i,v) {
            var attr = prefix + v;
            options[v] = $element.hasAttr(attr) ? parseFloat($element.attr(attr)) : undefined;
        });
        $.each(optionTypes['arrays'], function(i,v) {
            var attr = prefix + v;
            options[v] = $element.hasAttr(attr) ? $.map($element.attr(attr).split(","), $.trim) : undefined;
        }); 
        $.each(optionTypes['booleans'], function(i,v) {
            var attr = prefix + v;
            options[v] = $element.hasAttr(attr) ? $element.attr(attr) == 'true' : false;
        });       
        return options;
    }

    /*
    FIXME: possibly improve - http://stackoverflow.com/questions/1318076/jquery-hasattr-checking-to-see-if-there-is-an-attribute-on-an-element#1318091
    */
    $.fn.hasAttr = function(attr) {
        return this.attr(attr) != undefined;
    };

})(jQuery);

