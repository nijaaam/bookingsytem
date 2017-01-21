var cache = {};
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