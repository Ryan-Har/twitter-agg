var times = document.getElementsByClassName("tweetTime")
for (var i = 0; i < times.length; i++) {
    let time = times[i].innerHTML;
    var localTweetTime = new Date(time);
    var options = { month: 'long', day: '2-digit',
                hour: 'numeric', minute: '2-digit' };
    times[i].innerHTML = localTweetTime.toLocaleString('en-uk', options);
}