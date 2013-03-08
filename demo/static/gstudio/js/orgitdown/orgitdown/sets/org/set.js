// ----------------------------------------------------------------------------
// orgitdown!
// ----------------------------------------------------------------------------
// Html tags
// http://en.wikipedia.org/wiki/html
// ----------------------------------------------------------------------------
// Basic set. Feel free to add more tags
// ----------------------------------------------------------------------------
var mySettings = {
	
        onShiftEnter:  	{keepDefault:false, replaceWith:'<br />\n'},
	onCtrlEnter:  	{keepDefault:false, openWith:'\n<p>', closeWith:'</p>'},
	onTab:    	{keepDefault:false, replaceWith:'    '},
	onAltEnter:     {keepDefault:false, replaceWith:'\n* '},
	onAltrightArrow: {keepDefault:false, replaceWith:'*'},
	markupSet:  [ 	
                {name:'Save',call:'save' },
	        {separator:'---------------' },
		{name:'Bold', key:'B', openWith:'*', closeWith:'*' },
		{name:'Italic', key:'I', openWith:'/', closeWith:'/'  },
		{name:'Stroke through', key:'S', openWith:'+', closeWith:'+' },
		{separator:'---------------' },
		{name:'Bulleted List', openWith:'    - ', closeWith:'', multiline:true, openBlockWith:'\n', closeBlockWith:'\n'},
		{name:'Numeric List', openWith:'    1. ', closeWith:'', multiline:true, openBlockWith:'\n', closeBlockWith:'\n'},
		{separator:'---------------' },
		{name:'Picture', key:'P', replaceWith:'\n#+CAPTION: \n#+ATTR_HTML: width="600" \n[[http:fileName.jpg]]\n' },
		{name:'Link', key:'L', openWith:'[[http://your.address.com here/][Your visible link text here]]', closeWith:'', placeHolder:'' },
	        {separator:'---------------' },
                {name:'Insert Embed Html', replaceWith:'\n#+BEGIN_HTML \n#+END_HTML\n' },
                {name:'Close',call:'close' }

		//{name:'Clean', className:'clean', replaceWith:function(orgitdown) { return orgitdown.selection.replace(/<(.*?)>/g, "") } }		
		//{name:'Preview', className:'preview',  call:'preview'}
	]
}
