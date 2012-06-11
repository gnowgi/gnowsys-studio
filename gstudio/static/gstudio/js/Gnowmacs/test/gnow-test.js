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

// Author Divya <divyas15@gmail.com>

var desktop = new DlDesktop({});
var tableg = 0;
var row, col;
var str_sym;
var options1, position, char_at_pos, index1, pt,pt1,pt2;
var formats;
formats = ["Save","HTML", "PDF", "LaTeX", "DocBook", "XOXO"];
var al;
var str1;
var al1,al2;
var gImage;
var gOptions;
function print(obj) {
        var a = [], i;
        for (i in obj) {
                var val = obj[i];
                if (val instanceof Function)
                        val = val.toString();
                else
                        val = DlJSON.encode(val);
                a.push(DlJSON.encode(i) + " : " + val);
        }
        return a.map(function(line){
                return line.replace(/^/mg, function(s) {
                        return "        ";
                });
        }).join("\n");
};

var info = ( "Existing keybindings:\n\n" +
             print(Ymacs_Keymap_Emacs().constructor.KEYS)
             + "\n\nHave fun!\n" );


try {
        var org = new Ymacs_Buffer({ name: test });

	org.cmd("org_mode");

        var keys = new Ymacs_Buffer({ name: "keybindings.txt" });
        keys.setCode(info);

	var layout = new DlLayout({ parent: desktop });

        var empty = new Ymacs_Buffer({ name: "empty" });
        var ymacs = window.ymacs = new Ymacs({ buffers: [ org, keys ] });
        ymacs.setColorTheme([ "dark", "y" ]);

        try {
                ymacs.getActiveBuffer().cmd("eval_file", ".ymacs");
        } catch(ex) {}

        var menu = new DlHMenu({});
        menu.setStyle({ marginLeft: 0, marginRight: 0 });


	var item = new DlMenuItem({ parent: menu, label: "Menu".makeLabel() });


	/* -------------- Org Export --------------*/

	//formats = ["HTML", "PDF", "LaTeX", "DocBook", "XOXO"];
	var submenu = new DlVMenu({});
        item.setMenu(submenu);
        formats.foreach(function(format){
                var item = new DlMenuItem({ label: format, parent: submenu });
                item.addEventListener("onSelect", function(){
			
                       try{

			   var is_Firefox = navigator.userAgent.toLowerCase().indexOf('firefox') > -1;
			   if (is_Firefox)
			       netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");

			   var xhr = new XMLHttpRequest();
			   var url = "http://127.0.0.1:9292/";
			  
		       	   xhr.open("POST", url, true);
			 
		       	   xhr.onreadystatechange=function() {
		       	       if (xhr.readyState==4) {
		       	   	  alert(xhr.status);
			
		       	       }
		       	   }
		      	   xhr.setRequestHeader("Content-type", "text/plain");

			if(format=="HTML" && gImage==1) // checking if insertImage() is called 
				{
				//ymacs.getActiveBuffer().cmd("delete_region_or_line",str1);
				al = "#+ATTR_HTML: align="+"\"left\""+"\n";
				al1 = al;
				ymacs.getActiveBuffer().cmd("insert",al1);
				//if(al2!=null)
				//ymacs.getActiveBuffer().cmd("delete_region_or_line",al2);
				}
				else if(format=="PDF" && gImage==1)
				{
				//ymacs.getActiveBuffer().cmd("delete_region_or_line",str1);
				al = "#+ATTR_LaTeX:placement = {r}"+"\n";
				al2 = al;
				ymacs.getActiveBuffer().cmd("insert",al2);
				//if(al1!=null)
				//ymacs.getActiveBuffer().cmd("delete_region_or_line",al1);
				}
			   xhr.send("gnow-select: "+format+"\n"+ymacs.getActiveBuffer().getCode());
				



//alert("gnow-select: "+format+"\n"+ymacs.getActiveBuffer().getCode());
//alert(format+"\n"+ymacs.getActiveBuffer().getCode());
			
}	
                       catch(e){
			   alert("Some Error");
			   alert(e);} 
		    });
	    });


        menu.addFiller();

        var item = new DlMenuItem({ parent: menu, label: "Toggle line numbers".makeLabel() });
        item.addEventListener("onSelect", function() {
                ymacs.getActiveBuffer().cmd("toggle_line_numbers");
        });
        
        /*------[ Wrap ]--------
         flag is a variable to store the current status of wrap.wrap itself switches On n Off depending on previous status.
         so it is necessary to keep record of previous status*/
        
         var item = new DlMenuItem({ parent: menu, label: "Wrap".makeLabel() });
         var flag = "False" ; 
         item.addEventListener("onSelect", function() {
               if(flag == "False")
               {      
                          flag = "True";
		          alert("Wrapping is ON");
                          ymacs.getActiveBuffer().cmd("wrap_text"); 
               }
               else
               {           	
		     flag = "False";	  
                     alert("Wrapping is OFF"); 
                     ymacs.getActiveBuffer().cmd("wrap_text");              
	       }    
                      
       });
       
	 /*------[ save ]--------*/
        
         var item = new DlMenuItem({ parent: menu, label: "Save".makeLabel() });
         item.addEventListener("onSelect", function() {
		 /var fso = new DOMParser("Scripting.FileSystemObject");
		 varFileObject = fso.OpenTextFile("/home/supriya/Desktop/test1.txt", 2, true,0);
		 varFileObject.write("hello");
		 varFileObject.close();
		 alert ("hi");
	     });
       
	

        /* -----[ insert - just a try] ----- */

        var item = new DlMenuItem({ parent: menu, label: "Insert".makeLabel() });
	 var item1 = new DlMenuItem({ parent: submenu, label: "TOC" });
        var submenu = new DlVMenu({});
        item.setMenu(submenu);
         var subToc = new DlVMenu({});
        item = new DlMenuItem({ parent: submenu, label: "Default from ymacs.css" });
        item.addEventListener("onSelect", function(){
                ymacs.getActiveFrame().setStyle({ fontFamily: "" });
        });

       submenu.addSeparator();
item1 = new DlMenuItem({ parent: submenu, label: "Table Of Content" });
item1.addEventListener("onSelect", function()
			      {
				  options1 = "#+OPTIONS:" + " "+ "H:3 num:t toc:t \\n:nil @:t ::t |:t ^:t -:t f:t *:t <:t" +"\n";
				  insertOPTIONS();

			      });
   var files =     [
                "Table",
		"Insert Column",
		"Insert Row",
		"Insert hline",
                "Images",                            
        ]
           item1.setMenu(subToc); 

       


      files.foreach(function(i){   
                item = new DlMenuItem({ parent: submenu, label: "<span style='font-size:" + i + "'>" + i + "</span>" });		
		item.addEventListener("onSelect", function(){
		            
	//	alert("You selected " +i);	
		
		switch(i)
		{
		case "Table": insertTable(); 
  		break;
		case "Insert Column": if(tableg == 1) // if insertTable() is called previously then call insertColumn()
				       {  insertColumn();					   
				        }
				       else
					{ alert("First create a table");
					}
	        break;
		case "Insert Row": if(tableg == 1) // if insertTable() is called previously then call insertRow()
				       {  insertRow();					   
				        }
				       else
					{ alert("First create a table");
					}
	        break;
		case "Insert hline": if(tableg == 1)// if insertTable() is called previously then call insertHline()
				       {  insertHline();					   
				        }
				       else
					{ alert("First create a table");
					}
	        break;
		
		case "Images": insertImage1();
  		break;
		default:
  		alert("code to be executed if n is different from case 1 and 2");
		}
        });
      });


             var files2 =  [
                "OPTIONS"
                                   

        ].foreach(function(font){
                 item = new DlMenuItem({ parent: subToc, label: "<span style='font-family:" + font + "'>" + font + "</span>" });
                  var test_flag = "False" ;
                 item.addEventListener("onSelect", function(){

                                            //  var pt2 = ymacs.getActiveBuffer().cmd("point");      
                                             // alert(pt2);      
				    
					        if(test_flag == "False" && gOptions == 1)
						{
                                                    test_flag = "True";
						    alert("OPTIONS is ON");
                                                    ymacs.getActiveBuffer().cmd("goto_char",pt1);
                                                     alert(pt1);
                                                    ymacs.getActiveBuffer().cmd("end_of_line");
                                           	   ymacs.getActiveBuffer().cmd("insert","\n"); 
                                                    pt2 = ymacs.getActiveBuffer().cmd("point");      
                                                    alert(pt2);      
						    options1 = "#+OPTIONS:" + " "+ "H:3 num:t toc:t \\n:nil @:t ::t |:t ^:t -:t f:t *:t <:t"+"\n";
						    ymacs.getActiveBuffer().cmd("insert",options1);
                                                  //ymacs.getActiveBuffer().cmd("insert","\n"); 
						                                                  
						}
                                           else if(gOptions!=1){

                                                                     alert("Insert TOC first");



                                                  }

					    else
						{
						    
                                                  // ymacs.getActiveBuffer().cmd("beginning_of_buffer");
          						
                                                    test_flag = "False";
						    alert("OPTIONS is OFF");
				                                                                                                                                                                                                                      
						   
                                                     // if(gOptions == 1)
                                                      
                                                  
						  ymacs.getActiveBuffer().cmd("goto_char",pt2);  
                                                    alert(pt2);
                                               
                                                 // ymacs.getActiveBuffer().cmd("forward_line");  
                                                     
                                                 // var pt1 = ymacs.getActiveBuffer().cmd("point");      
                                                 // alert("pt1",pt1);  
                                                 //  ymacs.getActiveBuffer().cmd("goto_char",pt1);  
                                                 
                                                   ymacs.getActiveBuffer().cmd("delete_line");
						  options1 = "#+OPTIONS:" + " "+ "H:3 num:nil toc:nil \\n:nil @:t ::t |:t ^:t -:t f:t *:t <:t" +"\n";
						   ymacs.getActiveBuffer().cmd("insert",options1);
                                                   

						
                                             }
  

				
			


                 

            });
	 });

         function insertOPTIONS()
        {
            gOptions = 1;          
            var a1 = "#+AUTHOR:" + " " + "\n";
	    var t1 = "#+TITLE:" + " " + "\n";
	    var currentDate = new Date();
	    var month = currentDate.getMonth() + 1;
	    var day = currentDate.getDate();
	    var year = currentDate.getFullYear();
	    var weekday=new Array(7);
	    weekday[0]="Sunday";
	    weekday[1]="Monday";
	    weekday[2]="Tuesday";
	    weekday[3]="Wednesday";
	    weekday[4]="Thursday";
	    weekday[5]="Friday";
	    weekday[6]="Saturday";
	    var d1 = weekday[currentDate.getDay()];
	    var fullDate = "#+DATE:" + " " + year + " " + month + " " + day + " " + d1 + "\n";
	    var language1 = "#+LANGUAGE:" + " " + "en" + "\n";	    
	    var emailId = "#+EMAIL:" + " " + "\n";
	    var desc = "#+DESCRIPTION:" + " "+"\n";
	    var keywords ="#+KEYWORDS:" + " "+"\n";
	    var options2 = "#+OPTIONS:" + " "+ "TeX:t LaTeX:nil skip:nil d:nil todo:t pri:nil tags:not-in-toc"+"\n";
	    var info = "#+INFOJS_OPT:" + " " + "view:nil toc:nil ltoc:t mouse:underline buttons:0 path:http://orgmode.org/org-info.js" + "\n";
	    var export_select_tag = "#+EXPORT_" + " SELECT_" + "TAGS:" + " " + "export " +"\n";
	    var export_exclude_tag = "#+EXPORT_" + " EXCLUDE_" + "TAGS:" + " " + "noexport" + "\n";
	    var link_up = "#+LINK_UP:" + " " + "\n";
	    var link_home = "#+LINK_HOME:" + " " + "\n";
	    ymacs.getActiveBuffer().cmd("insert",t1);
	    ymacs.getActiveBuffer().cmd("insert",a1);
	    ymacs.getActiveBuffer().cmd("insert",emailId);
	    ymacs.getActiveBuffer().cmd("insert",fullDate);
	    ymacs.getActiveBuffer().cmd("insert",keywords);
	    ymacs.getActiveBuffer().cmd("insert",language1);             
            //pt = ymacs.getActiveBuffer().cmd("point");      
            //alert(pt);          
	    //ymacs.getActiveBuffer().cmd("insert",options1);  
        //   ymacs.getActiveBuffer().cmd("insert","\n");   
     
	    ymacs.getActiveBuffer().cmd("insert",options2);
        
             ymacs.getActiveBuffer().cmd("insert","\n");  
            pt1 = ymacs.getActiveBuffer().cmd("point");     
           // alert(pt1);  
	    ymacs.getActiveBuffer().cmd("insert",info);
	    ymacs.getActiveBuffer().cmd("insert",export_select_tag);
	    ymacs.getActiveBuffer().cmd("insert",export_exclude_tag);
	    ymacs.getActiveBuffer().cmd("insert",link_up);
            ymacs.getActiveBuffer().cmd("insert",link_home);
            //ymacs.getActiveBuffer().cmd("goto_char",pt);  
          }




// This function creates a table with the user specified no. of rows & columns.
		function insertTable()
		{
			row = prompt("Enter no. of rows",1);			
			col = prompt("Enter no. of cols",1);
			tableg = 1;
			for(k=0;k<=col;k++)
			{
				ymacs.getActiveBuffer().cmd("org_table_create");
			}
			ymacs.getActiveBuffer().cmd("insert","\n"); ymacs.getActiveBuffer().cmd("insert","|");
			 ymacs.getActiveBuffer().cmd("insert","---");		
			for(k=0;k<(col-1);k++)
			{
		        
		         ymacs.getActiveBuffer().cmd("insert","@");
		         ymacs.getActiveBuffer().cmd("insert","---");
			} 
			ymacs.getActiveBuffer().cmd("insert","|");
			ymacs.getActiveBuffer().cmd("insert","\n");
			for(m=1;m<row;m++)
			{
				
				for(j=0;j<=col;j++)
				{
				  
				  ymacs.getActiveBuffer().cmd("org_table_create");
				}
				//alert(row);
				ymacs.getActiveBuffer().cmd("insert","\n");
			}
		}

	// This function creates a column for the table.	
	
		function insertColumn()

		{ 
						
		ymacs.getActiveBuffer().cmd("backward_paragraph");
		ymacs.getActiveBuffer().cmd("forward_line");
		ymacs.getActiveBuffer().cmd("end_of_line");	

		
		ymacs.getActiveBuffer().cmd("insert","|");
		
			ymacs.getActiveBuffer().cmd("forward_line");
			ymacs.getActiveBuffer().cmd("backward_char");ymacs.getActiveBuffer().cmd("insert","@");	
			ymacs.getActiveBuffer().cmd("delete_char");
		
			ymacs.getActiveBuffer().cmd("insert","---");	
			ymacs.getActiveBuffer().cmd("insert","|");	ymacs.getActiveBuffer().cmd("forward_line");
			for(k=1;k<row;k++){
			ymacs.getActiveBuffer().cmd("insert","|");
			ymacs.getActiveBuffer().cmd("forward_line");
		
	}  col = parseInt(col)+1;


	}	

	// This function creates a row for the table.

		function insertRow()

		{ 
		for(j=0;j<=col;j++)
				{
				  
				  ymacs.getActiveBuffer().cmd("org_table_create");
				} ymacs.getActiveBuffer().cmd("insert","");	
			ymacs.getActiveBuffer().cmd("newline"); 
						
		 row = parseInt(row)+1;

	}

	// This function creates a Horizontal Line for the table.

		function insertHline()
		{
			ymacs.getActiveBuffer().cmd("end_of_line");
			ymacs.getActiveBuffer().cmd("insert","\n");
			
			ymacs.getActiveBuffer().cmd("insert","|");
			 ymacs.getActiveBuffer().cmd("insert","---");		
			for(k=0;k<(col-1);k++)
			{
		        
		         ymacs.getActiveBuffer().cmd("insert","@");
		         ymacs.getActiveBuffer().cmd("insert","---");
			} 
			ymacs.getActiveBuffer().cmd("insert","|");


		}

		function insertImage()
      		{
                               

				//gImage = 1;
				//ymacs.getActiveBuffer().cmd("end_of_buffer");
				//var img1 = prompt("Enter url for image","/home/sndt/Music/img2.jpeg");                            
                                //mywindow = window.open("fileupload2.html", "", "location=0,status=0,scrollbars=0, width=300,height=150");
                                mywindow = window.open("one.html", "", "location=0,status=0,scrollbars=0, width=300,height=150");
                                mywindow.moveTo(400, 400);

                                  //document.write("<INPUT TYPE=file + >");

                                 //document.write("hi");
                                
				//window.open(img1);
				//var al;
				//var str1;
				//var img2 = img1;				
				//var str3 = img1.indexOf(".");					
				//var str4 = img1.lastIndexOf("/");			
				//var str2 = img1.slice(str4+1,str3); 								
				//var str1 = "[[" + img1 + "]" + "["+ str2 +"]]";				
				//var al = "#+ATTR_HTML: align="+"\"left\""+"\n";	
				//str1 = "[[" + img1 + "]]";
				//var str = img1.lastIndexOf("]");
				//var a = str-1;
				//var c = img1.length;				
				//var b = img1.slice(str4+1,c);				
				//var d = "/home/sndt/imgtry/" + b;
				//var newPath = "[[" + d + "]]";
				//ymacs.getActiveBuffer().cmd("insert",newPath);	
				//ymacs.getActiveBuffer().cmd("insert",str1);
				
		}

function insertImage1()
      		{

                                // alert(img0);
				gImage = 1;
				ymacs.getActiveBuffer().cmd("end_of_buffer");
				var img1 = prompt("Enter url for image","/home/sndt/Music/img2.jpeg");                            
                                //mywindow = window.open("fileupload1.html", "", "location=0,status=0,scrollbars=0, width=300,height=150");
                               // mywindow.moveTo(400, 400);

                                  //document.write("<INPUT TYPE=file + >");

                                 //document.write("hi");
                                
				//window.open(img1);
				//var al;
				//var str1;
                              //  var img1 = img0;
				var img2 = img1;				
				var str3 = img1.indexOf(".");					
				var str4 = img1.lastIndexOf("/");			
				var str2 = img1.slice(str4+1,str3); 								
				//var str1 = "[[" + img1 + "]" + "["+ str2 +"]]";				
				//var al = "#+ATTR_HTML: align="+"\"left\""+"\n";	
				str1 = "[[" + img1 + "]]";
				var str = img1.lastIndexOf("]");
				var a = str-1;
				var c = img1.length;				
				var b = img1.slice(str4+1,c);				
				var d = "/home/sndt/imgtry/" + b;
				var newPath = "[[" + d + "]]";
				//ymacs.getActiveBuffer().cmd("insert",newPath);	
				ymacs.getActiveBuffer().cmd("insert",str1);
				ymacs.getActiveBuffer().cmd("backward_line");
		}




        /* -----[ color theme ]----- */

        var item = new DlMenuItem({ parent: menu, label: "Color theme".makeLabel() });
        var submenu = new DlVMenu({});
        item.setMenu(submenu);

        [
                "dark|y|Dark background (default)",
                "dark|billw|>Billw",
                "dark|charcoal-black|>Charcoal black",
                "dark|clarity-and-beauty|>Clarity and beauty",
                "dark|classic|>Classic",
                "dark|gnome2|>Gnome 2",
                "dark|calm-forest|>Calm forest",
                "dark|linh-dang-dark|>Linh Dang Dark",
                "dark|blue-mood|>Blue mood",
                "dark|zenburn|>Zenburn",
                "dark|standard-dark|>Emacs standard (dark)",
                null,
                "light|y|Light background (default)",
                "light|andreas|>Andreas",
                "light|bharadwaj|>Bharadwaj",
                "light|gtk-ide|>GTK IDE",
                "light|high-contrast|>High contrast",
                "light|scintilla|>Scintilla",
                "light|standard-xemacs|>Standard XEmacs",
                "light|vim-colors|>Vim colors",
                "light|standard|>Emacs standard (light)"
        ].foreach(function(theme){
                if (theme == null) {
                        submenu.addSeparator();
                } else {
                        theme = theme.split(/\s*\|\s*/);
                        var label = theme.pop();
                        label = label.replace(/^>\s*/, "&nbsp;".x(4));
                        var item = new DlMenuItem({ parent: submenu, label: label });
                        item.addEventListener("onSelect", ymacs.setColorTheme.$(ymacs, theme));
                }
        });
		  /*-------Insert-------
           
        var item = new DlMenuItem({ parent: menu, label: "Insert".makeLabel() });
        var item1 = new DlMenuItem({ parent: submenu, label: "TOC" });
        var submenu = new DlVMenu({});
        
        var subToc = new DlVMenu({});
        item.setMenu(submenu); 
        item = new DlMenuItem({ parent: submenu, label: "Default file" });
        submenu.addSeparator(); 
        item1 = new DlMenuItem({ parent: submenu, label: "Table Of Content" });
        item.addEventListener("onSelect", function(){
        
        });
        
       var files1 =  [
                "Image",
                "Text",
                "Table"
                 	
                   

        ]
        
        

                item1.setMenu(subToc);   
                 files1.foreach(function(font){
                 item = new DlMenuItem({ parent: submenu, label: "<span style='font-family:" + font + "'>" + font + "</span>" });
                 item.addEventListener("onSelect", function(){
                 
                        
		if(font == "Image")
		{ 
                 var imgPath = prompt("Enter the location:", "/home/snehal1/pics/ ");
                 window.open(imgPath);
                 
                }

            });
	 });
       
        var files2 =  [
                "Title",
                "Author",
                "Email",
                "Description",
                "Language"

                 
                   

        ].foreach(function(font){
                 item = new DlMenuItem({ parent: subToc, label: "<span style='font-family:" + font + "'>" + font + "</span>" });
                 item.addEventListener("onSelect", function(){
                 var name1 = prompt("Enter data",""); 

            });
	 });
       */

     


		/* -----[ Symbol Insert ]----- */

        /* var item = new DlMenuItem({ parent: menu, label: "Symbol Insert".makeLabel() });
        var submenu = new DlVMenu({});
        item.setMenu(submenu);

        submenu.addSeparator();

        [
                "&alpha;",
                "&beta;",
                "&#947;",
                "&#948;",
                "&#949;",
                "&#952;",
                "&#955;",
		"&#956;",
		"&#960;",
		"&#961;",
		"&#963;",
		"&#934;",
		"&#931;"
                
        ].foreach(function(i){
                item = new DlMenuItem({ parent: submenu, label: "<span style='font-family:" + i + "'>" + i + "</span>" });
                item.addEventListener("onSelect", function(){
                       // ymacs.getActiveBuffer().cmd("insert",i);
			alert(i);		
			var greek_sym1 = [945,946,947,948,949,952,955,956,960,961,963,934,931];
		var greek_sym2 = ["&alpha;","&beta;","&#947;","&#948;","&#949;","&#952;","&#955;","&#956;","&#960;","&#961;","&#963;","&#934;","&#931;"];
			//var str_sym;
   			
			for(j=0;j<=13;j++)
			{
				for(k=0;k<=13;k++)
				{
					if(greek_sym2[j]==i && j==k)	
					{
						str_sym = String.fromCharCode(greek_sym1[k]);						
					}
					
				}


			}
			ymacs.getActiveBuffer().cmd("insert",str_sym);
			

               });
        });
*/
        /* -----[ font ]----- */

        var item = new DlMenuItem({ parent: menu, label: "Font family".makeLabel() });
        var submenu = new DlVMenu({});
        item.setMenu(submenu);

        item = new DlMenuItem({ parent: submenu, label: "Default from ymacs.css" });
        item.addEventListener("onSelect", function(){
                ymacs.getActiveFrame().setStyle({ fontFamily: "" });
        });

        submenu.addSeparator();

        [
                "Lucida Sans Typewriter",
                "Andale Mono",
                "Courier New",
                "Arial",
                "Verdana",
                "Tahoma",
                "Georgia",
                "Times New Roman"

        ].foreach(function(font){
                item = new DlMenuItem({ parent: submenu, label: "<span style='font-family:" + font + "'>" + font + "</span>" });
                item.addEventListener("onSelect", function(){
                        ymacs.getActiveFrame().setStyle({ fontFamily: font });
                });
        });

        // ymacs.getActiveFrame().setStyle({ fontFamily: "Arial", fontSize: "18px" });

/* -----[ gnowsys-mode ]----- */

       /* var item = new DlMenuItem({ parent: menu, label: "gnowsys-mode".makeLabel() });       
       
        item.addEventListener("onSelect", function(){
             // window.open("/home/sndt/Downloads/jknair-MozGnowser-42c5530/gnowm

oz@gnowledge.org/chrome/gnowmoz/content/gnowmoz.html");
            
		var org1 = new Ymacs_Buffer({ name: "gnowsysmode.org" });
		org1.setCode("hi");
		ymacs.getActiveBuffer().cmd("switch_to_buffer",org1);           
               // org1.cmd("org_mode");
		ymacs.getActiveBuffer().cmd("load_file");
		//window.open("http://sandboxatlas.gnowledge.org/gnowql");
		//window.open("/home/sndt/Downloads/jknair-MozGnowser-42c5530/gnowmoz@gnowledge.org/chrome/gnowmoz/content/gnowmoz.html");
		 //window.open("two.html","_blank","width=650,height=650");
	    	
        });    */ 
                 /* -----[ font size ]----- */

        var item = new DlMenuItem({ parent: menu, label: "Font size".makeLabel() });
        var submenu = new DlVMenu({});
        item.setMenu(submenu);

        item = new DlMenuItem({ parent: submenu, label: "Default from ymacs.css" });
        item.addEventListener("onSelect", function(){
                ymacs.getActiveFrame().setStyle({ fontSize: "" });
        });

        submenu.addSeparator();

        [
                "11px",
                "12px",
                "14px",
                "16px",
                "18px",
                "20px",
                "22px",
                "24px"

        ].foreach(function(font){
                item = new DlMenuItem({ parent: submenu, label: "<span style='font-size:" + font + "'>" + font + "</span>" });
                item.addEventListener("onSelect", function(){
                        ymacs.getActiveFrame().setStyle({ fontSize: font });
                });
        });

        layout.packWidget(menu, { pos: "top" });
        layout.packWidget(ymacs, { pos: "bottom", fill: "*" });
	
	layout.setSize({x:800, y:500});

} catch(ex) {
        console.log(ex);
}

DynarchDomUtils.trash($("x-loading"));

if (!is_gecko && !is_khtml) (function(){

        var dlg = new DlDialog({
                title   : "Information",
                modal   : true,
                quitBtn : "destroy"
        });

        var vbox = new DlVbox({ parent: dlg, borderSpacing: 5 });
        var tmp = new DlWidget({ parent: vbox });
        tmp.getElement().appendChild($("browser-warning"));
        var ok = new DlButton({ parent: vbox, focusable: true, label: "OK, let's see it" });
        ok.addEventListener("onClick", dlg.destroy.$(dlg));
        dlg._focusedWidget = ok;

        dlg.show(true);

})();
