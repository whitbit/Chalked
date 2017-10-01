function search(evt) {


    $.get('/search.json', displayStates)

}

function displayStates(results) {
    console.dir(results)
    alert('hi')
}

