from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect

from .models import Tweet
from .forms import TweetForm
from django.utils.http import is_safe_url

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)
    # return HttpResponse("<h1>Hello, world!</h1>")


def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    print('post data is ', request.POST)
    next_url = request.POST.get("next") or None
    print('next url is ', next_url)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url is not None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request, 'components/form.html', context={'form': form})


def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript
    return json data
    """
    qs = Tweet.objects.all()
    tweets_list = [{"id": x.id, "content": x.content, "likes": 12} for x in qs]
    data = {
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by JavaScript
    return json data
    """
    data = {
        "id": tweet_id,
        "content": tweet.content,
        # "image_path": tweet.image.url
    }
    status = 200
    try:
        tweet = Tweet.objects.get(id=tweet_id)
        data["content"] = tweet.content
    except:
        data["message"] = "Not found"
        status = 404

    return JsonResponse(data, status=status)  # json.dumps
