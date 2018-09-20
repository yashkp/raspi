var HID = require('node-hid')
//var devices = HID.devices()

var device = new HID.HID(3111, 15354)

var keyEvents = [],
    keyMapper = {
        39: 0, 30: 1, 31: 2, 32: 3, 33: 4,
        34: 5, 35: 6, 36: 7, 37: 8, 38: 9 };

device.on('data', function(data){
   
    if (data[2] !== 0 && data[2] !== 40) {
        keyEvents.push(keyMapper[data[2]]);
    } 
    else if (data[2] === 40) {
        var id = parseInt(keyEvents.join(''));
        console.log(id)
        keyEvents = [];
    }

    //if (data[2] !== 56)
    //    _this.rfidInterface.read(onRead);
});

device.on('error', function(err){
    console.log(err);
})

console.log('hello')