const express = require("express");
var app = express();
var path = require('path')
app.use(express.static(path.join(__dirname, 'public')));
var http = require('http').Server(app);
var io = require('socket.io')(http);
var bodyParser = require('body-parser')
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
var GoogleImages = require('google-images');

const client = new GoogleImages('SECRET ID', 'SECRET URL');

app.get('/', function(req, res){
	res.sendFile(__dirname + '/public/index.html');
});

//Event when user connects
io.on('connection', function(socket){
  console.log('a user connected');

	//User chatting to server
    socket.on('chat message', function(msg){
      console.log('message: ' + msg);
      io.emit('chat message', msg);
      const { spawn } = require('child_process');
      const pyProg = spawn('python', [__dirname + '/app/haibot.py', '"'+msg+'"']);

      pyProg.stdout.on('data', function(data) {

        console.log(data.toString());
        //res.write(data);
        io.emit('reply',data.toString());
        //res.end('end');
        if (data.toString().includes(':, Number 1: ')) {
          var array = data.toString().split(',')
          var hotel = array[2].replace(' Number 1: ', '')
          console.log(hotel)
          client.search(hotel).then(images => {
            io.emit('replyimage', '<img src="'+images[0].url+'" style="width:325px;height:200px;"</img>')
          }).catch((err) => { console.log(err) });
        }
        if (data.toString().includes('near that location: ')) {
          var array = data.toString().split(',')
          var hotel = array[0].replace('The following hotels are near that location: ', '')
          console.log(hotel)
          client.search(hotel).then(images => {
            io.emit('replyimage', '<img src="'+images[0].url+'" style="width:325px;height:200px;"</img>')
          }).catch((err) => { console.log(err) });
        }
      });

      pyProg.stderr.on('data', (data) => {
  	    console.log(`stderr: ${data}`);
	    });
    });

	//Event upon user disconnect
    socket.on('disconnect', function(){
      console.log('user disconnected');
    });
});

app.post('/submit', function (req, res) {
	var hname = req.body.hname
	var hdesc = req.body.hdesc

	const { spawn } = require('child_process');
	const pyProg = spawn('python', [__dirname + '/app/haibot.py', hname, '"'+hdesc+'"']);

	pyProg.stdout.on('data', function(data) {

		console.log(data.toString());
		res.write(data);
		res.end('end');
	});

	pyProg.stderr.on('data', (data) => {
		console.log(`stderr: ${data}`);
	});
})

app.post('/login', function (req, res) {
  var user1 = req.body.username
  var pass1 = req.body.password

  if (user1 == 'user' && pass1 == 'pass'){
    res.sendFile(__dirname + '/public/hoteladd.html')
  }
  else{
    res.write('Sorry! Wrong Password!')
  }
})

http.listen(3000, function(){
  console.log('listening on *:3000');
});