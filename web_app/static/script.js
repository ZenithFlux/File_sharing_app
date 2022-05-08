var socket = io();
    socket.on('connect', function() {
      socket.emit('connected', user);
    });

    socket.on('sending_file', function(filename, filedata) {
      var blob = new Blob([filedata])
      var link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = filename;
      link.click();
      socket.emit('print', filename + " recieved!");
    })
