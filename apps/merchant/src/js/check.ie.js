/**
 * check IE version
 * @returns {*}
 */
function getIEVersion() {
    var sAgent = window.navigator.userAgent;
    var Idx = sAgent.indexOf("MSIE");
    // If IE, return version number.
    if (Idx > 0) {
        return parseInt(sAgent.substring(Idx + 5, sAgent.indexOf(".", Idx)));
    }
    // If IE 11 then look for "Trident" in user agent string.
    else if (!!navigator.userAgent.match(/trident/gi)) {
        return 11;
    }
    // If IE Edge then look for "Edge" in user agent string.
    else if (!!navigator.userAgent.match(/edge/gi)) {
        return 13;
    }
    else {
        return 0;
    }
}

// check IE
var ie = getIEVersion();
if (ie > 0 && ie < 11) {
    window.location.href = '/static/views/browser.html';
}