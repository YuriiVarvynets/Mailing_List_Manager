from django.shortcuts import renderfrom .models import Propertyimport csvfrom django.http import HttpResponseimport loggingfrom django.contrib import messagesfrom datetime import datetimefrom django.core.exceptions import ValidationError, FieldErrorfrom django.views.decorators.csrf import ensure_csrf_cookiefrom django.views.decorators.csrf import csrf_exemptfrom django.http import JsonResponseimport threadingfrom Mail_Manager_Site.forms import PostForm, SearchFormfrom django.http import HttpResponseRedirectprint("we are on views.py")def get_file(request):    print("Getting file from request...")    uploaded_files = request.FILES.getlist('file_data')    for uploaded_file in uploaded_files:        print(uploaded_file.name)    data = []    for uploaded_file in uploaded_files:        with open(uploaded_file.name, newline='') as csv_file:            reader = csv.reader(csv_file, delimiter=';', quotechar='|')            for row in reader:                data.append(row)    return data# delete in futuredef tests(request):    if request.method == 'POST':        print("POST")    elif request.method == 'GET':        print("GET")    else:        print("Unclear")def import_to_db(request):    total_rows = 0    failed_rows = 0    success_rows = 0    already_exist_rows = 0    content = get_file(request)    a = datetime.now()    for c in content:        #skip header line        if c[0] == 'OWNER 1 LABEL NAME':            continue        # If the mail address + city + state + zip are different from the property address + city + state + zip YES. Else, NO.        ab = 'Yes'        if str(c[11]+c[12]+c[13]+c[14]) == str(c[19]+c[29]+c[30]+c[31]):            ab = 'No'        total_rows += 1        # id = House number . street . city . state . zip        p = Property(id=c[19]+c[29]+c[30]+c[31],                     Owner_Label_Name=c[0],                     Mail_Address=c[11],                     Mail_City=c[12],                     Mail_State=c[13],                     Mail_Zip=c[14],                     Property_Address=c[19],                     Property_City=c[29],                     Property_State=c[30],                     Property_Zip=c[31],                     Property_Type=c[36],                     Equity=c[37],                     Absentee_Owned=ab)        try:            p.full_clean(validate_unique=True)            p.save()        except ValidationError as e:            already_exist_rows += 1        else:            failed_rows += 1    # printing statistics    print("Total processed rows: ", total_rows)    print("Failed: ", failed_rows)    print("Success: ", success_rows)    print("The property with the same id: ", already_exist_rows)    print("Query time: ", datetime.now()-a)    #return go_to_done(request)    """    d[0] - Owner_Label_Name    d[11] - Mail_Address    d[12] - Mail_City    d[13] - Mail_State    d[14] - Mail_Zip    d[19] - Property_Address    d[29] - Property_City    d[30] - Property_State    d[31] - Property_Zip    d[36] - Property_Type    d[37] - Equity    """    #messages.success(request, 'Profile details updated.')    #messages.add_message(request, messages.INFO, 'All is OK with messages')    #messages.success(request, 'Profile details updated.')    print("Imported.")    """    if request.GET.get('savetodb'):        #return render(request, 'blog/done.html', {})        #print(request.POST.get("pz", ""))        print("asddd")        return save_to_db(request)    """    return    #return render(request, 'site/test.html', {})def go_to_done(request):    all_p = Property.objects.all()    return render(request, 'site/done.html', {'data': all_p})def save_to_db(request, content):    all_p = Property.objects.all()    print("blaaaaaaaa")    return render(request, 'site/done.html', {'data': all_p})def show_all_from_db(request):    all = Property.objects.all()    print("blalaaaaaaa")    return render(request, 'site/done.html', {'data': all})def home_page(request):    return render(request, 'site/home.html')def import_page(request):    #date_input_form = PostForm(request.POST)    #content = date_input_form.cleaned_data['content']    #print(content)    if request.method == 'GET':        date_input_form = PostForm()        print('form GET')    else:        # A POST request: Handle Form Upload        date_input_form = PostForm(request.POST) # Bind data from request.POST into a PostForm        print('form Post')        # If data is valid, proceeds to create a new post and redirect the user        if date_input_form.is_valid():            content = date_input_form.cleaned_data['content']            created_at = date_input_form.cleaned_data['created_at']            print(content)            return HttpResponseRedirect('#')        else:            print("not valid")            content = date_input_form.cleaned_data['content']            print(content)    return render(request, 'site/import.html',{        'date_input_form': date_input_form,    })def select_from_df():    print("select from DB")def search_page(request):    res = None    data = None    if request.method == 'GET':        search_form = SearchForm()        print('Search GET')    elif request.method == 'POST':        print('Search POST')        # A POST request: Handle Form Upload        search_form = SearchForm(data=request.POST) # Bind data from request.POST into a PostForm        if search_form.is_valid():            print("Valid.")            label = search_form.cleaned_data['Owner_Label_Name']            prop_addr = search_form.cleaned_data['Property_Address']            prop_city = search_form.cleaned_data['Property_City']            prop_st = search_form.cleaned_data['Property_State']            prop_type = search_form.cleaned_data['Property_Type']            mail_addr = search_form.cleaned_data['Mail_Address']            mail_city = search_form.cleaned_data['Mail_City']            mail_st = search_form.cleaned_data['Mail_State']            equity = search_form.cleaned_data['Equity']            absentee = search_form.cleaned_data['Absentee_Owned']            mail_date = search_form.cleaned_data['Last_Mail_Date']            print(prop_city)            result_query = Property.objects.filter(Property_City=prop_city).values()            for r in result_query:                print(r)            print(label)        #print(search_form.Property_Address)        #res = show_all_from_db(request)        #print("not valid")        #content = form.cleaned_data['content']        #created_at = form.cleaned_data['created_at']        #print(content)        #print(created_at)    if res:        return res    else:        return render(request, 'site/search.html', {            'form': search_form,            'data': data,        })def about_page(request):    return render(request, 'site/about.html')def return_success():    return JsonResponse({'success':'yes'})def test():    print("testing function")@csrf_exemptdef upload_handler(request):    print("Handling uploaded file...")    content = []    # testing request    if request.method == 'POST':        print("POST")    elif request.method == 'GET':        print("GET")    else:        print("Unclear")    print(request.REQUEST)    dt = ''    try:        dt = request.POST.getlist('last_mail_date')        print("Last Mail Date: ", dt)    except Exception as e:        print(e)    if dt[0] is not '':        lmd = datetime.strptime(dt[0], "%m/%d/%Y").strftime('%Y-%m-%d')    else:        lmd = None    uploaded_files = request.FILES.getlist('file_data')    for uploaded_file in uploaded_files:        print("Processing ", uploaded_file.name)        for chunk in uploaded_file.chunks():            try:                my_file = open(uploaded_file.name, 'wb+')                my_file.write(chunk)            except Exception as e:                print(e)        try:            with open(uploaded_file.name, newline='') as csv_file:                reader = csv.reader(csv_file, delimiter=';', quotechar='|')                for row in reader:                    content.append(row)        except Exception as e:            print(e)    total_rows = 0    failed_rows = 0    success_rows = 0    already_exist_rows = 0    a = datetime.now()    for c in content:        #skip header line (should be implemented)        if c[0] == 'OWNER 1 LABEL NAME':            continue        # If the mail address + city + state + zip are different from the property address + city + state + zip YES. Else, NO.        ab = 'Yes'        if str(c[11]+c[12]+c[13]+c[14]) == str(c[19]+c[29]+c[30]+c[31]):            ab = 'No'        total_rows += 1        # id = House number . street . city . state . zip        p = Property(id=c[19]+c[29]+c[30]+c[31],                     Owner_Label_Name=c[0],                     Mail_Address=c[11],                     Mail_City=c[12],                     Mail_State=c[13],                     Mail_Zip=c[14],                     Property_Address=c[19],                     Property_City=c[29],                     Property_State=c[30],                     Property_Zip=c[31],                     Property_Type=c[36],                     Equity=c[37],                     Absentee_Owned=ab,                     Last_Mail_Date=lmd)        try:            p.full_clean(validate_unique=True)            p.save()            success_rows += 1        except Exception as e:            if 'Property with this Id already exists' in str(e):                already_exist_rows += 1            else:                print(e)                failed_rows += 1    # printing statistics    print("Total processed rows: ", total_rows)    print("Failed: ", failed_rows)    print("Success: ", success_rows)    print("The property with the same id: ", already_exist_rows)    print("Query time: ", datetime.now()-a)    # return response to input plugin    return JsonResponse({'success': 'yes'})def post_form_upload(request):    if request.method == 'GET':        form = PostForm()        print('smth get')    else:        # A POST request: Handle Form Upload        form = PostForm(request.POST) # Bind data from request.POST into a PostForm        print('snth post')        # If data is valid, proceeds to create a new post and redirect the user        if form.is_valid():            content = form.cleaned_data['content']            created_at = form.cleaned_data['created_at']            print(content)            print(created_at)            #post = m.Post.objects.create(content=content,            #                             created_at=created_at)            return HttpResponseRedirect('#')        else:            print("not valid")            content = form.cleaned_data['content']            #created_at = form.cleaned_data['created_at']            print(content)            #print(created_at)    return render(request, 'site/about.html', {        'form': form,    })