from django.shortcuts import renderfrom .models import Property, Queryimport csvfrom django.http import HttpResponseimport loggingfrom django.contrib import messagesfrom datetime import datetimefrom django.core.exceptions import ValidationError, FieldErrorfrom django.views.decorators.csrf import ensure_csrf_cookiefrom django.views.decorators.csrf import csrf_exemptfrom django.http import JsonResponseimport threadingfrom Mail_Manager_Site.forms import PostForm, SearchForm, QueryManagementFormfrom django.http import HttpResponseRedirectimport jsonfrom django.core import serializersfrom django.core.serializers.json import Serializer, DjangoJSONEncoderprint("we are on views.py")def write_json(file, data):    with open(file, 'w') as outfile:        json.dump(data, outfile)def json_handler(request):    some_data_to_dump = [{'id': 0, 'name': 'Item 0', 'price': "$0"}]    data_2 = json.dumps(some_data_to_dump, sort_keys=True, indent=4)    data_json = open_json()    # return HttpResponse(data_2)    return JsonResponse(some_data_to_dump, safe=False)    #return HttpResponse([{'foo':'bar'}])def open_json():    with open('data1.json') as json_data:        data1 = json.load(json_data)  # deserialises it        # print(data1)    json_data.close()    return data1def home_page(request):    return render(request, 'site/home.html')def import_page(request):    # date_input_form = PostForm(request.POST)    #content = date_input_form.cleaned_data['content']    #print(content)    if request.method == 'GET':        date_input_form = PostForm()        print('form GET')    else:        # A POST request: Handle Form Upload        date_input_form = PostForm(request.POST)  # Bind data from request.POST into a PostForm        print('form Post')        # If data is valid, proceeds to create a new post and redirect the user        if date_input_form.is_valid():            content = date_input_form.cleaned_data['content']            created_at = date_input_form.cleaned_data['created_at']            print(content)            return HttpResponseRedirect('#')        else:            print("not valid")            content = date_input_form.cleaned_data['content']            print(content)    return render(request, 'site/import.html', {        'date_input_form': date_input_form,    })def select_from_df():    print("select from DB")def search_page(request):    res = None    data = None    json_data = None    query_form = None    if request.method == 'GET':        search_form = SearchForm()        print('Search GET')    elif request.method == 'POST':        print('Search POST')        search_form = SearchForm(data=request.POST)  # Bind data from request.POST into a PostForm        # A POST request: Handle Form Upload        if search_form.is_valid():            print("Valid.")            label = search_form.cleaned_data['Owner_Label_Name']            prop_addr = search_form.cleaned_data['Property_Address']            prop_city = search_form.cleaned_data['Property_City']            prop_st = search_form.cleaned_data['Property_State']            prop_type = search_form.cleaned_data['Property_Type']            mail_addr = search_form.cleaned_data['Mail_Address']            mail_city = search_form.cleaned_data['Mail_City']            mail_st = search_form.cleaned_data['Mail_State']            equity = search_form.cleaned_data['Equity']            absentee = search_form.cleaned_data['Absentee_Owned']            mail_date = search_form.cleaned_data['Last_Mail_Date']            query_limit = search_form.cleaned_data['Query_Limit']        if 'search_submit' in request.POST:            # if just one field is not empty then filter            #if label or prop_addr or prop_city or prop_st or prop_type or mail_addr or mail_city or mail_st or equity or absentee or mail_date:            p = Property.objects.all()            if label:                p = p.filter(Owner_Label_Name__contains=label)                print("Filter Owner Label Name")            if prop_addr:                p = p.filter(Property_Address__contains=prop_addr)                print("Filter Property Address")            if prop_city:                p = p.filter(Property_City__contains=prop_city)                print("Filter Property City")            if prop_st:                p = p.filter(Property_State=prop_st.upper())                print("Filter Property State")            if prop_type:                p = p.filter(Property_Type=prop_type)                print("Filter Property Type")            if mail_addr:                p = p.filter(Mail_Address__contains=mail_addr)                print("Filter Mail Address")            if mail_city:                p = p.filter(Mail_City__contains=mail_city)                print("Filter Mail_City")            if mail_st:                p = p.filter(Mail_State=mail_st.upper())                print("Filter Mail State")            if equity:                p = p.filter(Equity=equity)                print("Filter Equity")            if absentee and absentee != 'empty':                print(absentee)                p = p.filter(Absentee_Owned=str(absentee).capitalize())                print("Filter Absentee Owned")            if mail_date:                #p = p.filter(Last_Mail_Date=mail_date)                print(mail_date)                p = p.filter(Last_Mail_Date__range=["2000-01-01", mail_date])                print("Filter Last Mail Date")            if query_limit:                p = p[:query_limit]                print("Apply Query Limit")            result_query = p            # result_query = Property.objects.filter(Property_City=prop_city).values()            #for r in result_query:            #    print(r)            data = '1'            #json_data = json.dumps([result_query], sort_keys=True)            json_data = json.dumps([{'Owner_Label_Name': r.Owner_Label_Name,                                     'Property_Address': r.Property_Address,                                     'Property_City': r.Property_City,                                     'Property_State': r.Property_State,                                     'Property_Type': r.Property_Type,                                     'Mail_Address': r.Mail_Address,                                     'Mail_City': r.Mail_City,                                     'Mail_State': r.Mail_State,                                     'Equity': r.Equity,                                     'Absentee_Owned': r.Absentee_Owned,                                     'Last_Mail_Date': str(r.Last_Mail_Date),                                     } for r in result_query])            #json_data = serializers.serialize("json", list(p), fields=('Owner_Label_Name', 'Property_Address', 'Property_City', 'Property_State'), use_natural_foreign_keys=False, use_natural_primary_keys=False)            #print(search_form.Property_Address)            #created_at = form.cleaned_data['created_at']        if 'query_manage_submit' in request.POST:            print('query_manage_submit')            query_form = QueryManagementForm()        if 'query_save' in request.POST:            print('query_save')            q = Query(Owner_Label_Name=label,                     Mail_Address=mail_addr,                     Mail_City=mail_city,                     Mail_State=mail_st,                     Property_Address=prop_addr,                     Property_City=prop_city,                     Property_State=prop_st,                     Property_Type=prop_type,                     Equity=equity,                     Absentee_Owned=absentee,                     Last_Mail_Date=mail_date,                     Query_Limit=query_limit)            try:                q.full_clean(validate_unique=True)                q.save()            except Exception as e:                print(e)    return render(request, 'site/search.html', {        'form': search_form,        'query_form': query_form,        'json_data': json_data,    })def about_page(request):    return render(request, 'site/about.html')@csrf_exemptdef upload_handler(request):    print("Handling uploaded file...")    content = []    # testing request    if request.method == 'POST':        print("POST")    elif request.method == 'GET':        print("GET")    else:        print("Unclear")    print(request.REQUEST)    dt = ''    try:        dt = request.POST.getlist('last_mail_date')        print("Last Mail Date: ", dt)    except Exception as e:        print(e)    if dt[0] is not '':        lmd = datetime.strptime(dt[0], "%m/%d/%Y").strftime('%Y-%m-%d')    else:        lmd = None    uploaded_files = request.FILES.getlist('file_data')    for uploaded_file in uploaded_files:        print("Processing ", uploaded_file.name)        for chunk in uploaded_file.chunks():            try:                my_file = open(uploaded_file.name, 'wb+')                my_file.write(chunk)            except Exception as e:                print(e)        try:            with open(uploaded_file.name, newline='') as csv_file:                reader = csv.reader(csv_file, delimiter=';', quotechar='|')                for row in reader:                    content.append(row)        except Exception as e:            print(e)    total_rows = 0    failed_rows = 0    success_rows = 0    already_exist_rows = 0    a = datetime.now()    for c in content:        # skip header line (should be implemented)        if c[0] == 'OWNER 1 LABEL NAME':            continue        # If the mail address + city + state + zip are different from the property address + city + state + zip YES. Else, NO.        ab = 'Yes'        if str(c[11] + c[12] + c[13] + c[14]) == str(c[19] + c[29] + c[30] + c[31]):            ab = 'No'        total_rows += 1        # id = House number . street . city . state . zip        p = Property(id=c[19] + c[29] + c[30] + c[31],                     Owner_Label_Name=c[0],                     Mail_Address=c[11],                     Mail_City=c[12],                     Mail_State=c[13],                     Mail_Zip=c[14],                     Property_Address=c[19],                     Property_City=c[29],                     Property_State=c[30],                     Property_Zip=c[31],                     Property_Type=c[36],                     Equity=c[37],                     Absentee_Owned=ab,                     Last_Mail_Date=lmd)        try:            p.full_clean(validate_unique=True)            p.save()            success_rows += 1        except Exception as e:            if 'Property with this Id already exists' in str(e):                already_exist_rows += 1            else:                print(e)                failed_rows += 1    # printing statistics    print("Total processed rows: ", total_rows)    print("Failed: ", failed_rows)    print("Success: ", success_rows)    print("The property with the same id: ", already_exist_rows)    print("Query time: ", datetime.now() - a)    # return response to input plugin    return JsonResponse({'success': 'yes'})def post_form_upload(request):    if request.method == 'GET':        form = PostForm()        print('smth get')    else:        # A POST request: Handle Form Upload        form = PostForm(request.POST)  # Bind data from request.POST into a PostForm        print('snth post')        # If data is valid, proceeds to create a new post and redirect the user        if form.is_valid():            content = form.cleaned_data['content']            created_at = form.cleaned_data['created_at']            print(content)            print(created_at)            # post = m.Post.objects.create(content=content,            #                             created_at=created_at)            return HttpResponseRedirect('#')        else:            print("not valid")            content = form.cleaned_data['content']            # created_at = form.cleaned_data['created_at']            print(content)            #print(created_at)    return render(request, 'site/about.html', {        'form': form,    })"""# delete in futuredef tests(request):    if request.method == 'POST':        print("POST")    elif request.method == 'GET':        print("GET")    else:        print("Unclear")def go_to_done(request):    all_p = Property.objects.all()    return render(request, 'site/done.html', {'data': all_p})def save_to_db(request, content):    all_p = Property.objects.all()    print("blaaaaaaaa")    return render(request, 'site/done.html', {'data': all_p})def show_all_from_db(request):    all = Property.objects.all()    print("blalaaaaaaa")    return render(request, 'site/done.html', {'data': all})def get_file(request):    print("Getting file from request...")    uploaded_files = request.FILES.getlist('file_data')    for uploaded_file in uploaded_files:        print(uploaded_file.name)    data = []    for uploaded_file in uploaded_files:        with open(uploaded_file.name, newline='') as csv_file:            reader = csv.reader(csv_file, delimiter=';', quotechar='|')            for row in reader:                data.append(row)    return datadef import_to_db(request):    total_rows = 0    failed_rows = 0    success_rows = 0    already_exist_rows = 0    content = get_file(request)    a = datetime.now()    for c in content:        #skip header line        if c[0] == 'OWNER 1 LABEL NAME':            continue        # If the mail address + city + state + zip are different from the property address + city + state + zip YES. Else, NO.        ab = 'Yes'        if str(c[11]+c[12]+c[13]+c[14]) == str(c[19]+c[29]+c[30]+c[31]):            ab = 'No'        total_rows += 1        # id = House number . street . city . state . zip        p = Property(id=c[19]+c[29]+c[30]+c[31],                     Owner_Label_Name=c[0],                     Mail_Address=c[11],                     Mail_City=c[12],                     Mail_State=c[13],                     Mail_Zip=c[14],                     Property_Address=c[19],                     Property_City=c[29],                     Property_State=c[30],                     Property_Zip=c[31],                     Property_Type=c[36],                     Equity=c[37],                     Absentee_Owned=ab)        try:            p.full_clean(validate_unique=True)            p.save()        except ValidationError as e:            already_exist_rows += 1        else:            failed_rows += 1    # printing statistics    print("Total processed rows: ", total_rows)    print("Failed: ", failed_rows)    print("Success: ", success_rows)    print("The property with the same id: ", already_exist_rows)    print("Query time: ", datetime.now()-a)    #return go_to_done(request)    #messages.success(request, 'Profile details updated.')    #messages.add_message(request, messages.INFO, 'All is OK with messages')    #messages.success(request, 'Profile details updated.')    print("Imported.")    return    #return render(request, 'site/test.html', {})""""""d[0] - Owner_Label_Named[11] - Mail_Addressd[12] - Mail_Cityd[13] - Mail_Stated[14] - Mail_Zipd[19] - Property_Addressd[29] - Property_Cityd[30] - Property_Stated[31] - Property_Zipd[36] - Property_Typed[37] - Equity""""""if request.GET.get('savetodb'):    #return render(request, 'blog/done.html', {})    #print(request.POST.get("pz", ""))    print("asddd")    return save_to_db(request)"""