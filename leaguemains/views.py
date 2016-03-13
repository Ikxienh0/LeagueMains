from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout

from leaguemains.models import LeagueMainsUser
from leaguemains.models import UserChampionList
from leaguemains.models import ChampionsInChampionList
from riotapi.update import LeagueMainsUpdater
from riotapi_static.models import Champion


# Create your views here.
def home(request):
    context = {}
    errormessages = request.session.get('errorMessages', None)
    if errormessages:
        del request.session['errorMessages']
    if request.user.is_authenticated():
        userlists = UserChampionList.objects.filter(fk_leaguemainsuser=request.user)
        context['userLists'] = userlists
    context['championList'] = Champion.objects.all().order_by('name')
    context['errorMessages'] = errormessages
    return render(request, 'home.html', context=context)


def login_user(request):
    errormessages = []
    if request.user.is_authenticated():
        errormessages.append("You cannot log in while already logged in!")
    else:
        if request.POST:
            usermail = request.POST['usermail']
            password = request.POST['password']
            user = authenticate(username=usermail, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    errormessages.append("You provided a valid user but the user is disabled!")
            else:
                errormessages.append("You provided a wrong email address or password!")
        else:
            errormessages.append("You did not provide any log in data!")
    request.session['errorMessages'] = errormessages
    return redirect('home')


def create_championlist(request):
    errormessages = []
    if request.user.is_authenticated() and request.POST:
        new_championlist = UserChampionList()
        championlist_name = request.POST.get('createListName', None)
        championlist_description = request.POST.get('createListDescription', None)
        championlist_ispublic = request.POST.get('createListPublic', None)
        if championlist_name is None:
            errormessages.append("Your champion list requires a name!")
        else:
            new_championlist.name = championlist_name
            new_championlist.description = championlist_description
            if championlist_ispublic:
                new_championlist.is_public = True
            else:
                new_championlist.is_public = False
            new_championlist.fk_leaguemainsuser = request.user
            try:
                new_championlist.save()
            except:
                errormessages.append("Something went wrong while writing your list to the database!")
    else:
        errormessages.append("Use the appropiate button in order to create valid champion lists for your user!")
    request.session['errorMessages'] = errormessages
    return redirect('home')


def delete_championlist(request):
    errormessages = []
    if request.user.is_authenticated() and request.GET:
        delete_championlist_id = request.GET.get('id', None)
        if delete_championlist_id is not None:
            deleted_championlist = UserChampionList.objects.get(pk_id=delete_championlist_id)
            if deleted_championlist.fk_leaguemainsuser == request.user:
                try:
                    deleted_championlist.delete()
                except:
                    errormessages.append("Could not delete the selected champion list!")
            else:
                errormessages.append("You are not authorized to delete that champion list!")
        else:
            errormessages.append("The selected champion list could not be found!")
    else:
        errormessages.append("You are not authenticated! Please use the right button!")
    request.session['errorMessages'] = errormessages
    return redirect('home')


def championlist(request):
    context = {}
    errormessages = request.session.get('errorMessages', None)
    if errormessages:
        del request.session['errorMessages']
    if request.user.is_authenticated() and request.GET:
        championlist_id = request.GET.get('id', None)
        if championlist_id is not None:
            championlist = UserChampionList.objects.get(pk_id=championlist_id)
            if championlist.fk_leaguemainsuser == request.user or championlist.is_public:
                context['userList'] = championlist
                context['championEntries'] = championlist.champions.all().values_list('fk_champion', flat=True)
            else:
                errormessages.append("You are not authorized to access this userlist!")
    context['championList'] = Champion.objects.all().order_by('name')
    context['errorMessages'] = errormessages
    return render(request, 'championlist.html', context=context)


def save_championlist(request):
    errormessages = []
    this_userlist = 0
    is_valid = True
    if request.user.is_authenticated() and request.POST:
        userlist = None
        userlist_id = request.POST.get('userlistID', None)
        changelist_name = request.POST.get('changeListName', None)
        changelist_description = request.POST.get('changeListDescription', None)
        changelist_is_public = request.POST.get('changeListPublic', None)
        champions_in_list = request.POST.getlist('champion_id')
        if userlist_id is not None:
            try:
                this_userlist = int(userlist_id)
                userlist = UserChampionList.objects.get(pk_id=this_userlist)
            except:
                is_valid = False
                errormessages.append("The specified userlist could not be found!")
        else:
            is_valid = False
            errormessages.append("There was no userlist ID specified!")
        if is_valid:
            if changelist_name is not None and changelist_name != '':
                userlist.name = changelist_name
            else:
                errormessages.append("The list name cannot be empty!")
            if changelist_description is not None:
                userlist.description = changelist_description
            if changelist_is_public:
                userlist.is_public = True
            else:
                userlist.is_public = False
            try:
                userlist.save()
            except:
                errormessages.append("The general list information could not be updated!")
        if is_valid and userlist.fk_leaguemainsuser != request.user:
            is_valid = False
            errormessages.append("You are not authorized to save this userlist!")
        if is_valid and champions_in_list is not None:
            list_of_preexisting_champions = ChampionsInChampionList.objects.filter(fk_userchampionlist=userlist)
            for existing_entry in list_of_preexisting_champions:
                existing_entry.delete()
            for champion_in_list in champions_in_list:
                try:
                    this_champion = int(champion_in_list)
                    champion = Champion.objects.get(pk_id=this_champion)
                    champion_in_list = ChampionsInChampionList()
                    champion_in_list.fk_champion = champion
                    champion_in_list.fk_userchampionlist = userlist
                    champion_in_list.save()
                except:
                    errormessages.append("The champion with ID " + champion_in_list + " could not be added to this list!")
    else:
        errormessages.append("Please change your list from your list settings!")
    request.session['errorMessages'] = errormessages
    response = redirect('championlist')
    response['Location'] += ('?id=' + str(this_userlist))
    return response


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    errormessages = []
    isvalid = True
    if request.user.is_authenticated():
        errormessages.append("You cannot create another account while logged in!")
    else:
        if request.POST:
            usermail = request.POST.get('inputEmail', None)
            password1 = request.POST.get('inputPassword', None)
            password2 = request.POST.get('inputPassword2', None)
            alias = request.POST.get('inputAlias', None)
            region = request.POST.get('inputRegion', None)
            summoner = request.POST.get('inputSummoner', None)
            if usermail is None:
                isvalid = False
                errormessages.append("You did not provide an email address!")
            if (password1 is None) or (password2 is None):
                isvalid = False
                errormessages.append("You did not provide valid passwords!")
            if password1 != password2:
                isvalid = False
                errormessages.append("You provided different passwords!")
            if len(password1) < 6:
                isvalid = False
                errormessages.append("Your password must be more than 5 characters!")
            if alias is None:
                isvalid = False
                errormessages.append("You did not provide a username!")
            if isvalid:
                try:
                    new_user = LeagueMainsUser.objects.create_user(usermail, password=password1, nickname=alias, region=region, summoner=summoner)
                    new_user.save()
                except:
                    isvalid = False
                    errormessages.append("The provided email address does already exist!")
        else:
            isvalid = False
            errormessages.append("You did not provide any data for registering a new user!")
    request.session['errorMessages'] = errormessages
    return redirect('home')


def settings(request):
    if request.user.is_authenticated():
        errormessages = []
        if request.POST:
            changeMail1 = request.POST.get('changeMail1', None)
            changeMail2 = request.POST.get('changeMail2', None)
            changePassword1 = request.POST.get('changePassword1', None)
            changePassword2 = request.POST.get('changePassword2', None)
            changeNickname = request.POST.get('changeNickname', None)
            changeRegion = request.POST.get('changeRegion', None)
            changeSummoner = request.POST.get('changeSummoner', None)
            """ Change email """
            if changeMail1 != request.user.email:
                if changeMail1 == changeMail2:
                    try:
                        prevmail = request.user.email
                        request.user.email = changeMail1
                        request.user.save()
                    except:
                        request.user.email = prevmail
                        errormessages.append("The specified email address already exists!")
                else:
                    errormessages.append("Make sure both email addresses are spelt correctly!")
            """ Change password """
            if changePassword1 is not None and changePassword1 != '':
                if changePassword1 == changePassword2:
                    if len(changePassword1) > 5:
                        request.user.set_password(changePassword1)
                        request.user.save()
                    else:
                        errormessages.append("Your password must at least contain 6 characters!")
                else:
                    errormessages.append("Make sure both passwords are spelt correctly!")
            """ Change nickname """
            if changeNickname is not None and changeNickname != '':
                request.user.nickname = changeNickname
                request.user.save()
            """ Change region """
            if changeRegion is not None:
                request.user.region = changeRegion
                request.user.save()
            """ Change summoner """
            request.user.summoner = changeSummoner
            request.user.save()
        context = { 'errorMessages':errormessages }
        return render(request, 'settings.html', context=context)
    else:
        errormessages = []
        errormessages.append("You cannot access settings while not logged in!")
        request.session['errorMessages'] = errormessages
        return redirect('home')


def test(request):
    context = {}
    if request.user.is_authenticated():
        updater = LeagueMainsUpdater()
        updater.update()
    context = { 'championlist':Champion.objects.all().order_by('name') }
    return render(request, 'test.html', context=context)