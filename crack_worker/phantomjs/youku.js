var system = require('system');
var timeout = parseInt(system.args[1]);
var url = system.args[2];

var webpage = require('webpage');
var page = webpage.create();
phantom.cookiesEnabled = true;

page.open(url, function (status) {
  var data;
  if (status === 'fail') {
    console.log('');
    // release the memory
    page.close();
    phantom.exit();
  } else {
    window.setTimeout(function(){
        console.log(page.content); 
        page.close();
        phantom.exit();
    },timeout);
  }
});

