var HID = require('node-hid')
var devices = HID.devices()

var device = new HID.HID(3111, 15354)

var keyEvents = [],
    keyMapper = {
        57: 0, 48: 1, 49: 2, 50: 3, 51: 4,
        52: 5, 53: 6, 54: 7, 55: 8, 56: 9 };

device.on('data', function(data){
    //console.log(typeof(data))
    //console.log(data.length)
    console.log(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])
    var d = data.toString('ascii').match(/\w*/)[0];
    //console.log(d);
    /*
    if (data[2] !== 0 && data[2] !== 88) {
                keyEvents.push(keyMapper[parseInt(data[2], 16)]);
                //_this.emit('input', data[2]);
                console.log(data[2])
            } else if (data[2] === 88) {
                var id = parseInt(keyEvents.join(''), 10);
                //_this.emit('scan', id);
                console.log(id)
                keyEvents = [];
            }

            //if (data[2] !== 56)
            //    _this.rfidInterface.read(onRead);
    */
    //console.log(data);
});

device.on('error', function(err){
    console.log(err);
})

console.log(devices)
console.log('hello')


