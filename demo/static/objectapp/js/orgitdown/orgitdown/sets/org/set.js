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
                {name:'Save', key:'S',call:'save' },
		{name:'Bold', key:'B', openWith:'*', closeWith:'*' },
		{name:'Italic', key:'I', openWith:'/', closeWith:'/'  },
		{name:'Stroke through', key:'S', openWith:'+', closeWith:'+' },
		{separator:'---------------' },
		{name:'Bulleted List', openWith:'    - ', closeWith:'', multiline:true, openBlockWith:'\n', closeBlockWith:'\n'},
		{name:'Numeric List', openWith:'    1. ', closeWith:'', multiline:true, openBlockWith:'\n', closeBlockWith:'\n'},
		{separator:'---------------' },
		{name:'Picture', key:'P', replaceWith:'[[http:fileName.jpg]]' },
		{name:'Link', key:'L', openWith:'[[http://your.address.com here/][Your visible link text here]]', closeWith:'', placeHolder:'' },
		{separator:'---------------' },
		{name:'Clean', className:'clean', replaceWith:function(orgitdown) { return orgitdown.selection.replace(/<(.*?)>/g, "") } },		
		{name:'Preview', className:'preview',  call:'preview'}
	]
}
