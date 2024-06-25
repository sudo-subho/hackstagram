from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from .models import Profile, Post,  FollwersCount, Comment, LikePost, Messages
from django.contrib import messages
from itertools import chain
import random, json
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q



def forgot_password(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST['email']
            otp = request.POST['otp']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:
                if User.objects.filter(email=email).exists():

                    messages.success(request, "Password has been Change successfully!!")
                    return redirect('login')
                
                else:
                    messages.info(request, 'Email does not exist')
                    return redirect('forgot_password')
                

            else:
                messages.info(request, "Password doesn't match")
                return redirect('forgot_password')
        else:
            return render(request, 'forgot_password.html', {})


    else:
        messages.success(request, "You Are Already Logged in..")
        return redirect('home')
    
def send_messages(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            message_text = request.POST.get('message')
            message_by = request.user.username
            user = request.POST.get('recipient_id')

            try:
                recipient_user = str(User.objects.get(pk=user))
                print(recipient_user)
            except User.DoesNotExist:
                redirect_url = reverse('load_messages', kwargs={'user_id': user})
                return redirect(redirect_url)

            if message_text == '':
                messages.success(request, "Messages Text Cannot Be Empty")
                redirect_url = reverse('load_messages', kwargs={'user_id': user})
                return redirect(redirect_url)
            
            
            
            else:
                new_message = Messages.objects.create(message_by=message_by, message_text=message_text, user=recipient_user)
                new_message.save()
                redirect_url = reverse('load_messages', kwargs={'user_id': user})
                return redirect(redirect_url)

        else:
            pass

    else:
        messages.error(request, 'Access Denied. You Are Not Logged In..')
        return redirect('login')
    
def load_messages(request, user_id):
    if request.user.is_authenticated:
        # Filter messages based on the user IDs

        username = User.objects.get(id=user_id)
        print(username)

        messages = Messages.objects.filter(
            (Q(message_by=request.user.username, user=username) | Q(message_by=username, user=request.user.username))
        ).order_by('send_time')

        print(messages)
        # Pass the messages and the user ID to the template
        context = {
            'user_id': user_id,
            'messages': messages
        }

        return render(request, 'messages_window.html', context)

    else:
        messages.error(request, 'Access Denied. You Are Not Logged In..')
        return redirect('login')
    
def messages_list(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        
        user_following_list = []
        feed = []
        following_user_profiles = []

        user_following = FollwersCount.objects.filter(follower=request.user.username)

        for users in user_following:
            user_following_list.append(users.user)

        print(user_following_list)

        for usernames in user_following_list:
            feed_lists = User.objects.get(username=usernames)
            feed.append(feed_lists)

        for follow_user_pro in feed:
            follow_user_pros = Profile.objects.get(user=follow_user_pro)
            following_user_profiles.append(follow_user_pros)

        return render(request, 'all_messages.html', {'username_profile_list':following_user_profiles, 'current_user':user_profile})

    else:
        messages.error(request, 'Access Denied. You Are Not Logged In..')
        return redirect('login')

def user_messages(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user_object = User.objects.get(username=request.user.username)
            user_profile = Profile.objects.get(user=user_object)

        
            user_following_list = []
            feed = []
            following_user_profiles = []

            user_following = FollwersCount.objects.filter(follower=request.user.username)

            for users in user_following:
                user_following_list.append(users.user)

            print(user_following_list)

            for usernames in user_following_list:
                feed_lists = User.objects.get(username=usernames)
                feed.append(feed_lists)

            for follow_user_pro in feed:
                follow_user_pros = Profile.objects.get(user=follow_user_pro)
                following_user_profiles.append(follow_user_pros)

            return render(request, 'messages.html', {'following_user_profiles': following_user_profiles, 'current_user':user_profile})
        
        else:
            user_object = User.objects.get(username=request.user.username)
            user_profile = Profile.objects.get(user=user_object)
        
            user_following_list = []
            feed = []
            following_user_profiles = []

            user_following = FollwersCount.objects.filter(follower=request.user.username)

            for users in user_following:
                user_following_list.append(users.user)

            print(user_following_list)

            for usernames in user_following_list:
                feed_lists = User.objects.get(username=usernames)
                feed.append(feed_lists)

            for follow_user_pro in feed:
                follow_user_pros = Profile.objects.get(user=follow_user_pro)
                following_user_profiles.append(follow_user_pros)

            return render(request, 'messages.html', {'following_user_profiles': following_user_profiles, 'current_user':user_profile})

    else:
        messages.error(request, 'Access Denied. You Are Not Logged In..')
        return redirect('login')

def help(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)


        return render(request, 'search.html', {'user_profile': user_profile,})
    else:
        messages.error(request, 'Access Denied. You Are Not Logged In...')
        return redirect('login')

def comment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            commented_text = request.POST.get('comment')
            post_id = request.POST.get('comment_postId')
            commented_by = request.user.username

            if Post.objects.get(id=post_id):

                if commented_text == '':
                    return redirect('home')

                else:
                    post_instance = Post.objects.get(pk=post_id)
                    new_comment = Comment.objects.create(post=post_instance, commented_by=commented_by, commented_text=commented_text)
                    new_comment.save()
                    messages.success(request, 'Comment Posted Successfully')
                    return redirect('home')
            
            else:
                return redirect('home')
            
        else:
            return redirect('home')

    else:
        messages.error(request, 'Access Denied. You Are Not Logged In...')
        return redirect('login')

def search(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        if request.method == 'POST':
            username = request.POST.get('search_username')  # Use get() method to safely retrieve POST data
            username_profile_list = []  # Reset the list before populating it with search results
            if username is not None:  # Check if username is not None
                username_objects = User.objects.filter(username__icontains=username)
                username_profile_list = Profile.objects.filter(user__in=username_objects)

        else:
            username_profile_list = []  # Initialize an empty list if the request method is not POST

        return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

    else:
        messages.error(request, 'Access Denied. You Are Not Logged In...')
        return redirect('login')



def explore(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        feed_posts = Post.objects.all()

        return render(request, 'explore.html', {'user_profile':user_profile, 'feed_posts':feed_posts, 'user_object':user_object})

    else:
        messages.success(request, 'Access Denied. You Are Not Logged In...')
        return redirect('login')

def fast_follow(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            follower = request.POST['follower']
            user = request.POST['user']

            if FollwersCount.objects.filter(follower=follower, user=user).first():
                unfollow = FollwersCount.objects.get(follower=follower, user=user)
                unfollow.delete()
                messages.success(request, 'You have unfollow '+user)
                return redirect('home')

            else:
                new_follow = FollwersCount.objects.create(follower=follower, user=user)
                new_follow.save()
                messages.success(request, 'You have follow '+user)
                return redirect('home')

        else:
            return redirect('home')

    else:
        messages.success(request, 'Access Denied. You Are Not Logged In...')
        return redirect('login')


def follow(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            follower = request.POST['follower']
            user = request.POST['user']

            if FollwersCount.objects.filter(follower=follower, user=user).first():
                unfollow = FollwersCount.objects.get(follower=follower, user=user)
                unfollow.delete()
                #messages.info(request, 'You have unfollow '+user)
                return redirect('/profile/'+user)

            else:
                new_follow = FollwersCount.objects.create(follower=follower, user=user)
                new_follow.save()
                #messages.info(request, 'You have follow '+user)
                return redirect('/profile/'+user)
            

        else:
            return redirect('home')

    else:
        messages.success(request, 'Access Denied. You Are Not Logged In...')
        return redirect('login')

def profile(request, pk):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=pk)
        user_profile = Profile.objects.get(user=user_object)
        user_posts = Post.objects.filter(user=pk)
        user_post_lenght = len(user_posts)

        follower = request.user.username
        user = pk

        if FollwersCount.objects.filter(follower=follower, user=user).first():
            button_text = "Unfollow"

        else:
            button_text = "Follow"

        user_followers = len(FollwersCount.objects.filter(user=pk))
        user_following = len(FollwersCount.objects.filter(follower=pk))

        context = {
            'user_object':user_object,
            'user_profile':user_profile,
            'user_posts':user_posts,
            'user_post_lenght':user_post_lenght,
            'button_text':button_text,
            'user_followers':user_followers,
            'user_following':user_following,
        }

        return render(request, 'profile.html', context)
    
    else:
        messages.success(request, 'Access Denied. You Are Not Logged In...')
        return redirect('login')


def like_post(request):
    if request.user.is_authenticated:
            username = request.user.username
            post_id = request.GET.get('post_id')

            post = Post.objects.get(id=post_id)
            #post = get_object_or_404(Post, id=post_id)

            like_filter = LikePost.objects.filter(post=post_id, liked_by=username).first()

            if like_filter == None:
                new_like = LikePost.objects.create(post=post_id, liked_by=username)
                new_like.save()
                post.no_of_like = post.no_of_like + 1
                post.save()
                return redirect('/')
            
            else:
                like_filter.delete()
                post.no_of_like = post.no_of_like - 1
                post.save()
                return redirect('/')

    else:
        messages.success(request, 'Access Denied. You Are Not Logged In...')
        return redirect('login')


def post_like(request):
    if request.user.is_authenticated and request.method == 'POST':
        data = json.loads(request.body)
        username = request.user.username
        post_id = data.get('post_id')

        if post_id is not None:
            post = get_object_or_404(Post, id=post_id)
            like_filter, created = LikePost.objects.get_or_create(post=post, liked_by=username)

            if created:
                post.no_of_like += 1
                post.save()
                return redirect('home')
            else:
                like_filter.delete()
                post.no_of_like -= 1
                post.save()
                return redirect('home')

        else:
            return JsonResponse({'success': False, 'error': 'post_id parameter missing'}, status=400)
    else:
        messages.success(request, 'Access Denied. You Are Not Logged In...')
        return redirect('login')



def upload_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user.username
            post_file = request.FILES.get('upload_file')
            caption = request.POST['caption']

            new_post = Post.objects.create(user=user, image=post_file, caption=caption)
            new_post.save()

            return redirect('/')

        else:
            return redirect('/')

    else:
        messages.success(request, 'Access Denied. You Are Not Logged In...')
        return redirect('login')

def account_settings(request):
    if  request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)

        current_user_email = request.user.email

        if request.method == 'POST':

            if request.FILES.get('image') == None:
                image = user_profile.profile_img
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                bio = request.POST['bio']
                location = request.POST['location']
                email = request.POST['email']
                working_at = request.POST['working_at']
                relationship = request.POST['relationship']

                user_profile.profile_img = image
                user_profile.first_name = first_name
                user_profile.last_name = last_name
                user_profile.bio = bio
                user_profile.location = location
                #user_object.update(email=email)
                print()
                user_profile.working_at = working_at
                user_profile.relationship = relationship
                user_profile.save()

                return redirect('account_settings')

            if request.FILES.get('image') != None:
                image = request.FILES.get('image')
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                bio = request.POST['bio']
                location = request.POST['location']
                email = request.POST['email']
                working_at = request.POST['working_at']
                relationship = request.POST['relationship']

                user_profile.profile_img = image
                user_profile.first_name = first_name
                user_profile.last_name = last_name
                user_profile.bio = bio
                user_profile.location = location
                user_profile.working_at = working_at
                user_profile.relationship = relationship
                user_profile.save()

                return redirect('account_settings')

        return render(request, 'account_settings.html', {'user_profile':user_profile, 'current_user_email':current_user_email, 'user_object':user_object})
    else:
        messages.success(request, 'Access Denied. You Are Not Logged In...')
        return redirect('login')
    

def logout(request):
    if  not request.user.is_authenticated:
        messages.success(request, 'You Are Not Logged In...')
        return redirect('home')
    else:
        auth.logout(request)
        return redirect('login')    

def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Wrong Username/Password')
                return redirect('login')

        else:
            return render(request, 'login.html', {})

    else:
        messages.error(request, 'Access Denied. Please Logout First.')
        return redirect('home')

def register(request):

    if  not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email is already taken')
                    return redirect('register')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username is already taken')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    user_login = auth.authenticate(username=username, password=password)
                    auth.login(request, user_login)

                    user_model = User.objects.get(username=username)
                    create_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                    create_profile.save()

                    messages.success(request, "{username} has been register successfully!!")
                    return redirect('account_settings')

            else:
                messages.info(request, "Password doesn't match")
                return redirect('register')
        else:
            return render(request, 'register.html', {})
        
    else:
        messages.success(request, 'Access Denied. Please Logout First..')
        return redirect('home')


def home(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        user_profile = Profile.objects.get(user=user_object)        

        user_following_list = []
        feed = []
        feed1 = []
        following_user_profiles = []

        user_following = FollwersCount.objects.filter(follower=request.user.username)

        for users in user_following:
            user_following_list.append(users.user)

        for usernames in user_following_list:
            feed_lists = Post.objects.filter(user=usernames)
            feed.append(feed_lists)

        feed_list = list(chain(*feed))

        print(user_following_list)

        for usernames in user_following_list:
                feed_lists = User.objects.get(username=usernames)
                feed1.append(feed_lists)

        for follow_user_pro in feed1:
            follow_user_pros = Profile.objects.get(user=follow_user_pro)
            following_user_profiles.append(follow_user_pros)


        #comments

        for post in feed_list:
            post.comments = Comment.objects.filter(post=post)

        # user suggestion 
        all_users = User.objects.all()
        user_following_all = []

        for user in user_following:
            user_list = User.objects.get(username=user.user)
            user_following_all.append(user_list)

        new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
        current_user = User.objects.filter(username=request.user.username)

        final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
        random.shuffle(final_suggestions_list)

        username_profile = []
        username_profile_list = []

        for users in final_suggestions_list:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        suggestions_username_profile = list(chain(*username_profile_list))


        return render(request, 'home.html', {'user_profile':user_profile, 'feed_posts':feed_list, 'user_object':user_object, 'suggestions_username_profile':suggestions_username_profile[:8], 'following_user_profiles':following_user_profiles[:5]})
    else:
        messages.success(request, 'Access Denied. Please Login First..')
        return redirect('login')
