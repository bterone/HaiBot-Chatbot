const Discord = require('discord.js');
const client = new Discord.Client();
var path = require('path')

client.on('ready', () => {
  console.log("I'm in");
  console.log(client.user.username);
});

client.on('message', msg => {
    if (msg.author.id != client.user.id) {
        //msg.channel.send(msg.content.split('').reverse().join(''));
        const { spawn } = require('child_process');
        const pyProg = spawn('python', [[__dirname + '/app/haibot.py', '"'+msg.content+'"']);

        pyProg.stdout.on('data', function(data) {

            console.log(data.toString());
            //res.write(data);
            msg.channel.send(data.toString());
            //res.end('end');
        });

        pyProg.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
    }
});

client.login('SECRET TOKEN');