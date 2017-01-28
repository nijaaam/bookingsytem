var cache = {};
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
function loadSearch() {
    $('#search').typeahead({
        hint: true,
        highlight: true,
        minLength: 2,
    }, {
        name: 'res',
        source: function(query, process) {
            return autocomplete(query, process);
        },
    });
}

function autocomplete(query, process) {
    var searchQuery = $('#search').val();
    searchQuery = searchQuery.slice(0,-1);
    if (cache[searchQuery] != undefined){
        var results = cache[searchQuery];
        var updatedResults = [];
        var sQuery = $('#search').val();
        for (var x = 0; x < results.length;x++){
            var value = results[x];
            if(value.indexOf(sQuery) != -1){
                updatedResults.push(value);
            }
        }
        cache[sQuery] = updatedResults;
        return process(updatedResults);
    } else {
        $.ajax({
            type: 'POST',
            url: '/autocomplete/',
            dataType: 'json',
            async: false,
            data: 'search=' + $('#search').val(),
            success: function(data) {
                var cacheResult = {
                    query: $('#search').val(),
                    data: data,
                    currentTime: new Date(),
                };
                cache[$('#search').val()] = data;
                return process(data);
            },
        });
    }
}