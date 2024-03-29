import React from 'react';
import SeriesBoard from './SeriesBoard.jsx'
import ReactDOM from 'react-dom'
import $ from 'jquery'

let current_user = null
const series = $("#series_component").data("series")
const series_sock = 'ws://' + window.location.host + "/series/" + series + "/"

$.get('http://127.0.0.1:8000/current-user/?format=json', function(result){
    // gets the current user information from Django
    current_user = result
    render_component()
})


function render_component(){
    ReactDOM.render(<SeriesBoard current_user={current_user} series_id={series} socket={series_sock}/>, document.getElementById("series_component"))
    }

