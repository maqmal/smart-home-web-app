var chart;
var dataChart = [];

//mqtt declaration
var reconnectTimeout = 2000;
var mqtt_server = "broker.hivemq.com";
var mqtt_port = 1883;
// var mqtt_tls = 1;
var mqtt_username = "";
var mqtt_password = "";
var mqtt_topic = "suhu/001";

//MQTT System
function MQTTconnect() {
    client = new Paho.MQTT.Client(mqtt_server, mqtt_port, "web_" + parseInt(Math.random() * 100, 10));

    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;
    var options = {
        // useSSL: mqtt_tls,
        userName: mqtt_username,
        password: mqtt_password,
        onSuccess: onConnect,
        onFailure: doFail
    }

    // $('#url').val(mqtt_server);
    // $('#port').val(mqtt_port);
    // $('#tls').val(mqtt_tls);

    client.connect(options);
}

function onConnect() {
    $('#status').val("Connected");
    console.log("onConnect");
    client.subscribe(mqtt_topic);
    $('#topic').val(mqtt_topic);
}

function doFail(e) {
    console.log(e);
}

function onConnectionLost(responseObject) {
    setTimeout(MQTTconnect, reconnectTimeout);
    console.log("onConnectionLost:" + responseObject.errorMessage);
    $('#status').val("Failed to Connect");
};

function onMessageArrived(message) {
    console.log("onMessageArrived:" + message.payloadString);
    var topic = message.destinationName;
    var payload = message.payloadString;

    var data = JSON.parse(payload);
    var x = new Date();
    console.log(data)
    if (data.serial) {
        document.getElementById("serial").innerHTML = data.serial;
        document.getElementById("ip").innerHTML = data.ip_address;
        document.getElementById("mac").innerHTML = data.mac_address;
    } else {
        dataChart.push([x, data.data1]);
        dataChart.shift();
        chart.updateOptions({
            'file': dataChart
        });
    }
};

// $(document).ready(function() {
//     MQTTconnect();

//     var t = new Date();
//     for (var i = 100; i >= 0; i--) {
//         var x = new Date(t.getTime() - i * 1000);
//         dataChart.push([x, 0]);
//     }

//     chart = new Dygraph(document.getElementById("chart_data_1"), dataChart, {
//         drawPoints: true,
//         showRoller: false,
//         drawXAxis: true,
//         labels: ['Time', 'Data 1']
//     });
// });