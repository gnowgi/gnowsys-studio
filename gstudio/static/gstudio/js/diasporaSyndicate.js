
function hasProt(s)
{
	var re=/^\b(https?):\/\//i;
	return re.test(s);
};

function getPodName()
{
	var _1=localStorage.getItem("diasporapodname");
	{
	    
		_1=prompt("Enter your Diaspora pod...","");
		if(_1==""||_1==null)
		{
			alert("Pod name is empty or invalid!");
			return;
		}
		else
		{
			if(hasProt(_1))
			{
				_1=_1.replace(/(https?):\/\//,"");
			}
			localStorage.setItem("diasporapodname",_1);
		}
	}
    shareOnD(_1);
};

function shareOnD(_2)
{
    f="https://"+_2+"/bookmarklet?url="+encodeURIComponent(window.location.href)+"&title="+encodeURIComponent(document.title)+"&notes="+encodeURIComponent(""+(window.getSelection?window.getSelection():document.getSelection?document.getSelection():document.selection.createRange().text)+document.getElementById("diasporacontent").value)+"&v=1&";
	a=function()
	{	
		if(!window.open(f+"noui=1&jump=doclose","diasporav1","location=yes,links=no,scrollbars=no,toolbar=no,width=620,height=350"))
		{
			location.href=f+"jump=yes";
		}
	};
	if(/Firefox/.test(navigator.userAgent))
	{
		setTimeout(a,0);
	}
	else
	{
		a();
	}
};

window.onload=function()
{       var _3=document.getElementById("asterisk").src;
	var _4=document.getElementById("R-button");
	_4.innerHTML="";
	var R=Raphael("R-button",44,44);
	R.circle(22,22,20).attr({fill:"r(.5,.10)#ccc-#aaa","fill-opacity":0.3,"stroke-width":3});
	var _5=R.image(_3,9,9,26,26);
	var _6=null,_7=0;
	_4.onmouseover=function()
			{
				_7+=180;
				_5.animate({transform:"r"+_7},5000,"backOut");
			};
	_4.onmouseout=function()
			{	
				_7+=180;
				_5.animate({transform:"r"+_7},5000,"elastic");
			};
	_4.onclick=function()
			{
				getPodName();
			};
};
