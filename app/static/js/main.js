function fanOn() {
    $.post("fan/on", {}, function (result) {
    });
}
function heatOn() {
    $.post("heater/on", {}, function (result) {
    });
}
function acOn() {
    $.post("ac/on", {}, function (result) {
    });
}
function systemOff() {
    $.post("system/off", {}, function (result) {
    });
}