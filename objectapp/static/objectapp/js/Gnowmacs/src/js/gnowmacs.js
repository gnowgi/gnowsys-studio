// This file is part of Ymacs for GNOWSYS: Gnowledge Networking 
// and Organizing System.

// Ymacs is free software; you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation; either version 3 of
// the License, or (at your option) any later version.

// Ymacs is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU Affero General Public
// License along with Ymacs (agpl.txt); if not, write to the
// Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
// Boston, MA  02110-1301  USA59 Temple Place, Suite 330,

// Author: Divya <divyas15@gmail.com>

// @require ymacs-tokenizer.js

var arr4;
Ymacs_Tokenizer.define("org", function(stream, tok){

        var PARSER = {
                next        : next,
                copy        : copy,
                indentation : indentation
        };

        var $parens = [];
        var $passedParens = [];
        var $cont = [];
        var $inString = null;
        var $inComment = null;
	var $inHeading = null;
	
        function copy() {
                var c = resume.context = {
                        parens       : $parens.slice(0),
                        passedParens : $passedParens.slice(0),
                        cont         : $cont.slice(0),
                        inString     : $inString,
                        inComment    : $inComment,
			inHeading    : $inHeading
                };
                function resume() {
                        $parens       = c.parens.slice(0);
                        $passedParens = c.passedParens.slice(0);
                        $cont         = c.cont.slice(0);
                        $inString     = c.inString;
			$inComment    = c.inComment;
			$inHeading    = c.inHeading;
                        return PARSER;
                    };
                return resume;
        };

        function INDENT_LEVEL() {
                return tok.buffer.getq("indent_level");
        };

        var OPEN_PAREN = {
                "(" : ")",
                "{" : "}",
                "[" : "]"
        };

        var CLOSE_PAREN = {
                ")" : "(",
                "}" : "{",
                "]" : "["
        };

        function isOpenParen(ch) {
                return OPEN_PAREN[ch];
        };

        function isCloseParen(ch) {
                return CLOSE_PAREN[ch];
        };

        function foundToken(c1, c2, type) {
                tok.onToken(stream.line, c1, c2, type);
        };

        function readComment() {
                var line = stream.lineText(), pos = line.indexOf("*/", stream.col);
                var m = /^\s*\*+/.exec(line.substr(stream.col));
                if (m) {
                        foundToken(stream.col, stream.col += m[0].length, "mcomment-starter");
                }
                if (pos >= 0) {
                        $cont.pop();
                        $inComment = null;
                        foundToken(stream.col, pos, "mcomment");
                        foundToken(pos, pos += 2, "mcomment-stopper");
                        stream.col = pos;
                } else {
                        foundToken(stream.col, line.length, "mcomment");
                        stream.col = line.length;
                }
        };

        function readString(end, type) {
                var ch, esc = false, start = stream.col;
                while (!stream.eol()) {
                        ch = stream.peek();
                        if (ch === end && !esc) {
                                $cont.pop();
                                $inString = null;
                                foundToken(start, stream.col, type);
                                foundToken(stream.col, ++stream.col, type + "-stopper");
                                return true;
                        }
                        esc = !esc && ch === "\\";
                        stream.nextCol();
                }
                foundToken(start, stream.col, type);
        };

	function readHeading(type) {
                var start = stream.col;
                while (!stream.eol()) {
                        stream.nextCol();
                }
                foundToken(start, stream.col, type);
        };

        function next() {
                stream.checkStop();
                if ($cont.length > 0)
                        return $cont.peek()();
                var ch = stream.peek(), tmp;
                if (stream.lookingAt("/*")) {
                        $inComment = { line: stream.line, c1: stream.col };
                        foundToken(stream.col, stream.col += 2, "mcomment-starter");
                        $cont.push(readComment);
                }
                else if (ch === '"' || ch === "'") {
                        $inString = { line: stream.line, c1: stream.col };
                        foundToken(stream.col, ++stream.col, "string-starter");
                        $cont.push(readString.$C(ch, "string"));
                }	
		//to start with org
		else if ((tmp = stream.lookingAt(/^(\[\[)(.+?)(\]\[)(.+?)(\]\])/))) {
			foundToken(stream.col, stream.col += tmp[2].length+4, "org-link-url");
			var url = tmp[2];
			foundToken(stream.col, stream.col += (tmp[4].length+1), "org-link-text");
			window.open(url);						
			foundToken(stream.col, stream.col += 1, "org-link-close");
			
							
                }		
		else if ((tmp = stream.lookingAt(/^(\*.+?\*)/))) {
		    if (tmp[1].substring(1,2) === " " ||  tmp[1].substring(tmp[1].length-2, tmp[1].length-1) === " ")
			{foundToken(stream.col, stream.col += tmp[1].length, null);}
		    else{
                        foundToken(stream.col, stream.col += tmp[1].length, "org-bold");
		    }
                }
		else if ((tmp = stream.lookingAt(/^(\/.+?\/)/))) {
		    if (tmp[1].substring(1,2) === " " ||  tmp[1].substring(tmp[1].length-2, tmp[1].length-1) === " ")
			{foundToken(stream.col, stream.col += tmp[1].length, null);}
		    else{
                        foundToken(stream.col, stream.col += tmp[1].length, "org-italic");
		    }
                }
		else if ((tmp = stream.lookingAt(/^(_.+?_)/))) {
		    if (tmp[1].substring(1,2) === " " ||  tmp[1].substring(tmp[1].length-2, tmp[1].length-1) === " ")
			{foundToken(stream.col, stream.col += tmp[1].length, null);}
		    else{
                        foundToken(stream.col, stream.col += tmp[1].length, "org-underline");
		    }
                }
		else if ((tmp = stream.lookingAt(/^(\+.+?\+)/))) {
		    if (tmp[1].substring(1,2) === " " ||  tmp[1].substring(tmp[1].length-2, tmp[1].length-1) === " ")
			{foundToken(stream.col, stream.col += tmp[1].length, null);}
		    else{
                        foundToken(stream.col, stream.col += tmp[1].length, "org-strike");
		    }
	        }
		
		else if ((tmp = stream.lookingAt(/^(\*+\s+)/))) {
		    if (stream.col == 0){
			var headtype = "org-heading" + (tmp[1].length -1);
                        foundToken(stream.col, stream.col += tmp[1].length, headtype);
			readHeading(headtype);
		    }
                }

		
		//to end with org
                
                else {
                        foundToken(stream.col, ++stream.col, null);
                }
        };
		



        function indentation() {
                // no indentation for continued strings
                if ($inString)
                        return 0;

                var row = stream.line;
                var currentLine = stream.lineText();
                var indent = 0;

                if ($inComment) {
                        var commentStartLine = stream.lineText($inComment.line);
                        indent = $inComment.c1 + 1;
                        if (!/^\s*\*/.test(currentLine)) {
                                // align with the first non-whitespace and non-asterisk character in the comment
                                var re = /[^\s*]/g;
                                re.lastIndex = $inComment.c1 + 1;
                                var m = re.exec(commentStartLine);
                                if (m)
                                        indent = m.index;
                        }
                            return indent;
                }

                var p = $parens.peek();
                if (p) {
                        // check if the current line closes the paren
                        var re = new RegExp("^\\s*\\" + OPEN_PAREN[p.type]);
                        var thisLineCloses = re.test(currentLine);

                        // Check if there is text after the opening paren.  If so, indent to that column.
                        var line = stream.lineText(p.line);
                        re = /\S/g;
                        re.lastIndex = p.col + 1;
                        var m = re.exec(line);
                        if (m) {
                                // but if this line closes the paren, better use the column of the open paren
                                indent = thisLineCloses ? p.col : m.index;
                        }
                        else {
                                // Otherwise we should indent to one level more than the indentation of the line
                                // containing the opening paren.
                                indent = stream.lineIndentation(p.line) + INDENT_LEVEL();

                                // but if this line closes the paren, then back one level
                                if (thisLineCloses)
                                        indent -= INDENT_LEVEL();
                        }
                }

                return indent;
        };

        return PARSER;

});

DEFINE_SINGLETON("Ymacs_Keymap_Org", Ymacs_Keymap);
Ymacs_Keymap_Org().defineKeys({
        "ENTER"       : "newline_and_indent",
        ": && } && )" : "c_insert_and_indent"
});

Ymacs_Buffer.newMode("org_mode", function(){

        var tok = this.tokenizer;
        this.setTokenizer(new Ymacs_Tokenizer({ buffer: this, type: "org" }));
        var was_paren_match = this.cmd("paren_match_mode", true);
        this.pushKeymap(Ymacs_Keymap_Org());

        return function() {
                this.setTokenizer(tok);
                if (!was_paren_match)
                        this.cmd("paren_match_mode", false);
                this.popKeymap(Ymacs_Keymap_Org());
        };
});


Ymacs_Buffer.newCommands({

	org_insert_heading: Ymacs_Interactive(function() {
		this.cmd("beginning_of_line");
		this.cmd("insert", "* ");
	    }),

        org_bold: Ymacs_Interactive("r", function(begin, end) {
		if (end < begin) { var tmp = begin; begin = end; end = tmp; }
		this.cmd("goto_char", begin);
		this.cmd("insert", "*");
		this.cmd("goto_char", end+1);
		this.cmd("insert", "*");
	    }),

	org_italic: Ymacs_Interactive("r", function(begin, end) {
		if (end < begin) { var tmp = begin; begin = end; end = tmp; }
		this.cmd("goto_char", begin);
		this.cmd("insert", "/");
		this.cmd("goto_char", end+1);
		this.cmd("insert", "/");
	    }),

	org_underline: Ymacs_Interactive("r", function(begin, end) {
		if (end < begin) { var tmp = begin; begin = end; end = tmp; }
		this.cmd("goto_char", begin);
		this.cmd("insert", "_");
		this.cmd("goto_char", end+1);
		this.cmd("insert", "_");
	    }),

	org_strike: Ymacs_Interactive("r", function(begin, end) {
		if (end < begin) { var tmp = begin; begin = end; end = tmp; }
		this.cmd("goto_char", begin);
		this.cmd("insert", "+");
		this.cmd("goto_char", end+1);
		this.cmd("insert", "+");
	    }),
	    
        org_file: Ymacs_Interactive("f", function() {
		if (end < begin) { var tmp = begin; begin = end; end = tmp; }
		this.cmd("goto_char", begin);
		this.cmd("insert", "+");
		this.cmd("goto_char", end+1);
		this.cmd("insert", "+");
	    }),
       org_link: Ymacs_Interactive("r", function(begin, end) {
		if (end < begin) { var tmp = begin; begin = end; end = tmp; }
	        this.cmd("goto_char", begin);
		this.cmd("insert", "[[");			
		this.cmd("goto_char", end+2);
		this.cmd("insert", "]]");			
	    }),
	org_table_create: Ymacs_Interactive("r", function(begin, end) {		
		if (end < begin) { var tmp = begin; begin = end; end = tmp; }
		this.cmd("goto_char", begin);
		this.cmd("insert", "|");
		this.cmd("insert","   ");
		//this.cmd("goto_char", end+1);
		//this.cmd("insert", "|");
	    })
       

});
