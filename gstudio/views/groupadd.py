# Copyright (c) 2011,  2012 Free Software Foundation

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gstudio.models import *
from gstudio.methods import *
import datetime
def groupadd(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a title.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
	stDate1 =  (request.POST["stDate"])
	stDate = stDate1.split("/")
        endDate1=(request.POST["endDate"])
	endDate = endDate1.split("/")
        hours1 = request.POST["hours1"]
	usr = request.POST.get("usr",'')	
        minutes1 = request.POST["minutes1"]
        hours2 = request.POST["hours2"]
        minutes2 = request.POST["minutes2"]
	if not (str(stDate1.encode('utf8')) and str(endDate1.encode('utf8'))):
		print "in fi dat4e"
		stDate = (str(date.today().strftime("%m/%d/%y"))).decode('utf8').split("/")
		endDate = (str(date.today().strftime("%m/%d/%y"))).decode('utf8').split("/")
		hours1 = 0
		minutes1 = 0
		hours2 = 0
		minutes2 = 0
	time1 = datetime.datetime(int(stDate[2]),int(stDate[0]),int(stDate[1]),int(hours1),int(minutes1))
        time2 = datetime.datetime(int(endDate[2]),int(endDate[0]),int(endDate[1]),int(hours2),int(minutes2))
	
        if not errors:
  	     title=request.POST['subject']
 	     content=unicode(request.POST['message'])
	     idusr=request.POST['idusr']
             meetId = create_meeting(title,int(idusr),content,usr)
	     schedule_time(time1, time2, meetId)
             if meetId :
                return HttpResponseRedirect('/gstudio/group/gnowsys-grp/'+ str(meetId))
    variables = RequestContext(request,{'errors' : errors })
    template = "gstudio/NewGroup.html"
    return render_to_response(template, variables)
 
