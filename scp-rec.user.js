// ==UserScript==
// @name         SCP-rec
// @version      0.1
// @description  insert recommendation serve code into SCP
// @author       AJMansfield
// @include       http://www.scp-wiki.net/*
// @include       http://scp-wiki.wikidot.com/*
// @exclude       http://www.scp-wiki.net/forum*
// @exclude       http://scp-wiki.wikidot.com/forum*
// @require http://code.jquery.com/jquery-1.12.4.min.js
// @require https://raw.githubusercontent.com/davidjbradshaw/iframe-resizer/master/js/iframeResizer.min.js


// ==/UserScript==

(function() {
    'use strict';

    var src = "https://ajmansfield.github.io/scp-rec/X" + window.location.pathname.split("/").pop();

    $.get(src).done(function () {
        //console.log('modding page');

        var content = document.getElementById('page-content');
        var myframe = document.createElement('iframe');
        myframe.id = 'scp-rec';
        myframe.frameBorder = 0;
        myframe.src = src;

        content.parentNode.insertBefore(myframe, content.nextSibling);

        var ifsizer = iFrameResize({checkOrigin:false, inPageLinks:true}, myframe);

        //console.log('done');
    }).fail(function () {
        console.log('page opted-out of recommendations');
    });
})();

