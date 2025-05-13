if(sessionStorage.getItem("queries") === null){
    console.log(sessionStorage.getItem("queries"));
    queries = new Map();
}
else{
    queries = new Map(Object.entries(JSON.parse(sessionStorage.getItem("queries"))));
}




function handleLookup(query, doneCallback) {
    console.log("autocomplete initiated")

    // TODO: if you want to check past query results first, you can do it here

    if(queries.has(query)){
        console.log("suggestion list is coming from front-end cache");
        handleLookupAjaxSuccess(queries.get(query), query, doneCallback)

    }
    else{

        // sending the HTTP GET request to the Java Servlet endpoint hero-suggestion
        // with the query data
        jQuery.ajax({
            "method": "GET",
            // generate the request url from the query.
            // escape the query string to avoid errors caused by special characters
            "url": "playersearch?pname=" + escape(query),
            "success": function(data) {
                // pass the data, query, and doneCallback function into the success handler
                console.log("sending AJAX request to backend Java Servlet")
                console.log("lookup ajax successful - suggestion list is coming from backend server");
                handleLookupAjaxSuccess(data, query, doneCallback)
            },
            "error": function(errorData) {
                console.log("lookup ajax error")
                console.log(errorData)
            }
        })

    }

}

function handleLookupAjaxSuccess(data, query, doneCallback) {

    // parse the string into JSON
    console.log(data)
    //var jsonData = JSON.parse(data);
    var jsonData = data;
    if(!queries.has(query)){
        queries.set(query, data);
        sessionStorage.setItem("queries", JSON.stringify(Object.fromEntries(queries)));
    }

    // TODO: if you want to cache the result into a global variable you can do it here

    // call the callback function provided by the autocomplete library
    // add "{suggestions: jsonData}" to satisfy the library response format according to
    //   the "Response Format" section in documentation

    console.log(jsonData)
    doneCallback( { suggestions: jsonData } );

}

/*Needs to be changed for new attribute names*/
function handleSelectSuggestion(suggestion) {

    console.log("you selected " + suggestion["value"])
    //window.location = "single-movie.html?id=" + suggestion["data"]["heroID"];
}

$('#autocomplete').autocomplete({
    // documentation of the lookup function can be found under the "Custom lookup function" section
    lookup: function (query, doneCallback) {
        handleLookup(query, doneCallback)
    },
    onSelect: function(suggestion) {
        handleSelectSuggestion(suggestion)
    },
    // set delay time
    deferRequestBy: 400,
    minChars: 4,
    // there are some other parameters that you might want to use to satisfy all the requirements
});