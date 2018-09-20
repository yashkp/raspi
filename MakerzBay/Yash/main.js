const electron = require('electron')
const {app, BrowserWindow, Menu} = electron
const path = require('path')
const url = require('url')

/*
// Module to control application life.
const app = electron.app
// Module to create native browser window.
const BrowserWindow = electron.BrowserWindow
*/

menuTemplate = [
  {
    label: 'Application',
    submenu: [
      {
        label: 'About',
        click: () => {
          openAboutWindow()
        }
      }
    ]
  }
]

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let mainWindow

function createWindow () {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 1280, height: 720
  });

  // and load the index.html of the app.
  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'dynamic_page.html'),
    protocol: 'file:',
    slashes: true
  }))

  var menu = Menu.buildFromTemplate(menuTemplate)
  mainWindow.setMenu(menu)

  // Open the DevTools.
  // mainWindow.webContents.openDevTools()

  // Emitted when the window is closed.
  mainWindow.on('closed', function () {
    // Dereference the window object, usually you would store windows
    // in an array if your app supports multi windows, this is the time
    // when you should delete the corresponding element.
    mainWindow = null
  })
}

function openAboutWindow() {
  let aboutWindow = new BrowserWindow({
    parent: mainWindow,
    modal: true,
    show: false,
    width: 400,
    height: 200
  })

  aboutWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'about.html'),
    protocol: 'file',
    slashes: true
  }))

  aboutWindow.setMenu(null)
  aboutWindow.once('ready-to-show', () => {
    aboutWindow.show()
  })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// Quit when all windows are closed.
app.on('window-all-closed', function () {
  // On OS X it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', function () {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (mainWindow === null) {
    createWindow()
  }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.

console.log('Hello from main process')

const {ipcMain} = electron

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
      sendIdToRenderer(id)
      keyEvents = [];
  }

  //if (data[2] !== 56)
  //    _this.rfidInterface.read(onRead);
});

device.on('error', function(err){
  console.log(err);
})


var adal = require('adal-node').AuthenticationContext;

var authorityHostUrl = 'https://login.microsoftonline.com';
var tenant = 'microsoft.onmicrosoft.com';
var authorityUrl = authorityHostUrl + '/' + tenant;
var clientId = 'e4073485-e526-402f-bfcf-13eb3d3aea17';
var clientSecret = 'z65v23O57mtA38QiT3BEPfZUB6sfm8On/spLGP2wTMI='
var resource = 'https://employeeInformationAPI';

var context = new adal(authorityUrl);

var token = null;

function sendIdToRenderer(id) {
  context.acquireTokenWithClientCredentials(resource, clientId, clientSecret, function (err, tokenResponse) {
    if (err) {
      console.log('well that didn\'t work: ' + err.stack);
    } else {
      token = (tokenResponse.accessToken);

      getAlias(token, id);
    }
  });
}

function getAlias(token, id) {
	var request = require('request');

	request.get('https://azcardsw01.redmond.corp.microsoft.com/api/GetEmailId?cardNumber='+id,
		{
			'auth': {
				'bearer': token
			}
		},
		function (err, response, body) {
			//console.log(response.statusCode);
			console.log(body);
      mainWindow.webContents.send('cardId', body)
		}
	);
}
