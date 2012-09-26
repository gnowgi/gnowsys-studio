
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.



from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gstudio.models import *
from gstudio.methods import *

def sectionadd1(request,pageid):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
             errors.append('Enter a title.')
        if not request.POST.get('org', ''):
             errors.append('Enter a page.')
        if not errors:
  	     title=request.POST['subject']
 	    # content=request.POST['page']
             content_org=unicode(request.POST['org'])
	     idusr=request.POST['idusr']
             usr=request.POST['usr']
             tp = make_section_object(title,int(idusr),content_org,usr)
             System.objects.get(id=int(pageid)).system_set.all()[0].gbobject_set.add(tp)
             if  tp:
              return HttpResponseRedirect('/gstudio/page/gnowsys-page/'+pageid)
    
    
    variables = RequestContext(request,{'errors' : errors,'pageid' : pageid})
    template = "gstudio/NewSection1.html"
    return render_to_response(template, variables)
 

