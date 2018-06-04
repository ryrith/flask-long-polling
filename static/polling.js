var prev_data = null;           // remember data fetched last time
const LONG_POLL_DURATION = 60000; // how long should we wait? (msec)
var pulling_update = false;
window.polling = {
    onupdate : function(e) {
        console.log(e);
    },
    onerror: function (e) {
        console.log(e);
    },
    pull_update : function(sid) {
        if (!pulling_update) {
            pulling_update = true;
            $.ajax({
                url: '/polling/' + sid,
                success: function (e){
                    polling.onupdate(e);
                    pulling_update = false
                    if (e.running){
                        polling.pull_update(sid);
                    }
                    return;
                } , // if /onupdate signals results ready, load them!
                completed: function (e) {

                },
                error: function (e) {
                    polling.onerro(e);
                },
                timeout: LONG_POLL_DURATION,
            });
        }
    },
    start: function(operation, params){
        $.ajax({
            url: '/polling-start?operation='+operation+(params?"&"+params:""),
            success: function (e){
                pulling_update = false
                polling.pull_update(e.sid);
            }
        });
    }
}