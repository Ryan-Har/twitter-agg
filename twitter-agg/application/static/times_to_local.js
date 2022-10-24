function change_time() {
    var times = document.getElementsByClassName("tweetTime")
    for (var i = 0; i < times.length; i++) {
        if(i > times.length - 21){
            let time = times[i].innerHTML;
            var options = { month: 'long', day: '2-digit',
                        hour: 'numeric', minute: '2-digit' };
            var localTweetTime = new Date(time);
            times[i].innerHTML = localTweetTime.toLocaleString('en-uk', options);
            }
        }
    } 
change_time()